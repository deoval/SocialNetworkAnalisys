import numpy, csv, sys
import networkx as nx
import matplotlib.pyplot as plt

class myarray(numpy.ndarray):
	def __new__(cls, *args, **kwargs):
		return numpy.array(*args, **kwargs).view(myarray)
	def where(self, value):
		return numpy.where(self==value)[0][0]

def addTeam( teams, name):   
	i = 0
	for team in teams:
		if team == name:
			return
		if team == None:
			break
		i+=1
	teams[i] = name

def addTeamPoints(points, teams, home, away, winner):
	if (winner == 'D'):
		points[teams.where(home)] += 1
		points[teams.where(away)] += 1
	elif (winner == 'H'):
		points[teams.where(home)] += 3
	elif (winner == 'A'):
		points[teams.where(away)] += 3
	

if len(sys.argv) != 5:
	exit('numero de argumentos errados: !=5')
print 'Argument List:', str(sys.argv)

# nome_ficheiro = 'premierleague1415.csv'
nome_ficheiro = sys.argv[1]
atrib1 = int(sys.argv[2])
atrib2 = int(sys.argv[3])
nome_eixo=sys.argv[4]
teams = myarray([None for x in range(20)], dtype=object)
points = [0 for x in range(20)]

G=nx.DiGraph()

with open(nome_ficheiro, 'rb') as ficheiro:
	reader = csv.reader(ficheiro)
	cabecalho = next(reader)
	try:
		for linha in reader:
			addTeam(teams, linha[2])
	except csv.Error as e:
		sys.exit('ficheiro %s, linha %d: %s' % (nome_ficheiro, reader.line_num, e))

G.add_nodes_from(teams)

with open(nome_ficheiro, 'rb') as ficheiro:
	reader = csv.reader(ficheiro)
	cabecalho = next(reader)
	try:
		for linha in reader:
			addTeamPoints(points, teams, linha[2], linha[3], linha[6])

			oldweight1 = int(linha[atrib1])
			oldweight2 = int(linha[atrib2])

			weights=nx.get_edge_attributes(G,'weight')

			if (linha[2], linha[3]) in weights:    
				oldweight1 += weights[linha[2], linha[3]] 
				G.remove_edge(linha[2], linha[3])
				G.add_edge(linha[2], linha[3], weight = oldweight1)
			G.add_edge(linha[2], linha[3], weight = oldweight1)
			 
			if (linha[3], linha[2]) in weights:         
				oldweight2 += weights[linha[3], linha[2]]
				G.remove_edge(linha[3], linha[2])
				G.add_edge(linha[3], linha[2], weight = oldweight2)
			G.add_edge(linha[3], linha[2], weight= oldweight2)
	except csv.Error as e:
		sys.exit('ficheiro %s, linha %d: %s' % (nome_ficheiro, reader.line_num, e))


# print G.in_degree('Arsenal', weight='weight')
# print G.number_of_edges()
# print G.edges('Arsenal', data=True)

# G1 = nx.DiGraph()
# G1.add_nodes_from(G.nodes())
# G1.add_edges_from(G.edges(['Chelsea', 'West Brom', 'Sunderland'], data=True))

# nx.draw_spring(G, with_labels = True)
pos=nx.spring_layout(G)
# nx.draw_networkx_nodes(G,pos)
# nx.draw_networkx_labels(G,pos)
# nx.draw_networkx_edges(G,pos,edgelist=G.edges(['Chelsea', 'West Brom', 'Sunderland']))
# plt.show()

# exit()

# nx.draw_spring(G, with_labels = True)

maior=-1
menor=1000

edges = G.edges(['Chelsea'], data=True)
# edges = G.edges(data=True)

for (u,v,d) in edges:
        if d['weight'] >maior:maior=d['weight']
        elif d['weight'] <menor:menor=d['weight']
intervalo=int((maior-menor)/5)
elarge=[(u,v) for (u,v,d) in edges if d['weight'] >4*intervalo]
esmall=[(u,v) for (u,v,d) in edges if (d['weight'] <=4*intervalo and d['weight'] >3*intervalo)]
esmall1=[(u,v) for (u,v,d) in edges if (d['weight'] <=3*intervalo and d['weight'] >2*intervalo)]
esmall2=[(u,v) for (u,v,d) in edges if (d['weight'] <=2*intervalo and d['weight'] >intervalo)]
esmall3=[(u,v) for (u,v,d) in edges if d['weight'] <=intervalo ]
# pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos,node_size=700)
nx.draw_networkx_edges(G,pos,edgelist=elarge, edge_color='gray', width=2.5)
nx.draw_networkx_edges(G,pos,edgelist=esmall, edge_color='blue', width=2.0,alpha=0.5)
nx.draw_networkx_edges(G,pos,edgelist=esmall1, edge_color='yellow', width=1.5,alpha=0.5)

nx.draw_networkx_edges(G,pos,edgelist=esmall2, edge_color='orange', width=1.0,alpha=0.5)

nx.draw_networkx_edges(G,pos,edgelist=esmall3, edge_color='green', width=0.5,alpha=0.5)

nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
plt.show()

# attribute = [0 for x in G.nodes()]

# for node in G.nodes():
# 	attribute[teams.where(node)] = G.out_degree(node, weight='weight')

# scatter_plot = plt.scatter(points, attribute, alpha=0.5, c=attribute)
# if(nome_eixo!=None):plt.ylabel(nome_eixo)
# plt.xlabel('Pontos')
# plt.show()








# a = nx.betweenness_centrality(G, normalized=True, weight='weight')
# a = nx.closeness_centrality(G, distance='weight')
# a = nx.eccentricity(G)
# print a
# exit()

# for x in a:
# 	attribute[teams.where(x)] = a[x]

# scatter_plot = plt.scatter(points, attribute, alpha=0.5, c=attribute)
# for i in xrange(0, len(teams)):
#     plt.annotate(teams[i], (points[i],attribute[i]))
# if(nome_eixo!=None):plt.ylabel(nome_eixo)
# plt.xlabel('Pontos')
# plt.show()