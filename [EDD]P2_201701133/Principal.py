#Librerias
#para instalar curses python -m pip install windows-curses
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import subprocess
import os
from ListaDoble_Block import  ListaDoblementeEnlazada_Block



#Metodos de Curses
stdscr = curses.initscr()
TamañoTablero_y=20
TamañoTablero_x=70
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
    Vent.addstr(7,21, '1. INSERT BLOCK  ')#49
    Vent.addstr(8,21, '2. SELECT BLOCK')#50
    Vent.addstr(9,21, '3. REPORTS')#51
    Vent.addstr(10,21, '4. EXIT')#52

    Vent.timeout(-1)

def Pintado_Titulo(Vent,cadena):
    Vent.clear()
    Vent.border(0)
    posicion_x = round((60-len(cadena))/2)
    Vent.addstr(0,posicion_x,cadena)

#Muestra Pantalla
ListaBlockes=ListaDoblementeEnlazada_Block()
Pintado_Menu(window)
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
            window.addstr(7, 19, 'INGRESE EL NOMBRE DEL ARCHIVO')
            nombre = window.getstr(0, 0, 40)
            window.addstr(8, 23, nombre)
            window.addstr(9, 19, '¿EL NOMBRE ES CORRECTO?')
            window.addstr(10, 19, '1.  SI')
            window.addstr(11, 19, '2.  NO')
            nombrecorrecto=window.getch()
            if(nombrecorrecto==49):
                #iterador para datos
                CadenaImprimir=""
                CambioCarga=0
                #NOTA:Colocar extension
                f = open(nombre)
                for linea in f:
                    Dato=linea.split(",")
                    if(Dato[0]=="Class" or Dato[0]=="CLASS" or Dato[0]=="class" ):
                        CambioCarga = 1
                    if (Dato[0] == "Data" or Dato[0] == "DATA" or Dato[0] == "data"):
                        CambioCarga = 2
                    if(CambioCarga==1):
                        NombreEnvio=Dato[1]
                    if(CambioCarga==2):
                        for i in range(len(Dato)):
                            if(Dato[0]!=Dato[i]):
                                CadenaEnvio+=Dato[i]
                                CadenaImprimir+=Dato[i]

                file = open("L.txt", "w")
                file.write(CadenaImprimir)
                file.close()

                #insertamos el valor en la lista
                ListaBlockes.Insertar_Final(NombreEnvio,CadenaEnvio)


            elif(nombrecorrecto==50):
                #no pasa nada
                nombrecorrecto = 50

        window.addstr(12, 21, 'Presione DELETE para salir')

        #fin de abrir archivo
        Espera_Salir(window)
        Pintado_Menu(window)
        opcion=0

    elif(opcion==51):#opcion 3
        Pintado_Titulo(window, ' REPORTS ')
        window.addstr(7, 21, '1. BLOCKCHAIN ')  # 49
        window.addstr(8, 21, '2. TREE REPORT')  # 50
        window.addstr(12, 21, 'Presione DELETE para salir')
        opcionreporte=window.getch()
        if(opcionreporte==49):
            ListaBlockes.Graficar()
        #opcion de de reporte
        if(opcionreporte==50):
            Pintado_Titulo(window, ' TREE REPORTS ')
            window.addstr(7, 21, '1. TREE ')  # 49
            window.addstr(8, 21, '2. RECORRIDOS')  # 50
            window.addstr(12, 21, 'Presione DELETE para salir')
        # fin de abrir archivo5
        Espera_Salir(window)
        Pintado_Menu(window)
        opcion = 0

    elif (opcion==52):
        #opcion 4 Salir
        opcion = 100
    else:
        opcion=0


curses.endwin() #Cierra ventanas
