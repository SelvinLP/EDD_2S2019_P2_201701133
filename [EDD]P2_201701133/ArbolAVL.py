import subprocess
import os

class Block():
    def __init__(self):
        #datos del nodo arbol
        self.Izquierda=None
        self.Derecha=None
        self.Nivel
        self.Equilibrio
        self.Nombre
        self.Carnet


class ArbolAVL_B():

    def __init__(self):
        self.Raiz = None
        self.size = 0

    def vacio(self):
        return self.Raiz is None