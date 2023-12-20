from flask import Flask
from website import create_app, read_sheets

app = create_app()
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.json'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)