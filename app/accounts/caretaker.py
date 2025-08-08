from .user import User

class Caretaker(User):
    

    def __init__(self, username, email, password ):
        super().__init__(username, email, password)
        
        

   

    def get_user_type(self):
        return 'Caretaker'