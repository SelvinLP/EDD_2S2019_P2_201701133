
import os
import hashlib
import json

from datetime import datetime

from ArbolAVL import ArbolAVL_B


class Block():
    def __init__(self,index,NombreClase,tiempo,PreHash,hash,Arbol):
        self.anterior = None
        self.siguiente = None
        self.INDEX=index
        self.TIMESTAMP=tiempo
        self.CLASS=NombreClase
        self.PREVIOUSHASH=PreHash
        self.HASH=hash
        self.DATA=""
        self.ARBOL=Arbol


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


    def Encriptador(self, cadena):
        Confidencial = \
            hashlib.sha256(cadena.encode()).hexdigest()
        return Confidencial

    def LiberarJSON(self, data, NuevoArbol):
        inf = json.loads(data)
        self.LiberarJSONCICLODATOS(inf, NuevoArbol)


    def LiberarJSONCICLODATOS(self, CambioR, NuevoArbol):
        if (CambioR["left"] is not None):
            self.LiberarJSONCICLODATOS(CambioR["left"], NuevoArbol)
        Dato = CambioR["value"].split("-")
        NuevoArbol.InsertarArbol(Dato[0], Dato[1])
        if (CambioR["right"] is not None):
            self.LiberarJSONCICLODATOS(CambioR["right"], NuevoArbol)

    def Seleccion(self, pos):
        aux = self.primero
        TR = aux
        while (aux is not None):
            if (aux.INDEX == pos):
                TR = aux
            aux = aux.siguiente
        return TR

    def Insertar_Final(self, NombreClas, DATO):
        # obtenemos la timestamp
        now = datetime.now()
        Hora = str(now.day) + '-' + str(now.month) + '-' + str(now.year) + '-::' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)

        # para arbol
        NuevoArbol = ArbolAVL_B()
        self.LiberarJSON(DATO, NuevoArbol)

        # para el hash
        d = json.dumps(DATO)
        d = d.replace('\\n', '').replace(' ', '').replace('\\"', '"').strip('"')

        if self.vacio():
            # obtenemos el hash
            EnviarCadena = str(self.size) + Hora + NombreClas + d + "0000"
            ValorHash = self.Encriptador(EnviarCadena)

            nuevaLista = Block(self.size, NombreClas, Hora, "0000", ValorHash, NuevoArbol)
            nuevaLista.DATA = DATO
            self.primero = self.ultimo = nuevaLista
        else:
            self.size += 1
            # obtenemos el hash
            EnviarCadena = str(self.size) + Hora + NombreClas + d + self.ultimo.HASH
            ValorHash = self.Encriptador(EnviarCadena)

            nuevaLista = Block(self.size, NombreClas, Hora, self.ultimo.HASH, ValorHash, NuevoArbol)
            nuevaLista.DATA = DATO

            aux = self.ultimo
            self.ultimo = nuevaLista
            aux.siguiente = nuevaLista
            self.ultimo.anterior = aux

        # fin de Agregar a mi lista
        # creamos la respuesta y envio del archivo .json
        CadenaJSON = {
            "INDEX": nuevaLista.INDEX,
            "TIMESTAMP": nuevaLista.TIMESTAMP,
            "CLASS": nuevaLista.CLASS,
            "DATA": nuevaLista.DATA,
            "PREVIOUSHASH": nuevaLista.PREVIOUSHASH,
            "HASH": nuevaLista.HASH
        }
        DocFile = json.dumps(CadenaJSON)
        # documento json es DocFile
        return DocFile

    def VerificadorJSON(self, JSON):
        Valores = json.loads(JSON)
        index = str(Valores["INDEX"])
        tiempo = str(Valores["TIMESTAMP"])
        NombreClass = str(Valores["CLASS"])
        dato = str(Valores["DATA"])
        PreHash = str(Valores["PREVIOUSHASH"])
        Hash = str(Valores["HASH"])
        d = json.dumps(dato)
        d = d.replace('\\n', '').replace(' ', '').replace('\\"', '"').strip('"')
        CadenaEncriptador = index + tiempo + NombreClass + d + PreHash
        ResultadoHash = self.Encriptador(CadenaEncriptador)
        if (Hash == ResultadoHash):
            retorno = "true"
        else:
            retorno = "false"
        file = open("Verificador.txt", "w")
        file.write(retorno)
        file.close()
        # fin prueba
        return retorno

    def InsertarDesdeJSON(self, JSON):
        Valores = json.loads(JSON)
        tiempo = str(Valores["TIMESTAMP"])
        NombreClass = str(Valores["CLASS"])
        dato = str(Valores["DATA"])
        self.Insertar_Final(NombreClass, dato)
        # fin prueba

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
            CadenaImprimir = CadenaImprimir + " " + '"(' +aux.CLASS+str(aux.INDEX)+ ')"' +'[label ='+'"{'
            CadenaImprimir= CadenaImprimir+'|'+" INDEX= "+str(aux.INDEX)+ '\\n CLASS='+aux.CLASS+"\\n TIMESTAMP= "+aux.TIMESTAMP+"\\n PREHASH="+aux.PREVIOUSHASH+"\\n HASH="+aux.HASH+'| }"]'+ '\n'
            if aux.siguiente is None:
                CadenaSig=CadenaSig+" "+ '"(' +aux.CLASS+str(aux.INDEX)+ ')"'
            else:
                CadenaSig=CadenaSig+" "+ '"(' +aux.CLASS+str(aux.INDEX)+ ')"' +" -> "

            aux = aux.siguiente

        CadenaAnte=CadenaSig+"[dir=back]\n"
        CadenaSig='"NULL."'+' -> '+CadenaSig+' -> '+'"NULL"'
        CadenaImprimir = CadenaImprimir+'\n'+CadenaSig+'\n'+CadenaAnte+'\n'+"}"
        file = open("ListaDobleBlock.dot", "w")
        file.write(CadenaImprimir)
        file.close()
        os.system('dot -Tpng ListaDobleBlock.dot -o  ListaDobleBlock.png')
        os.system('Start ListaDobleBlock.png')
