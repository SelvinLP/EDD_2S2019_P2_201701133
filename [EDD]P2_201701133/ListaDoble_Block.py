import subprocess
import os

from ArbolAVL import ArbolAVL_B

class Block():
    def __init__(self,index,NombreClase):
        self.anterior = None
        self.siguiente = None
        self.INDEX=index
        self.TIMESTAMP=""
        self.CLASS=NombreClase
        self.PREVIOUSHASH=""
        self.HASH=""
        self.DATA=""


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

    def Mostrar(self):
        tem=self.primero
        while tem is not None:
            print(tem.CLASS)
            tem=tem.siguiente

    def Eliminar(self):
        aux=self.ultimo.anterior
        self.ultimo.anterior = None
        self.ultimo=aux
        self.ultimo.siguiente=None
        self.size-=1

    def Graficar(self):
        CadenaImprimir="digraph List { rankdir=TB "+'\n'
        CadenaImprimir=CadenaImprimir+' size="9,9"'+'\n'
        CadenaImprimir = CadenaImprimir + 'node[shape=record,style=filled] ' + '\n'
        CadenaImprimir=CadenaImprimir+'"NULL"'+" [shape=box] "+ '\n'
        CadenaImprimir = CadenaImprimir + '"NULL."' + " [shape=box] "+ '\n'
        aux = self.primero

        #ciclo para los enlaces siguientes

        while aux is not None:
            CadenaImprimir = CadenaImprimir + " " + '"(' +aux.CLASS+ ')"' +'[label ='+'"{'
            CadenaImprimir= CadenaImprimir+'|'+ '( CLASS='+aux.CLASS+" TIMESTAMP= "+aux.TIMESTAMP+" PREHASH="+aux.PREVIOUSHASH+" HASH="+aux.HASH+')' +'| }"]'+ '\n'
            if aux.siguiente is None:
                CadenaSig=CadenaSig+" "+ '"(' +aux.CLASS+ ')"'
            else:
                CadenaSig=CadenaSig+" "+ '"(' +aux.CLASS+ ')"' +" -> "

            aux = aux.siguiente

        CadenaSig=CadenaSig+' -> '+'"NULL"'
        CadenaImprimir = CadenaImprimir+" "+CadenaSig++"}"
        file = open("ListaDobleBlock.dot", "w")
        file.write(CadenaImprimir)
        file.close()
        os.system('dot -Tpng ListaDobleBlock.dot -o  ListaDobleBlock.png')
        os.system('Start ListaDobleBlock.png')
