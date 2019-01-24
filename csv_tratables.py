#!/usr/bin/env python
#
# csv_tratable.py 1.5 24/01/2019
# Iker De Echaniz ideechaniz@gmail.com
# Genera CSV tratables a traves de los falsos CSV de Schneider Electric para Elektra en Martutene
# Requiere python 3.2 minimo
#  
# Changelog
# 1.5 Incluir funcion tantas_lineas_en_tmp1_como_en_tmp2 para tratar datos finales con pluto
#     Incluir debugeo avanzado con nombre de funcion
# 1.4.1 Incluir aviso en ayuda de que las rutas con espacios deben ir entre comillas
# 1.4 Incluir ayuda y numero de version en la ayuda
# 1.3 Crear directorios de destino con el nombre del fichero en el directorio base destino.
#     Que no importe si el fichero destino ya existe y lo sobreescriba
# 1.2 Dejar en variable dir_origen, dir_destino y lugar
# 1.1 Cambiar el nombre de los ficheros tratados para no nombrar fecha para ser encontrados por pluto
# 1.0 Version inicial 

import os
import sys
import getopt
import logging
import pandas as pd # pip install pandas

version="1.5"
    
def main(argv):
  logger.debug('Modo Debug activado')
  
  dir_origen=""
  dir_destino=""
  lugar=""
  
  if len(sys.argv) < 4:
    ayuda()
    sys.exit(2)
  
  try:
     opts, args = getopt.getopt(argv,"o:d:l:",["origen=","destino=","lugar="])
  except getopt.GetoptError:
    ayuda()
    sys.exit(2)
  for opt, arg in opts:
     if opt in ("-o", "--origen"):
        dir_origen = arg
     elif opt in ("-d", "--destino"):
        dir_destino = arg
     elif opt in ("-l", "--lugar"):
        lugar = arg
     else:
       ayuda()
       sys.exit(2)
  
  logger.debug("Origen= %s " % dir_origen)
  logger.debug("Destino= %s" % dir_destino)
  logger.debug("Lugar= %s" % lugar)
   
  os.chdir(dir_origen)
  files= os.listdir('.')
  for fichero in files:
    if lugar in fichero:
      if not "tratado_" in fichero:
        logger.info(fichero)
        a_dos_ficheros(fichero)
        tantas_lineas_en_tmp1_como_en_tmp2(fichero)
        fichero_tratado="tratado_"+fichero[0:-19]+".csv"
        concatenar(fichero+"_tmp1",fichero+"_tmp2",fichero_tratado)
        borrar_temporales(fichero)
        logger.debug("Moviendo "+ fichero_tratado +" a "+ dir_destino+"\\"+fichero[0:-19]+"\\")
        os.makedirs(dir_destino+"\\"+fichero[0:-19], exist_ok=True)
        os.replace(fichero_tratado, dir_destino+"\\"+fichero[0:-19]+"\\"+fichero_tratado) #os no tiene mv tiene rename y replace

# Magia me crea datos donde no habia copiando una fila n veces.
def tantas_lineas_en_tmp1_como_en_tmp2(fichero_original):

  # leer cantidad de lineas en el tmp2
  f2= open(fichero_original+"_tmp2")
  line=f2.readline()
  numlinef2=0
  while line:    
    #print(line)
    line = f2.readline()
    numlinef2=numlinef2 +1
  f2.close()
  logger.debug("Lineas en f2=%d" % numlinef2);
   
  #Abrir fichero 1 y guardar dos primeras lineas en variable
  f1= open(fichero_original+"_tmp1")
  f1_linea0=f1.readline() 
  f1_linea1=f1.readline()
  f1.close()
  
  #Abrir fichero 1 en escritura y escribir primera linea y la segunda numlinef2 veces.
  f1= open(fichero_original+"_tmp1","w")
  f1.write(f1_linea0)
  for x in range(numlinef2 -1): #todo menos el titulo de cabecera
    f1.write(f1_linea1)
  f1.close()  
  
# Crea dos ficheros a partir de un CSV de Martutene para tratar los CSV
def a_dos_ficheros(fichero_original):
  f = open(fichero_original)
  line = f.readline()

  f1 = open(f.name+"_tmp1","w") 
  f2 = open(f.name+"_tmp2","w") 

  numline=0
  while line:
	#Primera parte del CSV a un fichero
    if(numline <= 1):
      f1.write(line)

	# Lo de entre medias lo ignoramos
	
	#Segunda parte del CSV a otro fichero
    if (numline >= 6):
      f2.write(line)

    line = f.readline()
    numline=numline+1

  logger.debug(fichero_original +" dividido en " + f1.name + " y " + f2.name)
  f.close()
  f1.close()
  f2.close()

def concatenar(A,B,C): # A y B en C
  a= pd.read_csv(A, sep=';')
  b= pd.read_csv(B, sep=';')

  # axis=1 son columnas, axis=0 son filas.
  result= pd.concat([a,b], axis=1, join='outer', sort=False, ignore_index=False)
  result.to_csv(C, sep=';', index=False)
  logger.debug(A + " " + B + " unidos en "+ C)

def borrar_temporales(fichero):
  os.remove(fichero+"_tmp1")  
  os.remove(fichero+"_tmp2")
  logger.debug("Borrados temporales "+ fichero+"_tmp1" + " y " +fichero+"_tmp2")

def ayuda():
  print("csv_tratables.py %s crea unos CSV reales a partir de los falsos de Schneider para uso con Pluto\n" % version)
  print("csv_tratables.py -o directorio_origen -d directorio_destino -l lugar")
  print("\nEjemplo:")
  print('csv_tratables.py -o "C:\\Users\\x230\\Origen" -d "C:\\Users\\x230\\Destino" -l "MARTUTENE"')
  print("Nota: Si los parametros tienen espacios ponlos entre comillas")
    
if __name__== "__main__":
  FORMAT = "%(funcName)s => %(message)s"
  logging.basicConfig(level=logging.INFO, format=FORMAT)
  logger = logging.getLogger(__name__ )
  #logger.setLevel(logging.DEBUG) 
  main(sys.argv[1:])