# Caracterizacion-de-Amenazas-de-tipo-Insider-mediante-el-uso-de-NLP
Universidad Politécnica de Madrid

Grado en Ingeniería de Técnicas y Servicios de Telecomunicación

Trabajo Fin de Grado

Título: Caracterización de Amenazas de tipo Insider mediante el uso de NLP

Autor: Álvaro Sánchez Martínez

Ponente: Luis Pérez Miguel

Tutor: Xavier Larriva Novo

Este es el código desarrollado para obtener los resultados del Trabajo de Fin de Grado (TFG) del mismo nombre.

Se pueden encontrar 2 partes:
  -  La parte que ejecuta sobre la base de datos de emails de ENRON
  -  La parte que ejecuta sobre la base de datos de CERT

Se pueden obtener las bases de datos en los siguientes vínculos:

  -  ENRON: http://www.cs.cmu.edu/~enron/
            William W. Cohen, MLD, CMU Last modified: Fri May 8 09:52:31 EDT 2015

  -  CERT: https://kilthub.cmu.edu/articles/dataset/Insider_Threat_Test_Dataset/12841247/1
           Lindauer, Brian (2020). Insider Threat Test Dataset. Carnegie Mellon University. Dataset. https://doi.org/10.1184/R1/12841247.v1


Sobre el programa:
  - Está diseñado para ejecutar en Windows. Para ejecutar en linux hay que ir programa a programa cambiando las '\\' por '/'.


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

