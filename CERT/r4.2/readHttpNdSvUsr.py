import csv

import os

def process_large_csv(path, input_file):
    # Diccionario para mantener un set de usuarios encontrados
    users_seen = set()
    

    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            user = row['user']
            content = row['content']
            
            # Si el usuario no ha sido encontrado antes
            if user not in users_seen:
                users_seen.add(user)
                
                # Escribir contenido en archivo específico del usuario
                with open(f"{path}\\Outputs\\http_{user}.txt", 'w', encoding='utf-8') as user_file:
                    user_file.write(content)
            else:
                # Concatenar el contenido al archivo existente
                with open(f"{path}\\Outputs\\http_{user}.txt", 'a', encoding='utf-8') as user_file:
                    user_file.write(content)
                    
if __name__ == "__main__":
    mypath = os.getcwd() # Directory path
    input_file = mypath+'\\http.csv'
    process_large_csv(mypath,input_file)