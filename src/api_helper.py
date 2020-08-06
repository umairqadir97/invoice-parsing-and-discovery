import json
import os
import re
import time
from json2html import *
import traceback
from zipfile import ZipFile
import pandas as pd
from flask import flash, redirect, jsonify, Response, render_template
from werkzeug.utils import secure_filename
from src.config import *
from src import data_preprocessing, fuzzy_match
from src import process
# from src.tesseract_process import excel_to_text

DC_FILENAME = ""   # we need to access it globally !


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_existing_pos(request):
    pos_data = json.load(open(PURCHASE_ORDERS_JSON, "r"))
    return json.dumps(list(pos_data.keys()))


def upload_dc_file(request):
    global DC_FILENAME
    if os.listdir(UPLOAD_FOLDER):  # clear previous DCs
        os.popen('rm {}*'.format(UPLOAD_FOLDER))

    if request.method == 'POST':
        if 'dc_file' not in request.files:
            flash('No DC file part')
            print("No DC File")
            return redirect('/')
        file = request.files['dc_file']

        if file.filename == '':
            flash('No selected file')
            print("No Selected File")
            return redirect('/')

        if file and allowed_file(file.filename, {'pdf', 'jpg', 'tif', 'bmp'}):
            # DC should be in pdf / image format
            DC_FILENAME = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, DC_FILENAME))
            match_result, status_code = get_matches_for_dc(dc_filepath=UPLOAD_FOLDER, dc_filename=DC_FILENAME)
            return jsonify(match_result), status_code
        else:
            return jsonify({"Error": "Invalid File Extension/ Empty File"}), 400


def get_matches_for_dc(dc_filepath, dc_filename, benchmark=False):
    dc_data = {}
    keywords = json.load(open(KEYWORDS_FILE, 'r'))
    filename_without_extension = ".".join(dc_filename.split(".")[:-1])

    try:
        start_time = time.time()
        status, server_message = process.main(dc_filepath + dc_filename, dc_filepath + filename_without_extension+'.txt')
        print("\n#####    ABBY processing time --- %s seconds ---" % (time.time() - start_time))
    except Exception as e:
        return {"Error": "Unable to process document with OCR"}, 503

    start_time = time.time()
    if not status:
        return {"Error": server_message}, 503

    dc_text = open(dc_filepath + filename_without_extension + '.txt', 'r', encoding='utf-8').readlines()
    dc_data[dc_filename] = dc_text
    pos_data = json.load(open(PURCHASE_ORDERS_JSON, "r"))

    # todo: update benchmark scripts
    # if benchmark:
    #     match_result = fuzzy_match.match_single_po_with_dc(
    #                                                     po=po_obj,
    #                                                     dc_data=dc_data,
    #                                                     keywords=keywords,
    #                                                     benchmark=True)
    #     return po_obj, match_result

    match_result = fuzzy_match.match_single_dc_with_pos(
                                                        pos_data=pos_data,
                                                        dc_data=dc_data,
                                                        keywords=keywords,
                                                        dc_filename=dc_filename)
    match_result_string = json.dumps(match_result).replace('\\n', ' ').replace('\\r', ' ')
    print("\n#####    Items Matching Time--- %s seconds ---" % (time.time() - start_time))
    return json.loads(match_result_string), 200


def add_new_purchase_orders(request):
    # delete all upoaded that are not in master file
    if os.listdir(EXTRACTED_PURCHASE_ORDERS_FOLDER):
        os.popen('rm {}*'.format(EXTRACTED_PURCHASE_ORDERS_FOLDER))
    po_file = ""

    if request.method == 'POST':
        if 'po_file' not in request.files:
            print('No file part')
            return redirect('/')
        file = request.files['po_file']
        if file.filename == '':
            print('No selected file')
            return redirect('/')
        try:
            # create empty json, if 'PURCHASE ORDERS MASTER JSON' does not exists already
            if not os.path.isfile(PURCHASE_ORDERS_JSON):
                with open(PURCHASE_ORDERS_JSON, "w") as output_file:
                    json.dump({}, output_file)
            po_data = json.load(open(PURCHASE_ORDERS_JSON, 'r'))

            if file and allowed_file(file.filename, {'zip', 'pdf'}):
                if file.filename.endswith('zip'):
                    file.save(os.path.join(UPLOAD_FOLDER, "new_purchase_orders.zip"))
                    with ZipFile(UPLOAD_FOLDER + 'new_purchase_orders.zip', 'r') as zipObj:
                        zipObj.extractall(EXTRACTED_PURCHASE_ORDERS_FOLDER)
                    for po_file in os.listdir(EXTRACTED_PURCHASE_ORDERS_FOLDER):
                        if po_file.endswith('.pdf'):
                            print(po_file)
                            if po_file in po_data.keys():
                                continue
                            # last update: Overwrite POs every Time
                            po_obj = data_preprocessing.parse_single_purchase_order(
                                filepath=EXTRACTED_PURCHASE_ORDERS_FOLDER,
                                filename=po_file)
                            po_data[po_file] = po_obj

                    # Remove Uploaded .zip after extraction
                    os.remove(UPLOAD_FOLDER + 'new_purchase_orders.zip')
                elif file.filename.endswith('pdf'):
                    # if file.filename not in po_data.keys():
                    # last update: Overwrite POs every Time

                    po_filename = secure_filename(file.filename)
                    file.save(os.path.join(EXTRACTED_PURCHASE_ORDERS_FOLDER, po_filename))
                    po_data[file.filename] = data_preprocessing.parse_single_purchase_order(
                                                                            filepath=EXTRACTED_PURCHASE_ORDERS_FOLDER,
                                                                            filename=po_filename)

                #
                # write new data to POs MASTER JSON file !'
                with open(PURCHASE_ORDERS_JSON, "w") as output_file:
                    json.dump(po_data, output_file)
                return jsonify({"message": "Uploaded Purchase Orders Successfully"}), 200
            else:
                return jsonify({"Error": "Invalid File Extension"}), 400
        except Exception as e:
            traceback.print_exc()
            print(f"ERROR FOR FILE: {po_file}")
            return jsonify({"Error": "Invalid File/ Empty File"}), 400


#
# Benchmark for all Purchase Orders provided & all Delivery Challans in ./data/delivery_challans folder
def benchmark_for_all_pos(input_directory, output_directory, write_to_file=True):
    po_files = [file for file in os.listdir(input_directory) if file.endswith('.pdf')]
    final_matches = {}
    po_objects = {}
    for purchase_order in po_files:
        po_obj, match_result = get_matches_for_po(os.path.join(input_directory + purchase_order), benchmark=True)
        final_matches.update(match_result)   # add match result dict to final matches
        po_objects[purchase_order] = json.loads(json.dumps(po_obj).replace('\\n', ' ').replace('\\r', ' '))["data"]

    if write_to_file:
        #
        # write final_matches to "updated_matches.json"
        print("\n\nFINAL MATCHES:", final_matches)
        with open(os.path.join(output_directory + MATCHES_OUTPUT_FILES), "w") as output_file:
            json.dump(final_matches, output_file)

        #
        # write po_objects to "updated_purchase_orders.json"
        with open(os.path.join(output_directory + PURCHASE_ORDERS_JSON), 'w') as output_file:
            json.dump(po_objects, output_file)
    extract_benchmark_stats(MATCHES_OUTPUT_FILES, PURCHASE_ORDERS_JSON, output_directory)
    return final_matches


def extract_benchmark_stats(final_matches_file, parsed_pos_file, output_directory):
    # will generate two files:
    # 1) Purchase Orders ==> matched Delivery Challans
    # 2) Detailed matches with (PO, matched DC, Items_Matched)
    with open(os.path.join(output_directory + final_matches_file), 'r') as file:
        final_matches = json.load(file)

    with open(os.path.join(output_directory + parsed_pos_file), 'r') as file:
        pos_json = json.load(file)

    dc_summary_df = pd.DataFrame(columns=["purchase_order", "PO#", "items_in_PO", "dc_matched", "items_matched_with_dc"])
    items_summary_df = pd.DataFrame(columns=["PO", "Item_Code", "Item_Name", "DC_File", "DC_Match", "Item_Match"])

    for po in pos_json.keys():
        po_items = set([item["s_no"] for item in pos_json[po]["product_desc"]])  # let's assume item serial==item index
        if final_matches[po] != ['NO MATCH']:
            for dc in final_matches[po]:
                ##########################
                # Prepare First DataFrame
                ##########################
                row = {"purchase_order": po,
                       "PO#": pos_json[po]['purchase_order'],
                       "items_in_PO": len(pos_json[po]['product_desc']),
                       "dc_matched": dc['delivery_challan'],
                       "items_matched_with_dc": len(dc['items_matched']) if dc['items_matched'] else 0}
                dc_summary_df = dc_summary_df.append(row, ignore_index=True)

                ###########################
                # Prepare Second DataFrame
                # - append items matched in items_summary_df
                ###########################
                items_summary_row = None
                if dc["items_matched"]:
                    matched_item_serials = set([item["s_no"] for item in dc["items_matched"]])
                    po_items = po_items - matched_item_serials

                    for item in pos_json[po]["product_desc"]:
                        if item["s_no"] in matched_item_serials:
                            items_summary_row = {
                                "PO": po,
                                "Item_Code": item["Item Code"],
                                "Item_Name": item["Description"]["category"],
                                "DC_File": dc["delivery_challan"],
                                "DC_Match": 1,
                                "Item_Match": 1
                            }
                            items_summary_df = items_summary_df.append(items_summary_row, ignore_index=True)

                # else:
                #     items_summary_row = {
                #                 "PO": po,
                #                 "Item_Code": "None",
                #                 "Item_Name": "None",
                #                 "DC_File": dc["delivery_challan"],
                #                 "DC_Match": 1,
                #                 "Item_Match": 0
                #             }
                #     items_summary_df = items_summary_df.append(items_summary_row, ignore_index=True)
        else:
            row = {"purchase_order": po,
                   "PO#": pos_json[po]['purchase_order'],
                   "items_in_PO": len(pos_json[po]['product_desc']),
                   "dc_matched": None,
                   "items_matched_with_dc": None
                   }
            dc_summary_df = dc_summary_df.append(row, ignore_index=True)

        # append items not matched
        if po_items:
            for item in pos_json[po]["product_desc"]:
                items_summary_df = items_summary_df.append({
                        "PO": po,
                        "Item_Code": item["Item Code"],
                        "Item_Name": item["Description"]["category"],
                        "DC_File": "None",
                        "DC_Match": 0,
                        "Item_Match": 0
                    }, ignore_index=True)

    dc_summary_df.to_csv(os.path.join(output_directory + "PO_DC_mappings_summary.csv"), index=False)
    items_summary_df.to_csv(os.path.join(output_directory + "PO_DC_mappings_detailed.csv"), index=False)
