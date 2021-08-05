import json
import math
import pandas as pd
import requests
from tqdm import tqdm


def category_results(token, category, offset):
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    # MLU es el sitio de Uruguay
    # ITEM_CONDITION = 2230581 -> Usados solamente
    url = 'https://api.mercadolibre.com/sites/MLU/search?category={}&offset={}&ITEM_CONDITION=2230581'.format(category,
                                                                                                              offset)
    response = requests.get(url, headers=headers)
    return response.json()


def att_value_name(attributes, att_name):
    value = find_attribute(attributes, att_name)
    if value is None:
        return None

    return find_attribute(attributes, att_name)['value_name']


def att_number_value(attributes, att_name):
    value = find_attribute(attributes, att_name)
    if value is None or value['value_struct'] is None:
        return -1
    return value['value_struct']['number']


def find_attribute(attributes, att_name):
    res = list(filter(lambda x: x['id'] == att_name, attributes))
    if len(res) > 0:
        return res[0]
    else:
        return None


def map_car(result):
    car = {}
    car['price'] = result['prices']['prices'][0]['amount']

    attributes = result['attributes']

    car['used'] = att_value_name(attributes, 'ITEM_CONDITION')
    car['engine_displacement'] = att_number_value(attributes, 'ENGINE_DISPLACEMENT')
    car['vehicle_year'] = att_value_name(attributes, 'VEHICLE_YEAR')
    car['brand'] = att_value_name(attributes, 'BRAND')
    car['model'] = att_value_name(attributes, 'MODEL')
    car['engine'] = att_value_name(attributes, 'ENGINE')
    car['doors'] = att_value_name(attributes, 'DOORS')
    car['traction_control'] = att_value_name(attributes, 'TRACTION_CONTROL')
    car['power'] = att_number_value(attributes, 'POWER')
    car['fuel_type'] = att_value_name(attributes, 'FUEL_TYPE')
    car['km'] = att_number_value(attributes, 'KILOMETERS')
    car['transmission'] = att_value_name(attributes, 'TRANSMISSION')
    car['trim'] = att_value_name(attributes, 'TRIM')
    car['permalink'] = result['permalink']

    return car


def main(token):
    page_size = 50
    response = category_results(token, 'MLU1744', 0)  # autos y camionetas

    response['paging']['total'] = 100  # -----> cantidad de autos que pienso descargar <<<<<<

    total_cars = response['paging']['total']

    print("Autos para descargar: {}".format(total_cars))

    page_count = math.ceil(total_cars / page_size)
    cars = []
    for i in tqdm(range(page_count)):
        response = category_results(token, 'MLU1744', i * page_size)

        page_cars = list(map(lambda x: map_car(x), response['results']))
        cars += page_cars

    ids = []
    for i in range(len(cars)):
        ids.append(i)
    df = pd.DataFrame.from_dict({'id': ids})
    for k in cars[0].keys():
        df[k] = df.id.apply(lambda x: cars[x][k])

    df.to_csv('used_cars.csv', index=False)


if __name__ == "__main__":
    secrets = json.loads(open('secrets.json', 'r').read())
    access_token = secrets['access_token']
    main(access_token)

# TODO convertir a dolares el renault megane: https://auto.mercadolibre.com.uy/MLU-480294333-renault-megane-turbo-diesel-_JM
