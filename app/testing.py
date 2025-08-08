import shelve

with shelve.open('storage_database/storage.db', writeback=True) as db:
    module_dict = db.get('Modules', {})
    print(list(module_dict.keys()))  # See what's inside
    del module_dict[1]  # Replace with real key
    db['Modules'] = module_dict
