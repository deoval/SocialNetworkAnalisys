import snap

G = snap.TNodeEDatNet.New()
G.AddNode(1)
G.AddNode(2)
G.AddNode(3)
G.AddNode(4)
G.AddEdge(1,2,weight=0.6)
G.AddEdge(2,3,2)
G.AddEdge(1,3,5)
G.AddEdge(2,4,5)
G.AddEdge(3,4,3)

S = snap.TIntStrH()
S.AddDat(1,"David")
S.AddDat(2,"Emma")
S.AddDat(3,"Jim")
S.AddDat(4,"Sam")

for EI in G.Nodes():
	print "out (%d)" % (EI.GetOutDeg())

# snap.DrawGViz(G, snap.gvlDot, "gviz.dot", "Graph", S)