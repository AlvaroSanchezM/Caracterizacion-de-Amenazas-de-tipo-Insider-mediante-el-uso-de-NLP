import random
from re import split
from tabnanny import verbose
from matplotlib.pylab import randint
from sklearn.exceptions import FitFailedWarning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier

def nuevoArchivo (tipo, prefix, separ):
    if tipo == "":
        tipo="csv"
    if separ == "":
        separ="_"
    if prefix == "":
        prefix="test"# Los archivos de resultados se llaman prefix_1.tipo, prefix_2.tipo, etc

    import os
    path = os.getcwd()

    lista = os.listdir(path)
    
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
    #logFileName = "msgsID"+separ+str(control)+"."+tipo
    print("Resultados en "+resultFileName)
    return resultFileName

# INICIO DE EJECUCIÓN

# Archivo de entrada XXXX
#fileNameOrigin = "zTruPostProc_2.txt"
#fileNameOrigin = "zPostProc_2.txt"
fileNameOrigin = "zTruPostProc_2.txt"
fnew = open(fileNameOrigin, "r", encoding="utf-8")

# Presets del bucle
contador = 0
dummy = 0
array_poi = []
array_user = []
array_texto = []
array_sizes = []


for line in fnew:
    # Pre setting de cada linea
    poi_nonpoi, user, texto = line.split(",")

    if contador == 0:
        # Primera linea del csv, con la cabecera
        dummy = 1
    else:
        #Lineas de datos del csv
        array_poi.append(poi_nonpoi)
        array_user.append(user)
        array_texto.append(texto)
        array_sizes.append(len(texto))
    # Post setting de cada linea
    contador = contador + 1

fnew.close()

#Ver cuanto ocupa cada usuario

# for i in range(len(array_poi)):
#     ocup = len(array_texto[i].split(" "))
#     spaceI = "      "
#     spacesI="   "

#     if i > 9 and i < 100:
#         spacesI="  "
#     elif i > 99:
#         spacesI=" "

#     if ocup > 9:
#         spaceI = "      "
#     elif ocup > 99:
#         spaceI = "     "
#     elif ocup > 999:
#         spaceI = "    "
#     elif ocup > 9999:
#         spaceI = "   "
#     elif ocup > 99999:
#         spaceI = "  "
#     elif ocup > 999999:
#         spaceI = " "
#     #print("Num="+str(i)+spacesI+"Poi="+str(array_poi[i])+" Ocupación="+str(ocup)+spaceI+"User="+str(array_user[i]))

# Vectorizar
vectorizer = TfidfVectorizer()

x = vectorizer.fit_transform(array_texto) #Vectorizer
y = array_poi

# Separación en train y test 
testSize=0.3 # XXXX
from sklearn.model_selection import train_test_split
import numpy as np
randX=randint(1,50)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=testSize, random_state=randX, shuffle=True) # Split
#print(str(X_train), str(y_train))

# Hacer oversampling de insiders la parte entrenada
from imblearn.over_sampling import RandomOverSampler

ros = RandomOverSampler(random_state=randX)

X_resampled, y_resampled = ros.fit_resample(X_train, y_train)


# Entrenamiento y tipo de modelo que se usa XXXX
# from sklearn.linear_model import LogisticRegression
# from sklearn.svm import SVC
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB # TypeError: Sparse data was passed for X, but dense data is required. Use '.toarray()' to convert to a dense numpy array.

model_type = "RandomForestClassifier"
model = GaussianNB()
# model = RandomForestClassifier(random_state=randX)
# model = DecisionTreeClassifier(max_features='sqrt', random_state=randX)
# model = SVC(kernel='poly',degree=4, coef0=0.5,random_state=randX)
# model = LogisticRegression(C=0.1, penalty=None, solver='saga',random_state=randX)

model.fit(X_resampled.toarray(), y_resampled) # fit

# El modelo formula predicciones "y" a partir de los datos x_test y se compara/evalúa con los datos reales
y_pred = model.predict(X_test.toarray()) # predict

from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

# print("Accuracy:", accuracy_score(y_test, y_pred))
# print("Classification Report:")
target_names = ['nonPoi','poi']
# print(classification_report(y_test, y_pred, target_names = target_names))

print("Used Model: "+model_type+" sin parameters")

# metrics arrays
# def find_TP(y, y_hat):
#    # counts the number of true positives (y = 1, y_hat = 1)
#    return sum((y == 1) & (y_hat == 1))
# def find_FN(y, y_hat):
#    # counts the number of false negatives (y = 1, y_hat = 0) Type-II error
#    return sum((y == 1) & (y_hat == 0))
# def find_FP(y, y_hat):
#    # counts the number of false positives (y = 0, y_hat = 1) Type-I error
#    return sum((y == 0) & (y_hat == 1))
# def find_TN(y, y_hat):
#    # counts the number of true negatives (y = 0, y_hat = 0)
#    return sum((y == 0) & (y_hat == 0))


accMed = 0.0
precMedP = 0.0
recaMedP = 0.0
f1MedP = 0.0

# metrics
# TP = find_TP(y, y_pred)
# FN = find_FN(y, y_pred)
# FP = find_FP(y, y_pred)
# TN = find_TN(y, y_pred)
# print('TP:',TP)
# print('FN:',FN)
# print('FP:',FP)
# print('TN:',TN)

# Número de repeticiones XXXX
n_repeats = 19

# Inicialización de las métricas
accuracy_list = []
precision_list1 = []
recall_list1 = []
f1_list1 = []

precision_list0 = []
recall_list0 = []
f1_list0 = []

# Para guardar datos de cada iteración para hacer la media
clasifReportList = []
arrpoiXpredPOI = []
arrNpoiXpredPOI = []
arrpoiXpredNpoi = []
arrNpoiXpredNpoi = []

for _ in range(n_repeats):
    randNum=randint(1,50)
    # División del conjunto en training y testing
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=testSize, random_state=randNum)

    # Hacer oversampling de insiders la parte entrenada
    ros = RandomOverSampler(random_state=randNum)

    X_resampled, y_resampled = ros.fit_resample(X_train, y_train)

    # Modelo de ML XXXX
    model = GaussianNB()
    #model = RandomForestClassifier(random_state=randX)
    # model = DecisionTreeClassifier(max_features='sqrt', random_state=randNum)
    # model = SVC(kernel='poly',degree=4, coef0=0.5,random_state=randX)
    # model = LogisticRegression(C=0.1, penalty=None, solver='saga',random_state=randX)
    # Entrenamiento del modelo
    model.fit(X_resampled.toarray(), y_resampled)

    # Predicción
    y_pred = model.predict(X_test.toarray())

    # Tabla de verdades
    poiXpredPOI = 0
    NpoiXpredPOI = 0
    poiXpredNpoi = 0
    NpoiXpredNpoi = 0
    for num in range(len(y_pred)):
        if y_pred[num] == '1' and y_test[num] == '1':
            poiXpredPOI = poiXpredPOI + 1
        elif y_pred[num] == '1' and not y_test[num] == '1':
            NpoiXpredPOI = NpoiXpredPOI + 1
        elif not y_pred[num] == '1' and y_test[num] == '1':
            poiXpredNpoi = poiXpredNpoi + 1
        elif not y_pred[num] == '1' and not y_test[num] == '1':
            NpoiXpredNpoi = NpoiXpredNpoi + 1

    arrpoiXpredPOI.append(poiXpredPOI)
    arrNpoiXpredPOI.append(NpoiXpredPOI)
    arrpoiXpredNpoi.append(poiXpredNpoi)
    arrNpoiXpredNpoi.append(NpoiXpredNpoi)
    # print("Matriz de confusión; totPred="+str(len(y_pred))+"; totTest="+str(len(y_test)))
    # print("       PredPOI  PredNPOI")
    # print("   POI   "+str(poiXpredPOI)+"       "+str(poiXpredNpoi))
    # print("nonPOI   "+str(NpoiXpredPOI)+"       "+str(NpoiXpredNpoi))

    # Evaluación
    # print("y_test="+str(y_test)+"\ny_pred="+str(y_pred))
    # print(confusion_matrix(y_test, y_pred))
    
    accuracy_list.append(accuracy_score(y_test, y_pred))

    precision_list1.append(precision_score(y_test, y_pred, pos_label='1', zero_division=0))
    recall_list1.append(recall_score(y_test, y_pred, pos_label='1', zero_division=0))
    f1_list1.append(f1_score(y_test, y_pred, pos_label='1', zero_division=0))

    precision_list0.append(precision_score(y_test, y_pred, pos_label='0', zero_division=0))
    recall_list0.append(recall_score(y_test, y_pred, pos_label='0', zero_division=0))
    f1_list0.append(f1_score(y_test, y_pred, pos_label='0', zero_division=0))

    clasifReport = classification_report(y_test, y_pred, target_names = target_names, output_dict=True)
    clasifReportList.append(clasifReport)

# RESULTADOS XXXX
# Media de la matriz de confusión
print("\n---Matriz de confusión; totPred="+str(len(y_pred))+"; totTest="+str(len(y_test)))
print("       PredPOI  PredNPOI")
print("   POI   "+str(np.mean(arrpoiXpredPOI).round(decimals=2))+"       "+str(np.mean(arrpoiXpredNpoi).round(decimals=2)))
print("nonPOI   "+str(np.mean(arrNpoiXpredPOI).round(decimals=2))+"       "+str(np.mean(arrNpoiXpredNpoi).round(decimals=2)))

# Cálculo de las medias de las métricas

print("\n\n+++---Calc Clasif report Medio---+++\n")
ClaRepPrec = [[],[]]
ClaRepReca = [[],[]]
ClaRepf1 = [[],[]]
ClaRepsup = [[],[]]
ClaRepAcc = []

for item in clasifReportList:
    # print("item len="+str(len(item))+" item = "+str(item))
    clasifLongit=len(item)
    for labelItem in item:
        # print(labelItem, 'corresponds to', str(item[labelItem]))
        if labelItem == 'nonPoi' or  labelItem == 'poi':
            # print(str(item[labelItem]))
            for metricItem in item[labelItem]:
                posList = 0
                if labelItem == 'nonPoi': posList = 0
                else: posList = 1
                # print("metricItem ="+metricItem+"="+str(item[labelItem][metricItem]))
                if metricItem == 'precision':
                    ClaRepPrec[posList].append(item[labelItem][metricItem])
                elif metricItem == 'recall':
                    ClaRepReca[posList].append(item[labelItem][metricItem])
                elif metricItem == 'f1-score':
                    ClaRepf1[posList].append(item[labelItem][metricItem])
                elif metricItem == 'support':
                    ClaRepsup[posList].append(item[labelItem][metricItem])
        elif labelItem == 'accuracy':
            ClaRepAcc.append(item[labelItem])

# Medias de clasifReport XXXX
m_np_prec = np.mean(ClaRepPrec[0]).round(decimals=2)
m_p_prec = np.mean(ClaRepPrec[1]).round(decimals=2)
m_np_reca = np.mean(ClaRepReca[0]).round(decimals=2)
m_p_reca = np.mean(ClaRepReca[1]).round(decimals=2)
m_np_f1 = np.mean(ClaRepf1[0]).round(decimals=2)
m_p_f1 = np.mean(ClaRepf1[1]).round(decimals=2)
m_np_sup = np.mean(ClaRepsup[0]).round(decimals=2)
m_p_sup = np.mean(ClaRepsup[1]).round(decimals=2)
m_acc = np.mean(ClaRepAcc).round(decimals=2)

print(f"Accuracy: {m_acc}")
print("           precision    recall    f1-score    support")
print("  nonPoi       "+str(m_np_prec)+"      "+str(m_np_reca)+"      "+str(m_np_f1)+"      "+str(m_np_sup))
print("     poi       "+str(m_p_prec)+"      "+str(m_p_reca)+"      "+str(m_p_f1)+"      "+str(m_p_sup))
print("Origin Data: "+fileNameOrigin)
print(f"With {n_repeats} iterations")
print("Used Model: "+model_type+" sin parametros\n")

# medias en general XXXX
mean_accuracy = np.mean(accuracy_list).round(decimals=2)

mean_precision1 = np.mean(precision_list1).round(decimals=2)
mean_recall1 = np.mean(recall_list1).round(decimals=2)
mean_f11 = np.mean(f1_list1).round(decimals=2)

mean_precision0 = np.mean(precision_list0).round(decimals=2)
mean_recall0 = np.mean(recall_list0).round(decimals=2)
mean_f10 = np.mean(f1_list0).round(decimals=2)

print(f'  Mean Accuracy: {mean_accuracy}')
print(f'Mean Precision0: {mean_precision0}'+f' Mean Precision1: {mean_precision1}')
print(f'   Mean Recall0: {mean_recall0}'+f'    Mean Recall1: {mean_recall1}')
print(f' Mean F1 Score0: {mean_f10}'+f'  Mean F1 Score1: {mean_f11}')


