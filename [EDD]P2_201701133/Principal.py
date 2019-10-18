#Librerias
import csv
import threading
import socket
import select
import sys
#para instalar curses python -m pip install windows-curses
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

from ListaDoble_Block import  ListaDoblementeEnlazada_Block



#Metodos de Curses
stdscr = curses.initscr()
TamañoTablero_y=20
TamañoTablero_x=80
window = curses.newwin(TamañoTablero_y,TamañoTablero_x,0,0)
window.keypad(True)
curses.noecho()
curses.curs_set(0)
window.nodelay(True)


#variables del menu
opcion =0

def Espera_Salir(Vent):
    key = Vent.getch()
    while key!=8:#posicion para retroceder DELETE
        key = Vent.getch()

def Pintado_Menu(Vent):
    Pintado_Titulo(Vent,' MENU PRINCIPAL ')
    Vent.addstr(7,25, '1. INSERT BLOCK  ')#49
    Vent.addstr(8,25, '2. SELECT BLOCK')#50
    Vent.addstr(9,25, '3. REPORTS')#51
    Vent.addstr(10,25, '4. EXIT')#52

    Vent.timeout(-1)

def Pintado_Titulo(Vent,cadena):
    Vent.clear()
    Vent.border(0)
    posicion_x = round((60-len(cadena))/2)
    Vent.addstr(0,posicion_x,cadena)

#Muestra Pantalla
ListaBlockes=ListaDoblementeEnlazada_Block()
#Pintado_Menu(window)
#Bloque
NodoBLOCK=None
#Comprobacion si hay que enviar
Envio=False
EnvioJson=""
#Hilo y Servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

window.addstr(7, 23, 'INGRESE IP DEL SERVIDOR')
NombreIP= window.getstr(0, 0, 40)
window.addstr(8, 23, NombreIP)
window.addstr(9, 23, 'INGRESE PUERTO DEL SERVIDOR')
Puerto= int(window.getstr(0, 0, 40))
window.addstr(10, 23, str(Puerto))
server.connect((NombreIP, Puerto))
Pintado_Menu(window)

def Conexion():
    while True:
        read_sockets = select.select([server], [], [], 1)[0]
        import msvcrt
        if msvcrt.kbhit(): read_sockets.append(sys.stdin)
        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                Pintado_Titulo(window, " ENTRADA MENSAJE DEL SERVIDOR ")
                window(7,15,message.decode('utf-8'))
            else:
                if(Envio is True):
                    Pintado_Titulo(window, " ENVIO MENSAJE AL SERVIDOR ")
                    server.sendall(EnvioJson.encode('utf-8'))
                    Envio=False
                    Pausa= int(window.getstr(0, 0, 40))




#inicio de menu
hilo=threading.Thread(target=Conexion)
hilo.start()
while opcion==0:
    #obtenemos posicion del menu
    opcion= window.getch()
    if (opcion == 49):#metodo insrtar
        #opcion 1
        nombrecorrecto=50
        while(nombrecorrecto==50):
            #variable para enviar a la lista doble
            NombreEnvio=""
            CadenaEnvio=""
            Pintado_Titulo(window, " INSERT BLOCK ")
            window.addstr(7, 23, 'INGRESE EL NOMBRE DEL ARCHIVO')
            nombre = window.getstr(0, 0, 40)
            window.addstr(8, 25, nombre)
            window.addstr(9, 25, '¿EL NOMBRE ES CORRECTO?')
            window.addstr(10, 25, '1.  SI')
            window.addstr(11, 25, '2.  NO')
            nombrecorrecto=window.getch()
            if(nombrecorrecto==49):
                #probando con libreria csv
                with open(nombre) as File:
                    Lectura=csv.reader(File)
                    ReservadaCLASE,NombreCLASE=next(Lectura)
                    ReservadaDATA,InfoDATA=next(Lectura)
                    file = open("CONcsv.txt", "w")
                    file.write(InfoDATA)
                    file.close()
                EnvioJson=ListaBlockes.Insertar_Final(NombreCLASE,InfoDATA)
                Envio=True


            elif(nombrecorrecto==50):
                #no pasa nada
                nombrecorrecto = 50

        window.addstr(12, 21, 'Presione DELETE para salir')

        #fin de abrir archivo
        Espera_Salir(window)
        Pintado_Menu(window)
        opcion=0
    elif(opcion==50):#opcion 2
        CambioSeleccion=0
        Fin_Ciclo=0
        #Prueba
        while(Fin_Ciclo==0):
            Pintado_Titulo(window, ' SELECT BLOCK ')
            window.addstr(4, 21, "Cambio")
            window.addstr(4, 17, '->')
            window.addstr(4, 43, '<-')
            CadenaNombre=ListaBlockes.Seleccion(CambioSeleccion)
            window.addstr(5, 19, "INDEX: "+str(CadenaNombre.INDEX))
            window.addstr(6, 19, "TIMESTAMP: "+str(CadenaNombre.TIMESTAMP))
            window.addstr(7, 19, "DATA: " +CadenaNombre.DATA[0:60])
            window.addstr(12, 19, "PREVIOUSHASH: " +CadenaNombre.PREVIOUSHASH[0:30])
            window.addstr(13, 19, "HASH: " +CadenaNombre.HASH[0:30])
            window.addstr(15, 19, '¿DESEA SELECCIONAR?')
            window.addstr(16, 19, '1.  SI')
            window.addstr(17, 19, 'Presione DELETE para salir')
            opcionseleccion = window.getch()
            if(opcionseleccion==KEY_RIGHT):
                CambioSeleccion+=1
                if(CambioSeleccion>ListaBlockes.size):
                    CambioSeleccion=ListaBlockes.size
                if(CambioSeleccion<0):
                    CambioSeleccion=0
            elif (opcionseleccion == KEY_LEFT):
                CambioSeleccion -= 1
            elif(opcionseleccion==49):
                NodoBLOCK=ListaBlockes.Seleccion(CambioSeleccion)
                Fin_Ciclo=1
            elif(opcionseleccion==8):
                Fin_Ciclo=1

        # fin de abrir archivo5
        Pintado_Menu(window)
        opcion = 0

    elif(opcion==51):#opcion 3
        Pintado_Titulo(window, ' REPORTS ')
        window.addstr(7, 25, '1. BLOCKCHAIN ')  # 49
        window.addstr(8, 25, '2. TREE REPORT')  # 50
        window.addstr(12, 25, 'Presione DELETE para salir')
        opcionreporte=window.getch()
        if(opcionreporte==49):
            ListaBlockes.Graficar()
        #opcion de de reporte
        if(opcionreporte==50):
            Pintado_Titulo(window, ' TREE REPORTS ')
            window.addstr(7, 25, '1. TREE ')  # 49
            window.addstr(8, 25, '2. RECORRIDOS')  # 50
            window.addstr(12, 25, 'Presione DELETE para salir')
            opcionarbol=window.getch()
            if(opcionarbol==49):#opcion 1
                if(NodoBLOCK is None):
                    window.addstr(13, 21, 'NO SE HA SELECCIONADO UN BLOCK')
                else:
                    NodoBLOCK.ARBOL.GraficarArbol()

            if(opcionarbol==50):#opcion 2
                Pintado_Titulo(window, ' RECORRIDOS ')
                window.addstr(7, 25, '1. INORDEN ')  # 49
                window.addstr(8, 25, '2. PREORDEN')  # 50
                window.addstr(9, 25, '3. POSTORDEN')  # 51

                opcionrecorrido=window.getch()
                if(opcionrecorrido==49):#opcion 1
                    if (NodoBLOCK is None):
                        window.addstr(13, 21, 'NO SE HA SELECCIONADO UN BLOCK')
                    else:
                        #imagen
                        NodoBLOCK.ARBOL.GraficarInorden()
                        #consola
                        Pintado_Titulo(window, ' RECORRIDOS ')
                        NodoBLOCK.ARBOL.CadenaConsola=""
                        NodoBLOCK.ARBOL.ImprimirInorden(NodoBLOCK.ARBOL.Raiz)
                        window.addstr(7, 9, "INICIO->"+NodoBLOCK.ARBOL.CadenaConsola)
                        window.addstr(13, 21, 'Presione DELETE para salir')
                        Espera_Salir(window)

                if (opcionrecorrido == 50):  # opcion 2
                    if (NodoBLOCK is None):
                        window.addstr(13, 21, 'NO SE HA SELECCIONADO UN BLOCK')
                    else:
                        # imagen
                        NodoBLOCK.ARBOL.GraficarPreorden()
                        # consola
                        Pintado_Titulo(window, ' RECORRIDOS ')
                        NodoBLOCK.ARBOL.CadenaConsola = ""
                        NodoBLOCK.ARBOL.ImprimirPreorden(NodoBLOCK.ARBOL.Raiz)
                        window.addstr(7, 9, "INICIO->" + NodoBLOCK.ARBOL.CadenaConsola)
                        window.addstr(13, 21, 'Presione DELETE para salir')
                        Espera_Salir(window)

                if (opcionrecorrido == 51):  # opcion 3
                    if (NodoBLOCK is None):
                        window.addstr(13, 11, 'NO SE HA SELECCIONADO UN BLOCK')
                    else:
                        # imagen
                        NodoBLOCK.ARBOL.GraficarPosorden()
                        # consola
                        Pintado_Titulo(window, ' RECORRIDOS ')
                        NodoBLOCK.ARBOL.CadenaConsola = ""
                        NodoBLOCK.ARBOL.ImprimirPosorden(NodoBLOCK.ARBOL.Raiz)
                        window.addstr(7, 9, "INICIO->" + NodoBLOCK.ARBOL.CadenaConsola)
                        window.addstr(13, 21, 'Presione DELETE para salir')
                        Espera_Salir(window)


        # fin de abrir archivo5
        Pintado_Menu(window)
        opcion = 0

    elif (opcion==52):
        #opcion 4 Salir
        opcion = 100
        server.close()
    else:
        opcion=0


curses.endwin() #Cierra ventanas
