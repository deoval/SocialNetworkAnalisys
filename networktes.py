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
	

if len(sys.argv) != 4:
	exit('numero de argumentos errados: !=4')
print 'Argument List:', str(sys.argv)

# nome_ficheiro = 'premierleague1415.csv'
nome_ficheiro = sys.argv[1]
atrib1 = int(sys.argv[2])
atrib2 = int(sys.argv[3])
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

nx.draw_circular(G, with_labels = True)
plt.show()

attribute = [0 for x in G.nodes()]

for node in G.nodes():
	attribute[teams.where(node)] = G.out_degree(node, weight='weight')

scatter_plot = plt.scatter(points, attribute, alpha=0.5, c=attribute)
plt.show()