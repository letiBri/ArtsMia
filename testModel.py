from model.model import Model

mymodel = Model()
mymodel.buildGraph()
print("Numero nodi:", mymodel.getNumNodes(), "; Numero archi:", mymodel.getNumEdges())

print("Modo 4:", mymodel.getInfoConnessa(1234))
