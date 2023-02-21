import json

import requests
from loguru import logger
from requests import get

from config_data.config import RAPID_API_KEY, X_RAPIDAPI_HOST


def api_request(method_endswith: str, params: dict, method_type: str) -> dict and list:
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"
    if method_type == 'GET':
        return get_request(url=url, params=params)
    else:
        return post_request(url=url, params=params)


def get_request(url: str, params: dict) -> dict:
    try:
        response = get(url,
                       headers={
                           "X-RapidAPI-Key": RAPID_API_KEY,
                           "X-RapidAPI-Host": X_RAPIDAPI_HOST
                       },
                       params=params,
                       timeout=15
                       )
        if response.status_code == requests.codes.ok:
            logger.info('Идет GET запрос на сайт.')
            data = json.loads(response.text)
            cities = dict()
            for id_dict in range(len(data['sr'])):
                if data['sr'][id_dict]['type'] != 'AIRPORT' and data['sr'][id_dict]['type'] != 'HOTEL':
                    cities[data['sr'][id_dict]['gaiaId']] = data['sr'][id_dict]['regionNames']['shortName']
            return cities
    except TypeError('Ошибка'):
        print('Сука')


def post_request(url: str, params: dict) -> list:
    try:
        logger.info('Идет POST запрос на сайт.')
        response = requests.request("POST",
                                    url=url,
                                    headers={
                                        "content-type": "application/json",
                                        "X-RapidAPI-Key": RAPID_API_KEY,
                                        "X-RapidAPI-Host": X_RAPIDAPI_HOST
                                    },
                                    json=params,
                                    timeout=15
                                    )
        if response.status_code == requests.codes.ok:
            if url.endswith('list'):
                logger.info('POST-list запрос на сайт прошел.')
                data = json.loads(response.text)
                info_hotel = list()
                for id_dict in range(len(data['data']['propertySearch']['properties'])):
                    info_hotel.append({'id': data['data']['propertySearch']['properties'][id_dict]['id'],
                                       'name': data['data']['propertySearch']['properties'][id_dict]['name'],
                                       'by_center': data['data']['propertySearch']['properties'][id_dict]
                                       ['destinationInfo']['distanceFromDestination']['value'],
                                       'price': data['data']['propertySearch']['properties'][id_dict]['price']
                                       ['lead']['amount']})

                return info_hotel
            elif url.endswith('detail'):
                logger.info('POST-detail запрос на сайт прошел.')
                data = json.loads(response.text)
                photo_hostels = list()
                for id_dict in range(len(data['data']['propertyInfo']['propertyGallery']['images'])):
                    photo_hostels.append(data['data']['propertyInfo']['propertyGallery']['images'][id_dict]['image']
                                         ['url'])
                photo_hostels.append(data['data']['propertyInfo']['summary']['location']['address']['addressLine'])
                return photo_hostels
    except TypeError('Ошибка'):
        print('Сука')
