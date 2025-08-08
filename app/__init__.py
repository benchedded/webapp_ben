from flask import Flask, render_template, request, redirect, url_for # type: ignore
import calendar
from datetime import datetime
import shelve, module
from createModuleForm import module_form
from python_stuff.createEmergencyNumsForm import emergency_nums_form
from python_stuff.emergencyNums import EmergencyNums
from datetime import datetime, timedelta
import requests

from flask import session, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.utils import secure_filename
import os, shelve, re
from dotenv import load_dotenv
import csv
from accounts.caretaker import Caretaker



load_dotenv()

app = Flask(__name__)
app.secret_key = 's3cr3t_k3y_4_caretaker_app_2025'


app.permanent_session_lifetime = timedelta(days=70)


app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
)
mail = Mail(app)
s = URLSafeTimedSerializer(app.secret_key)


ALLOWED_EMAILS = [
    "mockmock582@gmail.com",
    "epicaresystem@gmail.com"
]

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('home'))

# 🔑 Login Route with Persistent Session
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with shelve.open('storage_database/users.db') as db:
            user = db.get(email)
            if user and user.get_password() == password:
                session['user_id'] = email
                session.permanent = True  # 👈 Enables 70-day session
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

# 🧾 Registration Route with Whitelist
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email format.', 'warning')
            return redirect(url_for('register'))

        if email not in ALLOWED_EMAILS:
            flash('This email is not authorized to register.', 'danger')
            return redirect(url_for('register'))

        username = email.split('@')[0]

        with shelve.open('storage_database/users.db', writeback=True) as db:
            if email in db:
                flash('Email already registered.', 'danger')
                return redirect(url_for('register'))
            new_caretaker = Caretaker(username=username, email=email,password=password)

            db[email] = new_caretaker


        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


def log_page_view(user=None):
    with open('page_views.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        user_type = 'Unknown'
        if user is not None:
            user_type = user.get_user_type()

        writer.writerow([datetime.now().isoformat(),user_type])

def get_current_user():
    user_email = session.get('email')
    if not user_email:
        return None

    with shelve.open('admin_accounts.db') as db:
        user = db.get(user_email)

    return user

@app.route('/logout')
def logout():
    '''logs out the current user'''

    session.clear()
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    email = session['user_id']
    username = email.split('@')[0]  # 👈 Extracts the part before '@'
    return render_template('home.html', username=username)


@app.route('/resources')
def resources():
    API_KEY = 'd8624abf4116ec9e5f289db52f8b5fbf'
    NEWS_URL = 'https://gnews.io/api/v4/search'
    db_path = 'storage_database/storage.db'
    articles = []
    last_fetched = None

    with shelve.open(db_path, writeback=True) as db:
        last_fetched = db.get('news_last_fetched')
        should_refresh = (
            not last_fetched or 
            datetime.now() - last_fetched > timedelta(hours=1)
        )

        if should_refresh:
            print("Fetching fresh articles...")
            params = {
                'q': 'epilepsy',
                'lang': 'en',
                'country': 'us',
                'max': 3,
                'token': API_KEY
            }

            try:
                response = requests.get(NEWS_URL, params=params)
                data = response.json()
                articles = data.get('articles', [])

                db['news_articles'] = articles
                db['news_last_fetched'] = datetime.now()
            except Exception as e:
                print("Error fetching news:", e)
                articles = db.get('news_articles', [])
        else:
            print("Using cached articles...")
            articles = db.get('news_articles', [])

    return render_template('resources.html', articles=articles, last_updated=last_fetched)




    return render_template('resources.html', )

@app.route('/learningModules')
def learningModules():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    module_dict = {}
    assigned_modules = []

    try:
        db = shelve.open('storage_database/storage.db', 'r')
    except:
        print('Doesnt exist yet')
        
    else:
        
        module_dict = db.get('Modules',{})
        print('Retrieved Modules:', module_dict)
        for key in module_dict:
            module = module_dict.get(key)
            assigned_modules.append(module)
        db.close()
    return render_template('learningModules.html', count = len(assigned_modules), assigned_modules = assigned_modules)



@app.route('/assignModule', methods = ['GET','POST'])
def assign_module():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    

    assign_module = module_form(request.form)
    if request.method == 'POST' and assign_module.validate():
        module_dict = {}
        db = shelve.open('storage_database/storage.db',writeback = True)

        try:
            module_dict = db['Modules']
        except:
            print('Error in retriving modules')
            module_dict = {}

        
        new_module = module.Module(
            assign_module.module_type.data,
            assign_module.module_num.data
        )
        module_dict[(new_module.get_module_assign_id())] = new_module
        db['Modules'] = module_dict

        db.close()
        return redirect(url_for('learningModules'))

    return render_template('assignModule.html', form = assign_module)


@app.route('/delete_module/<string:module_id>', methods=['POST'])
def delete_module(module_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        module_id = int(module_id)
        db = shelve.open('storage_database/storage.db', writeback=True)
        module_dict = db.get('Modules', {})

        if module_id in module_dict:
            del module_dict[module_id]
            db['Modules'] = module_dict
            print(f"Deleted module with ID: {module_id}")
        else:
            print(f"Module ID {module_id} not found.")

    except Exception as e:
        print("Error deleting module:", e)
    finally:
        db.close()

    return redirect(url_for('learningModules'))


@app.route('/emergency')
def emergency():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    num_dict = {}
    added_nums = []

    try:
        db = shelve.open('storage_database/storage.db', 'r')
    except:
        print('Doesnt exist yet')
        
    else:
        
        num_dict = db.get('emergencyNums',{})
        print('Retrieved nums:', num_dict)
        for key in num_dict:
            nums = num_dict.get(key)
            added_nums.append(nums)
        db.close()
    return render_template('emergency.html', count = len(added_nums), added_nums = added_nums)
    

@app.route('/addEmergencyNums', methods = ['GET','POST'])
def add_emergency_nums():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    add_num = emergency_nums_form(request.form)
    if request.method == 'POST' and add_num.validate():
        nums_dict = {}
        db = shelve.open('storage_database/storage.db',writeback = True)

        try:
            nums_dict = db['emergencyNums']
        except:
            print('Error in retriving nums')
            nums_dict = {}

        
        new_nums = EmergencyNums(
            add_num.emergency_num.data,
            add_num.contact_name.data
        )
        nums_dict[(new_nums.get_num_id())] = new_nums
        db['emergencyNums'] = nums_dict

        db.close()
        return redirect(url_for('emergency'))

    return render_template('addEmergencyNum.html', form = add_num)

@app.route('/deleteEmergencyNum/<string:num_id>', methods=['POST'])
def delete_emergency_num(num_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        num_id = int(num_id)
        db = shelve.open('storage_database/storage.db', writeback=True)
        num_dict = db.get('emergencyNums', {})

        if num_id in num_dict:
            del num_dict[num_id]
            db['emergencyNums'] = num_dict
            print(f"Deleted emergency number with ID: {num_id}")
        else:
            print(f"Emergency number ID {num_id} not found.")

    except Exception as e:
        print("Error deleting emergency number:", e)
    finally:
        db.close()

    return redirect(url_for('emergency'))

if __name__ == '__main__':
    app.run(debug=True)
