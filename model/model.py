import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()  # grafo non orientato semplice
        self._nodes = DAO.getAllNodes()
        self._idMap = {}  # creo la idMap per accedere agli oggetti tramite l'id
        for v in self._nodes:
            self._idMap[v.object_id] = v

    def buildGraph(self):
        nodes = DAO.getAllNodes()
        self._graph.add_nodes_from(nodes)  # aggiungo i nodi al grafo tramite la lista che abbiamo appena importato dal DAO
        self.addAllEdges()

    def addEdgesV1(self):
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getPeso(u, v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight=peso)

    def addAllEdges(self):
        allEdges = DAO.getAllArchi(self._idMap)  # passo la mappa per accedere all'oggetto attraverso la chiave
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)

    def getInfoConnessa(self, idInput):
        """
        Identifica la componente connessa che contiene idInput e ne restituisce la dimensione
        """
        # DFS è molto utile per trovare la componente connessa
        if not self.hasNode(idInput):
            return None

        source = self._idMap[idInput]

        # Modo 1: conto i successori
        succ = nx.dfs_successors(self._graph, source)
        res = []
        for s in succ.values(): # itero sui valori associati alle chiavi
            res.extend(s)  # se la riga è un oggetto, mi aggiunge un oggetto, se il valore è una lista allora mi aggiunge tutti gli elementi della lista
        print("Size connessa con modo 1:", len(res))  # mi dà tutti i nodi della componente connessa. succ è un dizionario, per i successori: per ogni nodo ho un lista di nodi a cui posso arrivare associata
        # dovrei aggiungere 1 alla return

        # Modo 2: conto i predecessori
        pred = nx.dfs_predecessors(self._graph, source)  # pred è un dizionario, per ogni nodo come chiave mi dà l'oggetto da cui arrivo
        print("Size connessa con modo 2:", len(pred.values()))  # dovrei aggiungere 1 al return
        # Modo 3: conto i nodi nell'albero di visita
        dfsTree = nx.dfs_tree(self._graph, source)
        print("Size connessa con modo 3:", len(dfsTree.nodes()))  # va bene nella return

        # Modo 4: uso il metodo node_connected_component di nx
        conn = nx.node_connected_component(self._graph, source)
        return len(conn)

    def hasNode(self, idInput):
        # return self._idMap[idInput] in self._graph
        return idInput in self._idMap

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getIdMap(self):
        return self._idMap

    def getObjectFromId(self, id):
        return self._idMap[id]
