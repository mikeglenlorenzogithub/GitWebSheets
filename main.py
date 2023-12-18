from flask import Flask
from website import create_app, read_sheets

app = create_app()
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sc_bc_ac.json'

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)