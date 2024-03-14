
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, request
from flask_app.models import parent, child


class Chore:
    db = "chore_tracker"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.location = data['location']
        self.day = data['day']
        self.completed = data['completed']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.parent_id = data['parent_id']
        self.child_id = data['child_id']
        self.parent = None
        self.child = None


# CREATE CHORE MODELS
    @classmethod
    def create_chore(cls,data):
        query_data = {'title' : data['title'],
                    'description' : data['description'],
                    'location' : data['location'],
                    'day' : data['day'],
                    'completed' : data['completed'],
                    'parent_id' : data['user_id'],
                    'child_id' : data['child_id']
                    }
        query = ''' 
            INSERT INTO
            chores
                (title,
                description,
                location,
                day,
                completed,
                parent_id,
                child_id)
            VALUES
                (%(title)s,
                %(description)s,
                %(location)s,
                %(day)s,
                %(completed)s,
                %(parent_id)s,
                %(child_id)s)
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
            LEFT JOIN children ON chores.child_id = children.id
            WHERE children.id = %(id)s
            ;'''
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        chores = []
        for result in results:
            chores.append(cls(result))
        return chores
    
    @classmethod
    def get_chore_by_id(cls,chore_id):
        data = {'id' : chore_id }
        query = '''
            SELECT * 
            FROM chores
            JOIN children
            ON chores.child_id = children.id
            WHERE chores.id = %(id)s
            ;'''
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        one_chore_data = {
            'id' : result[0]['id'],
            'parent_id' : result[0]['parent_id'],
            'child_id' : result[0]['child_id'],
            'title' : result[0]['title'],
            'description' : result[0]['description'],
            'location' : result[0]['location'],
            'day' : result[0]['day'],
            'completed' : result[0]['completed'],
            'created_at' : result[0]['created_at'],
            'updated_at' : result[0]['updated_at']
        }
        one_chore = cls(one_chore_data)
        one_child_data = {
            'id' : result[0]['children.id'],
            'parent_id' : result[0]['children.parent_id'],
            'first_name' : result[0]['first_name'],
            'last_name' : result[0]['last_name'],
            'email' : result[0]['email'],
            'password' : result[0]['password'],
            'created_at' : result[0]['children.created_at'],
            'updated_at' : result[0]['children.updated_at']
        }
        one_chore.child = child.Child(one_child_data)
        return one_chore
    
    @classmethod
    def get_all_chores_by_parent_id(cls,parent_id):
        data = {'id' : parent_id}
        query = '''
            SELECT * 
            FROM parents
            JOIN chores 
            ON chores.parent_id = parents.id
            WHERE parents.id = %(id)s
            ;'''
        results = connectToMySQL(cls.db).query_db(query, data)
        all_chores = []
        if not results:
            return all_chores
        for row in results:
            one_chore_data = {
                'id' : row['chores.id'],
                'parent_id' : row['parent_id'],
                'child_id' : row['child_id'],
                'title' : row['title'],
                'description' : row['description'],
                'location' : row['location'],
                'day' : row['day'],
                'completed' : row['completed'],
                'created_at' : row['chores.created_at'],
                'updated_at' : row['chores.updated_at']
                }
            one_chore = cls(one_chore_data)
            one_child = child.Child.get_child_by_id(one_chore.child_id)
            one_chore.child = one_child
            all_chores.append(one_chore)
        return all_chores

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
    
    @classmethod
    def delete_chores_by_child_id(cls, id):
        data = {
            'id' : id
        }
        query = """
        DELETE
        FROM chores
        WHERE child_id = %(id)s
        ;
        """
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
        