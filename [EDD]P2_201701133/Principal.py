#Librerias
import csv
import threading
import socket
import select
import sys
import os
import os.path
import time
#para instalar curses python -m pip install windows-curses

from ListaDoble_Block import  ListaDoblementeEnlazada_Block



#variables del menu
opcion =0


def Pintado_Menu():
    os.system("cls")
    print("                 MENU PRINCIPAL")
    print("")
    print('                 1. INSERT BLOCK  ')#49
    print('                 2. SELECT BLOCK  ')  # 49
    print('                 3. REPORTS  ')  # 49
    print('                 4. EXIT  ')  # 49


#Creacion de la lista
ListaBlockes=ListaDoblementeEnlazada_Block()

#Bloque
NodoBLOCK=None
#Comprobacion si hay que enviar
Envio=1
Cadenatruefalse="false"

EnvioJson=""
#Hilo y Servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("                 INGRESE IP DEL SERVIDOR")
NombreIP=input()
print("")
print("                 INGRESE PUERTO DEL SERVIDOR")
Puerto=int(input())
server.connect((NombreIP, Puerto))
Pintado_Menu()



def LeerNOTOCAR():
    f = open('NOTOCAR.txt', 'r')
    mensaje = f.read()
    f.close()
    global Cadenatruefalse
    Cadenatruefalse=ListaBlockes.VerificadorJSON(mensaje)

def InsertarNOTOCAR():
    f = open('NOTOCAR.txt', 'r')
    mensaje = f.read()
    ListaBlockes.InsertarDesdeJSON(mensaje)
    f.close()


def Conexion():
    while True:
        read_sockets = select.select([server], [], [], 1)[0]
        import msvcrt
        if msvcrt.kbhit(): read_sockets.append(sys.stdin)
        # para recibir
        if (server is not None):

            message = server.recv(2048)
            if (message.decode('utf-8') == "true" or message.decode('utf-8') == "false"):
                #print("")
                if (message.decode('utf-8') == "true"):
                    InsertarNOTOCAR()

            else:
                file = open("NOTOCAR.txt", "w")
                file.write(message.decode('utf-8'))
                file.close()
                LeerNOTOCAR()
                Ms = Cadenatruefalse
                server.sendall(Ms.encode('utf-8'))


#inicio de menu
hilo=threading.Thread(target=Conexion)
hilo.start()
iteradormessage = server.recv(2048)
paso=iteradormessage.decode('utf-8')
while opcion==0:

    #obtenemos posicion del menu
    opcion= int(input())
    if (opcion == 1):#metodo insrtar
        #opcion 1
        nombrecorrecto=50
        while(nombrecorrecto==50):
            #variable para enviar a la lista doble
            NombreEnvio=""
            CadenaEnvio=""
            os.system("cls")
            print("                     INSERT BLOCK")
            print("                     INGRESE EL NOMBRE DEL ARCHIVO")
            nombre = input()
            print("                     "+nombre)
            print("                     ¿EL NOMBRE ES CORRECTO?")
            print("                     1.  SI")
            print("                     2.  NO")
            nombrecorrecto=int(input())
            if(nombrecorrecto==1):
                #probando con libreria csv
                with open(nombre) as File:
                    Lectura=csv.reader(File)
                    ReservadaCLASE,NombreCLASE=next(Lectura)
                    ReservadaDATA,InfoDATA=next(Lectura)
                    file = open("CONcsv.txt", "w")
                    file.write(InfoDATA)
                    file.close()
                EnvioJson=ListaBlockes.Insertar_Final(NombreCLASE,InfoDATA,"")
                #para validacion de enviio
                message = EnvioJson
                server.sendall(message.encode('utf-8'))




            elif(nombrecorrecto==50):
                #no pasa nada
                nombrecorrecto = 50

        Pintado_Menu()
        opcion=0
    elif(opcion==2):#opcion 2
        CambioSeleccion=0
        Fin_Ciclo=0
        #Prueba
        while(Fin_Ciclo==0):
            os.system("cls")
            print("                     SELECT BLOCK ")
            print("                   <-  Cambio  ->")
            CadenaNombre=ListaBlockes.Seleccion(CambioSeleccion)
            print("                     INDEX: "+str(CadenaNombre.INDEX))
            print("                     TIMESTAMP: "+str(CadenaNombre.TIMESTAMP))
            print("                     DATA: "+CadenaNombre.DATA[0:60])
            print("                     PREVIOUSHASH: "+CadenaNombre.PREVIOUSHASH[0:30])
            print("                     HASH: "+CadenaNombre.HASH[0:30])
            print("                     ¿DESEA SELECCIONAR?")
            print("                     1.  SI")
            print("                     2.  IZQUIERDA")
            print("                     3.  DERECHA")
            print("                     4.  NO")
            opcionseleccion = int(input())
            if(opcionseleccion==3):
                CambioSeleccion+=1
                if(CambioSeleccion>ListaBlockes.size):
                    CambioSeleccion=ListaBlockes.size
                if(CambioSeleccion<0):
                    CambioSeleccion=0
            elif (opcionseleccion == 2):
                CambioSeleccion -= 1
            elif(opcionseleccion==1):
                NodoBLOCK=ListaBlockes.Seleccion(CambioSeleccion)
                Fin_Ciclo=1
            elif(opcionseleccion==4):
                Fin_Ciclo=1

        # fin de abrir archivo5
        Pintado_Menu()
        opcion = 0

    elif(opcion==3):#opcion 3
        os.system("cls")
        print("                     REPORTS")
        print("                     1. BLOCKCHAIN")
        print("                     2. TREE REPORT")
        opcionreporte=int(input())
        if(opcionreporte==1):
            ListaBlockes.Graficar()
        #opcion de de reporte
        if(opcionreporte==2):
            os.system("cls")
            print("                     TREE REPORTS")
            print("                     1. TREE")
            print("                     2. RECORRIDOS")
            opcionarbol=int(input())
            if(opcionarbol==1):#opcion 1
                if(NodoBLOCK is None):
                    print("                     NO SE HA SELECCIONADO UN BLOCK")
                else:
                    NodoBLOCK.ARBOL.GraficarArbol()

            if(opcionarbol==2):#opcion 2
                os.system("cls")
                print("                     RECORRIDOS")
                print("                     1. INORDEN")
                print("                     2. PREORDEN")
                print("                     3. POSTORDEN")

                opcionrecorrido=int(input())
                if(opcionrecorrido==1):#opcion 1
                    if (NodoBLOCK is None):
                        print("                     NO SE HA SELECCIONADO UN BLOCK")
                    else:
                        #imagen
                        NodoBLOCK.ARBOL.GraficarInorden()
                        #consola
                        print("                     RECORRIDO INORDEN")
                        NodoBLOCK.ARBOL.CadenaConsola=""
                        NodoBLOCK.ARBOL.ImprimirInorden(NodoBLOCK.ARBOL.Raiz)
                        print("")
                        print("                INICIO->"+NodoBLOCK.ARBOL.CadenaConsola)
                        print("                Ingrese Salir para salir")
                        pausa=input()

                if (opcionrecorrido == 2):  # opcion 2
                    if (NodoBLOCK is None):
                        print("                     NO SE HA SELECCIONADO UN BLOCK")
                    else:
                        # imagen
                        NodoBLOCK.ARBOL.GraficarPreorden()
                        # consola
                        print("                     RECORRIDO PREORDEN")
                        NodoBLOCK.ARBOL.CadenaConsola = ""
                        NodoBLOCK.ARBOL.ImprimirPreorden(NodoBLOCK.ARBOL.Raiz)
                        print("")
                        print("                INICIO->" + NodoBLOCK.ARBOL.CadenaConsola)
                        print("                Ingrese Salir para salir")
                        pausa = input()

                if (opcionrecorrido == 3):  # opcion 3
                    if (NodoBLOCK is None):
                        print("                     NO SE HA SELECCIONADO UN BLOCK")
                    else:
                        # imagen
                        NodoBLOCK.ARBOL.GraficarPosorden()
                        # consola
                        print("                     RECORRIDO POSTORDEN")
                        NodoBLOCK.ARBOL.CadenaConsola = ""
                        NodoBLOCK.ARBOL.ImprimirPosorden(NodoBLOCK.ARBOL.Raiz)
                        print("")
                        print("                INICIO->" + NodoBLOCK.ARBOL.CadenaConsola)
                        print("                Ingrese Salir para salir")
                        pausa = input()


        # fin de abrir archivo5
        Pintado_Menu()
        opcion = 0

    elif (opcion==4):
        #opcion 4 Salir
        opcion = 100
        server.close()
    else:
        opcion=0


#Cierra ventanas
