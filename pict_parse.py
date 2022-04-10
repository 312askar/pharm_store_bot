import shutil
import requests

# Parsing image script
def get_file(url):
    response = requests.get(url, stream=True)
    return response

def save_data(name, file_data):
    file = open(name, 'bw') #Бинарный режим, изображение передається байтами
    for chunk in file_data.iter_content(4096): # Записываем в файл по блочно данные
        file.write(chunk)
    shutil.move(name, 'images') # move picture to directory

def get_name(url):
    name = url.split('/')[-1]
    return name
