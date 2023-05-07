from flask_app.config.postgresqlconnection import connectToPostgreSQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    db_name = 'engine_swapper_db'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def add_user(cls, data):
        query = """
        INSERT INTO users (name, email, password)
        VALUES (%(name)s,%(email)s,%(password)s)
        ;"""
        return connectToPostgreSQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        ;"""
        results = connectToPostgreSQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            print('-----> Results', results[0])
            return cls(results[0])
        
    @classmethod
    def get_user_by_id(cls, data):
        query = """
        SELECT * FROM users
        WHERE id = %(id)s
        ;"""
        results = connectToPostgreSQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            print('-----> Results', results[0])
            return cls(results[0])
        
    @staticmethod
    def validate_signup(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            flash('Name must be 3 character or more', 'register')
            is_valid = False
        if form_data['name'].isalpha() == False and form_data['name'] != '':
            flash('Name field only accepts letters', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']):
            flash('Invalid email address', 'register')
            is_valid = False
        data = {
            'email': form_data['email']
        }
        is_user_found = User.get_user_by_email(data)
        if is_user_found != None:
            flash('Email is already taken', 'register')
            is_valid = False
        if len(form_data['password']) < 8:
            flash('Password must be 8 characters or more', 'register')
            is_valid = False
        if not form_data['password'] == form_data['confirm_password']:
            flash("Passwords don't match", 'register')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(form_data):
        if not EMAIL_REGEX.match(form_data['email']):
            flash('Invalid log in credentials', 'login')
            return False
        data = {
            'email': form_data['email']
        }
        is_user_found = User.get_user_by_email(data)
        if is_user_found == None:
            flash('Invalid log in credentials', 'login')
            return False
        if not bcrypt.check_password_hash(is_user_found.password, form_data['password']):
            flash('Invalid log in credentials', 'login')
            return False
        return is_user_found