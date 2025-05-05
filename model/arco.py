from dataclasses import dataclass

from model.artObject import ArtObject


@dataclass
class Arco:
    o1: ArtObject
    o2: ArtObject
    peso: int

    # non serve fare hash ed eq perchè è solo una struttura dati che creo per il DAO
