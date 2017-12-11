import csv, sys, numpy, snap
import matplotlib.pyplot as plt


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

def addTeamPoints(points, teams, home, away, winner):
	if (winner == 'D'):
		points[teams.where(home)] += 1
		points[teams.where(away)] += 1
	elif (winner == 'H'):
		points[teams.where(home)] += 3
	elif (winner == 'A'):
		points[teams.where(away)] += 3

def addTeamFaults(faults, teams, home, away, homeFaults, awayFaults):
	faults[teams.where(home)] += int(homeFaults)
	faults[teams.where(away)] += int(awayFaults)

def writeTeamNodesCSV(teams, orginalcsvname, points):	
	node_csv_name = 'nodes' + orginalcsvname;
	file = open(node_csv_name, 'wb')
	writer = csv.writer(file)
	writer.writerow(['Id', 'Label', 'Weight'])
	for x in xrange(0,len(teams)):
		if teams[x] == None:
			break
		writer.writerow([x, teams[x], points[x]])

def writeTeamEdgesCSV(writer, teams, home, away, valueHome, valueAway):	
	writer.writerow([teams.where(home), teams.where(away), 'Directed', valueHome])
	writer.writerow([teams.where(away), teams.where(home), 'Directed', valueAway])

nome_ficheiro = 'premierleague1617.csv'
teams = myarray([None for x in range(20)], dtype=object)
points = myarray([0 for x in range(20)], dtype=object)
faults = myarray([0 for x in range(20)], dtype=object)

G1 = snap.TNGraph.New()
i = 0

edges_csv_name = 'edges' + nome_ficheiro;
file = open(edges_csv_name, 'wb')
writer = csv.writer(file)
writer.writerow(['Source', 'Target', 'Type', 'Weight'])

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
        	addTeamPoints(points, teams, linha[2], linha[3], linha[6])
        	addTeamFaults(faults, teams, linha[2], linha[3], linha[4], linha[5])
        	# writeTeamEdgesCSV(writer, teams, linha[2], linha[3], linha[4], linha[5])
    except csv.Error as e:
        sys.exit('ficheiro %s, linha %d: %s' % (nome_ficheiro, reader.line_num, e))

print faults;
print points;

scatter_plot = plt.scatter(points, faults, alpha=0.5)
plt.show()
# writeTeamNodesCSV(teams, nome_ficheiro, points)