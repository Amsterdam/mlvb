import requests
import time
import xml.etree.cElementTree as ET
import os
import errno
import json
import csv


def create_dir_if_not_exists(directory):
    """
    Create directory if it does not yet exists.

    Args:
        Specify the name of directory, for example: `dir/anotherdir`

    Returns:
        Creates the directory if it does not exists, of return the error message.
    """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def save_file(data, output_folder, filename):
    """
        save_file currently works with: csv, txt, geojson and json as suffixes.
        It reads the filename suffix and saves the file as the appropriate type.

        Args:
            1. data: list of flattened dictionary objects for example: [{id:1, attr:value, attr2:value}, {id:2, attr:value, attr2:value}]
            2. filename: data_output.csv or data_output.json
            3. output_folder: dir/anotherdir

        Returns:
            Saved the list of objects to the given geojson or csv type.
    """
    create_dir_if_not_exists(output_folder)
    suffix = filename.split('.')[-1]
    full_path = os.path.join(output_folder, filename)
    if suffix in ('geojson', 'json'):
        with open(full_path, 'w') as out_file:
            json.dump(data, out_file, indent=2)
    if suffix in ('csv', 'txt'):
        with open(full_path, 'w') as out_file:
            # get header titles based on first object in array
            header = list(data[0].keys())
            csvWriter = csv.writer(out_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            csvWriter.writerow(header)
            for row in data:
                csvWriter.writerow(row.values())

    print("File saved here: {}".format(full_path))

def get_xml(url):
    data = requests.get(url).text
    #print(data)
    root = ET.fromstring(bytes(data, 'utf-8'))
    return root


def get_item(parent, parent_name, child_name, namespaces):
    for child in parent.findall(parent_name, namespaces):
        #print(child)
        item = child.find(child_name, namespaces)
        print(item)
        return item


def get_items(parent, parent_name, namespaces):
    for child in parent.findall(parent_name, namespaces):
        items = child.getchildren()
        return items


def get_latest_xml_data(meta_url, namespaces):
    root = get_xml(meta_url)

    record = get_item(root, 'locgov:records', 'locgov:record', namespaces)
    record_data = get_item(record, 'locgov:recordData','sru:gzd', namespaces)
    meta_data = get_item(record_data, 'sru:originalData','overheidbwb:meta', namespaces)
    title = get_item(meta_data, 'sru:owmskern', 'dcterms:title', namespaces).text
    date = get_item(meta_data, 'sru:owmskern', 'dcterms:modified', namespaces).text

    location_data = get_item(record_data, 'sru:enrichedData','overheidbwb:locatie_toestand', namespaces)
    print("""
        Retrieving    : {}
        Date modified : {}
        Uri           : {}
          """.format(title, date, location_data.text))
    return get_xml(location_data.text)


def get_traffic_signs(xml_toestand, namespaces):
    borden = []
    image_path = 'http://wetten.overheid.nl/afbeelding?toestandid=BWBR0004825/2017-07-01_0&naam='

    wetbesluit = get_item(xml_toestand, 'wetgeving', 'wet-besluit', namespaces)
    for bijlage in wetbesluit.findall("bijlage[@bwb-ng-variabel-deel='/Bijlage1']"):
        for hoofdstuk in bijlage:
            print(hoofdstuk.get('bwb-ng-variabel-deel'))
            for elements in hoofdstuk.iter():
                if elements != None:
                    for kop in elements.iter('kop'):
                        print(kop)
                        fields = []
                        images = []
                        for field in elements.findall(".//table/tgroup/tbody/row/entry/*"):
                            for image in field.findall('illustratie'):
                                images.append(image.get("naam"))
                            if field.text is not None:
                                if field.text.strip(' \t\n\r') not in ('Bord', 'Omschrijving', ''):
                                    fields.append(field.text.strip(' \t\n\r'))
                        bordnummer = fields[::2]  # uneven rows in table
                        #print('bord ', bordnummer)
                        omschrijving = fields[1::2]  # even rows in table
                        #print('omschrijving ', omschrijving)
                        for a,b,c in zip(bordnummer, omschrijving, images):
                            bord = {
                                'traffic_sign_id_short':a,
                                'traffic_sign_id_long':a[0]+str(a[1:]).zfill(2),
                                'description': b,
                                'division': kop[1].text,
                                'image_url': '{}{}'.format(image_path, c),
                                'law_url':'http://wetten.overheid.nl/jci1.3:c:BWBR0004825&bijlage=1&z=2017-07-01&g=2017-07-01'}
                            borden.append(bord)
    print(borden)
    return borden


def main():
    """
    Docs for using the SRU service:

        http://koop.overheid.nl/sites/koop.wmrijk.nl/files/Basiswettenbestand%20-%20Gebruikersdocumentatie%20-%20SRU%20v1.2.pdf

    Examples using the SRU service:

        http://koop.overheid.nl/producten/bwb/sru-use-cases

    Readable url:

        'http://wetten.overheid.nl/BWBR0004825'

    Final XML which is used:

        https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0004825/2014-03-20_0/xml/BWBR0004825_2014-03-20_0.xml

    """
    today = time.strftime("%Y-%m-%d")  # to get the latest applicable law
    identifier = 'BWBR0004825'

    query = 'dcterms.identifier=={} and \
             overheidbwb.geldigheidsdatum={}'.format(identifier, today)

    dutch_law_url = 'http://zoekservice.overheid.nl/sru/Search?operation=searchRetrieve&version=1.2&x-connection=BWB&query='
    meta_url = '{}{}'.format(dutch_law_url, query)

    namespaces = {
        'locgov': 'http://www.loc.gov/zing/srw/',
        'sru': 'http://standaarden.overheid.nl/sru',
        'overheidbwb': 'http://standaarden.overheid.nl/bwb/terms/',
        'dcterms': 'http://purl.org/dc/terms/'
        }

    xml_toestand = get_latest_xml_data(meta_url, namespaces)
    data = get_traffic_signs(xml_toestand, namespaces)
    save_file(data, 'data', 'traffic_signs.json')
    save_file(data, 'data', 'traffic_signs.csv')


if __name__ == "__main__":
    main()
