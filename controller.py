
# Integrating the python script into a webpage using flask
from flask import Flask, render_template, request, send_file
from wtforms import Form, FloatField, StringField, validators
from icsShift import main


app = Flask(__name__)

# Model
class InputForm(Form):
    r = StringField(validators= [validators.InputRequired()])
    


# View
filename = ""
app = Flask(__name__)


@app.route('/')
def upload():
    return render_template("upload.html") # a template for the user to enter the date and upload their file

#the redirect after clicking on the submit button
@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        text = request.form['text']
        f.save(f.filename)
        s = main(text, f.filename)
        return render_template("success.html", name=f.filename, s = s) # shows the user a copy-paste version of the file or a link to download the file
    

#the redirect after clicking download
@app.route('/return-files/')
def return_files_tut():
	try:
		return send_file('answers.ics', attachment_filename='modified.ics') #inbuilt flask method to send a file from the program's directory into the server
	except Exception as e:
		return str(e)
if __name__ == '__main__':
    app.run(debug=True)
