import os
from nltk.corpus import  stopwords
from nltk.stem import WordNetLemmatizer

def crear_escribirArchivo(path,prefix, separ, tipo):
    # Los archivos de resultados se llaman prefix_1.tipo, prefix_2.tipo, etc
    if tipo == "": tipo="csv"
    if separ == "": separ="_"
    if prefix == "": prefix="stW+lemmAll"

    import os
    # Leer la carpeta local en busca de archivos .tipo
    lista = os.listdir(path)# Get the list of all files and directories

    control = 0
    for dir_folder in lista:
        if dir_folder.__contains__("."):
            parts = dir_folder.split(".")
            if parts[1] == tipo:
                prefix_sep = parts[0].split(separ)
                if prefix_sep[0] == prefix and int(prefix_sep[1][0]) > control:
                    control = int(prefix_sep[1])
    control = control + 1
    # Ver el último número que hay, y crear el siguiente y abrir como escritura
    
    resultFileName = prefix+separ+str(control)+"."+tipo
    writing_on = open(path+"\\"+resultFileName, "w", encoding="utf-8")
    print("Escribiendo en "+resultFileName)
    return writing_on

### INICIO DE LA EJECUCIÓN

path = os.getcwd()

# Lista/archivo de escritura
writing_on = crear_escribirArchivo(path,"zTruPostProc","_","txt")
clave = ","

# Leer el archivo CSV original
archFte = 'zMidProc_3.txt'
file = open(archFte, mode='r', encoding='utf-8')
lineNum = 1

# remove english stopwords function [https://ayselaydin.medium.com/1-text-preprocessing-techniques-for-nlp-37544483c007]
def remove_stopwords(text, language):
    stop_words = set(stopwords.words(language))
    word_tokens = text # .split(" ")
    filtered_text = [word for word in word_tokens if word not in stop_words]
    #print(language)
    return " ".join(filtered_text)

lemmatizer = WordNetLemmatizer()
# Use vocabulary and morphological analysis to determine the base form of a word
def lemmatize_word(text):
    word_tokens = text.split()
    lemmas = [lemmatizer.lemmatize(word) for word in word_tokens]
    return lemmas
# LEER file Y PROCESAR LINEA A LINEA
for line in file:

    linea = line.split(",")
    poi_nonpoi = linea[0]
    from_field = linea[1]
    contenido_total = linea[2].rstrip()

    if lineNum >= 2:
        # Lemmatization
        lems_text = lemmatize_word(contenido_total)#cleanString)

        # procesado de stopWords
        content_wo_Stopwords = remove_stopwords(lems_text, "english")

        writing_on.write(poi_nonpoi+clave+from_field+clave+content_wo_Stopwords+"\n")
        print("Processed line "+str(lineNum)+" user "+from_field)
    else:
        writing_on.write(poi_nonpoi+clave+from_field+clave+contenido_total+"\n")
        print("Pasada cabecera")

    lineNum = lineNum + 1

writing_on.close()
file.close()