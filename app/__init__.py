from flask import Flask, render_template, request, redirect, url_for # type: ignore
import calendar
from datetime import datetime
import shelve, module
from createModuleForm import module_form
from python_stuff.createEmergencyNumsForm import emergency_nums_form
from python_stuff.emergencyNums import EmergencyNums


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


@app.route('/emergency')
def emergency():
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


if __name__ == '__main__':
    app.run(debug=True)
