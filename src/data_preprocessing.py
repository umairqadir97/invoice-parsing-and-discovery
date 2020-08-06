import re

import pandas as pd
import pdfquery
import json
import os
from src.config import KEYWORDS_FILE
import time
try:
    from tabula import read_pdf
except:
    from tabula.wrapper import read_pdf


def get_coordinates_for_description(page, continuation_flag, description_start_flag):
    height = float(page.attrib['y1'])
    left = float(page.attrib['x0'])
    right = float(page.attrib['x1'])
    bottom = None
    top = None
    for x in page.iter():
        if x.text:
            if 'description' in x.text.lower().strip():
                if not top:   # in case 'description' occurs mutiple times !
                    top = height - float(x.attrib['y0']) - 10
                    # top = height - float(x.attrib['y1'])
                description_start_flag = True
            if 'Total Firm & Fixed'.lower() in x.text.lower() or 'total amount' in x.text.lower():
                bottom = height - float(x.attrib['y0'])
                continuation_flag = False
    if description_start_flag and not top:
        top = 5
    if description_start_flag and not bottom:
        bottom = height - float(page.attrib['y0'])
    return top, left, bottom, right, continuation_flag, description_start_flag


def get_text_of_p_o_no(page):
    height = float(page.attrib['y1'])
    for x in page.iter():
        if not x.text:
            continue
        if 'p.o. number' in x.text.lower().strip():
            top = height - float(x.attrib['y1'])
            bottom = top + 10
            left = float(x.attrib['x0'])
            return x.text


# header should be same, I'm not checking in this function !
def merge_dataframes(list_of_df, column_header):
    final_df = pd.DataFrame()
    for df in list_of_df:
        if type(df) is not pd.DataFrame:
            continue
        if df.empty:
            continue
        if column_header in df.iloc[0, :].values:
            df = df.iloc[1:, ]
        final_df = pd.concat([final_df, df], ignore_index=True, sort=False)
    return final_df


def get_column_header(pages, filepath):
    column_header = []
    df = None
    cont_flag, des_flag = True, False
    for page in pages:
        top, left, bottom, right, cont_flag, des_flag = get_coordinates_for_description(page, cont_flag , des_flag)
        if top is None:
            continue
        df = read_pdf(filepath, area=(top, left, bottom, right), pages=page.attrib['pageid'], lattice=True)
        if type(df[0]) is pd.DataFrame:
            df = df[0]
            df = df.dropna(axis=0, how="all")

        if type(df) is pd.DataFrame:
            if not df.empty:
                column_header = df.columns.values
                break
    return column_header


def refine_description(description):
    # todo: skip category where == 'No Noun'
    #   example case: 'FPO-30030.pdf'
    lines = description.split('\r')
    response = {'category': lines[0]}
    previous_key = 'category'
    for line in lines[1:]:
        line = re.sub(r'[^a-zA-Z0-9 :]', ' ', line).replace('  ', ' ').strip()
        if ':' in line:
            splits = [sp.strip() for sp in line.split(':')]
            if splits[0] and splits[1]:
                response[splits[0]] = splits[1]
                previous_key = splits[0]
        else:
            response[previous_key] += '\n' + line
    return response


def description_df_to_json(df, po_num):
    response = {
        "purchase_order": po_num,
        "product_desc": []
    }

    with open(KEYWORDS_FILE, 'r') as file:
        keywords = json.load(file)

    for row in df.iterrows():
        header = df.columns.values
        response['product_desc'].append({})
        key_black_list = []
        for black_key in ["amount", "quantity", "U/M", "rate"]:
            key_black_list += keywords['description_table'][black_key]
        try:
            for key in header:
                if key in key_black_list:
                    continue
                # for black_key in key_black_list:
                #     if black_key.lower() in key.lower():
                #         black_listed_key = True
                # if black_listed_key:

                # todo: test it, export black_list code to function
                clean_key = key.replace("\r"," ")
                # print(key,clean_key)
                if 'sr #' in key.lower():
                    if "total amount" in row[1][key].lower():
                        values = row[1].values
                        values = [v for v in values if type(v) is str]
                        response['total_amount'] = values

                    if len(row[1]['Sr #']) > 3:   # serial number is mostly within 3 digits. This is false info.
                        break
                    index = int(row[1]['Sr #'])
                    response['product_desc'][-1]['s_no'] = index
                elif 'description' in key.lower():
                    response['product_desc'][-1][key] = refine_description(row[1][key])
                elif 'quantity' in key.lower():
                    if len(row[1][key])>3:   # let's assume for a moment quantity is max 3 digits
                        quantity  = row[1][key].split('-')[0][:-2]
                        response['product_desc'][-1][key] = quantity
                    else:
                        response['product_desc'][-1][key] = row[1][key]
                else:
                    response['product_desc'][-1][clean_key] = row[1][key]
        except Exception as e:
            if row[1]['Sr #'] != row[1]['Sr #']:
                continue
            else:
                print(e)
    response['product_desc'] = [desc for desc in response['product_desc'] if desc]
    return response


def parse_single_purchase_order(filepath, filename):
    file = os.path.join(filepath, filename)
    po_regex = r"(\bFPO-.\d+\b)|(\bLPO-.\d+\b)"
    _list = []
    # todo: remove time scripts
    start_time = time.time()
    pdf = pdfquery.PDFQuery(file)
    print("loading file: ", file)
    pdf.load()
    print("\n#####    PDF-QUERY load time--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    pages = pdf.tree.findall('LTPage')
    column_header = get_column_header(pages, file)
    cont_flag, desc_start_flag = True, False
    po_num = ""
    for page in pages:
        po_text = get_text_of_p_o_no(page)
        if po_text:
            match = re.search(po_regex, po_text)
            if match:
                po_num = match.group(0)
        top, left, bottom, right, cont_flag, desc_start_flag = get_coordinates_for_description(page, cont_flag, desc_start_flag)
        if top is None:
            continue
        df = pd.DataFrame()
        try:
            df = read_pdf(file, area=(top, left, bottom, right), pages=page.attrib['pageid'],
                          lattice=True, pandas_options={"names": list(column_header)})

            if type(df[0]) is pd.DataFrame:
                df = df[0]
        except:
            pass

        if type(df) is pd.DataFrame:
            _list.append(df)

        if not cont_flag:
            break
    print("\n#####   TABULA time for parsing different sections --- %s seconds ---" % (time.time() - start_time))
    po_obj = {
        "page": filename,
        "data": description_df_to_json(merge_dataframes(_list, column_header), po_num)
        }

    return po_obj


# def create_po_json(file_path):
#     # todo: sanity check, bulk vs single
#     # PARSE purchase orders and convert to JSON : "po_list"
#     purchase_orders = [f for f in os.listdir(file_path) if f.endswith('.pdf')]
#     po_list = []
#     for file in purchase_orders:
#         po_list.append()
#     print("Purchase Orders Parsed . . .")
#     return po_list
