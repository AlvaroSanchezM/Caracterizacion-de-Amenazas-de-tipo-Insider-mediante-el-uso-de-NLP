#!/usr/bin/python
#Este script es para extraer y concatenar los contenidos de los correos de cada usuario
#en un solo String, y hacer un CSV, una lista o una tabla con el formato |user|String|

import os

carpeta_orig="enron_mail_20150507\\maildir"

# Get the list of all files and directories
path = os.getcwd()
user_list = os.listdir(path+"\\"+carpeta_orig) # Array of usernames (array of strings)
#print("Files and directories in '", path, "' :")
# prints all files
#print(user_list)


# Lista/archivo donde se escriben las cosas
# Leer la carpeta local en busca de archivos .txt
lista = os.listdir(path)
#print("Files and directories in '", pathy, "' :")
# prints all files
#print("lista ="+str(lista))
tipo="txt"
separ="_"
prefix="carpetas"# Los archivos de resultados se llaman resul_1.txt, resul_2.txt, etc
control = 0
for dir_folder in lista:
    if dir_folder.__contains__("."):
        parts = dir_folder.split(".")
        #print("parts ="+str(parts))
        if parts[1] == tipo:
            prefix_sep = parts[0].split(separ)
            #print("prefix_sep ="+str(prefix_sep))
            if prefix_sep[0] == prefix and int(prefix_sep[1]) > control:
                control = int(prefix_sep[1])
                #print("control="+str(control))
control = control + 1
# Ver el último número que hay, y crear el siguiente y abrir como escritura
resultFileName = prefix+separ+str(control)+"."+tipo
print("Resultados en "+resultFileName)
writing_on = open(path+"\\"+resultFileName, "w")


dummy = 0
folderlist = []
# Extraer nombres de carpeta
for user in user_list:
    pathUser = path+"\\"+carpeta_orig+"\\"+user
    print("Parsing user "+user)
    dir_list = os.listdir(pathUser)
    for folderName in dir_list:# Para cada nombre de carpeta que encontremos,
        
        if folderName in folderlist:# Si está en la lista, no hacer nada
            dummy=1
        else:                       # Si NO está en la lista, meterla en la lista
            writing_on.write(folderName+"\n")
            folderlist.append(folderName)
writing_on.close()

writing_on = open(path+"\\"+resultFileName, "w")
folderlist.sort()
for item in folderlist:
    writing_on.write(item+"\n")
writing_on.close()
