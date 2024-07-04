import csv
from collections import defaultdict
import os

def process_large_csv(path, input_file):
    # Diccionario para mantener un set de usuarios encontrados
    users_seen = set()
    # Diccionario para almacenar contenido de usuarios
    user_contents = defaultdict(list)

    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            user = row['user']
            content = row['content']
            
            # Si el usuario no ha sido encontrado antes
            if user not in users_seen:
                users_seen.add(user)
                user_contents[user].append(content)
                # Escribir contenido en archivo específico del usuario
                with open(f"{path}\\Outputs\\email_{user}.txt", 'w', encoding='utf-8') as user_file:
                    user_file.write(content)
            else:
                # Concatenar el contenido al archivo existente
                with open(f"{path}\\Outputs\\email_{user}.txt", 'a', encoding='utf-8') as user_file:
                    user_file.write(content)
                    
if __name__ == "__main__":
    mypath = os.getcwd()# Directory path
    input_file = mypath+'\\email.csv'
    process_large_csv(mypath, input_file)