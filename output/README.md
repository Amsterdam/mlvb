# output files

This folder contains all the files used for visualising and building up training sets

## asset-registration

One GeoJson of all the 7 municipality registrations coming from 5 Access db's, an excel and a Shapefile ranging from 2014-2017 data. Using data from our objectstore and using [this docker/python script](https://github.com/Amsterdam/mlvb/tree/master/current_traffic_signs). It combines the traffic signs with nearest pano views from 2017 from our [WFS service](https://map.data.amsterdam.nl/maps/panorama?REQUEST=GetCapabilities&SERVICE=wfs).

## detections

The geojson output for each of the detected signs.

## pano-traffic-sign-pre-selection

Pre selection of nearest pano image for each sign to use as training material.
