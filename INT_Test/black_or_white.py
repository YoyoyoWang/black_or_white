import os
import subprocess
from flask import Flask, render_template, request, g, flash, redirect, url_for, redirect, send_from_directory
from werkzeug import secure_filename
from os.path import exists
import sys


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['DOWNLOAD_FOLDER'] = 'downloads/'
app.config['RESULT'] = False
app.config['FILENAMES'] = None
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def about():
	return render_template('index.html')

@app.route('/transfer')
def transfer():
    return render_template('transfer.html')


@app.route('/transfer', methods=['POST'])
def upload():
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            print(filename)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    #result = exists("downloads/"+str(filenames[0])[8:-4]+"_transfer.jpg")
    app.config['FILENAMES'] = filenames
    result = app.config['RESULT']
    return render_template('transfer.html', filenames=filenames, result=False)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/action/<filename>')
def transfer_action(filename):
	print(filename)
	subprocess.check_call(["python2","forward.py","uploads/"+str(filename)])
	print("downloads/"+str(filename)[:-4]+"_transfer.jpg")
	print(app.config['RESULT'])
	app.config['RESULT'] = exists("downloads/"+str(filename)[:-4]+"_transfer.jpg")
	print(app.config['RESULT'])	
	return render_template('transfer.html', filenames=app.config['FILENAMES'], result=app.config['RESULT'], complete=str(filename)[:-4]+"_transfer.jpg")

@app.route('/downloads/<filename>')
def downloaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'],str(filename)[:-4]+"_transfer.jpg")

@app.route('/contact')
def contact():
	return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=int(sys.argv[1]))
	#app.run(host ='140.138.155.214',port=5010)
