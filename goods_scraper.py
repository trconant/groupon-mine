__author__ = 'troyconant'

import json
from urllib2 import urlopen
import urllib2
from pprint import pprint
import os
import datetime
import time
import random
import itertools

## Collects Groupon Deals, specifically the 'GOODS' section. https://www.groupon.com/goods

---------------------------------------------------------------------------------------------

# Proxies are setup and cycled through if Groupon shuts the current IP address out.


proxies = [{'https': '183.207.232.119:8080'}, {'https': '194.154.74.210:8080'}, {'https': '68.68.97.2:3128'}]

random_proxy = random.choice(proxies)

print random_proxy

opener = urllib2.build_opener(
    urllib2.HTTPHandler(),
    urllib2.HTTPSHandler(),
    urllib2.ProxyHandler(random_proxy))

urllib2.install_opener(opener)

# Importio User Key.
userkeys = '_user=645a6982-801f-4396-a14d-84611b05032c&_apikey=%2Bz2zMKlb1YLAkiAPG4ZSI%2FYyTo3xEkjaOA3cIC%2FHcRL9kODyZ46cGkp4lfNEPW3Gbn6RWmvte0fMTGXrJECTWQ%3D%3D'

# Takes the Importio setup and collects the individual deals on the Groupon Website.



def get_goods_deals():
    print 'START : %s' % datetime.datetime.now()

    # empty lists to put data
    links_list = []
    link_strings = []
    deals_list = []
    page_data_list = []
    char_convert = {'/': '%2F', '=': '%3D', '&': '%26', ':': '%3A', '?': '%3F'}

    # Collects individual Deal data
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
            d['city'] = "montana-city"
            return d

        page_example = url
        link = 'https://api.import.io/store/data/dea8c030-fc2d-4a68-ad86-75ef92d21810/_query?input/webpage/url=' + page_example + '&' + userkeys

        while True:
            try:
                link_result = json.load(urlopen(link, timeout=20))['results']
                break

            except BaseException, e:
                print 'timeout'
                print link
                time.sleep(60)
                continue

        link_result = [trim(d) for d in link_result]
        return link_result

    def gg_total_page(link):
        url = 'https://api.import.io/store/data/c1ea6c12-c034-4b99-9252-81a5395c1701/_query?input/webpage/url=' + link + '&' + userkeys
        return url

    # removes duplicates from the final deals_list
    def remove_duplicates(deals_list):
        seen = set()
        for d in deals_list:
            h = d.copy()
            h = tuple(h.items())
            if h not in seen:
                unique_deals_list.append(d)
                seen.add(h)
            return unique_deals_list

    def convert(url, dic):
        for k, v in dic.iteritems():
            url = url.replace(k, v)
        return url


    category_links_url = 'https://api.import.io/store/data/7edf6eaf-5c6e-4935-b52c-c0e5bec574f2/_query?input/webpage/url=http://www.groupon.com/goods?category=all&' + userkeys

    for url in json.load(urlopen(category_links_url))['results']:
        del url['my_column/_source']
        del url['my_column/_text']
        links_list.append(url)

    [link_strings.append(str((links_list[d]['my_column']))) for d in range(len(links_list))]

    new_link_strings = []

    for l in range(len(link_strings)):
        cate = link_strings[l]

        while True:
            try:
                goods_categories = 'https://api.import.io/store/data/0de630ab-7e51-424b-897c-8e676ba683cd/_query?input/webpage/url=' + cate + '&' + '_user=645a6982-801f-4396-a14d-84611b05032c&_apikey=%2Bz2zMKlb1YLAkiAPG4ZSI%2FYyTo3xEkjaOA3cIC%2FHcRL9kODyZ46cGkp4lfNEPW3Gbn6RWmvte0fMTGXrJECTWQ%3D%3D'
                result = json.load(urlopen(goods_categories))['results']
                for d in result:
                    if 'category2' in d['goods_categories']:
                        new_link_strings.append(d['goods_categories'])
                    else:
                        pass
                break
            except Exception, e:
                print 'error'
                time.sleep(3)
                continue

    print pprint(new_link_strings)

    print datetime.datetime.now()
    for links in new_link_strings:
        links = convert(links, char_convert)
        backup_page_list = []
        for each in range(0, 6):
            if json.load(urlopen(gg_total_page(links)))['results'] != []:
                for backup in json.load(urlopen(gg_total_page(links)))['results']:
                    total_pages = int((backup['my_column/_text'][-1]))
                    backup_page_list.append(total_pages)


            else:
                total_pages = 1
                backup_page_list.append(total_pages)

                continue

            total_pages = max(backup_page_list)

        print '%s has %s pages' % (links, total_pages)

        for s in range(1, total_pages + 1):

            category_link = links
            page_number = str(s)
            deal_list_crawler = 'https://api.import.io/store/data/affd236e-be39-4952-9100-d7f3564add10/_query?input/webpage/url=' + category_link + '%26page%3D' + page_number + '&' + userkeys

            try:
                while True:
                    result = json.load(urlopen(deal_list_crawler))['results']
                    if result != []:
                        for d in result:
                            del d['all_deals_links/_source']
                            del d['all_deals_links/_text']
                        deals_list = deals_list + result
                        break
                    else:
                        try:
                            trial_3 = [json.load(urlopen(deal_list_crawler))['results'] for each in range(0, 15)]
                            trial_3 = itertools.ifilter(None, trial_3).next()
                            for d in trial_3:
                                del d['all_deals_links/_source']
                                del d['all_deals_links/_text']
                            deals_list = deals_list + trial_3
                            # print "trial_2 %s" %trial_2
                            break
                        except BaseException, e:

                            time.sleep(10)
            except BaseException, e:
                pass

        print len(deals_list)
        print datetime.datetime.now()
        pass

    print "Gathering Deals Complete"

    unique_deals_list = []
    unique_deals_list = remove_duplicates(deals_list)

    print len(unique_deals_list)
    print unique_deals_list

    starting_deal_number = 0
    # takes a list of deals and extracts the data in each and writes it to a file
    try:
        with open('GOODS_sample_groupon_page_data.json', 'w') as jsonfile:
            jsonfile.write('[')

            for data in range(starting_deal_number, len(unique_deals_list)):
                if data + 1 == (len(unique_deals_list)):

                    json.dump((url_page(str(unique_deals_list[data]['all_deals_links']))), jsonfile, encoding='utf8')
                    jsonfile.write(']')

                else:
                    json.dump((url_page(str(unique_deals_list[data]['all_deals_links']))), jsonfile, encoding='utf8')
                    time.sleep(3)
                    jsonfile.write(',')

    except BaseException, e:
        with open('GOODS_sample_groupon_page_data.json', 'a') as jsonfile:
            jsonfile.write(']')

            print 'error in gathering'
            print 'Ended at %s' % data

    jsonfile.close()

    print len(page_data_list)

    jsonfile.close()
    os.system('say "Complete"')


get_goods_deals()