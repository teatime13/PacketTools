#アドレスを表示
from scapy.all import *
import networkx as nx
import matplotlib.pyplot as plt

#パケットのリストを用意しておく
packet = rdpcap("sample.pcap")
ip_list = []


#ip_listに辞書型のsrcとdstを保存
for p in packet:
    if p["Ethernet"].type == 0x800:
        data = {}
        data["src"] = p["IP"].src
        data["dst"] = p["IP"].dst
        ip_list.append(data)

G = nx.OrderedGraph() #無向グラフ

for ip in ip_list:
    src = ip["src"]
    dst = ip["dst"]
    
    if not G.has_node(src):
        G.add_node(src)
    if not G.has_node(dst):
        G.add_node(dst)

    if G.has_edge(src, dst):
        G.edges[src, dst]["weight"] += 1
    else:
        G.add_edge(src, dst)
        G.edges[src, dst]["weight"] = 1


#太さ指定して表示
plt.figure(figsize=(8,8))
pos = nx.spring_layout(G, k=1.5)

nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G, pos)
edge_width = [d["weight"]*0.1 if d["weight"]<50 else 5 for (u,v,d) in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, edge_color="Black", width=edge_width)


#表示
plt.axis("off")
plt.savefig("sample.png")
plt.show()