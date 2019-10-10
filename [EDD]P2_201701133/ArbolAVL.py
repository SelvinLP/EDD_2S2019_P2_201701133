import subprocess
import os

class Nodo():
    def __init__(self):
        #datos del nodo arbol
        self.Izquierda=None
        self.Derecha=None
        self.Nivel=0
        self.Equilibrio=0
        self.Nombre=""
        self.Carnet=0


class ArbolAVL_B():

    def __init__(self):
        self.Raiz = None
        self.size = 0

    def vacio(self):
        return self.Raiz is None

    def InsertarData(self,Nodo,CarnetNuevo):
        NuevoNodo=Nodo()
        if self.vacio():
            self.Raiz=NuevoNodo
        else:
            ComparadorCarnet=Nodo.Carnet
            if(CarnetNuevo<ComparadorCarnet):
                self.InsertarData(Nodo.Izquierda,CarnetNuevo)
            else:
                self.InsertarData(Nodo.Derecha, CarnetNuevo)
