import requests
import csv
import json
import time
import ipdb
# "http://where.yahooapis.com/geocode?q=Wittelsbacher+Allee+151+Frankfurt+Germany&appid=[yourappidhere]"

def get_coordinates(line):
    name1 = line[0]
    name2 = line[1]
    name3 = line[2]
    ort = line[4]
    land = line[5]
    url = 'http://maps.google.com/maps/api/geocode/json?address=%s,+%s&sensor=true' % (ort.replace(' ','+'), land.replace(' ', '+'))
    g = requests.get(url)
    api_results = json.loads(g.content)
    if len(api_results['results']) == 0:
        location = {'lat': 0, 'lng': 0}
    else:
        location = api_results['results'][0]['geometry']['location']
    return location

with open( 'data/samentausch_partner_frankfurt.csv', 'rb') as f, open('data/samentausch_partner_frankfurt_geo.json', 'wb') as fw:# Samentausch Partner2.txt", 'rU') as f:
    reader = csv.reader(f, delimiter=';')
    reader.next()
    fieldnames = ('name', 'city', 'country', 'latitude', 'longitude')
    outputs = []
    print dict( (n,n) for n in fieldnames )
    # writer = csv.DictWriter(fw, fieldnames, dialect=csv.excel_tab)
    # writer.writerow(dict( (n,n) for n in fieldnames ))
    for line in reader:
        location = get_coordinates(line)
        output = {'name': line[0] + " " + line[1] + " " + line[2], 'city': line[4], 'country': line[5], 'latitude': location['lat'], 'longitude': location['lng']}
        outputs.append( output )
        # writer.writerow(output)
        time.sleep(0.2)
    json.dump(outputs, fw)