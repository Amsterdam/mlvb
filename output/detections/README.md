# Detections
This directory contains the output of the detection pipeline.

## VGG16 + transferlearning results
Data set used in traning:
~ 2100 example images containing "vluchtheuvelbakens"
~ 17500 counter examples not containing "vluchtheuvelbakens"

Results (data files below) were obtained on a random sub-sample of panorama
images from 2017.

`locations-detected-2018-05-07.csv`: locations of "vluchtheuvelbaken" images
`locations-detected-2018-05-11.csv`: locations of "vluchtheuvelbaken" images

## Conversion

To show the locations with the correct pano url's we convert the csv to geojson and adding the pano images urls by running:

`python create_geojson.py --csv locations-detected-2018-05-15.csv --geojson 2018-05-15-detections-vluchtheuvel-bakens.json``

