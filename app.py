from flask import Flask, render_template
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scopes = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json')
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
    app.run()
