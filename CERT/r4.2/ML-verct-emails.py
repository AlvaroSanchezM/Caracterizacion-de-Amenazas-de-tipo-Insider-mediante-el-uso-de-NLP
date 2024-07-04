import csv
import re
import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from winsound import Beep 

import os

# Path
mypath = os.getcwd() + '\\'  # Ajusta el path según sea necesario

# Aumentar el límite de tamaño de campo CSV
csv.field_size_limit(131072*512) # 128KB * 256 = 32MB

def preprocess_text(text):
    # Eliminar números, guiones y guiones bajos usando expresiones regulares
    text = re.sub(r'\d+', '', text)  # Eliminar números
    text = text.replace('-', '')     # Eliminar guiones
    text = text.replace('_', '')     # Eliminar guiones bajos
    
    # Tokenización
    words = nltk.tokenize.word_tokenize(text)
    return ' '.join(words)

def process_and_vectorize(path, input_file):
    
    data = {'insider': [], 'user': [], 'text': []}
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)

        # Saltar la primera fila (encabezado)
        next(reader)
        
        # Leer y procesar el archivo línea por línea
        for row in reader:
            
            if len(row) < 3:
                continue
            
            insider = row[0]
            user = row[1]
            email_text = ','.join(row[2:])
            
            # Procesar el campo httpText
            processed_text = preprocess_text(email_text)
            
            # Agregar datos al diccionario
            data['insider'].append(int(insider))
            data['user'].append(user)
            data['text'].append(processed_text)
            print(user)
            Beep(1000,200)
    
    df = pd.DataFrame(data)
    
    # Vectorización usando TfidfVectorizer
    vectorizer = TfidfVectorizer(max_features=10000)
    X = vectorizer.fit_transform(df['text'])
    y = df['insider']
    
    # Guardar los datos vectorizados y las etiquetas
    pd.DataFrame(X.toarray()).to_csv(path+'vectorized_emailData.csv', index=False)
    pd.DataFrame(y).to_csv(path+'emailLabels.csv', index=False)

if __name__ == "__main__":
    path= mypath+'Outputs\\'
    input_file = path+'joinedEmails_1.csv'
    process_and_vectorize(path, input_file)