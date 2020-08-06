from flask import Flask, render_template, redirect
import glob
import json
import os

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def home():
	return redirect("/viewer", code=302)


@app.route('/viewer')
def viewer_ui():
	return render_template("test.html")

@app.route('/validate')
def validate_xml():
	inputFiles = glob.glob('./xml_output_validation/*.json')
	filenames = []
	for i in inputFiles:
		name = i.replace('./xml_output_validation/', '')
		filenames.append({'id': name, 'name': name[:-5]})
	return render_template("validate.html", doc_data={'fileNames': filenames, 'currId': -1, 'fileData': [], 'docStatus': 2})

@app.route('/validate/<Id>', methods=['GET', 'POST'])
def load_document(Id):
	inputFiles = glob.glob('./xml_output_validation/*.json')
	filenames = []
	fileData = []
	docStatus = -1
	for i in inputFiles:
		name = i.replace('./xml_output_validation/', '')
		filenames.append({'id': name, 'name': name[:-5]})
		if name == Id:
			data = json.load(open(i, 'rb'))['textSegments']
			if os.path.exists('./xml_output_validation/current_values/' + name):
				currValues = json.load(open('./xml_output_validation/current_values/' + name, 'rb'))
			else:
				currValues = [2 for seg in range(0, len(data))]
				json.dump(currValues,
					open('./xml_output_validation/current_values/' + name,
						 'wb'))
			for segIdx in range(0,len(data)-1):
				fileData.append({'id': segIdx, 'text': data[segIdx]['text'], 'to_remove': currValues[segIdx]})
			docStatus = currValues[-1]
	return render_template("validate.html", doc_data = {'fileNames': filenames, 'currId': Id,  'fileData': fileData , 'docStatus': docStatus})


@app.route('/set_status/<Id>/<int:para_id>/<int:value>', methods=['GET'])
def set_para_status(Id,para_id, value):
	currValues = json.load(open('./xml_output_validation/current_values/' + Id, 'rb'))
	currValues[para_id] = value
	json.dump(currValues, open('./xml_output_validation/current_values/' + Id, 'wb'))
	return ''

@app.route('/reset_validation_values')
def reset_values():
	inputFiles = glob.glob('./xml_output_validation/*.json')
	for i in inputFiles:
		name = i.replace('./xml_output_validation/', '')
		dataLen = len(json.load(open(i, 'rb'))['textSegments'])
		currValues = [2 for seg in range(0, dataLen)]
		json.dump(currValues,open('./xml_output_validation/current_values/' + name, 'wb'))
	return "done"

@app.route('/set_all/<id>/<int:value>')
def set_all_values_of_doc(id,value):
	dataLen = len(json.load(open('./xml_output_validation/' + id, 'rb'))['textSegments'])
	currValues = [value for seg in range(0, dataLen)]
	json.dump(currValues,
			  open('./xml_output_validation/current_values/' + id, 'wb'))
	return ''

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=4000, debug=True)