import requests
import pandas
from bs4 import BeautifulSoup


class FatecSpaceService(object):
    def __init__(self):
        self.__URL = 'http://tinywebdb.appinventor.mit.edu/getvalue'
        self.__DATA = 'tag=fatec-space-avaliacoes&fmt=html'
        self.__HEADERS = {'user-agent': 'my-app'}

    def get_data_frame(self):
        content = self.__search()
        content = self.__normalize_content(content)
        data = self.__create_data(content)
        return pandas.DataFrame(data=data)

    def __search(self):
        request = requests.post(self.__URL, data=self.__DATA, headers=self.__HEADERS)
        soup = BeautifulSoup(request.text, 'lxml')
        return soup.find_all('p')[1].text

    def __normalize_content(self, content):
        content = content.replace('\n', '')
        content = content.replace('\\', '')
        content = content.replace('\"', '')
        content = content.replace(']', '')
        content = content.replace(',', '')
        content = content.replace('Jogabilidade', '')
        content = content.replace('Controles', '')
        content = content.replace('Layout', '')
        content = content.replace('Criatividade', '')
        content = content[30:]
        content = content.split('[')
        return list(content)

    def __create_data(self, content):
        data = {
            'Usuário': [],
            'Jogabilidade': [],
            'Controles': [],
            'Layout': [],
            'Criatividade': []
        }
        for i in range(0, len(content), 6):
            data['Usuário'].append(content[i])
            data['Jogabilidade'].append(content[i + 2])
            data['Controles'].append(content[i + 3])
            data['Layout'].append(content[i + 4])
            data['Criatividade'].append(content[i + 5])
        return data
