import json
import os

from config import *
from src import fuzzy_match

#
# ENDPOINT: get PO and return matches results
dc_data = {}
keywords = json.load(open(KEYWORDS_FILE, 'r'))
po_data = json.load(open(PURCHASE_ORDERS_JSON, 'r'))
for filename in os.listdir(DATA_DIRECTORY):
    if filename.endswith(".txt"):
        text = open(DATA_DIRECTORY + filename, 'r', encoding='utf-8').readlines()
        dc_data[filename] = text

match_result = fuzzy_match.match_po_with_dc(po_data=po_data,
                                            dc_data=dc_data,
                                            keywords=keywords)

with open(MATCHES_OUTPUT_FILES, "w") as output_file:
    json.dump(match_result, output_file)
