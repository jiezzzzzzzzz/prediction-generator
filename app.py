from flask import Flask, render_template
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)


def create_key():
    variables = {
        "type": os.getenv("SHEET_TYPE"),
        "project_id": os.getenv("SHEET_PROJECT_ID"),
        "private_key_id": os.getenv("SHEET_PRIVATE_KEY_ID"),
        "private_key": os.getenv("SHEET_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.getenv("SHEET_CLIENT_EMAIL"),
        "client_id": os.getenv("SHEET_CLIENT_ID"),
        "auth_uri": os.getenv("SHEET_AUTH_URI"),
        "token_uri": os.getenv("SHEET_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("SHEET_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("SHEET_CLIENT_X509_CERT_URL")
    }
    return variables


scopes = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(create_key(), scopes)
file = gspread.authorize(credentials)
worksheet = file.open("Spreadsheet").get_worksheet(0)

values_list = []

for value in worksheet.col_values(7):
    values_list.append(value)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/generator')
def make_prediction():
    return random.choice(values_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)