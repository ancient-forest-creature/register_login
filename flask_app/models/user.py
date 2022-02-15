from flask import flash
import re
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,20}$")

class User:
    def __init__(self , data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.birthday = data['birthday']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('log_and_reg_schema').query_db(query)
        print(results)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_user(cls, data):
        data = {'id':data}
        print(f"data is {data}")
        query = "SELECT * FROM users WHERE id = %(id)s;"
        res = connectToMySQL('log_and_reg_schema').query_db(query, data)
        print(f"res is {res}")
        if len(res) < 1:
            return False
        user = cls(res[0])
        print(user)
        return user

    @classmethod
    def get_user_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        res = connectToMySQL('log_and_reg_schema').query_db(query, data)
        print(f"res is {res}")
        if len(res) < 1:
            return False
        user = cls(res[0])
        print(user)
        return user

    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, birthday, password, created_at, updated_at ) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(birthday)s, %(password)s, NOW(), NOW());"
        print(f"Create email data is {data}")
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL('log_and_reg_schema').query_db(query, data)
        print(f"User create result is {result}")
        return result

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('log_and_reg_schema').query_db(query,data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email=%(email)s"
        res = connectToMySQL('log_and_reg_schema').query_db(query,user)
        if len(res) >= 1:
            flash("That email is taken!", "register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']):
            flash("Invaid password! Passwords must contain at least 1 uppercase charater, 1 number, and 1 special charater","register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid