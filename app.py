from flask import Flask, request, redirect, render_template, url_for, abort
from flaskext.markdown import Markdown
from neomodel.exception import DoesNotExist as NodeDoesNotExist
import jinja2
import os
import models
import forms

import re
import urllib
import pprint
from bs4 import BeautifulSoup
from operator import itemgetter

app = Flask(__name__)
app.debug = True
Markdown(app)

def get_or_404(uid, class_):
    if uid == 'new':
        return class_()
    try:
        return class_.index.get(uid=uid)
    except NodeDoesNotExist:
        abort(404)

def parse_legislation(url):
    response = {}
    data_url = '%s/data.xml' % url
    data = urllib.urlopen(data_url).read()
    soup = BeautifulSoup(data)

    #title and desctiption
    response['title'] = soup.find_all('dc:title')[0].string
    response['description'] = soup.find_all('dc:description')[0].string

    #regulations
    response['regulations'] = []
    regex = re.compile('Regulations may prescribe|provide|specify|make such provision|make provision|for the purpose|for any purpose')
    regulations = soup.find_all('text', text = regex)
    for regulation in regulations:
        response['regulations'].append(regulation.string)

    #definitions
    response['definitions'] = []
    # regex = re.compile(u'([0-9a-zA-Z_])*\u201d means.*', re.UNICODE)
    # definitions = soup.find_all('text', text = regex)
    definitions = soup.find_all('term')
    for definition in definitions:
        # print definition.parent
        response['definitions'].append({'term': definition.string.capitalize(), 'definition': definition.parent.contents[2].replace(u'\u201d ', u'')})
        # print regex.match(unicode(definition.string))

    response['definitions'].sort(key=itemgetter('term'))

    return response

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/intents")
def intents():
    intents = models.Intent.category()
    return render_template('intents.html', intents=intents.instance.all())

@app.route("/intents/edit/<uid>", methods=['GET', 'POST'])
def intent_edit(uid):

    form = forms.IntentForm(request.form)
    intent = get_or_404(uid, models.Intent)

    if request.method == 'GET' and uid != 'new':
        form.title.data = intent.title
        form.description.data = intent.description
        form.measured_by.choices = []

        for measure in models.Measure.category().instance.all():
            form.measured_by.choices.append((measure.uid, measure.title))

        for measure in intent.measured_by.all()

    if request.method == 'POST' and form.validate():
        
        #save intent
        intent.title = form.title.data
        intent.description = form.description.data
        intent.save()

        for measure_uid in form.meaured_by.data:
            measure = models.Measure.index.get(uid=measure_uid)
            intent.measured_by.connect(measure)


        return redirect(url_for('intents'))

    return render_template('intent_edit.html', form=form)

@app.route("/measures")
def measures():
    measures = models.Measure.category()
    return render_template('measures.html', measures=measures.instance.all())

@app.route("/measures/edit/<uid>", methods=['GET', 'POST'])
def measure_edit(uid):

    form = forms.MeasureForm(request.form)
    measure = get_or_404(uid, models.Measure)

    if request.method == 'GET' and uid != 'new':
        form.title.data = measure.title
        form.description.data = measure.description

    if request.method == 'POST' and form.validate():
        measure.title = form.title.data
        measure.description = form.description.data
        measure.save()
        return redirect(url_for('measures'))

    return render_template('measure_edit.html', form=form, uid=uid)

@app.route("/personas")
def personas():
    return render_template('personas.html')

@app.route("/journeys")
def journeys():
    return render_template('journeys.html')

@app.route("/legislation")
def legislation():
    return render_template('legislation.html')

@app.route("/themes")
def themes():
    return render_template('themes.html')

@app.route("/timeline")
def timeline():
    return render_template('timeline.html')

@app.route("/experts")
def experts():
    return render_template('experts.html')

@app.route("/definitions")
def definitions():
    response = {}

    #url = 'http://www.legislation.gov.uk/ukpga/2012/5'
    url = 'http://localhost:8000'
    response = parse_legislation(url)

    return render_template('definitions.html', definitions=response['definitions'], menu='definitions')

@app.route("/regulations")
def regulations():
    response = {}

    #url = 'http://www.legislation.gov.uk/ukpga/2012/5'
    url = 'http://localhost:8000'
    response = parse_legislation(url)

    return render_template('regulations.html', regulations=response['regulations'], menu='regulations')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)