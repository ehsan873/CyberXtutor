import csv
import io
import chardet
import openpyxl
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from openpyxl import Workbook


def convert_to_xlsx(file):
    # Load the file data into an in-memory workbook
    data = file.read()

    # Determine the file encoding
    detected_encoding = chardet.detect(data)['encoding']
    encodings_to_try = ['utf-8', 'iso-8859-1', detected_encoding]

    # Try decoding the file data using different encodings
    decoded_data = None
    for encoding in encodings_to_try:
        try:
            print(data.decode(encoding))
            decoded_data = data.decode(encoding)
            break
        except UnicodeDecodeError:
            pass

    if decoded_data is None:
        raise UnicodeDecodeError("Unable to decode file data using any of the supported encodings.")

    # Convert the decoded data to a workbook
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"
    for row in decoded_data.splitlines():
        sheet.append(row.split('\t'))

    # Save the workbook to a BytesIO object
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    return output


def csv_to_xlsx(file_content):
    # Create a new in-memory workbook
    output = io.BytesIO()
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Get the contents of the file as a string
    file_content_string = file_content.read().decode('utf-8')

    # Use the csv module to parse the file content
    csv_data = csv.reader(io.StringIO(file_content_string))

    # Write the CSV data to the worksheet
    for row in csv_data:
        sheet.append(row)

    # Save the workbook to a BytesIO object
    workbook.save(output)
    output.seek(0)
    return output


def get_file_path(csv_file):
    fs = FileSystemStorage(location='excelfile/')
    content = csv_file.read()  # these are bytes
    file_content = ContentFile(content)
    file_name = fs.save(
        "_tmp.xlsx", file_content
    )

    tmp_file = fs.path(file_name)
    return tmp_file


def get_csv_error(title,description):
    return str({'title': title, 'description':description , 'html': ''})