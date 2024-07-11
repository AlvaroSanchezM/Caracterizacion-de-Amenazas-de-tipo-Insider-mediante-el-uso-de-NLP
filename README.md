# Caracterizacion-de-Amenazas-de-tipo-Insider-mediante-el-uso-de-NLP
Universidad Politécnica de Madrid

Grado en Ingeniería de Técnicas y Servicios de Telecomunicación

Trabajo Fin de Grado

Título: Caracterización de Amenazas de tipo Insider mediante el uso de NLP

Autor: Álvaro Sánchez Martínez

Ponente: Xavier Larriva Novo

Tutor: Luis Pérez Miguel

Este es el código desarrollado para obtener los resultados del Trabajo de Fin de Grado (TFG) del mismo nombre.

Se pueden encontrar 2 partes:
  -  La parte que ejecuta sobre la base de datos de emails de ENRON
  -  La parte que ejecuta sobre la base de datos de CERT

Se pueden obtener las bases de datos en los siguientes vínculos:

  -  ENRON: http://www.cs.cmu.edu/~enron/
            William W. Cohen, MLD, CMU Last modified: Fri May 8 09:52:31 EDT 2015

  -  CERT: https://kilthub.cmu.edu/articles/dataset/Insider_Threat_Test_Dataset/12841247/1
           Lindauer, Brian (2020). Insider Threat Test Dataset. Carnegie Mellon University. Dataset. https://doi.org/10.1184/R1/12841247.v1

Se obtuvieron los insiders de ENRON del código contenido en el github de Jaycode, y sus nombres de usuario coinciden con los nombres de los imputados en el caso ENRON.
https://github.com/jaycode/identify-enron-frauds/blob/master/final_project/poi_email_addresses.py

Sobre la arquitectura:
  La imagen de la arquitectura del sistema incluye pasos con asteriscos (*). Eso significa que solo el programa para la ejecución sobre el dataset de ENRON sigue esos pasos o genera esos archivos.

Sobre el programa:
  - Está diseñado para ejecutar en Windows. Para ejecutar en Linux hay que ir programa a programa cambiando las '\\' por '/'.

  Para ejecutar CERT:
  -    1º Introducir el contenido de r4.2 en la carpeta descomprimida de CERT r4.2
  -    2º Ejecutar los scripts que comienzan por read...NdSvUsr.py
  -    3º Ejecutar los scripts que comienzan por mount... .py
  -    3.5º Aquí se puede ejecutar el wordcloud, y se puede cambiar el programa para que coja joinedEmails_1.csv o joinedWebAccess.csv
  -    4º Ejecutar los scripts que comienzan por ML-verct-... .py Esto da los archivos resultantes del vectorizado. Cada script saca 2 archivos, pero webLabels.csv y emailLabels.csv son equivalentes, porque solo indican quienes son los insiders.
  -    5º Ejecutar ML-postVect-grdSrchcv-chained.py Esto corre los 5 algoritmos sobre uno de los datasets. Se puede cambiar en el código cual se usa. Corre cada algoritmo, ajusta hiperparámetros, y corre 19 veces con diferentes 'random_state', sacando resultados. Al final, saca la media y la varianza de los resultados.


 Para ejecutar ENRON:
 -    1º Introducir el contenido de ENRON en una carpeta al mismo nivel que el archivo descomprimido enron_mail_20150507
 -    2º Ejecutar getEmailsFromUsersInDataset.py Esto dará un csv con los emails de cada usuario del dataset ENRON que coincida con la carpeta de usuario.
 -    4º Introducir manualmente los emails de los insiders. Solo hay 3 insiders que vienen con carpeta de usuario en el dataset: Skillig, Delainey y Lay, el resto no están incluidos. Se obtendrá un archivo igual al originEmailsPlusInsiders.csv 
 -    3º Ejecutar getMailIdsPerUserInFile.py Esto sacará un csv con los Message-Id de cada email que haya escrito cada usuario, aunque esté en el inbox de un segundo usuario distinto.
 -    4º Ejecutar getMailTxtPerUser.py Esto sacará un csv donde en cada línea estarán los campos: poi(1 si fue insider, 0 si no lo fue), user(identificado por el nombre de carpeta para los no insiders, y para los insiders que no aparecen en el dataset con carpeta propia, a ojo a partir de uno de sus correos), contenido(contenido de cada uno de sus correos electrónicos(Identificados por el Message-Id de la ejecución anterior).
 -    5º Ejecutar stopwordAndStemmingPrepreocessing.py Este script hará un preprocesado de "lemmatization" primero, y eliminación de "stopwords" después, y sacará el resultado en un csv similar al anterior, con la cabecera: poi, user, content
 -    5.5º Aquí es donde se ejecutaría el wordcloud para verificar que no se han quedado palabras raras o etiquetas en el corpus de emails
 -    6º Se realiza el vectorizado, splitting de datos, training del algoritmo de ML y extracción de parámetros en este último paso, ejecutando 'v ML-tuning.py'. Se obtienen los mejores hiperparámetros  de cada algoritmo, pero para cambiar de algoritmo hay que cambiar manualmente el código de este archivo.
 -    7º Para vect-train-test-MLpy para cambiar de algoritmo también hace falta un cambio manual del código en los sitios marcados con un comentario con XXXX. Este otro script no hace ajuste de hiperparámetros. En cambio se pueden introducir los parámetros calculados con el script del paso 6º.


--Librerías para CERT:

click==8.1.7
colorama==0.4.6
contourpy==1.2.1
cycler==0.12.1
fonttools==4.53.0
imbalanced-learn==0.12.3
joblib==1.4.2
kiwisolver==1.4.5
matplotlib==3.9.0
nltk==3.8.1
numpy==2.0.0
packaging==24.1
pandas==2.2.2
pillow==10.3.0
pyparsing==3.1.2
python-dateutil==2.9.0.post0
pytz==2024.1
regex==2024.5.15
scikit-learn==1.5.0
scipy==1.13.1
six==1.16.0
threadpoolctl==3.5.0
tqdm==4.66.4
tzdata==2024.1
wordcloud==1.9.3

Además, hay que descargarse el corpus 'punkt' de 'nltk'


--Librerías para ENRON:

beautifulsoup4==4.12.3
certifi==2024.6.2
charset-normalizer==3.3.2
clean-text==0.6.0
click==8.1.7
colorama==0.4.6
contourpy==1.2.1
cycler==0.12.1
emoji==1.7.0
filelock==3.15.1
fonttools==4.53.0
fsspec==2024.6.0
ftfy==6.2.0
huggingface-hub==0.23.3
idna==3.7
imbalanced-learn==0.12.3
intel-openmp==2021.4.0
Jinja2==3.1.4
joblib==1.4.2
kiwisolver==1.4.5
lxml==5.2.2
MarkupSafe==2.1.5
matplotlib==3.9.0
mkl==2021.4.0
mpmath==1.3.0
networkx==3.3
nltk==3.8.1
numpy==1.26.4
packaging==24.0
pandas==2.2.2
pillow==10.3.0
psutil==5.9.8
pyparsing==3.1.2
python-dateutil==2.9.0.post0
pytz==2024.1
PyYAML==6.0.1
regex==2024.5.15
requests==2.32.3
safetensors==0.4.3
scikit-learn==1.5.0
scipy==1.13.1
six==1.16.0
soupsieve==2.5
sympy==1.12.1
tbb==2021.12.0
threadpoolctl==3.5.0
tokenizers==0.19.1
tqdm==4.66.4
typing_extensions==4.12.2
tzdata==2024.1
urllib3==2.2.1
wcwidth==0.2.13
wordcloud==1.9.3

Además, hay que descargarse los corpus 'wordnet' y 'stopwords' de 'nltk'

