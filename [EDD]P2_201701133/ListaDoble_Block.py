
import os
import hashlib
import json

from datetime import datetime

#from ArbolAVL import ArbolAVL_B

class Block():
    def __init__(self,index,NombreClase,tiempo,PreHash,hash):
        self.anterior = None
        self.siguiente = None
        self.INDEX=index
        self.TIMESTAMP=tiempo
        self.CLASS=NombreClase
        self.PREVIOUSHASH=PreHash
        self.HASH=hash
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

    def  Encriptador(self,cadena):
        Confidencial= \
            hashlib.sha256(cadena.encode()).hexdigest()
        return Confidencial

    def LiberarJSON(self,data):
        inf=json.loads(data)
        file = open("J.txt", "w")
        file.write(inf["value"])
        file.close()

    def Insertar_Final(self, NombreClas,DATA):
        #obtenemos la timestamp
        now = datetime.now()
        Hora = str(now.day) + '-' + str(now.month) + '-' + str(now.year) +'::'+ str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)

        #para arbol
        self.LiberarJSON(DATA)
        if self.vacio():
            # obtenemos el hash
            EnviarCadena = str(self.size) + Hora + NombreClas + DATA + "0000"
            ValorHash = self.Encriptador(EnviarCadena)

            nuevaLista = Block(self.size, NombreClas, Hora,"0000",ValorHash)
            self.primero =self.ultimo = nuevaLista
        else:
            # obtenemos el hash
            EnviarCadena = str(self.size) + Hora + NombreClas + DATA+ self.ultimo.HASH
            ValorHash = self.Encriptador(EnviarCadena)

            nuevaLista = Block(self.size, NombreClas, Hora,self.ultimo.HASH,ValorHash)


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


    def Graficar(self):
        CadenaSig=""
        CadenaImprimir="digraph List { "+'\n'
        CadenaImprimir+="rankdir=TB"+'\n'
        CadenaImprimir+='size="9,9"'+'\n'
        CadenaImprimir +='node[shape=record,style=filled] ' + '\n'
        CadenaImprimir+='"NULL"'+" [shape=box] "+ '\n'
        CadenaImprimir +='"NULL."' + " [shape=box] " + '\n'

        aux = self.primero

        #ciclo para los enlaces siguientes

        while aux is not None:
            CadenaImprimir = CadenaImprimir + " " + '"(' +aux.CLASS+ ')"' +'[label ='+'"{'
            CadenaImprimir= CadenaImprimir+'|'+ ' CLASS='+aux.CLASS+"\\n TIMESTAMP= "+aux.TIMESTAMP+"\\n PREHASH="+aux.PREVIOUSHASH+"\\n HASH="+aux.HASH+'| }"]'+ '\n'
            if aux.siguiente is None:
                CadenaSig=CadenaSig+" "+ '"(' +aux.CLASS+ ')"'
            else:
                CadenaSig=CadenaSig+" "+ '"(' +aux.CLASS+ ')"' +" -> "

            aux = aux.siguiente

        CadenaAnte=CadenaSig+"[dir=back]\n"
        CadenaSig='"NULL."'+' -> '+CadenaSig+' -> '+'"NULL"'
        CadenaImprimir = CadenaImprimir+'\n'+CadenaSig+'\n'+CadenaAnte+'\n'+"}"
        file = open("ListaDobleBlock.dot", "w")
        file.write(CadenaImprimir)
        file.close()
        os.system('dot -Tpng ListaDobleBlock.dot -o  ListaDobleBlock.png')
        os.system('Start ListaDobleBlock.png')
