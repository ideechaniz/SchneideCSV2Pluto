#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Requiere python 3.2 minimo

'''
Script para cambiar el formato de fecha de los ComX de Schneider para Eneko en Elektra.
¿Porque?: Algunos ficheros tenian el formato de fecha incorrecto.

26/06/2019 Iker De Echaniz Herce

Coge un "Fichero.csv" de entrada y genera otro en "Fecha_Cambiado_Orden\Fichero.csv"

Nota: Desde Windows puedes hacer algo asi para varios ficheros:
     for %i in (*.csv) do fechas.py %i

Informacion sobre formato de fichero original
================================================
Hasta la linea numero 8 texto a no tratar
La linea numero 8 tiene valores separados en comas.
Las siguientes lineas hasta el fin de fichero tienen el mismo formato que la linea numero 8.

El tercer campo de los valores separados por comas es el "Local Time Stamp" tiene el formato:
20-02-2017 17:15:00
Hay que cambiarlo al siguiente formato:
20-02-2017 17:15:00

'''

import os
import sys

version="0.2"

# Logica de cambiar la fecha
# ============================
def cambia_la_fecha(linea):
    lista_campos=linea.split(",")
    # print(lista_campos[2])

    fecha_hora=lista_campos[2].split(" ")
    
    fecha=fecha_hora[0].split("-")
    dia=fecha[0]
    mes=fecha[1]
    ano=fecha[2]

    hora=fecha_hora[1]  
    # print("Dia="+dia+" mes="+mes+ " año="+ano+" Hora="+hora)

    # AQUI ES DONDE PONES EL FORMATO QUE TE DE LA GANA
    lista_campos[2]=ano+"-"+mes+"-"+dia+" "+hora
    
    linea_cambiada=', '.join(lista_campos)
    print("Linea cambiada="+ linea_cambiada)
    return linea_cambiada   


# Ayuda, parametros y creacion de directorio destino.
def preliminares():
  if len(sys.argv) <2 :
    print("Necesito el fichero a cambiar de formato como parametro")
    sys.exit(1)

  os.makedirs("Fecha_Cambiado_Orden", exist_ok=True)    
  
# Programa Principal
# =====================

preliminares()

f = open(sys.argv[1])
f1 = open(".\\Fecha_Cambiado_Orden\\"+ f.name,"w") 

# Leer el original y escribir el nuevo fichero linea a linea.
linea = f.readline()
numlinea=0
while linea:
  
  if (numlinea >= 8): # Aqui ya hay fechas
    linea=cambia_la_fecha(linea)

  f1.write(linea)

  linea = f.readline()
  numlinea+=1

f.close()
f1.close()


