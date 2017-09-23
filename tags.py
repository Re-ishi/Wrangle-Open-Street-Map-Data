"""
Count multiple patterns in the tags
"""

import xml.etree.cElementTree as ET
import pprint
import re

from collections import defaultdict

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

OSMFILE = "ahmedabad_india.osm"

def key_type(element, keys, keys_content):
    if element.tag == "tag":
        for tag in element.iter('tag'):
            k = tag.get('k')
            if lower.search(element.attrib['k']):
                keys['lower'] = keys['lower'] + 1
                keys_content['lower'].add(k)
            elif lower_colon.search(element.attrib['k']):
                keys['lower_colon'] = keys['lower_colon'] + 1
                keys_content['lower_colon'].add(k)
            elif problemchars.search(element.attrib['k']):
                keys['problemchars'] = keys['problemchars'] + 1
                keys_content['problemchars'].add(k)
            else:
                keys['other'] = keys['other'] + 1
                keys_content['other'].add(k)
    #pprint.pprint(keys_content)
    return keys, keys_content

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    keys_content = defaultdict(set)
    for _, element in ET.iterparse(filename):
        keys, keys_content = key_type(element, keys, keys_content)
    pprint.pprint(keys_content)
    return keys

pprint.pprint(process_map(OSMFILE))