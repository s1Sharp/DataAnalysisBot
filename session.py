
class Session:
    def __init__(self,users_db_link):
        self.all_users_id=[]
        self.uses_db = users_db_link
    
    def check_reg_id(self,user_id):
        if user_id in self.all_users_id:
            return True
        else:
            return False

    def addUserId(self,user_id):
        print("added "+ str(user_id))
        self.all_users_id.append(user_id)

    def save_session(self):
        f = open('last_session.txt','w')
        for curr_user in self.all_users_id:
            f.write(str(curr_user) + " ")
        f.write("\n")
        f.close()


class user:
    def __init__(self,name, surname, grop,
                                classes = [] # classes = []
                                user_id,):
        self.name    = name
        self.surname = surname
        self.grop    = grop 
        self.classes = classes
        self.user_id = user_id
    
    def check_reg_id(self,session):
        if user_id in self.all_users_id:
            return True
        else:
            return False

