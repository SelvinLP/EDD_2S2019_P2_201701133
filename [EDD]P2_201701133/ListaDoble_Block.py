import subprocess
import os

from ArbolAVL import ArbolAVL_B

class Block():
    def __init__(self,index,NombreClase):
        self.anterior = None
        self.siguiente = None
        self.INDEX=index
        self.TIMESTAMP
        self.NAMECLASS=NombreClase
        #arbol
        #Hash
        #previusHash

class ListaDoblementeEnlazada_Block():

    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0

#comprobacion si la lista esta vacia
    def vacio(self):
        return self.primero is None

    def Tamaño(self):
        return self.size

    def Insertar_Final(self, NombreClas):
        nuevaLista = Block(self.size,NombreClas)
        if self.vacio():
            self.primero =self.ultimo = nuevaLista
        else:
            aux = self.ultimo
            self.ultimo = nuevaLista
            aux.siguiente = nuevaLista
            self.ultimo.anterior=aux
            self.size += 1

    def Eliminar(self):
        aux=self.ultimo.anterior
        self.ultimo.anterior = None
        self.ultimo=aux
        self.ultimo.siguiente=None
        self.size-=1