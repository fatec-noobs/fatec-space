import requests
import pandas
import datetime
from bs4 import BeautifulSoup


class FatecSpaceService(object):
    def __init__(self):
        self.__URL = 'http://tinywebdb.appinventor.mit.edu/getvalue'
        self.__DATA = 'tag=fatec-space-avaliacoes&fmt=html'
        self.__HEADERS = {'user-agent': 'my-app'}

    def get_data_frame(self):
        data = self.__get_data({'save_backup': True})
        return pandas.DataFrame(data=data)

    def get_plot(self):
        data = self.__get_data()
        del data['Usuário']
        for key in data:
            total = 0
            for evaluation in data[key]:
                total += int(evaluation)
            data[key] = [total]
        data = pandas.DataFrame(data=data)
        data = data.astype(int)
        data.index = ['']
        return data.plot(kind='bar', title='Total de pontos', figsize=(8, 4))

    def __get_data(self, options={}):
        content = self.__search()
        if 'save_backup' in options:
            self.__save_backup(content)
        content = self.__normalize_content(content)
        return self.__create_data(content)

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

    def __save_backup(self, content):
        date = datetime.datetime.now()
        file_name = f'data/data_{date.year}-{date.month}-{date.day}_{date.hour}-{date.minute}-{date.second}.backup'
        file = open(file_name, 'x')
        file.write(content)
        file.close()

