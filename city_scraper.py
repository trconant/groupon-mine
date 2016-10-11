__author__ = 'troyconant'

import json
from urllib2 import urlopen
import urllib2
from pprint import pprint
import csv, codecs, cStringIO, sys
import os
import itertools
import datetime
import math
import time

## Web Scraper that cycles through each CITY in used in and partnered with Groupon
## Collects every deal from those city.

-----> # OUTPUTS JSON file

---------------------------------------------------------------------------

opener = urllib2.build_opener(
    urllib2.HTTPHandler(),
    urllib2.HTTPSHandler(),
    urllib2.ProxyHandler())
urllib2.install_opener(opener)

starting_deal_number = 0

userkeys = '_user=645a6982-801f-4396-a14d-84611b05032c&_apikey=%2Bz2zMKlb1YLAkiAPG4ZSI%2FYyTo3xEkjaOA3cIC%2FHcRL9kODyZ46cGkp4lfNEPW3Gbn6RWmvte0fMTGXrJECTWQ%3D%3D'

with open('Groupon_City_List(removed_duplicates).csv') as Groupon_Cities:
    readCities = csv.reader(Groupon_Cities, delimiter=',')
    for row in readCities:
        cities = row



def get_deals():
    def url_page(url):
        def trim(d):
            try:
                if d.has_key('retail_price/_currency'):
                    del d['retail_price/_currency']
                    del d['retail_price/_source']
                    del d['groupon_price/_currency']
                    del d['groupon_price/_source']
                    del d['discount/_source']
            except BaseException, e:
                pass

            if d.has_key('categories'):
                del d['categories']
                del d['categories/_source']
            d['time_retrieved'] = str(datetime.datetime.now())
            d['url'] = page_example
            return d

        page_example = url
        link = 'https://api.import.io/store/data/dea8c030-fc2d-4a68-ad86-75ef92d21810/_query?input/webpage/url=' + page_example + '&' + userkeys
        # print json.load(urlopen(link))['results']
        # print link
        f = json.load(urlopen(link))['results']
        f = [trim(d) for d in f]
        return f

    def total_page_extractor(city):
        url = 'https://api.import.io/store/data/974a1dc1-4fa8-4890-9312-d2b9ca43f385/_query?input/webpage/url=http://www.groupon.com/browse/' + city + '?context=local&' + userkeys
        return url

    def total_page_extractor_backup(city):
        url = 'https://api.import.io/store/data/c1ea6c12-c034-4b99-9252-81a5395c1701/_query?input/webpage/url=http://www.groupon.com/browse/' + city + '?context=local&' + userkeys
        return url

    backup_page_list = []
    deals_list = []
    page_data_list = []

    # with open('Updated_sample_groupon_page_data_test.json', 'w') as jsonfile:
    # json.dump(page_data_list, jsonfile, encoding='utf8')

    for c in cities[21:23]:
        print c
        try:
            trial = [json.load(urlopen(total_page_extractor(c)))['results'] for each in range(0, 10)]

            trial = itertools.ifilter(None, trial).next()
            for page in trial:
                total_pages = int(page['total_page_numb/_text'])
                print "%s total pages for %s" % (total_pages, c)
            # print type(total_pages)
            # print trial
            for s in range(1, total_pages + 1):
                city = c
                page_number = str(s)
                # print page_number
                deal_list_crawler = 'https://api.import.io/store/data/affd236e-be39-4952-9100-d7f3564add10/_query?input/webpage/url=http://www.groupon.com/browse%2F' + city + '%3Fcontext%3Dlocal%26page%3D' + page_number + '&' + userkeys
                result = json.load(urlopen(deal_list_crawler))['results']
                while True:
                    if result != []:
                        for d in result:
                            del d['all_deals_links/_source']
                            del d['all_deals_links/_text']
                        deals_list = result + deals_list
                        break
                    else:
                        print 'lookup backup'
                        trial_2 = [json.load(urlopen(deal_list_crawler))['results'] for each in range(0, 10)]
                        trial_2 = itertools.ifilter(None, trial_2).next()
                        for d in trial_2:
                            del d['all_deals_links/_source']
                            del d['all_deals_links/_text']
                        deals_list = trial_2 + deals_list
                        # print "trial_2 %s" %trial_2
                        break
            # print deals_list
            print len(deals_list)
            pass
        except BaseException, e:
            print "%s: using backup" % (c)
            for each in range(0, 5):
                for backup in json.load(urlopen(total_page_extractor_backup(c)))['results']:
                    total_pages = int((backup['my_column/_text'][-1]))
                    backup_page_list.append(total_pages)
                # print total_pages
                total_pages = max(backup_page_list)

            for s in range(1, total_pages + 1):
                city = c
                page_number = str(s)
                # print page_number
                deal_list_crawler = 'https://api.import.io/store/data/affd236e-be39-4952-9100-d7f3564add10/_query?input/webpage/url=http://www.groupon.com/browse%2F' + city + '%3Fcontext%3Dlocal%26page%3D' + page_number + '&' + userkeys
                result = json.load(urlopen(deal_list_crawler))['results']
                # print 'ffjasnfdk %s' % result
                while True:
                    # f= json.load(urlopen(deal_list_crawler))['results']
                    if result != []:
                        for d in result:
                            del d['all_deals_links/_source']
                            del d['all_deals_links/_text']
                        deals_list = result + deals_list
                        break
                    else:
                        try:
                            trial_3 = [json.load(urlopen(deal_list_crawler))['results'] for each in range(0, 15)]
                            trial_3 = itertools.ifilter(None, trial_3).next()
                            for d in trial_3:
                                del d['all_deals_links/_source']
                                del d['all_deals_links/_text']
                            deals_list = trial_3 + deals_list
                            # print "trial_2 %s" %trial_2
                            break
                        except BaseException, e:
                            print trial_3
                            time.sleep(10)
            # print deals_list
            print len(deals_list)
            pass

        print "Gathering Deals Complete"

    try:
        with open('Updated_sample_groupon_page_data_test.json', 'w') as jsonfile:
            jsonfile.write('[')

            for data in range(starting_deal_number, len(deals_list)):
                if data + 1 == (len(deals_list)):

                    json.dump((url_page(str(deals_list[data]['all_deals_links']))), jsonfile, encoding='utf8')
                    jsonfile.write(']')

                else:
                    json.dump((url_page(str(deals_list[data]['all_deals_links']))), jsonfile, encoding='utf8')
                    jsonfile.write(',')

    except BaseException, e:
        with open('Updated_sample_groupon_page_data_test.json', 'a') as jsonfile:
            jsonfile.write(']')

            print 'error in gathering'
            print 'Ended at %s' % data

    jsonfile.close()

    print len(page_data_list)

    jsonfile.close()
    os.system('say "Complete"')


Groupon_Cities.close()

get_deals()