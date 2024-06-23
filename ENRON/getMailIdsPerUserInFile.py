#!/usr/bin/python
#Este script es para extraer y concatenar los identificadores de los correos de cada usuario
#en un solo String, y hacer un CSV, una lista o una tabla con el formato poi|user|Ids

import os
#import re
#import cleantext
#from bs4 import BeautifulSoup
import csv

def crear_escribirArchivo (prefix, separ, tipo):
    import os
    # Leer la carpeta local en busca de archivos .tipo
    lista = os.listdir(path)

    if tipo == "": tipo="csv"
    if separ == "": separ="_"
    if prefix == "": prefix="res"
    # Los archivos de resultados se llaman prefix_1.tipo, prefix_2.tipo, etc
    control = 0
    for dir_folder in lista:
        if dir_folder.__contains__("."):
            parts = dir_folder.split(".")
            #print("parts ="+str(parts))
            if parts[1] == tipo:
                prefix_sep = parts[0].split(separ)
                #print("prefix_sep ="+str(prefix_sep))
                if prefix_sep[0] == prefix and int(prefix_sep[1][0]) > control:
                    control = int(prefix_sep[1])
                    #print("control="+str(control))
    control = control + 1
    # Ver el último número que hay, y crear el siguiente y abrir como escritura
    resultFileName = prefix+separ+str(control)+"."+tipo
    print("Resultados en "+resultFileName)
    writing_on = open(path+"\\"+resultFileName, "w", encoding="utf-8")
    return writing_on, resultFileName

#Cargar los emails del archivo externo (pre-procesado y corregido)
def cargar_emails(filename):
    poiData = {}
    data = {}
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            poi = row['poi']
            user = row['user']
            emails = row['emails']
            poiData[user] = poi
            data[user] = emails
    print(str(data))
    return poiData, data

# INICIO DE LA EJECUCIÓN

carpeta_orig="enron_mail_20150507\\maildir"

# Get the list of all files and directories
path = os.getcwd()
print("path ="+path)
user_list = os.listdir(path+"\\"+carpeta_orig) # Array of usernames (array of strings)

# Begin mid list?
midlist = False
if midlist:
    auxil = user_list
    user_list = [s for s in auxil if (s[0].lower() not in 'abcdefghijklmnopqrstuvwxy')]
    print("Midlist = true, begin with "+user_list[0])

# Generar la cabecera

# Marcar los headers que nos podemos encontrar
headers=("Message-ID:","Date:","From:","To:","Object:", "Bcc:","Subject:","Mime-Version:","Content-Type:","Content-Transfer-Encoding:","X-From:","X-To:","X-cc:","X-bcc:","X-Folder:","X-Origin:","X-FileName:", "cc:")
receiverHeaders=("To:", "Bcc:", "Cc:")

otroHeader1= "----------------------"
otroHeader2= "-----"

#Diccionario de direcciones de email
poiData, email_dict = cargar_emails('originEmailsPlusInsiders_1.csv')

#Diccionario de strings para extraer
salida = {usr: '' for usr in email_dict} #Inicializamos el array de string de salida
print(str(salida))


dummy = 0
mailCounter = 0
broken = 0
foundNum = 0
notFoundMail = 0

foundmails = ""
# Extraer mails

for user in user_list:
    # Fallos del dataset: ; phanis-s -> panus-s (pero ya existe); rodrique-r -> rodrigue-r; y otro también con un problema de nombre que no me acuerdo
    
    userAux = user
    if user == "mims-thurston-p":
        userAux = "mims-p"
    elif user == "merriss-s":
        userAux = "merris-s"

    userInitial = userAux.split("-")[1]
    user_surname = userAux.split("-")[0]

    if user == "lucci-p":
        userInitial = "t"# No tiene emails con 'p' pero sí con 't'
    elif user == "gilbertsmith-d":
        user_surname = "gilbert"
    elif user == "williams-w3":
            userInitial = "i" # Para incluir tanto "bill" como "iii" (se llama bill williams iii)
    elif user_surname == "ybarbo":
        user_surname = "y'barbo"

    print("Parsing User dataset "+ user )

    pathUser = path+"\\"+carpeta_orig+"\\"+ user

    if user == "stokley-c":#Todos sus emails y subcarpetas están metidos un "nivel" más abajo
       pathUser = path+"\\"+carpeta_orig+"\\"+user+"\\chris_stokley"
    
    dir_list = os.listdir(pathUser)

    thisUser = 0

    for carpeta_de_usuario in dir_list:

        pathMailList = pathUser+"\\"+carpeta_de_usuario

        if (not os.path.isfile(pathMailList)): # Verificar que estamos abriendo una carpeta y no un archivo

            print("Parsing folder "+ user +"/"+ carpeta_de_usuario)
            
            mail_list = os.listdir(pathMailList) # get all mails
            
            for mail in mail_list:

                pathMail = pathMailList+"\\"+mail
                if os.path.isfile(pathMail) and (not mail.__contains__(".")):
                    # Verificar que estamos abriendo un archivo y no una carpeta y que el nombre de archivo no contiene un "."
                    # Todos los archivos de email están repetidos: "1" y "1.", "2" y "2.", etc. 
                    f = open(pathMail, "r")

                    # Pre- mail-parsing sets
                    mail_id = ""

                    readingheaders = True

                    readingSources = False
                    readSources = False

                    foundMatchingEmail = False

                    bralloops = False

                    # Ver el cuerpo de cada mensaje

                    for line in f:
                        # Ver las cabeceras: Msg ID, From, To, CC, BCC, Subject
                        
                        if readingheaders and line.startswith(headers):
                            # Esta estructura permite detectar todas las líneas de header iniciales que contienen los correos
                            if line.startswith("Message-ID: "):
                                mail_id=line.split("Message-ID: ")[1]

                                if foundmails.__contains__(mail_id): #Si se ha encontrado este mensaje, pasa de él; XXXX
                                    broken = broken + 1
                                    break
                                foundmails = foundmails + mail_id + " "

                            if line.startswith(receiverHeaders):
                                dummy=1
                            else:
                                if line.startswith("From:"):
                                    readingSources = True
                                else:
                                    if readingSources:
                                        # Se verifica si se ha leido en el pasado la cabecera From
                                        # Si se ha leido ya, estamos en una cabecera diferente 
                                        readSources = True
                                    #Si tenemos una cabecera distinta de From (pero hay cabecera, no es una linea extra de la cabecera From), ya no estamos leyendo
                                    readingSources = False

                        if readingSources:
                            for poiuser, email_string in email_dict.items(): # Iterar por los términos del diccionario
                                for userSearchEmail in email_string.split(" "): # Iterar por los emails del item del diccionario
                                    if userSearchEmail in line and userSearchEmail.rstrip() != "":
                                        # Si encontramos el mail en la línea, guardamos el mail_id. Ya se mete en XXXX para no repetirlo
                                        # Ya se verifica que no se está repitiendo en XXXX
                                        salida[poiuser] = salida[poiuser] + mail_id.rstrip() + " "
                                        
                                        foundMatchingEmail = True
                                        foundNum = foundNum + 1
                                        bralloops = True # Ya hemos hecho lo que queríamos con el mail. Salimos de él.
                                        break
                                if bralloops:
                                    break
                            if bralloops:
                                    break # Romper el loop de leer mail
                        
                        if readSources: # una vez leidas las lineas de From, no hace falta leer más
                            if not foundMatchingEmail:
                                notFoundMail = notFoundMail + 1
                            break
                        
                    f.close()
                    mailCounter = mailCounter + 1
                    thisUser = thisUser + 1
                    #print("parsed="+str(parsed)+" broken="+str(broken)+" mailCounter="+str(mailCounter)+" thisUser="+str(thisUser)+" "+user+"/"+carpeta_de_usuario)
            stringSalAux = "Found="+str(foundNum)+" notFound="+str(notFoundMail)+" broken="+str(broken)+" mailCounter="+str(mailCounter)+" thisUser="+str(thisUser) + " " + user + "/" + carpeta_de_usuario
            print(stringSalAux)

#Una vez peinado el dataset, escribimos los mail_id en el archivo de salida

# No es necesario generarlo como csv, porque no lo puedo procesar como csv luego, da error
writing_on, resFileName = crear_escribirArchivo("zIdMails", "_", "txt")
clave = ","
#Escribe cabecera
writing_on.write("poi"+clave+"user"+clave+"mailIds"+"\n")

for userxxx in salida:
    writing_on.write(str(poiData[userxxx])+clave+userxxx+clave+salida[userxxx]+"\n") 


writing_on.close()
print("mailCounter="+str(mailCounter))
print("Datos escritos en "+resFileName)