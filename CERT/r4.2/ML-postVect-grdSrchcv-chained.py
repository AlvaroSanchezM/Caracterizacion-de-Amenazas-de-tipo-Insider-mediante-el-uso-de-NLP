import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report
#from sklearn.utils import resample
from imblearn.over_sampling import RandomOverSampler, SMOTE
from winsound import Beep
import os

# Cargar los datos
path = os.getcwd() + '\\Outputs\\'  # Ajusta el path según sea necesario

# X = pd.read_csv(path + 'vectorized_emailData.csv') # vectorized_emailData
X = pd.read_csv(path + 'vectorized_emailData.csv') # vectorized_webData
webLabels = pd.read_csv(path + 'webLabels.csv')

# Concatenar los datos
#X = pd.concat([vectorized_emailData], axis=1)#, vectorized_webData], axis=1)
Y = webLabels
Y = Y.values.ravel()

# Algoritmos a evaluar
algorithms = {
    'LogisticRegression': LogisticRegression(),
    'SVC': SVC(),
    'DecisionTreeClassifier': DecisionTreeClassifier(),
    'RandomForestClassifier': RandomForestClassifier(),
    'GaussianNB': GaussianNB()
}

# Parámetros para GridSearch
param_grids = {
    'LogisticRegression': {'C': [0.1, 1, 10]},
    'SVC': {'kernel': ['linear', 'rbf'], 'C': [0.1, 1, 10]},
    'DecisionTreeClassifier': {'max_depth': [None, 10, 20, 30]},
    'RandomForestClassifier': {'n_estimators': [10, 50, 100]},
    'GaussianNB': {}
}

# Resultados
results = {}
bestimators={}

# Proceso para cada algoritmo
for name, model in algorithms.items():
    print(f"Optimizing {name}...")

    # Dividir los datos en conjuntos de entrenamiento y prueba para GridSearchCV
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=13)
    
    # Sobremuestreo aleatorio
    #ros = RandomOverSampler(random_state=13)
    ros = SMOTE(random_state=13)
    X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)
    
    # GridSearchCV para encontrar los mejores parámetros
    grid_search = GridSearchCV(model, param_grids[name], scoring='recall', cv=5, verbose=2)
    grid_search.fit(X_train_resampled, y_train_resampled)
    
    # Guardar el mejor modelo
    best_model = grid_search.best_estimator_
    bestimators[name]=best_model
    print("Mejor estimador de GridSearchCV:", grid_search.best_estimator_)
    Beep(1000,1000)
    # Lista para almacenar resultados de cada iteración
    all_reports = []

    for i in range(19):
        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=i)
        
        # Sobremuestreo aleatorio
        ros = SMOTE(random_state=13)
        #ros = RandomOverSampler(random_state=i)
        X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)
        
        # Entrenar el modelo con los mejores parámetros
        best_model.fit(X_train_resampled, y_train_resampled)
        
        # Predecir en el conjunto de prueba
        y_pred = best_model.predict(X_test)
        
        # Obtener el classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        all_reports.append(report)
        # Beep(2000,200)
        print("alg="+name+" iter="+str(i)+" of 19-1")
    
    # Calcular la media y la varianza de las métricas
    metrics = ['precision', 'recall', 'f1-score', 'support']
    avg_report = {}
    for key in all_reports[0].keys():
        if isinstance(all_reports[0][key], dict):  # Verificar si el valor es un diccionario
            avg_report[key] = {}
            for metric in metrics:
                values = [r[key][metric] for r in all_reports if key in r and metric in r[key]]
                avg_report[key][metric] = {
                    'mean': np.mean(values),
                    'var': np.var(values)
                }
        else:  # Caso para claves que no son diccionarios
            values = [r[key] for r in all_reports if key in r]
            avg_report[key] = {
                'mean': np.mean(values),
                'var': np.var(values)
            }
    
    results[name] = avg_report
    # Resultados preliminares
    # print(f"\nResultados para {name}:")
    # print("auxInter = "+str(avg_report))
    # for label, metrics in avg_report.items():
    #     print(f"  Clase: {label}")
    #     if label != "accuracy":
    #         for metric, values in metrics.items():
    #             print(f"    {metric} - Media: {values['mean']:.4f}, Varianza: {values['var']:.4f}")
    #     else:
    #         print(f"    {label} - Media: {metrics['mean']:.4f}, Varianza: {metrics['var']:.4f}")


# Mostrar los resultados
for algo, report in results.items():
    print(f"\nResultados para {algo}:")
    #print("auxFin = "+str(report))
    for label, metrics in report.items():
        print(f"  Clase: {label}")
        if label != "accuracy":
            for metric, values in metrics.items():
                print(f"    {metric} - Media: {values['mean']:.4f}, Varianza: {values['var']:.4f}")
        else:
            print(f"    {label} - Media: {metrics['mean']:.4f}, Varianza: {metrics['var']:.4f}")

print(str(bestimators))

Beep(2000,300)
Beep(4000,400)
Beep(2000,300)

