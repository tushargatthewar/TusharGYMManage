from flask import Flask, render_template, request, redirect, url_for,send_from_directory
from pymongo import MongoClient
from bson import ObjectId


app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client['flask_app']

users_collection = db['users']
membership_collection=db['membership_collection']

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = users_collection.find_one({'username': username, 'password': password})
    if user:
        return redirect(url_for('gym'))
    else:
        return 'Login failed. Please try again.'

@app.route('/gym')
def gym():
    return render_template('gym.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            return 'Username already exists! Please choose a different one.'
        else:
            new_user = {'username': username, 'password': password,'name':name,'email':email,'phone':phone}
            users_collection.insert_one(new_user)
            return redirect(url_for('index'))
    return render_template('register.html')


    

@app.route('/membership_register1', methods=['POST','GET'])
def membership_register1():
    if request.method == 'POST':
       # username = request.form['username']
        membership_type = request.form['membership-type']
        payment_screenshot = request.files['payment']
        name=request.form['name']
        phone=request.form['phone']
        address=request.form['address']
        email=request.form['email']


        payment_screenshot_path = f"uploads/{payment_screenshot.filename}"
        payment_screenshot.save(payment_screenshot_path)

        new_membership = {
           # 'username': username,
            'membership_type': membership_type,
            'payment_screenshot': payment_screenshot_path,
            'name':name,
            'phone':phone,
            'address':address,
            'email':email

        }
        membership_collection.insert_one(new_membership)

        return redirect(url_for('gym'))
    return render_template("memberform.html")

@app.route('/memberships')
def memberships():
    memberships = membership_collection.find()
    return render_template('memberships.html', memberships=memberships)

@app.route('/view_payment/<membership_id>')
def view_payment(membership_id):
    membership = membership_collection.find_one({'_id': ObjectId(membership_id)})
    return render_template('view_payment.html', membership=membership)


@app.route('/delete_membership/<membership_id>')
def delete_membership(membership_id):
    membership_collection.delete_one({'_id': ObjectId(membership_id)})
    return redirect(url_for('memberships'))


@app.route('/download_payment/<path:filename>')
def download_payment(filename):
    return send_from_directory(app.config['uploads'], filename, as_attachment=True)

@app.route('/eq')
def eq():
    return render_template("eq.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
