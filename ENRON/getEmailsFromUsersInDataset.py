#!/usr/bin/python
#Este script es para extraer y concatenar los correos de cada usuario
#en un solo String, y hacer un CSV, una lista o una tabla con el formato poi|user|emails

import os
import re

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
tipo="csv"
separ="_"
prefix="originEmails"# Los archivos de resultados se llaman resul_1.txt, resul_2.txt, etc
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


headers=("Message-ID:","Date:","From:","To:","Object:", "Bcc:","Subject:","Mime-Version:","Content-Type:","Content-Transfer-Encoding:","X-From:","X-To:","X-cc:","X-bcc:","X-Folder:","X-Origin:","X-FileName:", "cc:")
receiverHeaders=("To:", "Bcc:", "Cc:")

dummy = 0
mailCounter=0
# Extraer nombres de carpeta
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

    partialUserMail = "."+user_surname+"@enron.com"
    mailString = ""
    print("Parsing user "+user+", mail="+partialUserMail)

    pathUser = path+"\\"+carpeta_orig+"\\"+user
    if user == "stokley-c":#Todos sus emails y subcarpetas están metidos un "nivel" más abajo
       pathUser = path+"\\"+carpeta_orig+"\\"+user+"\\chris_stokley"
    
    dir_list = os.listdir(pathUser)

    userlist = "" # Emails en "from" en mails enviados por este usuario

    thisUser = 0

    for carpeta_de_usuario in dir_list:
        
        if user == "phanis-s":
            break # Este usuario está repe de panus-s y todos sus emails son de panus-s

        pathMailList= pathUser+"\\"+carpeta_de_usuario

        if (not os.path.isfile(pathMailList)): # and ((carpeta_de_usuario.__contains__("sent") and carpeta_de_usuario.__contains__("_")) or carpeta_de_usuario == "sent" or carpeta_de_usuario.__contains__("deleted")): # Verificar que estamos abriendo una carpeta y no un archivo

            print("Parsing folder "+carpeta_de_usuario)
            # get all mails
            
            mail_list = os.listdir(pathMailList)
            
            for mail in mail_list:
                
                pathMail = pathMailList+"\\"+mail

                if os.path.isfile(pathMail) and (not mail.__contains__(".")): # Verificar que estamos abriendo un archivo y no una carpeta y que el nombre de archivo no contiene un "."
                    
                    # Todos los archivos de email están repetidos: "1" y "1.", "2" y "2.", etc. 
                    f = open(pathMail, "r")

                    # Pre- mail-parsing sets
                    readingheaders = True

                    from_string = ""

                    readingSources = False
                    readSources = False

                    mail_from_user = False

                    for line in f:
                        # Ver las cabeceras: Msg ID, From, To, CC, BCC, Subject
                        
                        if readingheaders and line.startswith(headers): # Esta estructura permite detectar todas las líneas que contienen los correos de destino
                            if line.startswith(receiverHeaders):
                                #readingReceivers = True
                                #print("readingReceivers")
                                dummy=1
                            else:
                                #readingReceivers = False
                                if line.startswith("From:"):
                                    readingSources = True
                                    #print("readingSources")
                                else:
                                    if readingSources:
                                        readSources = True
                                    readingSources = False

                        if readingSources:
                            from_string = from_string + line.rstrip()+" "
                            if line.__contains__(user_surname):#partialUserMail):
                                mail_from_user = True
                                mailString = mailString + line.rstrip()+" "
                        
                        if readSources and (not mail_from_user):
                            break # Si el mail no es del usuario, no hace falta parsearlo
                            # Esto permite ahorrar en torno a un 23% del tiempo
                        
                        # if readingReceivers:
                        #     if line.__contains__(partialUserMail):
                        #         mail_to_user = True

                        if line.startswith("X-FileName:"):#Llegado al final de las cabeceras principales
                            break
                    if mail_from_user:
                        localList = re.findall('\S+@\S+', from_string)
                        userlist = (userlist+ " ".join(localList)).rstrip() + " "

                    f.close()
                    mailCounter = mailCounter + 1
                    thisUser = thisUser + 1
                    #print(" mailCounter="+str(mailCounter)+" thisUser="+str(thisUser)+" "+user+"/"+carpeta_de_usuario)
    print("thisUser="+str(thisUser))
  
    # file_name=prefix+separ+str(control)+user+"."+tipo
    # fn = open(path+"\\"+file_name, "w")
    # fn.write(userlist)
    # fn.close
    # eliminar los repetidos 
    totuserlist = re.findall('\S+@\S+', userlist)
    aux = list(set(totuserlist))
    extra = []
    for dir in aux:
        if dir.__contains__(user_surname) and dir.__contains__(userInitial):
            extra.append(dir)
    aux2 = " ".join(extra)

    aux3 = " ".join(aux2.split(", "))    
    
    aux3_1 = aux2.split(" ")

    aux3_2 = []
    for item in aux3_1:
        if item.__contains__("@") and item.split("@")[0].__contains__(userInitial) and item.split("@")[0].__contains__(user_surname):
            if item.endswith(','):
                # Quitar la coma del final
                item = item[:-1]
            aux3_2.append(item)
    
    #Volver a quitar repes
    aux4 = list(set(aux3_2))

    userlist = " ".join(aux4)

    writing_on.write(user+","+userlist+"\n")

writing_on.close()
print("mailCounter="+str(mailCounter))