import pandas as pd
import json
import networkx as nx
from input import G
from ilp import optimize_node_disjoint
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


def get_distance(g):
    dist = dict(nx.all_pairs_dijkstra_path_length(g))
    d = {}
    for src in g.nodes():
        for dst in g.nodes():
            d[(src, dst)] = dist[src][dst]
    return d


def read_demands():
    filename = "demands.txt"
    fp = open(filename)
    lines = fp.readlines()
    # Reading demands from text file in the format
    # "source" "destination" "capacity"
    R = {}
    for line in lines:
        src, dst, cap = line.split(' ')
        R[(src, dst)] = int(cap)

    fp.close()
    return R


def plot_paths(working, backup):
    # format: list of tuples: [(link1), (link2), ...]
    # (linkA) = (node_i, node_j)
    # --------------------------------------------------------------------
    # reading topology from json file
    f = open('india_20.json', 'r')
    network_data = json.loads(f.read())
    nodes = pd.DataFrame(network_data['nodes'])["name"]
    links = G.edges()
    color_map = []
    edge_size = []
    for i, j in links:
        if (i, j) in working or (j, i) in working:
            color_map.append("#BF00BF")
            edge_size.append(5.0)
        elif (i, j) in backup or (j, i) in backup:
            color_map.append("red")
            edge_size.append(5.0)
        else:
            color_map.append("yellow")
            edge_size.append(0.8)

    # plot using Basemap
    m = Basemap(projection='merc', llcrnrlon=68.0, llcrnrlat=6.0,
                urcrnrlon=98.0, urcrnrlat=38.0, lat_ts=0, resolution='h', suppress_ticks=True)
    lats = pd.DataFrame(network_data['nodes'])["latitude"].tolist()
    lons = pd.DataFrame(network_data['nodes'])["longitude"].tolist()
    mx, my = m(lons, lats)
    pos = {}
    for j in range(len(nodes)):
        pos[nodes[j]] = (mx[j], my[j])
    m.drawcountries(linewidth=1.2, color='black')
    m.bluemarble()
    nx.draw_networkx(G, pos, node_size=10.0, width=edge_size, node_color="blue", edge_color=color_map, with_labels=False)
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    figname = "ilp_result_leh_chennai.png"
    plt.savefig(figname)
    plt.show()


if __name__ == "__main__":
    D = get_distance(G)
    R = read_demands()
    distance1, distance2, path1, path2 = optimize_node_disjoint(G, D, R)

    # plot paths for a demand pair
    plot_paths(path1[1], path2[1])
