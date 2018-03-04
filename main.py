from flask import Flask, jsonify, render_template, request 
import base64

app = Flask(__name__)

index_content=""

@app.route('/')
@app.route('/index')
def index_page():
    return render_template('index.html', content=index_content)


# test if an image is valid for registration
@app.route('/_registration_testimage', methods=['POST']) 
def registration_testimage():
    error=False
    errormsg = ""
    photo_data_jblob = request.form['photo']
    if (photo_data_jblob is None):
        error = True
        errormsg = "Unknown error; please try again"
    else:
        prefix = "data:image/png;base64,"
        if photo_data_jblob[0:len(prefix)].lower() == prefix.lower():
            photo_data = base64.b64decode(photo_data_jblob[len(prefix):])
            # TODO: see if this face pic is ok!
            error = False
        else:
            error = True
            errormsg = "Unknown error; please try again"
    return jsonify(error=error,errormsg=errormsg)

# register a face
@app.route('/_registration_registerface', methods=['POST']) 
def registration_registerface():
    error=False
    errormsg = ""
    photo_data_jblob = request.form['photo']
    qr_url = request.form['qrurl']
    if (photo_data_jblob is None):
        error = True
    else:
        prefix = "data:image/png;base64,"
        if photo_data_jblob[0:len(prefix)].lower() == prefix.lower():
            photo_data = base64.b64decode(photo_data_jblob[len(prefix):])
            if (qr_url is None) or (len(qr_url)==0):
                error = True
                errormsg = "Please enter a url."
            else:
                error = False
                # TODO: register the image
        else:
            error = True
            errormsg = "Unknown error; please try again"
    return jsonify(error=error,errormsg=errormsg)

@app.route('/registration')
def registration_page():
    return render_template('registration.html')

@app.route('/lookup')
def lookup_page():
    return render_template('lookup.html')

if __name__ == '__main__':
  app.run()
