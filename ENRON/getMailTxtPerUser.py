#!/usr/bin/python
#Este script es para extraer y concatenar los contenidos de los correos de cada usuario
#en un solo String, y hacer un CSV, una lista o una tabla con el formato |user|String|

import os
import re
import cleantext
#from bs4 import BeautifulSoup
#import csv

def crear_escribirArchivo(prefix, separ, tipo):
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
    return writing_on

#Cargar los emailIds del archivo externo (pre-procesado y corregido)
def descargar_emailIds(filename):
    # abrirlo como csv da: _csv.Error: field larger than field limit (131072)
    poiData = {}
    data = {}
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        cuenta = 1
        for row in csvfile:
            if cuenta != 1: # No incluir la cabecera
                arrFila=row.split(",")
                poi = arrFila[0]
                user = arrFila[1]
                msg_ids = arrFila[2]
                poiData[user] = poi
                data[user] = msg_ids
            cuenta = cuenta + 1
    return data, poiData

# INICIO DE LA EJECUCIÓN

carpeta_orig="enron_mail_20150507\\maildir"

# Get the list of all files and directories
path = os.getcwd()
print("path ="+path)
user_list = os.listdir(path+"\\"+carpeta_orig) # Array of usernames (array of strings)
#print("Files and directories in '", path, "' :")
# prints all files
#print(user_list)

# Begin mid list
midlist = False
if midlist:
    auxil = user_list
    user_list = [s for s in auxil if (s[0].lower() not in 'abcdefghijklmnopqrstuvwxy')]
    print("Midlist = true, begin with "+user_list[0])

# Generar la cabecera
clave = ","


# Marcar los headers que nos podemos encontrar
headers=("Message-ID:","Date:","From:","To:","Object:", "Bcc:","Subject:","Mime-Version:","Content-Type:","Content-Transfer-Encoding:","X-From:","X-To:","X-cc:","X-bcc:","X-Folder:","X-Origin:","X-FileName:", "cc:")
receiverHeaders=("To:", "Bcc:", "Cc:")

otroHeader1= "----------------------"
otroHeader2= "-----"

#Download Diccionario de direcciones de email
email_ids, poiData = descargar_emailIds('zIdMails_1.txt')

#Diccionario de strings para extraer
salida = {user: '' for user in email_ids} #Inicializamos el array de string de salida
print(str(salida))


dummy = 0
mailCounter = 0
broken = 0
parsed = 0
foundEmailIds = "" # Para no repetir los emails vistos
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

    #partialUserMail = "."+user_surname+"@enron.com"
    mailString = ""
    print("Parsing User "+user)

    pathUser = path+"\\"+carpeta_orig+"\\"+user

    if user == "stokley-c":#Todos sus emails y subcarpetas están metidos un "nivel" más abajo
       pathUser = path+"\\"+carpeta_orig+"\\"+user+"\\chris_stokley"
    
    dir_list = os.listdir(pathUser)

    userlist = "" # Emails en "from" en mails enviados por este usuario

    thisUser = 0

    for carpeta_de_usuario in dir_list:

        pathMailList = pathUser+"\\"+carpeta_de_usuario

        if (not os.path.isfile(pathMailList)): # and ((carpeta_de_usuario.__contains__("sent") and carpeta_de_usuario.__contains__("_")) or carpeta_de_usuario == "sent" or carpeta_de_usuario.__contains__("deleted")): # Verificar que estamos abriendo una carpeta y no un archivo

            print("Parsing folder "+user+"\\"+carpeta_de_usuario)
            # get all mails
            
            mail_list = os.listdir(pathMailList)
            
            for mail in mail_list:
                pathMail = pathMailList+"\\"+mail

                if os.path.isfile(pathMail) and (not mail.__contains__(".")): # Verificar que estamos abriendo un archivo y no una carpeta y que el nombre de archivo no contiene un "."
                    # Todos los archivos de email están repetidos: "1" y "1.", "2" y "2.", etc. 
                    f = open(pathMail, "r")

                    # Pre- mail-parsing sets
                    mail_id = ""

                    readingheaders = True
                    x = 100

                    readingSources = False
                    readSources = False

                    #mail_from_user = False
                    user_origin_mail = ''
                    foundEmail = False

                    this_is_mail_body = True

                    #bralloops = False

                    # Ver el cuerpo de cada mensaje

                    for line in f:
                        # Ver las cabeceras: Msg ID, From, To, CC, BCC, Subject
                        
                        if readingheaders and line.startswith(headers): # Esta estructura permite detectar todas las líneas que contienen los correos de destino
                            if line.startswith("Message-ID: "):
                                mail_id=line.split("Message-ID: ")[1]
                                if not foundEmailIds.__contains__(mail_id) or foundEmailIds == "":# verificar que no tocamos mails sobre los que ya pasamos
                                    for poiuser, email_id in email_ids.items():
                                        ms_id=line[len("Message-ID: "):].rstrip()
                                        if email_id.__contains__(ms_id):
                                            print("FOUND="+ms_id+" user "+poiuser+" at "+user+"\\"+carpeta_de_usuario)
                                            foundEmail = True
                                            foundEmailIds = foundEmailIds + ms_id
                                            user_origin_mail = poiuser
                                            #brk2liniter = True # break hasta el line iterator
                                            break

                                if not foundEmail:
                                    break # break this loop, get out of this email and look into the next email

                        if line.startswith("X-FileName:"):
                            x = 1

                        if x <= 0: 
                            readingheaders = False
                            #print("readingBody")
                        
                        if (line.startswith(headers) or line.__contains__(otroHeader2)) and (not readingheaders):
                            this_is_mail_body = False # Esto permite eliminar los reply dentro del mismo mensaje detectando los headers del reply
                        
                        # Logica de lineas

                        if this_is_mail_body and foundEmail and (not readingheaders):
                            if (not line == "\n"): # No escribir las lineas que constan solo de \n
                                # Procesamiento de las líneas

                                line = line.rstrip().lower() # Cortar espacios y "\n" al final de cada linea
                        
                                # # Añadir al string del usuario
                                if not (line.__contains__(">") and line.__contains__("<")):
                                    salida[user_origin_mail] = salida[user_origin_mail] + line + " "
                                    
                        # Post-setup de lógica de líneas
                        x = x - 1

                    f.close()

                    mailCounter = mailCounter + 1
                    thisUser = thisUser + 1
                    #print("parsed="+str(parsed)+" broken="+str(broken)+" mailCounter="+str(mailCounter)+" thisUser="+str(thisUser)+" "+user+"/"+carpeta_de_usuario)
                if user_origin_mail != "":
                    if salida[user_origin_mail].endswith("\n"):
                        print("Alert, mail contains \\n mailCounter="+str(mailCounter))
            print("parsed="+str(parsed)+" broken="+str(broken)+" mailCounter="+str(mailCounter)+" thisUser="+str(thisUser)+" "+user+"/"+carpeta_de_usuario)

# Guardamos los resultados en bruto
fBruto = crear_escribirArchivo("Zbrut", "_", "txt")
fBruto.write("poi"+clave+"user"+clave+"contenido\n")

# Para guardar los emails al final
writing_on = crear_escribirArchivo("zMidProc", "_", "txt")
writing_on.write("poi"+clave+"user"+clave+"contenido\n")

#Una vez peinado el dataset, preprocesamos datos y escribimos

for userxxx in salida:

    # Quitar caracteres especiales
    a = ""
    b = "" # Aquí cambio los caracteres a por b
    c = "," # Estos otros caracteres se eliminan sin cambiarse por nada
    tabla = str.maketrans(a, b, c)
    limpio = salida[userxxx].translate(tabla)

    fBruto.write(str(poiData[userxxx])+clave+userxxx+clave+limpio+"\n")
    mailString = limpio
    print("mailString TYPE="+str(type(mailString)))
    # PREPROCESADO

    # Quitar HTML

    # soup = BeautifulSoup(mailString, "lxml")
    # # Obtener el texto plano sin etiquetas HTML
    # texto_sin_html = soup.get_text()

    html_tags_pattern = r'<.*?>'
    texto_sin_html = re.sub(html_tags_pattern, '', mailString)

    # Quitar URLs
    patron_url = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # Usar re.sub() para reemplazar las URLs con una cadena vacía
    texto_sin_urls = re.sub(patron_url, '', texto_sin_html)

    # Quitar horas
    patron_horas = r'\b(?:[01]?[0-9]|2[0-3])[:.][0-5][0-9]\b|\b(?:[01][0-9]|2[0-3])[0-5][0-9]\b'
    texto_sin_horas = re.sub(patron_horas, '', texto_sin_urls)

    # Quitar fechas
    patrones_fechas = [
        r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # Formato MM/DD/YYYY o DD/MM/YYYY o M/D/YYYY
        r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # Formato MM-DD-YYYY o DD-MM-YYYY o M-D-YYYY
        r'\b\d{1,2}\.\d{1,2}\.\d{2,4}\b',  # Formato MM.DD.YYYY o DD.MM.YYYY o M.D.YYYY
        r'\b\d{4}/\d{1,2}/\d{1,2}\b',  # Formato YYYY/MM/DD
        r'\b\d{4}-\d{1,2}-\d{1,2}\b',  # Formato YYYY-MM-DD
        r'\b\d{4}\.\d{1,2}\.\d{1,2}\b',  # Formato YYYY.MM.DD
        r'\b\d{1,2} [A-Za-z]{3,9} \d{4}\b',  # Formato D MMMM YYYY o DD MMMM YYYY (e.g., 1 January 2023, 01 Jan 2023)
        r'\b[A-Za-z]{3,9} \d{1,2}, \d{4}\b',  # Formato MMMM D, YYYY o MMMM DD, YYYY (e.g., January 1, 2023, Jan 01, 2023)
    ]

    # Unir todos los patrones en una sola expresión regular
    patron_fechas = '|'.join(patrones_fechas)
    texto_sin_fechas = re.sub(patron_fechas, '', texto_sin_horas)

    # Quitar "[image]"
    patron_image = r'\[image\]'
    texto_sin_image = re.sub(patron_image, '', texto_sin_fechas)

    # Quitar Emails, numeros, puntuación 
    cleanStr = cleantext.clean(texto_sin_image,
                            fix_unicode=True,               # fix various unicode errors
                            to_ascii=True,                  # transliterate to closest ASCII representation
                            lower=True,                     # lowercase text
                            no_line_breaks=True,           # fully strip line breaks as opposed to only normalizing them
                            no_urls=True,                  # replace all URLs with a special token
                            no_emails=True,                # replace all email addresses with a special token
                            no_phone_numbers=True,         # replace all phone numbers with a special token
                            no_numbers=True,               # replace all numbers with a special token
                            no_digits=True,                # replace all digits with a special token
                            no_currency_symbols=True,      # replace all currency symbols with a special token
                            no_punct=True,                 # remove punctuations
                            replace_with_punct="",          # instead of removing punctuations you may replace them
                            replace_with_url="",
                            replace_with_email="",
                            replace_with_phone_number="",
                            replace_with_number="",
                            replace_with_digit="",
                            replace_with_currency_symbol="",
                            lang="en"                       # set to 'de' for German special handling
                            )

    # Quitar caracteres especiales
    a = ""
    b = "" # Aquí cambio los caracteres especiales que simbolizan una pausa por un espacio
    c = "¡!_?¿.:-|\"·#~\\&¬/()^[]*<>=,;@+" # Estos otros caracteres se eliminan sin cambiarse por nada
    tabla = str.maketrans(a, b, c)
    cleanString = cleanStr.translate(tabla)

    if cleanString.__contains__("\n"):
        print("Alert, cleanString contains \\n mailCounter="+str(mailCounter)+"user "+user)

    writing_on.write(str(poiData[userxxx])+clave+userxxx+clave+cleanString+"\n") 


writing_on.close()
print("mailCounter="+str(mailCounter))