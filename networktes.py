import numpy, csv
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
	

nome_ficheiro = 'premierleague1617.csv'
teams = myarray([None for x in range(20)], dtype=object)

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
        	oldweight1 = int(linha[4])
        	oldweight2 = int(linha[5])

        	weights=nx.get_edge_attributes(G,'weight')

        	if (linha[2], linha[3]) in weights: 	
        		oldweight1 += weights[linha[2], linha[3]] 
        	G.add_edge(linha[2], linha[3], weight = oldweight1)
        	 
        	if (linha[2], linha[3]) in weights:        	
        		oldweight2 = weights[linha[3], linha[2]] + int(linha[5])
        	G.add_edge(linha[3], linha[2], weight= oldweight2)
    except csv.Error as e:
        sys.exit('ficheiro %s, linha %d: %s' % (nome_ficheiro, reader.line_num, e))


print G.in_degree('Arsenal', weight='weight')
print G.number_of_edges()
# nx.draw_circular(G, with_labels = True)
# plt.show()