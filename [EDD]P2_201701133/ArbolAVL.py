import subprocess
import os


class Logical():
    def __init__(self, f):
        self.v = f
    def setLogical(self, f):
        self.v = f
    def GetValue(self):
        return self.v
class Nodo():
    def __init__(self,carnet,nombre):
        #datos del nodo arbol
        self.Izquierda=None
        self.Derecha=None
        self.Altura=0
        self.Equilibrio=0
        self.Nombre=nombre
        self.Carnet=carnet


class ArbolAVL_B():

    def __init__(self):
        self.CadenaImprimir = ""
        self.Raiz = None
        self.size = 0
        self.AlturaMax=0

    #ROTACIONES
    #Rotacion Izquierda
    def RotacionII(self,n,n1):
        n.Izquierda = n1.Derecha
        n1.Derecha= n
        #Actualizar
        if(n1.Equilibrio == -1):
            n1.Equilibrio = 0
            n.Equilibrio = 0
        else:
            n1.Equilibrio = 1
            n.Equilibrio = -1

        return n1
    #Rotacion Izquierda Derecha
    def RotacionID(self, n, n1):
        n2 = n1.Derecha
        n1.Derecha = n2.Izquierda
        n2.Izquierda = n1
        n.Izquierda = n2.Derecha
        n2.Derecha= n

        #Actualizacion de los factores de equilibrio
        if(n2.Equilibrio == 1):
            n1.Equilibrio = -1
        else:
            n1.Equilibrio = 0
        if(n2.Equilibrio == -1):
            n.Equilibrio = 1
        else:
            n.Equilibrio = 0
        n2.Equilibrio = 0
        return n2

    #Rotacion Derecha derecha
    def RotacionDD(self,n,n1):
        n.Derecha = n1.Izquierda
        n1.Izquierda = n
        #Actualizacion
        if(n1.Equilibrio == 1):
            n.Equilibrio = 0
            n1.Equilibrio = 0
        else:
            n.Equilibrio = +1
            n1.Equilibrio = -1
        return n1

    #Rotacion Derecha Izquierda
    def RotacionDI(self, n, n1):
        n2 = n1.Izquierda
        n.Derecha = n2.Izquierda
        n2.Izquierda= n
        n1.Izquierda = n2.Derecha
        n2.Derecha = n1
        #Actualizacion de los factores de equilibrio
        if(n2.Equilibrio == 1):
            n.Equilibrio = -1
        else:
            n.Equilibrio = 0
        if(n2.Equilibrio == -1):
            n1.Equilibrio = 1
        else:
            n1.Equilibrio = 0
        n2.Equilibrio = 0
        return n2

    def InsertarArbol(self,Carnet,Nombre):
        #el objetivo es mandar desde aqui la raiz
        Comprobarh = Logical(False)
        self.Raiz=self.InsertarData(self.Raiz,Carnet,Nombre,Comprobarh)

    def InsertarData(self, raiz, carnet, nombre, ComprobacionRT):

        if (raiz is None):
            raiz = Nodo(carnet,nombre)
            ComprobacionRT.setLogical(True)
        elif (carnet < raiz.Carnet):
            NodoI = self.InsertarData(raiz.Izquierda, carnet, nombre, ComprobacionRT)
            raiz.Izquierda = NodoI
            if (ComprobacionRT.GetValue()):
                if (raiz.Equilibrio == 1):
                    raiz.Equilibrio = 0
                    ComprobacionRT.setLogical(False)
                elif (raiz.Equilibrio == 0):
                    raiz.Equilibrio = -1
                elif (raiz.Equilibrio == -1):

                    n1 = raiz.Izquierda
                    if (n1.Equilibrio == -1):
                        raiz = self.RotacionII(raiz, n1)
                    else:
                        raiz = self.RotacionID(raiz, n1)
                    ComprobacionRT.setLogical(False)
        elif (carnet > raiz.Carnet):
            NodoD = self.InsertarData(raiz.Derecha, carnet, nombre, ComprobacionRT)
            raiz.Derecha = NodoD
            if (ComprobacionRT.GetValue()):

                if (raiz.Equilibrio == 1):

                    n1 = raiz.Derecha
                    if (n1.Equilibrio == 1):
                        raiz = self.RotacionDD(raiz, n1)
                    else:
                        raiz = self.RotacionDI(raiz, n1)
                    ComprobacionRT.setLogical(False)
                elif (raiz.Equilibrio == 0):
                    raiz.Equilibrio = 1
                elif (raiz.Equilibrio == -1):
                    raiz.Equilibrio = 0
                    ComprobacionRT.setLogical(False)
        return raiz



    def GraficarArbol(self):
        self.CadenaImprimir = "digraph ARBOL { " + '\n'
        self.CadenaImprimir += "rankdir=TB" + '\n'
        self.CadenaImprimir += 'size="9,9"' + '\n'
        self.CadenaImprimir += 'node[shape=record,style=filled] ' + '\n'
        #obtenemos alturas
        alt=0
        self.Altura(self.Raiz,alt)
        self.DatosArbol(self.Raiz,alt)
        self.CadenaImprimir += '\n' + "}"
        file = open("Arbol.dot", "w")
        file.write(self.CadenaImprimir)
        file.close()
        os.system('dot -Tpng Arbol.dot -o  Arbol.jpg')
        os.system('Start Arbol.jpg')



    def Altura(self,NodoRaiz,altura):
        if(NodoRaiz is not None):
            self.Altura(NodoRaiz.Izquierda,altura+1)
            if(altura>self.AlturaMax):
                self.AlturaMax=altura
            self.Altura(NodoRaiz.Derecha,altura+1)

    def DatosArbol(self,NodoRaiz,alt):

        NodoRaiz.Altura=(self.AlturaMax-alt)
        self.CadenaImprimir += "\"" + str(NodoRaiz.Carnet) + str(NodoRaiz.Nombre) + "\"" + "[label =\"<C0>|<C1>" + "Carnet: " + str(NodoRaiz.Carnet) + "\\n Nombre:  " + str(NodoRaiz.Nombre) + "\\n Altura:  " + str(NodoRaiz.Altura) + "\\n FE:  " + str(NodoRaiz.Equilibrio) + "|<C2>\"]; \n"

        if(NodoRaiz.Izquierda is not None ):
            self.DatosArbol(NodoRaiz.Izquierda,alt+1)
            self.CadenaImprimir += "\""+ str(NodoRaiz.Carnet) + str(NodoRaiz.Nombre) +"\":C0->"+"\""+str(NodoRaiz.Izquierda.Carnet)+str(NodoRaiz.Izquierda.Nombre)+"\"; \n"
        if (NodoRaiz.Derecha is not None):
            self.DatosArbol(NodoRaiz.Derecha,alt+1)
            self.CadenaImprimir += "\"" + str(NodoRaiz.Carnet) + str(NodoRaiz.Nombre) + "\":C2->" + "\"" + str(NodoRaiz.Derecha.Carnet) + str(NodoRaiz.Derecha.Nombre) + "\"; \n"

    #Recorridos
    def GraficarInorden(self):
        self.CadenaImprimir = "digraph ARBOLInorden { " + '\n'
        self.CadenaImprimir += "rankdir=LR" + '\n'
        self.CadenaImprimir += 'node[shape=record,style=filled] ' + '\n'
        self.size=0
        self.DatosInorden(self.Raiz)
        self.CadenaImprimir += '\n' + "}"
        file = open("ArbolInorden.dot", "w")
        file.write(self.CadenaImprimir)
        file.close()
        os.system('dot -Tpng ArbolInorden.dot -o  ArbolInorden.jpg')
        os.system('Start ArbolInorden.jpg')

    def DatosInorden(self,NodoRaiz):
        if(NodoRaiz is not None):
            self.DatosInorden(NodoRaiz.Izquierda)
            self.CadenaImprimir+="\""+ str(self.size) +"\""+"[label = \"Carnet: "+str(NodoRaiz.Carnet)+ "\\n Nombre: "+str(NodoRaiz.Nombre)+"\"]; \n"
            self.CadenaImprimir+="\""+ str(self.size) +"\" ->"+"\""+ str(self.size+1) +"\" \n"
            self.size = self.size + 1
            self.DatosInorden(NodoRaiz.Derecha)

    def GraficarPreorden(self):
        self.CadenaImprimir = "digraph ARBOLPreorden { " + '\n'
        self.CadenaImprimir += "rankdir=LR" + '\n'
        self.CadenaImprimir += 'node[shape=record,style=filled] ' + '\n'
        self.size=0
        self.DatosPreorden(self.Raiz)
        self.CadenaImprimir += '\n' + "}"
        file = open("ArbolPreorden.dot", "w")
        file.write(self.CadenaImprimir)
        file.close()
        os.system('dot -Tpng ArbolPreorden.dot -o  ArbolPreorden.jpg')
        os.system('Start ArbolPreorden.jpg')

    def DatosPreorden(self,NodoRaiz):
        if(NodoRaiz is not None):
            self.CadenaImprimir+="\""+ str(self.size) +"\""+"[label = \"Carnet: "+str(NodoRaiz.Carnet)+ "\\n Nombre: "+str(NodoRaiz.Nombre)+"\"]; \n"
            self.CadenaImprimir+="\""+ str(self.size) +"\" ->"+"\""+ str(self.size+1) +"\" \n"
            self.size = self.size + 1
            self.DatosPreorden(NodoRaiz.Izquierda)
            self.DatosPreorden(NodoRaiz.Derecha)


    def GraficarPosorden(self):
        self.CadenaImprimir = "digraph ARBOLPosorden { " + '\n'
        self.CadenaImprimir += "rankdir=LR" + '\n'
        self.CadenaImprimir += 'node[shape=record,style=filled] ' + '\n'
        self.size=0
        self.DatosPosorden(self.Raiz)
        self.CadenaImprimir += '\n' + "}"
        file = open("ArbolPosorden.dot", "w")
        file.write(self.CadenaImprimir)
        file.close()
        os.system('dot -Tpng ArbolPosorden.dot -o  ArbolPosorden.jpg')
        os.system('Start ArbolPosorden.jpg')

    def DatosPosorden(self,NodoRaiz):
        if(NodoRaiz is not None):
            self.DatosPosorden(NodoRaiz.Izquierda)
            self.DatosPosorden(NodoRaiz.Derecha)
            self.CadenaImprimir+="\""+ str(self.size) +"\""+"[label = \"Carnet: "+str(NodoRaiz.Carnet)+ "\\n Nombre: "+str(NodoRaiz.Nombre)+"\"]; \n"
            self.CadenaImprimir+="\""+ str(self.size) +"\" ->"+"\""+ str(self.size+1) +"\" \n"
            self.size = self.size + 1

    def ImprimirInorden(self,NodoRaiz,cadena):
        if(NodoRaiz is not None):
            self.DatosInorden(NodoRaiz.Izquierda,cadena)
            cadena+=" -> "+str(NodoRaiz.Carnet)+"-"+str(NodoRaiz.Nombre)
            self.DatosInorden(NodoRaiz.Derecha,cadena)
        return cadena

    def ImprimirPreorden(self,NodoRaiz,cadena):
        if(NodoRaiz is not None):
            cadena += " -> " + str(NodoRaiz.Carnet) + "-" + str(NodoRaiz.Nombre)
            self.DatosInorden(NodoRaiz.Izquierda,cadena)
            self.DatosInorden(NodoRaiz.Derecha,cadena)
        return cadena

    def ImprimirPosorden(self,NodoRaiz,cadena):
        if(NodoRaiz is not None):
            self.DatosInorden(NodoRaiz.Izquierda,cadena)
            self.DatosInorden(NodoRaiz.Derecha,cadena)
            cadena += " -> " + str(NodoRaiz.Carnet) + "-" + str(NodoRaiz.Nombre)
        return cadena


#tree = ArbolAVL_B()
#tree.InsertarArbol(10,"a")
#tree.InsertarArbol(6,"b")
#tree.InsertarArbol(8,"c")
#tree.InsertarArbol(15,"d")
#tree.InsertarArbol(7,"e")
#tree.InsertarArbol(1,"f")
#tree.InsertarArbol(9,"g")
#tree.InsertarArbol(11,"h")
#tree.InsertarArbol(3,"i")
#tree.InsertarArbol(17,"j")
#tree.InsertarArbol(12,"k")
#tree.InsertarArbol(13,"m")

#tree.GraficarArbol()
#tree.GraficarInorden()
#tree.GraficarPreorden()
#tree.GraficarPosorden()