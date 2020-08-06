from flask import *
from src.api_helper import *
from src.config import *
import os
import time

STATIC_DIR = os.path.abspath('./static')

app = Flask(__name__, static_folder=STATIC_DIR)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "invoice-matching-api"


@app.route('/')
def home():
    return render_template("tables.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_new_purchase_orders():
    """
    Upload Purchase Orders, duplicates will be replaced.
    request parameters:
        @po-file: purchase order file(s). allowed extensions (.pdf, .zip)
    """

    try:
        start_time = time.time()
        status_code = 200
        response_object, status_code = add_new_purchase_orders(request)
        print("\n#####   PO total upload & parse time --- %s seconds ---" % (time.time() - start_time))
        return response_object, status_code
    except Exception as exe:
        import traceback
        print(traceback.format_exc(exe))
        return jsonify({"Error": str(exe)}), 500


@app.route('/match', methods=['GET', 'POST'])
def match_dc():
    # <match delivery challan> main
    # Upload Delivery Challan
    # parameter: 'dc_file': delivery challan single PDF
    try:
        response_object, status_code = upload_dc_file(request)
        return response_object, status_code
    except Exception as exe:
        import traceback
        print(traceback.format_exc(exe))
        return jsonify({"Error": str(exe)}), 500


@app.route('/dc-download/<filename>', methods=['GET'])
def download_dc(filename):
    # Download Delivery Challan, click on results dc name

    try:
        response_object = send_file(UPLOAD_FOLDER + filename ,as_attachment=True)
        return response_object, 200
    except Exception as exe:
        import traceback
        print(traceback.format_exc(exe))
        return jsonify({"Error": str(exe)}), 500


@app.route('/po-download/<po_filename>', methods=['GET'])
def download_po(po_filename):
    # Download Purchase Order, click on results po name

    try:
        response_object = send_file(EXTRACTED_PURCHASE_ORDERS_FOLDER + po_filename, as_attachment=True)
        return response_object, 200
    except Exception as exe:
        import traceback
        print(traceback.format_exc(exe))
        return jsonify({"Error": str(exe)}), 500


@app.route('/get-existing-pos', methods=['GET', 'POST'])
def existing_pos():
    # get existing POS, stored in POs Master Json
    try:
        response_object = get_existing_pos(request)
        return response_object, 200
    except Exception as exe:
        import traceback
        print(traceback.format_exc(exe))
        return jsonify({"Error": str(exe)}), 500


if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0", port=5000)
