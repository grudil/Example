import vk_api
import json
import urllib
import os
import operator
import time
from urllib.error import HTTPError

import requests


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    login = 'your_login'
    password = 'your_password'
    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    """ VkApi.method позволяет выполнять запросы к API. В этом примере
        используется метод wall.get (https://vk.com/dev/wall.get) с параметром
        count = 1, т.е. мы получаем один последний пост со стены текущего
        пользователя.
    """

    def write_json(data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    response = vk.market.get(owner_id=-141247903, count=200, extended=1)

    def create_product(adress, response):

        for i in range(len(adress)):
            for item in response["items"]:
                if (item["id"] == adress[i][0]):
                    name_img = 'product/' + str(adress[i][1]) + '/' + \
                               str(adress[i][0]) + '/' + \
                               str(adress[i][0]) + '.jpg'

                    name = 'product/' + str(adress[i][1]) + '/' + \
                           str(adress[i][0]) + '/'

                    '''
                        Получаем адресс сервера для загрузки изображения
                    '''

                    photo_url = vk.photos.getMarketUploadServer(
                        group_id=158347757, main_photo=1)
                    write_json(photo_url, 'server.json')

                    '''
                        Загружаем фото на сервер
                        В file передавать путь до нашего изображения
                    '''
                    file = {'file': open(name_img, 'rb')}

                    photo_info = requests.post(
                        photo_url["upload_url"], files=file).json()

                    write_json(photo_info, name + 'image.json')

                    ''' Загружаем фото товара'''
                    save_photo = vk.photos.saveMarketPhoto(group_id=158347757,
                                                           photo=photo_info["photo"],
                                                           server=photo_info["server"],
                                                           hash=photo_info["hash"],
                                                           crop_data=photo_info["crop_data"],
                                                           crop_hash=photo_info["crop_hash"])
                    write_json(save_photo, name + 'save_photo.json')

                    category_id = int(item['category']['id'])
                    price = int(int(int(item['price']['amount']) / 100) * 1.2)
                    main_photo_id = int(save_photo[0]['id'])

                    ''' Добавляем товар'''
                '''    add_product = vk.market.add(owner_id = -158347757, name=item["title"],\
                                                description = item['description'],\
                                                category_id = category_id,\
                                                price = price,\
                                                main_photo_id = main_photo_id,\
                                                )
                    write_json(add_product, name + 'product_upload.json')
                '''

    def out_json(name='vk.txt'):
        file = open(name, 'w')
        file.write(json.dumps(response['items'], indent=2))

    def create_photo(adress, response):
        for i in range(len(adress)):
            for item in response["items"]:

                if (item["id"] == adress[i][0]):
                    img = item["photos"][0]['photo_604']
                    while True:
                        try:
                            with urllib.request.urlopen(img) as f:
                                name_img = 'product/' + str(adress[i][1]) + '/' + \
                                           str(adress[i][0]) + '/' + \
                                           str(adress[i][0]) + '.jpg'
                                name_text = 'product/' + str(adress[i][1]) + '/' + \
                                            str(adress[i][0]) + '/' + \
                                            str(adress[i][0]) + '.json'
                                out = open(name_img, "wb")
                                out.write(f.read())
                                out.close()
                                file = open(name_text, 'w')
                                file.write(json.dumps(item, indent=2))
                                file.close()
                                print('id: ', item["id"], 'status: OK')
                                # Прошло без ошибок, выходим
                                break

                        except HTTPError as e:
                            # Ждем 30 секунд перед повтором запроса
                            time.sleep(30)

    def add_album(cost_arr):

        for cost in cost_arr:
            title = str(int(cost * 1.2)) + ' руб'
            photo_id = 'product/' + \
                str(cost) + '/' + \
                str(cost_arr[cost][0]) + '/' + 'save_photo.json'
            file_json = open(photo_id)
            parse_id = json.load(file_json)
            album = vk.market.addAlbum(owner_id=-158347757, title=title,
                                       photo_id=parse_id[0]['id'], main_album=0)

    def create_dir(cost_arr, response):

        for key in cost_arr:
            cost_arr[int(key)] = []

        for key in cost_arr:
            for items in response["items"]:
                if int(int(items["price"]["amount"]) / 100) == key:
                    cost_arr[int(key)].append(items["id"])

        for key in cost_arr:
            for id in cost_arr[key]:
                path = 'product' + '/' + str(key) + '/' + str(id)
                if not os.path.exists(path):
                    os.makedirs(path)

    if response['items']:

        id = []
        amount = []

        for item in response["items"]:
            id.append(int(item["id"]))
            amount.append(int(int(item["price"]["amount"]) / 100))

        items = dict.fromkeys(id)

        j = 0
        for i in id:
            items[i] = amount[j]
            j += 1

        sorted_x = sorted(items.items(), key=operator.itemgetter(1))

        amount.sort()
        cost_arr = dict.fromkeys(amount)

        create_dir(cost_arr, response)
        add_album(cost_arr)
        out_json('product.json')


if __name__ == '__main__':
    main()
