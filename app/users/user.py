import users.data_access as db
from web_errors import WebError
from language_strings.language_string import LanguageString
import bcrypt
import bcrypt
import cryptography_util

class User:
    def __init__(self, id, name, role, email, hashed_password):
        self.id = id
        self.name = name
        self.role = role
        self.email = email
        self.hashed_password = hashed_password

    @classmethod
    def authenticate(cls, email, password):
        user = cls.from_db_row(db.user_data_by_email(email))
        if not bcrypt.checkpw(password.encode(), user.hashed_password):
            raise WebError("password incorrect", status_code=401)
        else:
            return user
        
    @classmethod
    def authenticateWithoutLang(cls, email, password):
        user = db.user_password_by_email(email)
        a  = bytes(user[0], 'utf-8')
        decodePassword = cryptography_util.decrypt_passowrd(a)
        if str(decodePassword) != str(password):
            raise WebError("password incorrect", status_code=401)
        else:
            return True
        #if not bcrypt.checkpw(encodePassword, user[0]):
            #raise WebError("password incorrect", status_code=401)
        #else:
            #return user
     
    def getTheUser():
        user = db.all_users()
        return user

 
    @classmethod
    def from_id(cls, user_id):
        return cls.from_db_row(db.user_data_by_id(user_id))

    @classmethod
    def from_db_row(cls, db_row):
        id, name, role, email, hashed_password = db_row
        return cls(id, LanguageString.from_id(name), role, email, hashed_password.encode())

    def reset_password(self, new_password):
        db.update_password(self.id, new_password)

    def logout(self):
        db.invalidate_all_tokens(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name.to_dict(),
            'role': self.role,
            'email': self.email,
        }

    def create_token(self):
        return db.create_token(self.id)
