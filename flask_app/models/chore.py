
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
        self.child_object = None


# CREATE CHORE MODELS
    @classmethod
    def create_chore(cls,data):
        print(data, "!!!!!!!!!!!!!!!!!!!!!")
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
    def get_chore_by_id(cls,id):
        data = {'id' : id }
        query = '''
            SELECT * 
            FROM chores
            WHERE id = %(id)s
            ;'''
        result = connectToMySQL(cls.db).query_db(query,data)
        return result[0]
    
    @classmethod
    def get_all_chores_by_parent_id(cls,id):
        data = {'id' : id}
        query = '''
            SELECT * 
            FROM chores
            LEFT JOIN parents ON chores.parent_id = parents.id
            LEFT JOIN children ON chores.child_id = children.id
            WHERE parents.id = %(id)s
            ;'''
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results,"RESULTS!!!!!!!!")
        return results
        # for result in results:
        #     this_child = cls(result)
        # this_child.child_object = Chore({
        #         'id' : result['children.id'],
        #         'first_name' : result['children.first_name'],
        #         'last_name' : result['children.last_name'],
        #         'email' : result['children.email'],
        #         'password' : result['children.password'],
        #         'created_at' : result['children.created_at'],
        #         'updated_at' : result['children.updated_at'],
        #         'parent_id' : result['children.parent_id']
        # })
        # all_children = []
        # all_children.append(this_child[0])
        # print("all children", all_children)
        # print("thischild", this_child)
        # return this_child
        # for result in results:
        #     these_chores = cls(result)
        #     these_chores.parent_user = parent.Parent({
        #         'id' : result['parents.id'],
        #         'first_name' : result['first_name'],
        #         'last_name' : result['last_name'],
        #         'email' : result['email'],
        #         'password' : result['password'],
        #         'created_at' : result['parents.created_at'],
        #         'updated_at' : result['parents.updated_at']
        #     })
        #     this_parents_chores.append(these_chores)
        # return this_parents_chores

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
        