#!/usr/bin/python
#Este script es para preprocesar (stemming + stop-word removal) los contenidos de los correos de cada usuario
#, y hacer un CSV, una lista o una tabla con el formato poi|user|String

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
def descargar_textoBruto(filename):
    # abrirlo como csv da: _csv.Error: field larger than field limit (131072)
    poiData = {}
    data = {}
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        cuenta = 1
        for row in csvfile:
            if cuenta != 1: # No incluir la cabecera
                arrFila=row.split(",")

                poi = arrFila[0]
                arrFila.remove(poi)
                user = arrFila[0]
                arrFila.remove(user)
                msg_txt = ",".join(arrFila)
                #print(msg_txt[1:10])

                poiData[user] = poi
                data[user] = msg_txt
            cuenta = cuenta + 1
    return data, poiData

# INICIO DE LA EJECUCIÓN

# Get the list of all files and directories
path = os.getcwd()
print("path ="+path)

# Generar la cabecera
clave = ","

#Download Diccionario de direcciones de email
txtBruto, poiData = descargar_textoBruto('Zbrut_2.txt')

# Para guardar los emails al final
writing_on = crear_escribirArchivo("zMidProc", "_", "txt")
writing_on.write("poi"+clave+"user"+clave+"contenido\n")

#Una vez peinado el dataset, preprocesamos datos y escribimos

for userxxx in txtBruto:
    
    mailString = txtBruto[userxxx].rstrip()

    print("mailString TYPE="+str(type(mailString))+" user "+userxxx)
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

    # quitar emails
    email_pattern = r"\b[A-Za-z0-9._%'+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    texto_sin_emails = re.sub(email_pattern, '', texto_sin_fechas)

    # Quitar "[image]"
    patron_image = r'\[image\]'
    texto_sin_image = re.sub(patron_image, '', texto_sin_emails)

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
    a = ".:,;!_?\""
    b = "        " # Aquí cambio los caracteres especiales que simbolizan una pausa por un espacio
    c = "$€¡¿-|·#~\\&¬/()^[]*<>=@+" # Estos otros caracteres se eliminan sin cambiarse por nada
    tabla = str.maketrans(a, b, c)
    cleanString = cleanStr.translate(tabla)

    writing_on.write(str(poiData[userxxx])+clave+userxxx+clave+cleanString+"\n")
    #print(str(poiData[userxxx])+clave+userxxx)


writing_on.close()