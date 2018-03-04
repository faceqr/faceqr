from flask import Flask, jsonify, render_template, request 
import base64

app = Flask(__name__)

index_content=""

@app.route('/')
@app.route('/index')
def index_page():
    return render_template('index.html', content=index_content)


# handle image data for registration
@app.route('/_registration_testimage', methods=['POST']) 
def registration_testimage():
    msg = "asdf"
    error=False
    errormsg = ""
    photo_data_jblob = request.form['photo']
    if (photo_data_jblob is None):
        error = True
    else:
        prefix = "data:image/png;base64,"
        if photo_data_jblob[0:len(prefix)].lower() == prefix.lower():
            photo_data = base64.b64decode(photo_data_jblob[len(prefix):])
            error = False
        else:
            error = True
            errormsg = "Unknown error; please try again"
    return jsonify(error=error,errormsg=errormsg)

# test ajax
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b) 

@app.route('/registration')
def registration_page():
    return render_template('registration.html')

@app.route('/lookup')
def lookup_page():
    return render_template('lookup.html')

if __name__ == '__main__':
  app.run()

