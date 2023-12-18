from flask import Blueprint, render_template, request
from website.static.run_scraping import run_script

views = Blueprint('views', __name__)

'''
    @login_required untuk syarat harus login dulu
'''

@views.route('/')
def home():
    return render_template("home.html", route='home_page')

@views.route('/scraping', methods=['POST', 'GET'])
def scraping():
    run_script()
    return render_template("home.html", route='home_page')