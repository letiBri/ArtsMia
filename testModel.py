from model.model import Model

mymodel = Model()
mymodel.buildGraph()
print("Numero nodi:", mymodel.getNumNodes(), "; Numero archi:", mymodel.getNumEdges())

mymodel.getInfoConnessa(1234)
