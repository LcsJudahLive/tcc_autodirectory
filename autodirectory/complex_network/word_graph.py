import networkx as nx
import matplotlib.pyplot as plt
from io import open

def generate_graph(words):
    words = list(set(words))
    from string import ascii_lowercase as lowercase
    G = nx.DiGraph(name="words")
    distance = 1 #Using to describe the distance of the network which will have in-connections with all nodes 
    first_word = True
    word_index = 0
    first_word_index = 0
    previous_nodes_connected = []
    for word in words:
        new_word = True
        first_word_weight = 1 - ((word_index - first_word_index)/len(words))
        for i in G.nodes():
            if word == i:
                new_word = False
                break
            else:
                continue
        if first_word:
            G.add_node(word)
            first_word = False
        else:
            if new_word:
                G.add_node(word)
                G.add_edge(G.nodes()[0], G.nodes()[G.nodes().index(word)],weight=first_word_weight)
                for source,dest in G.edges():
                    if dest == word:
                        print(source,dest)
                        previous_nodes_connected.append(source)
                for node in G.nodes():
                    weight = 1 - ((word_index - words.index(node))/(len(words)))
                    if node not in previous_nodes_connected:
                       G.add_edge(G.nodes()[G.nodes().index(word)],node, weight=weight )
                    else:
                        pass
        word_index+=1

    return G

def words_graph():
    """Return the words example graph from the Stanford GraphBase"""
    fh=open('newfile.txt','r')
    words=set()
    for line in fh.readlines():
        line = line.strip("\n")
        if line.startswith('*'):
            continue
        w=str(line)
        words.add(w.lower())
    return generate_graph(words)


def hubs(network, name, n=20, d="directed"):
    """Find top n nodes with highest degree and
    write results in the new file.
    Parameters
    ----------
    network : network edge list
    n : int
        number of wanted nodes
    d : directed or undirected
        if directed is selected than two new files
        will be created. One for in-degree and one
        for out-degree
    """
    n = int(n)

    if d == "directed":
        g = network
        if g.number_of_nodes() < n:
            n = int(g.number_of_nodes())

        degree_list_in = [node for node in g.in_degree().iteritems()]
        degree_list_in.sort(key=lambda x: x[1])
        degree_list_in.reverse()
        degree_list_out = [node for node in g.out_degree().iteritems()]
        degree_list_out.sort(key=lambda x: x[1])
        degree_list_out.reverse()

        with open(name.rsplit(".", 1)[0] + "_hubs_in.txt", "wb") as write_f_in:
            for i, value in enumerate(degree_list_in):
                if i < n:
                    write_f_in.write(value[0] + "\t\tIn-degree: " + str(value[1]) + "\n")
                else:
                    break

        with open(name.rsplit(".", 1)[0] + "_hubs_out.txt", "wb") as write_f_out:
            for i, value in enumerate(degree_list_out):
                if i < n:
                    write_f_out.write(value[0] + "\t\tOut-degree: " + str(value[1]) + "\n")
                else:
                    break

    elif d == "undirected":
        g = network
        if g.number_of_nodes() < n:
            n = int(g.number_of_nodes())

        degree_list = [node for node in g.degree().iteritems()]
        degree_list.sort(key=lambda x: x[1])
        degree_list.reverse()   

        with open(name.rsplit(".", 1)[0] + "_hubs.txt", "wb") as write_f:
            for i, value in enumerate(degree_list):
                print(type(value[0]),type(value[1]))
                if i < n:
                    write_f.write(value[0] + "\t\tDegree: " + str(value[1]) + "\n")
                else:
                    break




if __name__ == '__main__':
    from networkx import *
    G=words_graph()
    print('Nodes: {}'.format(G.nodes()))
    print('Edges: {}'.format(G.edges()))
    hubs(G,"new_network.txt", len(G.nodes()),"directed")
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx(G,arrows=True,with_labels=True)
    plt.show()
