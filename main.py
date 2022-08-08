import requests
import datetime  # Используется для фиксации времени при логгировании


# Задача №1 Кто самый умный супергерой?
def task_1():
    heroes = {'Hulk': '0', 'Thanos': '0', 'Captain America': '0'}
    token = '2619421814940190'
    base_url = 'https://superheroapi.com/api/' + token
    for hero in heroes.keys():
        search_id_url = base_url + '/search/' + hero.replace(' ', '%20')
        response = requests.get(search_id_url)
        if response.status_code == 200:
            heroes[hero] = response.json()['results'][0]['powerstats']['intelligence']
        else:
            print(f'Ответ не успешен. Response.status_code ='
                  f'{response.status_code}')

    sorted_int_list = sorted(heroes.values())
    max_int = sorted_int_list[0]
    for hero in heroes.keys():
        if heroes[hero] == max_int:
            most_int_hero = hero
            return(most_int_hero, max_int)


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def create_folder_on_disk(self, folder):
        create_folder_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {'path': folder}
        response = requests.put(create_folder_url, headers=headers,
                                params=params)
        if response.status_code == 201:
            print()
            print(f'Папка {folder} создана')
        elif response.status_code == 409:
            print()
            print(f'Папка {folder} уже существует на Диске')
        else:
            print()
            print("Ответ сервиса на запрос по созданию папки:")
            print(response.json())

        return

    def get_user_info(self):
        user_info_url = "https://cloud-api.yandex.net/v1/disk"
        headers = self.get_headers()
        response = requests.get(user_info_url, headers=headers)

        return response.json()['user']['display_name']

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return(response.json())

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self.get_upload_link(disk_file_path=disk_file_path).get('href', '')
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print()
            print(f'Файл {filename} успешно загружен на Диск,'
                  f' в папку {folder}')
        else:
            print()
            print(response.json())


if __name__ == '__main__':
    token = ''  # Позднее в токен сохраним значение в рамках сессии
    folder = ''
    while True:
        print()
        print('1. Кто самый умный супер-герой (Задача №1)')
        print('2. Сохранение файла на Яндекс.Диск (Задача №2)')
        print('3. Завершение работы')
        print()
        error = 1
        while error == 1:
            try:
                choise = int(input('Введите номер пункта: '))
            except ValueError:
                print()
                print('Неверный формат ввода номера пункта.')
                continue
            if choise < 1 or choise > 3:
                print()
                print('Неверный номер пункта.')
                continue
            error = 0

        if choise == 1:  # Задача №1 Кто самый умный супер-герой
            hero, intelligence = task_1()
            print()
            print('Наиболее умный герой -', hero)
            print('Показатель его интеллекта -', intelligence, 'баллов')
            print()
            delay = input('Нажмите Enter для продолжения ')
            continue

        elif choise == 2:  # Задача №2 Сохранение файла на Яндекс.Диск
            if token == '':
                token = input('Введите Ваш токен: ')  # Сохраним токен
                                                      # в рамках сессии
            uploader = YaUploader(token)
            disk_file_path = '00_test/test.txt'
            filename = 'test.txt'
            print()

            if folder == '':  # Выделяем из пути на диске имя папки
                list = list(disk_file_path)
                list2 = list
                for letter in reversed(list):
                    if letter != '/':
                        list2.pop(-1)
                    else:
                        list2.pop(-1)
                        break
                folder = ''.join(list2)

            print(f'{uploader.get_user_info().capitalize()}, файл {filename}'
                  f' будет загружен в папку {folder} на вашем Я.Диске')

            uploader.create_folder_on_disk(folder)

            with open(filename, 'a', encoding='utf-8') as file:
                file.write(f'{datetime.datetime.now()} - пользователь:'
                           f' {uploader.get_user_info()} - тестирование'
                           f' загрузки на Яндекс.Диск \n')

            uploader.upload_file_to_disk(disk_file_path, filename)

            print()
            delay = input('Нажмите Enter для продолжения ')
            continue

        else:
            print('Работа программы завершена')
            exit()
