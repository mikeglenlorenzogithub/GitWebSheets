from flask import Flask
from get_sheets import get_sheets

app = Flask(__name__)
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sc_bc_ac.json'

@app.route('/')
def home():
    sheet = get_sheets('reporting.json', 'REPORTING')
    rows = sheet.get_all_records()
    list_row = [x['Name'] + ', ' + x['Description'] for x in rows]
    return f"""
    <h3> LIST OF DATA: </h3>
    <ul>{'<br/>'.join(list_row)}</ul>
    """, 200

if __name__ == '__main__':
    app.run(debug=True)