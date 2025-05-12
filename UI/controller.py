import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._view.txt_result.controls.clear()
        self._model.buildGraph()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato. Il grafo contiene {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi."))
        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False
        self._view.update_page()
        return

    def handleCompConnessa(self, e):
        txtInput = self._view._txtIdOggetto.value
        if txtInput == "" or txtInput is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un id!", color="red"))
            self._view.update_page()
            return
        try:
            idInput = int(txtInput)  # lo metto dentro un blocco try perchè questa operazione potrebbe scatenare un errore se non è davvero un numero sottoforma di stringa
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Il valore inserito non è un numero!", color="red"))
            self._view.update_page()
            return

        if not self._model.hasNode(idInput):  # controllo se il nodo esiste all'interno del grafo
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("L'id inserito non corrisponde a un node del grafo (non è un ogg del DB)!", color="red"))
            self._view.update_page()
            return

        # se arrivo qui ho superato tutti i controlli e il nodo inserito in input appartiene al grafo
        sizeCompConnessa = self._model.getInfoConnessa(idInput)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che contiene il nodo {self._model.getObjectFromId(idInput)} ha dimensione pari a a {sizeCompConnessa}"))

        self._view._ddLun.disabled = False
        self._view._btnCerca.disabled = False

        myValues = range(2, sizeCompConnessa)
        # for v in myValues:
        #     self._view._ddLun.options.append(ft.dropdown.Option(v))
        # oppure posso fare così
        myValuesDD = list(map(lambda x: ft.dropdown.Option(x), myValues))
        self._view._ddLun.options = myValuesDD

        self._view.update_page()

    def handleCerca(self, e):
        source = self._model.getObjectFromId(int(self._view._txtIdOggetto.value))  # a questo punto ho già eseguito i controlli sull'input
        lun = self._view._ddLun.value
        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione: selezionare un parametro Lunghezza", color="red"))
            self._view.update_page()
            return
        lunInt = int(lun)
        path, pesoTot = self._model.getOptPath(source, lunInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino che parte da {source} trovato con peso totale {pesoTot}"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.update_page()
        return
