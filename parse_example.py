import csv
import numpy
import json
from json import dumps
import geocoder


MYFILE = "....repro.csv"

#Stage 1: Parse your data
class Parse (object):
    def __init__ (self, parsed_file = None):
        self.parsed_file = parsed_file

    def parse_data (self, raw_file, delimiter = ','):
        """Parse our CSV file and make it into data!"""
        #open our file
        opened_file = open (raw_file)
        #read our file
        csv_reader = csv.reader (opened_file, delimiter = delimiter)
        #convert contents of our file to a dict stored in an list
        parsed_data = []
        headers = csv_reader.next ()
        for items in csv_reader:
            parsed_data.append (dict(zip(headers,items)))
        #close file
        opened_file.close ()
        return parsed_data

    def saveparse (self, raw_file):
        """Parses your raw file and writes it to a new CSV file."""
        with open ('parsed_file.csv', 'w') as new_file:
            #write contents of parsed file to new file and close
            parsed_data = self.parse_data(raw_file)
            new_file.write (str(parsed_data))

def create_map (data_file):
    """Take our parsed data and geocode it to a map."""
    geo_map = {'type': 'FeatureCollection'}
    list_of_items = []
    for index, item in enumerate(data_file):
        data = {}
        if item['Country'] == "":
            continue
        else:
            countrytitle = item['Country'].encode('utf-8').strip ()
            g = geocoder.osm(countrytitle)
            if g.lat != None and g.lng != None:
                lat = float(g.lat)
                lng = float(g.lng)
                data ['type'] = "Feature"
                data ['id'] = index
                data ['geometry'] = {'type': 'Point', 'coordinates': (lng, lat)}
                data ['properties'] = {'risk': item ['Lifetime risk of maternal mortality'],
                    'prenatal care': item ['Pregnant women receiving prenatal care'],
                        'total fertility rate': item ['Total fertility rate'],
                        'adolescent fertility rate': item ['Adolescent fertility rate']}
                list_of_items.append (data)
    for point in list_of_items:
        geo_map.setdefault ('features', []).append(point)
    with open ('repro_world.geojson', 'w') as f:
        f.write (json.dumps(geo_map))

def main ():
    repro_parse = Parse ()
    data = repro_parse.parse_data (MYFILE)
    return create_map (data)

if __name__ == "__main__":
    main ()
