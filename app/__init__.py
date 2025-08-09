from flask import Flask, jsonify,flash, render_template, request, redirect, url_for # type: ignore
import calendar
from datetime import datetime, date , time 
import shelve, module
from createModuleForm import module_form
from python_stuff.createEmergencyNumsForm import emergency_nums_form
from python_stuff.emergencyNums import EmergencyNums
from datetime import datetime, timedelta
import requests
from wtforms import StringField, DateField, TimeField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional, NumberRange
from flask import session, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.utils import secure_filename
import os, shelve, re
from dotenv import load_dotenv
import csv
from accounts.caretaker import Caretaker
from urllib.parse import quote
from flask_wtf import FlaskForm
import uuid 
from python_stuff.activity import Activity
from python_stuff.createActivityForm import activity_form
from python_stuff.medication import Medication
from python_stuff.createMedicationForm import MedicationForm
from python_stuff.seizure import Seizure
from python_stuff.createSeizureForm import SeizureForm

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








@app.route('/assignActivity', methods=['GET', 'POST'])
def assign_activity():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    assign_form = activity_form(request.form)
    if request.method == 'POST' and assign_form.validate():
        activity_dict = {}
        db = shelve.open('storage_database/storage.db', writeback=True)

        try:
            activity_dict = db['Activities']
        except:
            activity_dict = {}

        new_activity = Activity(
            assign_form.activity_name.data,
            assign_form.estimated_time.data,
            assign_form.reps.data,
            assign_form.instructions.data
        )
        activity_dict[new_activity.get_activity_id()] = new_activity
        db['Activities'] = activity_dict
        db.close()
        return redirect(url_for('activity_journal'))

    return render_template('assignActivity.html', form=assign_form)

@app.route('/activityJournal')
def activity_journal():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    activity_dict = {}
    activities = []

    try:
        db = shelve.open('storage_database/storage.db', 'r')
        activity_dict = db.get('Activities', {})
        for key in activity_dict:
            activities.append(activity_dict[key])
        db.close()
    except:
        print("No activity data found.")

    return render_template('activityJournal.html', count=len(activities), activities=activities)

@app.route('/delete_activity/<string:activity_id>', methods=['POST'])
def delete_activity(activity_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        activity_id = int(activity_id)
        db = shelve.open('storage_database/storage.db', writeback=True)
        activity_dict = db.get('Activities', {})

        if activity_id in activity_dict:
            del activity_dict[activity_id]
            db['Activities'] = activity_dict
            print(f"Deleted activity with ID: {activity_id}")
        else:
            print(f"Activity ID {activity_id} not found.")

    except Exception as e:
        print("Error deleting activity:", e)
    finally:
        db.close()

    return redirect(url_for('activity_journal'))



@app.route('/calendar')
def calendar():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    """Main calendar page"""
    return render_template('NewCalendar.html')

@app.route('/addMedication', methods=['GET', 'POST'])
def add_medication():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    

    form = MedicationForm(request.form)
    if request.method == 'POST' and form.validate():
        db = shelve.open('storage_database/storage.db', writeback=True)
        medication_dict = db.get('Medications', {})

        new_med = Medication(
            form.medication_name.data,
            form.dosage.data,
            form.start_date.data,
            form.end_date.data,
            form.time_to_take.data,
            form.frequency.data,
            form.calendar_color.data,
            form.instructions.data
        )

        medication_dict[new_med.get_medication_id()] = new_med
        db['Medications'] = medication_dict
        db.close()
        return redirect(url_for('calendar'))

    return render_template('addMedication.html', form=form)

@app.route('/addSeizure', methods=['GET', 'POST'])
def add_seizure():
    if 'user_id' not in session:
        return redirect(url_for('login'))
   

    form = SeizureForm(request.form)
    if request.method == 'POST' and form.validate():
        db = shelve.open('storage_database/storage.db', writeback=True)
        seizure_dict = db.get('Seizures', {})

        new_seizure = Seizure(
            form.date.data,
            form.time.data,
            form.seizure_type.data,
            form.duration.data,
            form.severity.data,
            form.calendar_color.data,
            form.triggers.data,
            form.notes.data
        )

        seizure_dict[new_seizure.get_seizure_id()] = new_seizure
        db['Seizures'] = seizure_dict
        db.close()
        return redirect(url_for('calendar'))

    return render_template('addSeizure.html', form=form)



@app.route('/api/events')
def get_calendar_events():
    db = shelve.open('storage_database/storage.db')
    medication_dict = db.get('Medications', {})
    seizure_dict = db.get('Seizures', {})
    db.close()

    events = []

    for med in medication_dict.values():
        events.append({
            'id': f'med_{med.get_medication_id()}',
            'title': med.get_name(),
            'start': med.get_start_date().isoformat(),
            'end': (med.get_end_date() or med.get_start_date()).isoformat(),
            'type': 'medication',
            'dosage': med.get_dosage(),
            'time_to_take': med.get_time_to_take().strftime('%H:%M') if med.get_time_to_take() else '',
            'frequency': med.get_frequency()
        })

    for sz in seizure_dict.values():
        events.append({
            'id': f'seizure_{sz.get_seizure_id()}',
            'title': 'Seizure',
            'start': sz.get_date().isoformat(),
            'type': 'seizure',
            'severity': sz.get_severity(),
            'duration': sz.get_duration(),
            'triggers': sz.get_triggers(),
            'notes': sz.get_notes()
        })

    return jsonify(events)

@app.route('/delete_medication/<id>', methods=['POST'])
def delete_medication(id):
    try:
        medication_id = int(id)
    except ValueError:
        print(f"Invalid medication ID format: {id}")
        return redirect(url_for('calendar', success=quote("Invalid medication ID")))

    db = shelve.open('storage_database/storage.db', writeback=True)
    medication_dict = db.get('Medications', {})

    if medication_id in medication_dict:
        del medication_dict[medication_id]
        db['Medications'] = medication_dict
        print(f"Deleted medication with ID: {medication_id}")
    else:
        print(f"Medication ID not found: {medication_id}")

    db.close()
    return redirect(url_for('calendar', success=quote("Medication deleted")))

@app.route('/delete_seizure/<id>', methods=['POST'])
def delete_seizure(id):
    
    try:
        seizure_id = int(id)
    except ValueError:
        print(f"Invalid seizure ID format: {id}")
        return redirect(url_for('calendar', success=quote("Invalid seizure ID")))

    db = shelve.open('storage_database/storage.db', writeback=True)
    seizure_dict = db.get('Seizures', {})

    if seizure_id in seizure_dict:
        del seizure_dict[seizure_id]
        db['Seizures'] = seizure_dict
        print(f"Deleted seizure with ID: {seizure_id}")
    else:
        print(f"Seizure ID not found: {seizure_id}")

    db.close()
    return redirect(url_for('calendar', success=quote("Seizure deleted")))

if __name__ == '__main__':
    app.run(debug=True)
