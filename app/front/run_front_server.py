import json

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import DataRequired

import urllib.request
import json

from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets


class ClientDataForm(FlaskForm):
    Pclass = SelectField('Ticket class', choices=[(1, "First class"), (2, "Second Class"), (3, "Third class")], default=1)
    Sex = SelectField('Sex', choices=[(0, "Male"), (1, "Female")])
    Age = IntegerField('Age', validators=[DataRequired()], widget=h5widgets.NumberInput(min=0, max=100, step=5))
    Embarked = SelectField('Port of Embarked', choices=[(1, "Southampton (UK)"), (2, "Cherbourg (France)"), (3, "Queenstown (Ireland)")])


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)

def get_prediction(Pclass, Sex, Age, Embarked):
    body = {'Pclass': Pclass, 'Sex': Sex,'Age': Age, 'Embarked': Embarked}

    myurl = "http://127.0.0.1:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    #print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['Pclass'] = request.form.get('Pclass')
        data['Sex'] = request.form.get('Sex')
        data['Age'] = request.form.get('Age')
        data['Embarked'] = request.form.get('Embarked')


        try:
            response = str(get_prediction(data['Pclass'],
                                      data['Sex'],
                                      data['Age'],
                                      data['Embarked']))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8181, debug=True)
