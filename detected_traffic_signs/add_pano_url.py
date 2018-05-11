import json
# import re
import os
import requests

with open('../output/detections/2018-05-11-detections-vluchtheuvel-bakens.json') as data:
    geojson = json.load(data)
    for feature in geojson['features']:
        # https://data.amsterdam.nl/panorama/2017/03/07/TMX7316010203-000198/pano_0000_000000/equirectangular/panorama_2000.jpg
        # TMX7316010203-000301_pano_0000_003409
        pano_id = feature['properties']['pano_id']
        # dir1 = re.match(r'([A-Z0-9-]*)_(pano[_0-9]*)', pano_id)
        # print(dir1.group(1))
        # print(dir1.group(2))
        base_url = 'https://api.data.amsterdam.nl/panorama/recente_opnames/2017'
        uri = os.path.join(base_url, pano_id)
        print(uri)
        pano_uri = requests.get(uri)
        pano_json = pano_uri.json()
        feature['url'] = pano_json['image_sets']['equirectangular']['small']

with open('../output/detections/2018-05-11-detections-vluchtheuvel-bakens-panos.json') as f:
    json.dump(geojson, f)
