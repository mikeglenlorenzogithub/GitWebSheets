from flask import Blueprint, render_template, request, flash, redirect
import time
import werkzeug.exceptions as ex
from website.static.run_scraping import run_script
from website.static.push_bq import push_bq

views = Blueprint('views', __name__)

'''
    @login_required untuk syarat harus login dulu
'''

@views.route('/')
def home():
    return render_template("home.html", route='home_page')

# RUN PYTHON SCRIPT IN HTML
@views.route('/scraping-abahouse', methods=['POST', 'GET'])
def scrapingAbahouse():
    if request.method == 'POST':
        try:
            run_script('shopping_apparel_abahouse')
            flash('The scraping process is done', category='success')
        except:
            flash('There is some trouble while scraping the website', category='error')
    return render_template("home.html", route='home_page')

@views.route('/scraping-adabat', methods=['POST', 'GET'])
def scrapingAdabat():
    if request.method == 'POST':
        try:
            run_script('shopping_apparel_adabat')
            flash('The scraping process is done', category='success')
        except:
            flash('There is some trouble while scraping the website', category='error')
    return render_template("home.html", route='home_page')

@views.route('/scraping-adametrope', methods=['POST', 'GET'])
def scrapingAdametrope():
    if request.method == 'POST':
        try:
            run_script('shopping_apparel_adametrope')
            flash('The scraping process is done', category='success')
        except:
            flash('There is some trouble while scraping the website', category='error')
    return render_template("home.html", route='home_page')

@views.route('/scraping-anteprima', methods=['POST', 'GET'])
def scrapingAnteprima():
    if request.method == 'POST':
        try:
            run_script('shopping_apparel_anteprima')
            flash('The scraping process is done', category='success')
        except:
            flash('There is some trouble while scraping the website', category='error')
    return render_template("home.html", route='home_page')

@views.route('/scraping-bape', methods=['POST', 'GET'])
def scrapingBape():
    if request.method == 'POST':
        try:
            run_script('shopping_apparel_bape')
            flash('The scraping process is done', category='success')
        except:
            flash('There is some trouble while scraping the website', category='error')
    return render_template("home.html", route='home_page')

# PUSH TO BIGQUERY
@views.route('/pushbq-abahouse', methods=['POST', 'GET'])
def pushbqAbahouse():
    if request.method == 'POST':
        try:
            push_bq('shopping_apparel_bape')
            flash('Append bigquery process is done', category='success')
        except:
            flash('There is some trouble while append bigquery', category='error')
    return render_template("home.html", route='home_page')