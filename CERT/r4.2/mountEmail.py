import os
from winsound import Beep
# from nltk.corpus import  stopwords
# from nltk.stem import WordNetLemmatizer

def crear_escribirArchivo(path,prefix, separ, tipo):
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
    fileFullPath = path+"\\"+resultFileName
    writing_on = open(fileFullPath, "w", encoding="utf-8")
    return writing_on, fileFullPath

def cargar_insiders(filename):
    # abrirlo como csv da: _csv.Error: field larger than field limit (131072)
    poiData = {}
    with open(filename, mode='r', encoding='utf-8') as file:
        
        for line in file:
            stringInsiders = line

    return stringInsiders

# def remove_stopwords(text, language):
#     stop_words = set(stopwords.words(language))
#     word_tokens = text # .split(" ")
#     filtered_text = [word for word in word_tokens if word not in stop_words]
#     #print(language)
#     return " ".join(filtered_text)



outputPath = os.getcwd()+"\\Outputs"# Outputs Directory path
insiderFile = "insidersTru.txt"

emailFile, emailFilePath = crear_escribirArchivo(outputPath,"joinedEmails", "_", "csv")

stringInsiders=cargar_insiders(outputPath+"\\"+insiderFile)

# Generar la cabecera
clave = ","
emailFile.write("insider"+clave+"user"+clave+"emailText\n")

#Iterar por los archivos empezados por http_ en Outputs

OutputFileList = [f for f in os.listdir(outputPath) if os.path.isfile("\\".join([outputPath, f]))]
EmailFileList = []
userList = []
# Get list of http files
for name in OutputFileList:
    if name.__contains__("email_"):
        user = "".join( ( "".join(name.split("email_")) ).split(".txt") )
        EmailFileList.append(name)
        userList.append(user)

for filename in EmailFileList:
    # Previous params
    isInsider = False
    content = ""
    # Get username
    user = "".join( ( "".join(filename.split("email_")) ).split(".txt") )
    print(user)
    # Is Insider?
    if stringInsiders.__contains__(user):
        isInsider = True
    # Extract content
    with open(outputPath+"\\"+filename) as userEmailFile:
        for line in userEmailFile:
            content = content.rstrip().lower() + " " + line
    # # preprocesado (stemming & stopwords)

    # lemmatizer = WordNetLemmatizer()
    # # Use vocabulary and morphological analysis to determine the base form of a word
    # def lemmatize_word(text):
    #     word_tokens = text.split()
    #     lemmas = [lemmatizer.lemmatize(word) for word in word_tokens]
    #     return lemmas
    
    # lems_text = lemmatize_word(content)
    
    # #Elim de stopwords
    # content_wo_Stopwords = remove_stopwords(lems_text, "english")

    # Save content
    with open(emailFilePath, 'a', encoding='utf-8') as email_file:
        email_file.write(str(int(isInsider))+","+user+","+content+"\n")
    
    Beep(1000, 200)