import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()  # grafo non orientato semplice
        self._nodes = DAO.getAllNodes()
        self._idMap = {}  # creo la idMap per accedere agli oggetti tramite l'id
        for v in self._nodes:
            self._idMap[v.object_id] = v

        # per la ricorsione
        self._bestPath = []
        self._bestCost = 0

    def buildGraph(self):
        self._graph.add_nodes_from(self._nodes)  # aggiungo i nodi al grafo tramite la lista che abbiamo appena importato dal DAO
        self.addAllEdges()

    def addEdgesV1(self):  # poco efficiente quando ho un numero molto elevato di vertici
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getPeso(u, v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight=peso)

    def addAllEdges(self):
        allEdges = DAO.getAllArchi(self._idMap)  # passo la mappa per accedere agli oggetti ArtObject attraverso la chiave
        for e in allEdges:  # itero su oggetti di tipo Arco
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)

    def getInfoConnessa(self, idInput):
        """
        Identifica la componente connessa che contiene idInput e ne restituisce la dimensione
        """
        # DFS è molto utile per trovare la componente connessa
        if not self.hasNode(idInput):  # controllo ridondante perchè già fatto nel controller
            return None

        source = self._idMap[idInput]  # identifico l'oggetto associato alla chiave passata, che diventa il nodo sorgente

        # Modo 1: conto i successori
        succ = nx.dfs_successors(self._graph, source)
        res = []
        for s in succ.values():  # itero sui valori associati alle chiavi
            res.extend(s)  # se la riga è un oggetto, mi aggiunge un oggetto, se il valore è una lista allora mi aggiunge tutti gli elementi della lista
        print("Size connessa con modo 1:", len(res))  # mi dà tutti i nodi della componente connessa. succ è un dizionario. Per i successori: per ogni nodo ho un lista di nodi a cui posso arrivare associata
        # dovrei aggiungere 1 alla return perchè devo aggiungere il nodo sorgente

        # Modo 2: conto i predecessori
        pred = nx.dfs_predecessors(self._graph, source)  # pred è un dizionario, per ogni nodo come chiave mi dà l'oggetto da cui arrivo
        print("Size connessa con modo 2:", len(pred.values()))  # dovrei aggiungere 1 al return, per includere il nodo source

        # Modo 3: conto i nodi nell'albero di visita
        dfsTree = nx.dfs_tree(self._graph, source)
        print("Size connessa con modo 3:", len(dfsTree.nodes()))  # funziona come return

        # Modo 4: uso il metodo node_connected_component di nx
        conn = nx.node_connected_component(self._graph, source)  # mi trova direttamente i nodi della componente connessa partendo dal nodo source del grafo
        print("Size connessa con modo 4: ", len(conn))

        return len(conn)  # funziona come return

    def hasNode(self, idInput):
        # return self._idMap[idInput] in self._graph
        return idInput in self._idMap  # ritorna True se il nodo appartiene alla mappa, e quindi al grafo

    # per il punto 2, metodo ricorsivo
    def getOptPath(self, source, lun):
        self._bestPath = []  # azzero le soluzioni ottime
        self._bestCost = 0
        parziale = [source]  # conosciamo già il primo nodo

        for n in nx.neighbors(self._graph, source):  # trovo tutti i vicini di source sul grafo
            if parziale[-0].classification == n.classification:
                parziale.append(n)  # estendo la sol parziale
                self._ricorsione(parziale, lun)
                parziale.pop()  # backtracking
        return self._bestPath, self._bestCost

    def _ricorsione(self, parziale, lun):
        if len(parziale) == lun:
            # allora parziale ha la lunghezza desiderata, condizione terminale
            # verifico se è una soluzione migliore e in ogni caso esco
            if self.costo(parziale) > self._bestCost:
                self._bestPath = copy.deepcopy(parziale)  # perchè parziale viene cambiata ad ogni chiamata, quindi devo fare una copy, una deepcopy anche se ci sono oggetti all'interno
                self._bestCost = self.costo(parziale)
            return
        # se arrivo qui, allora parziale può ancora ammettere altri nodi
        for n in self._graph.neighbors(parziale[-1]):
            if parziale[-0].classification == n.classification and n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()

    def costo(self, listObjects):
        totCosto = 0
        for i in range(0, len(listObjects) - 1):
            totCosto += self._graph[listObjects[i]][listObjects[i + 1]]["weight"]  # accesso tramite i dizionari del grafo
        return totCosto

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getIdMap(self):
        return self._idMap

    def getObjectFromId(self, id):
        return self._idMap[id]
