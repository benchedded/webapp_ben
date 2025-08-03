from flask import Flask, render_template, request, redirect, url_for # type: ignore
import calendar
from datetime import datetime
import shelve, module
from createModuleForm import module_form


app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/resources')
def resources():
    return render_template('resources.html', )

@app.route('/learningModules')
def learningModules():
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

    '''

    db = shelve.open('storage_database/storage.db', 'r')  # Use 'r' for read-only access
    try:
        module_dict = db.get('Modules', {})
        assigned_modules = list(module_dict.values())
    except:
        print('Error retrieving modules')
    finally:
        db.close()

    return render_template('learningModules.html', assigned_modules=assigned_modules)
    '''


'''
def learningModules():
    return render_template('learningModules.html')
'''


'''

@app.route('/calendar')
def calendar_view():
    now = datetime.now()
    year = now.year
    month = now.month

    # Get calendar matrix for the month
    cal = calendar.Calendar(firstweekday=6)  # Sunday as first day
    month_days = cal.monthdayscalendar(year, month)

    month_name = calendar.month_name[month]

    return render_template('calendar.html', month=month_name, year=year, month_days=month_days)

'''

@app.route('/assignModule', methods = ['GET','POST'])
def assign_module():
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





if __name__ == '__main__':
    app.run(debug=True)
