from flask import Flask,render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Regexp
from flask_moment import Moment
from datetime import datetime
import uuid


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email address?', validators=[DataRequired()])
    submit = SubmitField('Submit')
app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # First, we check if the info entered by user is 
        # differ from the previous saved one.
        old_name = session.get('name')
        old_email = session.get('email')
        # If not, we issue the warning messages. 
        if old_name and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email and old_email != form.email.data:
            flash('Looks like you have changed your email!')

        # Now we validate if the email provided is a UofT 
        # email address.
        # NOTE: This validation is NOT accurate, but it is 
        # enough to meet the requirement(i.e. 'utoronto' is 
        # a substring of the email). 
        if 'utoronto' in form.email.data:
            session['email'] = form.email.data
        else:
            # If we got an invalid email, we lable it and 
            # later we can ask for a UofT email.
            session['email'] = 'INVALID'
        
        # User can update their name unconditionally.
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', 
                            name=session.get('name'), 
                            form=form,
                            email=session.get('email'))

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)