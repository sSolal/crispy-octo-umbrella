import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.backend_tools import ToolBase

def visualize_graph(Nodes, Edges):
	G = nx.DiGraph()
	for i, n in enumerate(Nodes):
		G.add_node(i)
	for e in Edges:
		G.add_edge(*e)

	# Create a list of colors for the nodes
	num_nodes = len(G.nodes())
	node_colors = ['green' if i == 0 else 'red' if i == num_nodes - 1 else 'blue' for i in G.nodes()]

	nx.draw(G, with_labels=True, font_weight='bold', node_color=node_colors)
	plt.show()
	
def visualize_strategy(Nodes, Edges, Strategy):
	G = nx.DiGraph()
	for i,n in enumerate(Nodes):
		G.add_node(i)
	list_weighted_edges = []
	dico_label_edges = {}
	for e in Edges :
		i,j = e
		w = 0
		all_possibilities = Strategy.probas[Nodes[i]]	# un dictionnaire edge : proba
		for real_edge in Strategy.G.edges :
			if real_edge.u == Nodes[i] and real_edge.v == Nodes[j] :
				w = all_possibilities[real_edge]
		dico_label_edges[e] = str(w)
		list_weighted_edges.append((i,j,w))
	G.add_weighted_edges_from(list_weighted_edges)
	pos = nx.spring_layout(G)
	# Create a list of colors for the nodes
	num_nodes = len(G.nodes())
	node_colors = ['green' if i == 0 else 'red' if i == num_nodes - 1 else 'blue' for i in G.nodes()]
	nx.draw(G, pos, with_labels=True, font_weight='bold', node_color=node_colors)
	nx.draw_networkx_edge_labels(G, pos, edge_labels = dico_label_edges, font_size=10, font_color='red')
	plt.show()
		
def movable_graph(Nodes, Edges, Strategy):
	G = nx.DiGraph()
	for i,n in enumerate(Nodes):
		G.add_node(i)
	list_weighted_edges = []
	dico_label_edges = {}
	for e in Edges :
		i,j = e
		w = 0
		all_possibilities = Strategy.probas[Nodes[i]]	# un dictionnaire edge : proba
		for real_edge in Strategy.G.edges :
			if real_edge.u == Nodes[i] and real_edge.v == Nodes[j] :
				w = all_possibilities[real_edge]
		dico_label_edges[e] = str(w)
		list_weighted_edges.append((i,j,w))
	G.add_weighted_edges_from(list_weighted_edges)
	num_nodes = len(G.nodes())
	node_colors = ['green' if i == 0 else 'red' if i == num_nodes - 1 else 'skyblue' for i in G.nodes()]
	fig, ax = plt.subplots()
	plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)

	pos = nx.planar_layout(G)  # Initial layout (you can use other layouts)
	
	weights = [5*w for (i,j,w) in list_weighted_edges]
	labeldict = {}
	for i,n in enumerate(Nodes) :
		labeldict[i] = chr(65+i)
	"""for edge in G.edges():
		source, target = edge
		if (target, source) in G.edges() : 
			rad = 0.2
		else :
			rad = 0
		arrowprops=dict(lw=G.edges[(source,target)]['weight'],
                    		arrowstyle="-",
                   		color='black',
                   		connectionstyle=f"arc3,rad={rad}",
                   		linestyle= '-', alpha=0.6)
		ax.annotate("",xy=pos[source], xytext=pos[target], arrowprops=arrowprops)"""

	nx.draw(G, pos ,labels=labeldict, with_labels=True, ax=ax, node_size=500, node_color=node_colors, font_size=12, font_color='black', width = weights)
	#edge_labels = {'' for u, v in G.edges()}
	#nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels )
	plt.axis('off')
	plt.subplots_adjust(left=0.2, right=0.8, bottom=0.2, top=0.8)
	
	DraggableNodes(ax, 'Select and drag nodes')
	
	plt.show()
		
class DraggableNodes(ToolBase):
    def __init__(self, *args, **kwargs):
        ToolBase.__init__(self, *args, **kwargs)
        self.current_node = None

    def trigger(self, sender, event, data=None):
        if event.name == 'button_press_event':
            x, y = event.xdata, event.ydata
            node, _ = nx.drawing.layout.find_layout({'x': x, 'y': y}, pos)
            self.current_node = node
            plt.canvas.mpl_connect('motion_notify_event', self.on_motion)
            plt.canvas.mpl_connect('button_release_event', self.on_release)
            self.original_position = pos[node]
        elif event.name == 'motion_notify_event' and self.current_node:
            pos[self.current_node] = [event.xdata, event.ydata]
            nx.draw(G, pos, ax=ax, with_labels=True, node_size=500, node_color='skyblue', font_size=12, font_color='black')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=10, font_color='red')
            plt.canvas.draw_idle()
        elif event.name == 'button_release_event' and self.current_node:
            self.current_node = None
            plt.canvas.mpl_disconnect(self.on_motion)
            plt.canvas.mpl_disconnect(self.on_release)
            plt.canvas.draw_idle()
		

