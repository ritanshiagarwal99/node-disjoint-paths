from mpl_toolkits.basemap import Basemap
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic


# reading topology from json file
f = open('india_20.json', 'r')
network_data = json.loads(f.read())
nodes = pd.DataFrame(network_data['nodes'])["name"]
links_a = pd.DataFrame(network_data["links"])["node_1"]
links_b = pd.DataFrame(network_data["links"])["node_2"]

# plot using Basemap
m = Basemap(projection='merc', llcrnrlon=68.0, llcrnrlat=6.0,
            urcrnrlon=98.0, urcrnrlat=38.0, lat_ts=0, resolution='h', suppress_ticks=True)
lats = pd.DataFrame(network_data['nodes'])["latitude"].tolist()
lons = pd.DataFrame(network_data['nodes'])["longitude"].tolist()
mx, my = m(lons, lats)

# graph using networkx
G = nx.Graph()

pos = {}
for j in range(len(nodes)):
    pos[nodes[j]] = (mx[j], my[j])
    G.add_node(nodes[j])
    G.nodes[nodes[j]]["latitude"] = lats[j]
    G.nodes[nodes[j]]["longitude"] = lons[j]
for a, b in zip(links_a.to_list(), links_b.to_list()):
    G.add_edge(a, b)
    p1 = (G.nodes[a]['latitude'], G.nodes[a]['longitude'])
    p2 = (G.nodes[b]['latitude'], G.nodes[b]['longitude'])
    weight = geodesic(p1, p2).meters / 1000
    G[a][b]["weight"] = round(weight, 2)

m.drawcountries(linewidth=1.2, color='black')
m.bluemarble()

# Comment below line if you do not want to display edges
nx.draw_networkx(G, pos, node_size=5.0, width=0.8, node_color="blue", edge_color="yellow", with_labels=False)

for city, lat, lon in zip(nodes, lats, lons):
    x, y = m(lon, lat)
    m.plot(x, y, 'bo', markersize=5)
    # Uncomment below line if you want to print city names on the graph
    # plt.text(x, y, city, fontsize=8)

plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
figname = "india_20.png"
plt.savefig(figname)
plt.show()
