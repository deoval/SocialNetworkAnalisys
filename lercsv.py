import csv, sys, numpy, snap


class myarray(numpy.ndarray):
    def __new__(cls, *args, **kwargs):
        return numpy.array(*args, **kwargs).view(myarray)
    def where(self, value):
        return numpy.where(self==value)[0][0]

def addTeam(graph, teams, name):
	i = 0
	for team in teams:
		if team == name:
			return
		if team == None:
			break
		i+=1
	teams[i] = name
	G1.AddNode(i)

def addTeamGames(graph, teams, home, away):
	G1.AddEdge(teams.where(home), teams.where(away))

nome_ficheiro = 'premierleague1617.csv'
teams = myarray([None for x in range(100)], dtype=object)

G1 = snap.TNGraph.New()
i = 0
with open(nome_ficheiro, 'rb') as ficheiro:
    reader = csv.reader(ficheiro)
    cabecalho = next(reader)
    try:
        for linha in reader:
        	addTeam(G1, teams, linha[2])
    except csv.Error as e:
        sys.exit('ficheiro %s, linha %d: %s' % (nome_ficheiro, reader.line_num, e))

with open(nome_ficheiro, 'rb') as ficheiro:
    reader = csv.reader(ficheiro)
    cabecalho = next(reader)
    try:
        for linha in reader:
        	addTeamGames(G1, teams, linha[2], linha[3])
    except csv.Error as e:
        sys.exit('ficheiro %s, linha %d: %s' % (nome_ficheiro, reader.line_num, e))

print G1.GetEdges();