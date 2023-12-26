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

@views.route('/visual')
def visual():
    return render_template("visual.html", route='visual_page')

# RUN PYTHON SCRIPT IN HTML

# RUN SCRAPING PROGRAM
@views.route('/scraping-abahouse', methods=['POST', 'GET'])
def scrapingAbahouse():
    if request.method == 'POST':
        try:
            run_script('shopping_apparel_abahouse')
            # flash('The scraping process is done', category='success')
            return redirect('https://docs.google.com/spreadsheets/d/1omwmuUJqZSLIpRj3WCLOLJvzfwllTEYID0AIb5V47Jg/edit#gid=1617524685')
        except:
            flash('There is some trouble while scraping the website', category='error')
            return render_template("home.html", route='home_page')

@views.route('/scraping-adabat', methods=['POST', 'GET'])
def scrapingAdabat():
    if request.method == 'POST':
        try:
            run_script('shopping_apparel_adabat')
            # flash('The scraping process is done', category='success')
            return redirect('https://docs.google.com/spreadsheets/d/1omwmuUJqZSLIpRj3WCLOLJvzfwllTEYID0AIb5V47Jg/edit#gid=1384088225')
        except:
            flash('There is some trouble while scraping the website', category='error')
            return render_template("home.html", route='home_page')

@views.route('/scraping-adametrope', methods=['POST', 'GET'])
def scrapingAdametrope():
    if request.method == 'POST':
        try:
            run_script('shopping_apparel_adametrope')
            # flash('The scraping process is done', category='success')
            return redirect('https://docs.google.com/spreadsheets/d/1omwmuUJqZSLIpRj3WCLOLJvzfwllTEYID0AIb5V47Jg/edit#gid=647396065')
        except:
            flash('There is some trouble while scraping the website', category='error')
            return render_template("home.html", route='home_page')

@views.route('/scraping-anteprima', methods=['POST', 'GET'])
def scrapingAnteprima():
    if request.method == 'POST':
        try:
            run_script('shopping_apparel_anteprima')
            # flash('The scraping process is done', category='success')
            return redirect('https://docs.google.com/spreadsheets/d/1omwmuUJqZSLIpRj3WCLOLJvzfwllTEYID0AIb5V47Jg/edit#gid=1317092021')
        except:
            flash('There is some trouble while scraping the website', category='error')
            return render_template("home.html", route='home_page')

@views.route('/scraping-bape', methods=['POST', 'GET'])
def scrapingBape():
    if request.method == 'POST':
        try:
            run_script('shopping_apparel_bape')
            # flash('The scraping process is done', category='success')
            return redirect('https://docs.google.com/spreadsheets/d/1omwmuUJqZSLIpRj3WCLOLJvzfwllTEYID0AIb5V47Jg/edit#gid=332122413')
        except:
            flash('There is some trouble while scraping the website', category='error')
            return render_template("home.html", route='home_page')

# PUSH TO BIGQUERY
@views.route('/pushbq-abahouse', methods=['POST', 'GET'])
def pushbqAbahouse():
    if request.method == 'POST':
        try:
            push_bq('shopping_apparel_abahouse')
            flash('Append bigquery process is done', category='success')
        except:
            flash('There is some trouble while append bigquery', category='error')
    return render_template("home.html", route='home_page')

@views.route('/pushbq-adabat', methods=['POST', 'GET'])
def pushbqAdabat():
    if request.method == 'POST':
        try:
            push_bq('shopping_apparel_adabat')
            flash('Append bigquery process is done', category='success')
        except:
            flash('There is some trouble while append bigquery', category='error')
    return render_template("home.html", route='home_page')

@views.route('/pushbq-adametrope', methods=['POST', 'GET'])
def pushbqAdametrope():
    if request.method == 'POST':
        try:
            push_bq('shopping_apparel_adametrope')
            flash('Append bigquery process is done', category='success')
        except:
            flash('There is some trouble while append bigquery', category='error')
    return render_template("home.html", route='home_page')

@views.route('/pushbq-anteprima', methods=['POST', 'GET'])
def pushbqAnteprima():
    if request.method == 'POST':
        try:
            push_bq('shopping_apparel_anteprima')
            flash('Append bigquery process is done', category='success')
        except:
            flash('There is some trouble while append bigquery', category='error')
    return render_template("home.html", route='home_page')

@views.route('/pushbq-bape', methods=['POST', 'GET'])
def pushbqBape():
    if request.method == 'POST':
        try:
            push_bq('shopping_apparel_bape')
            flash('Append bigquery process is done', category='success')
        except:
            flash('There is some trouble while append bigquery', category='error')
    return render_template("home.html", route='home_page')