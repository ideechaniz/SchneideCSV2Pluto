#
#  subirftp.py Version 1.0 07/02/2019 Iker De Echaniz ideechaniz@gmail.com
#
#  Sube ficheros con un nombre determinado por FTP a un server y luego los borra localmente
#  Si no consigue subir el fichero, luego no lo borra.
#

import os
import sys
import ftplib

# Configuracion para subir ficheros a DEXMA
# -------------------------------------------------------------
SERVER="192.16.16.82"
USER="iker"
PASSWORD="unapass"
ORIGEN="C:\\Users\\Iker\\Desktop\\borrame" # Directorio origen, recuerda usar dos \\ para \
NOMBRE="MARTUTENE" # Palabra clave en el nombre de los ficheros
# ---------------------------------------------------------------

def uploadFTP(fichero, dirDestino, server, username, password):
  ftp = ftplib.FTP(server, username, password)
  ftp.cwd(dirDestino)
  print("%s Subiendo" % fichero)
  fh = open(fichero, 'rb')
  
  try:
    ftp.storbinary('STOR %s' % fichero, fh)
  except ftplib.all_errors:
    fh.close()
    return "Error"    
  else:
    fh.close()
    return "Ok"


def main():
  print("Script para subir ficheros al FTP de Dexma")
  print("Cambiando a directorio %s" % ORIGEN)
  os.chdir(ORIGEN)

  dir = os.listdir()
  for fichero in dir:
    if NOMBRE in fichero:
      if os.path.isfile(fichero):
        print("%s Encontrado" % fichero)
        
        if uploadFTP(fichero,"/",SERVER, USER, PASSWORD) == "Ok":
          print("%s Subido correctamente" % fichero)
          os.remove(fichero)
          print("%s Borrado localmente" % fichero)
        else:
          print("Error, %s no se ha subido (tampoco se ha borrado localmente)" % fichero)

 
if __name__== "__main__":
  main()
