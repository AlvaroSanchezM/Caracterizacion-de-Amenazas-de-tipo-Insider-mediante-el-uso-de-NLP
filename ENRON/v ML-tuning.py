import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import precision_score, recall_score
from imblearn.over_sampling import RandomOverSampler

# from sklearn.ensemble import RandomForestClassifier # XXXX
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.svm import SVC # Los parametros son mejores cuando se dejan sin tocar
# from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB


# Paso 1: Cargar manualmente el archivo .txt
def load_data(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        # Ignorar la primera línea si contiene las cabeceras
        next(file)
        for line in file:
            poi, user, postprocessed_email_text = line.strip().split(',', 2)
            data.append((int(poi), postprocessed_email_text))
    df = pd.DataFrame(data, columns=['poi', 'PostprocessedEmailText'])
    return df

# Paso 2: Convertir los textos en vectores utilizando TfidfVectorizer
def vectorize_texts(texts):
    vectorizer = TfidfVectorizer(max_features=10000)
    X = vectorizer.fit_transform(texts)
    return X, vectorizer

# Paso 3: Dividir los datos en conjuntos de entrenamiento y prueba
def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    return X_train, X_test, y_train, y_test

# Paso 4: Aplicar oversampling a la clase minoritaria
def oversample_data(X_train, y_train):
    ros = RandomOverSampler(random_state=42)
    X_resampled, y_resampled = ros.fit_resample(X_train, y_train)
    return X_resampled, y_resampled

# Paso 5: Entrenar y evaluar el modelo de ML
def train_and_evaluate(X_train, X_test, y_train, y_test):
    # rf = SVC(random_state=42) # XXXX
    rf = GaussianNB()
    rf.fit(X_train.toarray(), y_train)
    y_pred = rf.predict(X_test)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    return precision, recall

# Paso 6: Optimizar los hiperparámetros del modelo utilizando GridSearchCV
def optimize_hyperparameters(X_train, y_train):
    # param_grid = {
    #     'n_estimators': [100],#, 200, 300],#1=100                 2=100
    #     'max_depth': [None],#, 10, 20, 30],#1=None                2=None
    #     'min_samples_split': [2],#, 5, 10],#1=2                   2=2
    #     'min_samples_leaf': [1],#, 2, 4],  #1=1                   2=1
    #     'max_features': ['sqrt'],# 'log2', None],# def = sqrt    2=sqrt
    #     'bootstrap': [True, False], # def=True          #3=True
    #     'criterion': ['gini', 'entropy'] # def = 'gini' #3='gini'
    # } #PARAMS DE RANDOMFOREST
    # param_grid = {
    #     'criterion': ['gini', 'entropy','log_loss'],# gini
    #     'max_depth': [None, 10, 20, 30, 40, 50],# None
    #     'min_samples_split': [2, 5, 10],# 2
    #     'min_samples_leaf': [1, 2, 4],# 1
    #     'max_features': ['sqrt', 'log2', None]# 'sqrt'
    # }#PARAMS DE DECISIONTREE
    # param_grid = {
    #     'C': [0.1, 0.2, 0.3],# 0.1
    #     'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],# 'poly'
    #     'gamma': ['scale', 'auto'],# 'scale'
    #     'degree': [3, 4, 5],# 4
    #     'coef0': [0.5, 0.53, 0.55]# 0.5
    # }#PARAMS DE SVM/SVC
    # param_grid = {
    #     'C': [0.01, 0.1, 1, 10, 100],#ignored   10   ignored   10   ignored ignored
    #     'penalty': [None],#None   l2   None   l2   None               None
    #     'solver': ['saga']#newton-cg   liblinear   saga   saga saga   saga
    # } # PARAMS LOGISTICREGRESSION
    param_grid = {
        'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]
    } # PARAMS GAUSSIANNB

    # rf = SVC(random_state=42) # XXXX
    rf = GaussianNB()
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, scoring='recall', cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X_train.toarray(), y_train)
    return grid_search.best_params_, grid_search.best_estimator_

# Ejecución del programa
def main(filepath):
    # Cargar los datos
    df = load_data(filepath)
    X, vectorizer = vectorize_texts(df['PostprocessedEmailText'])
    y = df['poi']
    
    # Dividir y oversample
    X_train, X_test, y_train, y_test = split_data(X, y)
    X_train_resampled, y_train_resampled = oversample_data(X_train, y_train)
    
    # Optimizar hiperparámetros
    best_params, best_model = optimize_hyperparameters(X_train_resampled, y_train_resampled)
    print(f"Mejores hiperparámetros: {best_params}")
    
    # Evaluar modelo optimizado
    precision, recall = train_and_evaluate(X_train_resampled, X_test, y_train_resampled, y_test)
    print(f"Precision: {precision:.4f}, Recall: {recall:.4f}")

# Ruta del archivo .txt
filepath = 'zTruPostProc_2.txt'
main(filepath)
