import ast
import re
import warnings

import numpy as np
from fuzzywuzzy import process, fuzz


# warnings.filterwarnings('ignore')


def get_properties(po_item_desc, categories):
    category_text = re.match(r'^(.*?):', po_item_desc)
    if category_text:
        category_text = category_text[0]
    else:
        category_text = po_item_desc
    category_names = categories.iloc[:, 0].values
    match = process.extractOne(category_text.lower().strip(), category_names, scorer=fuzz.token_set_ratio)
    index = np.where(category_names == match[0])[0][0]
    properties = categories.iloc[index, 1]
    return match[0], ast.literal_eval(properties)


def properties_found_in_desc(description_line, properties):
    for prop in properties:
        if prop.lower() in description_line.lower():
            return True
    return False


# changes: search prop:value on multi lines
# if ":" not found , no property key found, then proceed for next 3 lines
def match_po_single_item_to_dc(po_item, dc):
    # todo: Comment for Current 'match_po_single_item_to_dc' version
    #   tweak the scorer functions and thresholds
    #   with current version we are getting false results, make benchmark
    #   example case: thoroughly analyze for PO 'FPO-30030.pdf'
    item_code = po_item['Item Code']
    properties_matched = []
    dc_matched_text = ''
    for k, v in po_item['Description'].items():
        # property_value_match = fuzz.partial_token_set_ratio(k + ' ' + v, dc)
        # if property_value_match > 70:
        #     properties_matched.append({k: v})

        result = process.extractOne(k + ' ' + v, dc, scorer=fuzz.token_set_ratio)
        if result[1] > 60:
            properties_matched.append({k: v})
            dc_matched_text += "\n" + result[0]

    if len(properties_matched) >= 2:
        return True, properties_matched, dc_matched_text
    else:
        # if fuzz.token_set_ratio(item_code.lower(), dc) > 85:
        if process.extractOne(item_code.lower(), dc, scorer=fuzz.token_set_ratio)[1] > 85:
            return True, [{'item_code': item_code}], [item_code]
    return False, properties_matched, dc_matched_text


def match_po_description_to_dc(dc_text, po, keywords, benchmark=False):
    dc_text = [tl.lower().strip() for tl in dc_text if tl.strip()]
    key_variations = keywords['description_table']['description']  # key variations for 'description'

    for key_item in key_variations:
        match_key = process.extractOne(key_item.lower().strip(), dc_text, scorer=fuzz.token_set_ratio)
        items_matched, items_not_matched = [], []
        dc_text_combined = []
        if match_key[1] > 70:
            # entered 'Description' zone
            match_index = dc_text.index(match_key[0])
            for item in po['data']['product_desc']:
                match_flag, properties_matched, dc_text_matched = match_po_single_item_to_dc(item, dc_text) # [match_index + 1:])
                if match_flag:
                    item['Description'] = ' '.join(item['Description'].values())
                    items_matched.append(item)
                    dc_text_combined.append(dc_text_matched)
                else:
                    item['Description'] = ' '.join(item['Description'].values())
                    items_matched.append(item)
                    dc_text_combined.append('N/A')

        if items_matched:
            if benchmark:
                return items_matched
            return items_matched, dc_text_combined
    return [], []
