import pytesseract
import xlrd
from PIL import Image
from pdf2image import convert_from_path


def main(input_filepath, input_filename, output_filepath, output_filename):
    text = ''
    if input_filename.lower().endswith('.pdf'):
        # todo: check for different image resolutions
        pages = convert_from_path(input_filepath + input_filename, 500)   # each page is object of PIL
        for page in pages:
            text += str(pytesseract.image_to_string(page))
    elif input_filename[-3:].lower() in ['jpg', 'jpeg', 'png', 'bmp', 'mpeg']:
        print("IMAGE FILE: ", input_filename)
        text += str(pytesseract.image_to_string(Image.open(input_filepath + input_filename)))
    elif input_filename.lower().endswith('xlsx'):
        text += excel_to_text(input_filepath, input_filename)
    else:
        print("ERROR: Invalid File Format, filename={}".format(input_filename))
    
    #
    # Save Extracted text to output_filename
    if not text:
        print("WARNING: No Text Extected, filename={}".format(input_filename))
    else:
        with open(output_filepath + output_filename, 'w') as file:
            file.write(text)
        print("Successfully Parsed, filename={} \n".format(input_filename))


def excel_to_text(input_file, output_file):
    excel_workbook = xlrd.open_workbook(input_file)
    sheets = excel_workbook.sheets()
    text = ''
    for sheet in sheets:
        for row_idx in range(sheet.nrows):
            row = sheet.row_values(row_idx)
            text += ''.join([str(elt) for elt in row if elt]) + '\n'
    with open(output_file, "w") as out_file:
        out_file.write(text)
    return text


# if __name__=='__main__':
#     input_filepath = '/home/umair/redbuffer/fatima_group_invoices/merged DCs/'
#     output_filepath = '/home/umair/redbuffer/invoice_matching/data/delivery_challans/'
#     for _file in os.listdir(input_filepath):
#         main(input_filepath, _file, output_filepath, _file[:-3]+'txt')
