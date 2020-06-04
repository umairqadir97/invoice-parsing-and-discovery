from collections import defaultdict
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from src import description_matching
from json2html import *
import json
from itertools import chain
from collections import OrderedDict


def generate_item_table(response_data, dc_filename, po_filename):
    new_response = []
    # response_data[0][list(response_data[0].keys())[0]][0]
    # for match in response_data:
    #     print(match)

    for match in response_data:
        match_keys = list(match.keys())
        delivery_challan = match[match_keys[0]]
        purchase_order = match[match_keys[1]]
        print(delivery_challan)
        print(purchase_order)
        print(len(delivery_challan))
        print(len(purchase_order))
        # header = {}
        # for k in [match_keys[0],"1", match_keys[1],"2","3", "4", "5"]:
        #     header[k] = ""
        # new_response.append(header)
        for i in range(len(delivery_challan)):
            new_response.append(OrderedDict(chain(delivery_challan[i].items(),
                                                  {"": ""}.items(),
                                                  purchase_order[i].items())))

    resp_html_page = """<div id="match-table">
    <div class="row" style="height: 2.2rem;">
      <div align="center" class="col col-md-3"><a href=\"/dc-download/{dc_name}\">Delivery challan</a></div>
      <div align="center" class="col col-md-9"><a href=\"/po-download/{po_name}\">Purchase order</a></div>  
    </div>{table}<div>""".format(
        dc_name=dc_filename,
        po_name=po_filename,
        table=json2html.convert(
            new_response,
            table_attributes="class=\"table table-bordered match-table\" id='purchase-order-table' style=\"font-size: 0.8rem;\""
        ))
    return resp_html_page


def generate_match_object(match_count, dc_filename, po_filename, items_matched, dc_text_matched):
    dc_items = []
    po_items = []

    for index in range(len(items_matched)):
        # Add DC items
        dc_items.append({"description": dc_text_matched[index], " ": ""})

        # Add PO items
        po_items.append(items_matched[index])
        # for key, value in items_matched[index].items():
        #     po_items[key].append(value)
        # print(items_matched[index])

    items = [{
        "<a href=\"/dc-download/{dc_name}\">Delivery challan</a>".format(dc_name=dc_filename): dc_items,
        "<a href=\"/po-download/{po_name}\">Purchase order</a>".format(po_name=po_filename): po_items
    }]

    print(json.dumps(items))
    obj = {
        'id': match_count,
        'delivery_challan': po_filename,
        'items_matched': generate_item_table(items, dc_filename, po_filename)
    }
    print(obj)
    return obj


def match_single_dc_with_pos(pos_data, dc_data, keywords, dc_filename, benchmark=False):
    # Given: single DC, POs master json
    # Output: matches in json object
    match_result = defaultdict(lambda: [])
    match_count = 0

    match_found = False
    text = dc_data[dc_filename]
    for po_name in pos_data.keys():
        po = pos_data[po_name]
        print(po['page'])
        for key, value in po['data'].items():
            key_variations = keywords['generic'][key]
            for key_item in key_variations:
                match_keys = process.extractBests(key_item, text, scorer=fuzz.partial_ratio)
                for match_key in match_keys:
                    if match_key[1] > 90:
                        match_index = text.index(match_key[0])  # match index for corresponding KEY
                        search_values = text[match_index - 3:match_index + 4]
                        if key in ['purchase_order'] and len(value) > 0:
                            match_value = process.extractOne(value.split('-')[1].strip(), search_values,
                                                             scorer=fuzz.token_set_ratio)
                            if match_value and match_value[1] > 80:
                                print(match_key, '|', match_value)
                                print("=" * 60)
                                print("Matched {invoice} with {dc}".format(dc=dc_filename, invoice=po['page']))
                                print("=" * 60)
                                print("Match Found.")
                                # print(value, '|',match_value)
                                match_found = True
                                match_count += 1
                                items_matched, dc_text_matched = description_matching.match_po_description_to_dc(
                                    dc_text=text,
                                    po=po,
                                    keywords=keywords,
                                    benchmark=benchmark
                                )
                                match_result[po['page']].append(
                                    generate_match_object(match_count, dc_filename, po['page'], items_matched,
                                                          dc_text_matched))
                                break
                if match_found:
                    break
            if match_found:
                break
        if match_found:
            break
    if not bool(match_result):
        match_result[dc_filename].append('NO MATCH')
    return match_result
