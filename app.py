from flask import Flask,render_template,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,RadioField,TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired
import pickle

from model import casual_test,build_wordlist,wordlist
app=Flask(__name__)
app.config['SECRET_KEY']='some_random_secret'

class SignUpForm(FlaskForm):
    news=StringField('Enter your News to be tested',validators=[InputRequired()])
    email=EmailField('Enter your email',validators=[InputRequired()])
    publicity=RadioField('How did you hear about us ?',choices=[('social','Social Media'),('poster','Posters and flyers')])
    feedback=TextAreaField('Anything else you want to tell us ?')
    submit=SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def hello_world():

    form = SignUpForm()
    if form.validate_on_submit():
        session['news'] = form.news.data
        session['email'] = form.email.data
        session['publicity'] = form.publicity.data
        session['feedback'] = form.feedback.data

        return redirect(url_for("thankyou"))
    return render_template('index.html',form=form)

@app.route('/thankyou')
def thankyou():
    pred = casual_test(session['news'], loaded_model, wordlist)
    return render_template('thankyou.html',pred=pred)

if __name__ == '__main__':
    app.run(debug=True)
