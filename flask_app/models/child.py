from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, request
import re


class Child:
    db = "chore_tracker"
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.parent_id = data['parent_id']


# CREATE CHILDREN MODELS
    @classmethod
    def create_child(cls,data):
        query = ''' 
            INSERT INTO 
            children
                (first_name,last_name,email,password,completed,is_claimed,user_id,child_id)
            VALUES
                (%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(parent_id)s)
            ;'''
        child_id = connectToMySQL(cls.db).query_db(query,data)
        return child_id
    

# READ CHILDREN MODELS
    @classmethod
    def get_all_children(cls):
        query = '''
            SELECT *
            FROM children
            ;'''
        results = connectToMySQL(cls.db).query_db(query)
        return results
    

    @classmethod
    def get_child_by_id(cls,id):
        data = {'id' : id}
        query = '''
            SELECT * 
            FROM children
            WHERE id = %(id)s
            ;'''
        result = connectToMySQL(cls.db).query_db(query,data)
        return result[0]
    
    @classmethod
    def get_child_by_email(cls,email):
        data = {'email' : email}
        query = '''
            SELECT * 
            FROM children
            WHERE email = %(email)s
            ;'''
        child_email = connectToMySQL(cls.db).query_db(query, data)
        if child_email:
            return cls(child_email[0])
        return False
    
    @classmethod
    def get_chores_assigned_to_child(cls,id):
        data = {'id' : id}
        query = ''''
            SELECT * 
            FROM
            ;'''
    

# UPDATE CHILDREN MODELS
    @classmethod
    def edit_child(cls,data):
        query = ''' 
            UPDATE 
                children
            SET
                first_name = %(first_name)s,
                last_name = %(last_name)s,
                email = %(email)s, 
                email = %(password)s)
            WHERE id = %(id)s
            ;'''
        return connectToMySQL(cls.db).query_db(query, data)
    
# DELETE CHILDREN MODELS
    
    @classmethod
    def delete_child(cls,id):
        data = {'id' : id}
        query = '''
            DELETE 
            FROM children
            WHERE id = %(id)s
            ;'''
        connectToMySQL(cls.db).query_db(query, data)
        return 


    # validations
    
    @classmethod
    def validate_child_on_register(cls, data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 1:
            flash("First name is required")
            is_valid = False
        if len(data['last_name']) < 1:
            flash("Last name is required")
            is_valid = False
        if len(data['email']) < 1:
            flash("Email is required.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 charicters.")
            is_valid = False
        if len(data['confirm_password']) < 1:
            flash("Confirm Password is required.")
            is_valid = False
        if not data["password"] == data["confirm_password"]:
            flash("Your password must match confirm password.")
            is_valid = False
        if cls.get_child_by_email(data['email']):
            flash('There is already an account with that email')
            is_valid = False
        return is_valid