# ML pilot project

The results of a comparison between our current administration of traffic signs vs the machine learning found signs of the D02 sign 'vluchtheuvelbaken' can be viewed here:
https://amsterdam.github.io/mlvb

This project was a first effort to detect traffic signs on our panoramic images we provide as opendata:
https://api.data.amsterdam.nl/panorama

## offical_dutch_traffic_signs_by_law

The sign numbering is based on the offical traffic sign law:
http://wetten.overheid.nl/BWBR0004825/2017-07-01

This folder contains alle the offical Dutch traffic signs with descriptions and reference image urls scraped from this site.
[offical_dutch_traffic_signs_by_law/output](https://github.com/Amsterdam/mlvb/tree/master/offical_dutch_traffic_signs_by_law/output)

## frontend

This folder contains the website shown on https://amsterdam.github.io/mlvb
It uses the github.io docs folder to view the site. Which can be setup as a webpage in the settings page of your repository.
The website is build with the use of:
* [template_vue](https://github.com/Amsterdam/template_vue)
* [vue2leaflet](https://github.com/KoRiGaN/Vue2Leaflet)
* [Marzipano](https://github.com/google/marzipano)

To start the frontend locally on localhost:8080 run:
```
    cd frontend
	npm run dev
```

To build the site:
```
    cd frontend
    make docs
```

To view the site on localhost:8000:
```
    cd..
    cd docs
    python3 -m http.server
```

## current_traffic_signs

To compare the ML algorithm with our current administration we had to combine 4 access files, one excel and one shapefile into one database table.
We also imported all the metadata of the pano images (including coordinates) of 2017 into this database to combine the url's of the pano's with the current traffic signs.

To download the current traffic signs data into the database:


### Docker
1. Add the objecstore password to your environment:
```export OBJECTSTORE_PASSWORD=****```

2. Build and run the docker to start a database:
```
cd current_trafic_signs
docker-compose build
docker-compose up
```

### Run locally
1. Add the objecstore password to your environment:
```export OBJECTSTORE_PASSWORD=****```

2. Build and run the docker to start a database:
```
    cd current_trafic_signs
    docker-compose build database
    docker-compose up database
```
3. Install the needed packages and run all the import an export scripts locally:
```
 cd current_trafic_signs
 virtualenv --python=$(which python3) venv
 source venv/bin/activate
 pip install -r requirements.txt
import-dev.sh
```

## pre selection of traffic sign images

To create a positive ground truth we use a pre selection of traffic signs using our current administration to tag those images.
This script generates 3 CSV files containing the url's of the nearest pano images where there are traffics signs we then labeled positive or false:

`/current_traffic_signs/nearest_pano-dev.sh`

The CSV files can be found in the [output folder](https://github.com/Amsterdam/mlvb/tree/master/output/pano-traffic-sign-pre-selection)

## output

The [output folder](https://github.com/Amsterdam/mlvb/tree/master/output/pano-traffic-sign-pre-selection) contains the resulting csv/json output of the pano images found with the trained Model containing traffic sign and global N Z W E direction within the image.





