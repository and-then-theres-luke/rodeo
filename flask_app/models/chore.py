
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, request


class Chore:
    db = "chore_tracker"
    def __init__(self, data):
        self.title = data['title']
        self.description = data['description']
        self.location = data['location']
        self.day = data['day']
        self.completed = data['completed']
        self.is_claimed = data['is_claimed']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.child_id = data['child_id']


# CREATE CHORE MODELS
    @classmethod
    def create_chore(cls,data):
        if 'child_id' not in data:
            child_id = 0
        else:
            child_id = data['child_id']
        query_data = {'title' : data['title'],
                        'description' : data['description'],
                        'location' : data['location'],
                        'day' : data['day'],
                        'completed' : data['completed'],
                        'is_claimed' : data['is_claimed'],
                        'user_id' : data['user_id'],
                        'child_id' : child_id
                        }
        query = ''' 
            INSERT INTO 
            chores
                (title,description,location,day,completed,is_claimed,user_id,child_id)
            VALUES
                (%(title)s,%(description)s,%(location)s,%(day)s,%(completed)s,%(is_claimed)s,%(user_id)s,%(child_id)s)
            ;'''

        chore_id = connectToMySQL(cls.db).query_db(query, query_data)

        return chore_id
    

# READ CHORE MODELS
    @classmethod
    def get_all_chores(cls):
        query = '''
            SELECT *
            FROM chores
            ;'''
        results = connectToMySQL(cls.db).query_db(query)
        return results
    

    @classmethod
    def get_chores_assigned_to_child(cls, id):
        data = {"id" : id}
        query = ''' 
            SELECT *
            FROM chores
            LEFT JOIN children ON chores.child_id = child.id
            WHERE child.id = %(id)s
            ;'''
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        chores = []
        for result in results:
            chores.append(cls(result))
        return chores
    
    @classmethod
    def get_chore_by_id(cls,id):
        data = {'id' : id }
        query = '''
            SELECT * 
            FROM chores
            WHERE id = %(id)s
            ;'''
        result = connectToMySQL(cls.db).query_db(query,data)
        return result[0]
    

# UPDATE CHORE MODELS
    @classmethod
    def edit_chore(cls,data):
        query = ''' 
            UPDATE chores
            SET
                title = %(title)s,
                description = %(description)s,
                location = %(location)s,
                day = %(day)s,
                completed = %(completed)s,
                is_claimed = %(is_claimed)s,
            WHERE id = %(id)s
            ;'''
        return connectToMySQL(cls.db).query_db(query, data)
    
# DELETE CHORE MODELS
    
    @classmethod
    def delete_chore(cls,id):
        data = {'id' : id}
        query = '''
            DELETE 
            FROM chores
            WHERE id = %(id)s
            ;'''
        connectToMySQL(cls.db).query_db(query, data)
        return 

# CHORES VALIDATIONS 
    @classmethod
    def chore_validations(cls, data):
        is_valid = True
        if len(data['title']) < 1:
            is_valid = False
            flash("Title must not be empty.")
        if len(data['description']) < 1:
            is_valid = False
            flash("Description needed.")
        if len(data['location']) < 1:
            is_valid = False
            flash("Location must not be empty")
        if data['day']:
            is_valid = False
            flash("Day required")
        return is_valid
        