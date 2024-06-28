from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
from datetime import datetime


class Recipe:
    DB="recipes_belt"
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked_or_made=data['date_cooked_or_made']
        self.under_30_minutes=data['under_30_minutes']
        
        self.creator= None
        

    @classmethod 
    def save_recipe(cls,data):
        print('before saving recipe')
        query="INSERT INTO recipes (user_id,name,description,instructions,date_cooked_or_made,under_30_minutes) VALUES (%(user_id)s,%(name)s,%(description)s,%(instructions)s,%(selectedDate)s,%(yes_no)s);"
        result=connectToMySQL(cls.DB).query_db(query,data)
        
        return result
    
    @classmethod
    def update_recipe(cls,data):
        print('----------------------before updating recipe')
        query = """UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked_or_made=%(selectedDate)s, under_30_minutes=%(yes_no)s WHERE id=%(id)s"""
        result=connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod
    def delete_recipe(cls,recipe_id):
        query='DELETE FROM recipes WHERE id=%(recipe_id)s'
        data={
            'recipe_id':recipe_id
        }
        connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"        
        results = connectToMySQL(cls.DB).query_db(query)        
        recipes = []        
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes
    
    @classmethod
    def get_one_recipe_id(cls,recipe_id):
        query = """SELECT * FROM recipes WHERE id=%(recipe_id)s"""
        data={
            'recipe_id':recipe_id
        }
        result=connectToMySQL(cls.DB).query_db(query,data)
        
        return cls(result[0])  

    @classmethod
    def get_all_recipes_with_creator(cls):
        query='SELECT * FROM recipes JOIN users ON recipes.user_id=users.id;'
        results=connectToMySQL(cls.DB).query_db(query)
        
        all_recipes=[]
        for row in results:

            one_recipe=cls(row)

            one_recipe_author_info={
                'id':row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            author=user.User(one_recipe_author_info)

            one_recipe.creator=author

            all_recipes.append(one_recipe)
        
        return all_recipes

    @classmethod
    def get_one_recipe_with_creator(cls,recipe_id):
        query='SELECT * FROM recipes LEFT JOIN users ON recipes.user_id=users.id WHERE recipes.id=%(recipe_id)s'
        data={
            'recipe_id':recipe_id
        }
        results=connectToMySQL(cls.DB).query_db(query,data)
        recipe_object = cls(results[0])
        
        author_info={
                'id':results[0]['users.id'],
                'first_name':results[0]['first_name'],
                'last_name':results[0]['last_name'],
                'email':results[0]['email'],
                'password':results[0]['password'],
                'created_at':results[0]['users.created_at'],
                'updated_at':results[0]['users.updated_at']
            }
        author_object = user.User(author_info)
        recipe_object.creator = author_object
       
        return recipe_object

    @staticmethod
    def validate_date(date_str):
        try:
        # Attempt to parse the date string
            datetime.strptime(date_str, "%Y-%m-%d")
        # If parsing succeeds, return True
            return True
        except ValueError:
        # If parsing fails, return False
            return False

    @staticmethod
    def validate_recipe(recipe):
        is_valid=True        
        
        if len(recipe['name'])<3:
            flash('Recipe name must be at least 3 characters', "new_recipe")
            is_valid=False
        if len(recipe['description'])<3:
            flash('Description must be at least 3 characters', "new_recipe")
            is_valid=False
        if len(recipe['instructions'])<3:
            flash('Instructions must be at least 3 characters', "new_recipe")
            is_valid=False
        '''
        if recipe['date_cooked_or_made'] != "mm/dd/yyyy":
            flash('Select a Date Cooked/Made',"new_recipe")
            is_valid=False
        
        if Recipe.get('under_30_minutes') is not None:
            flash('Select if the recipe can be cooked under 30 minutes YES/NO',"new_recipe")
            is_valid=False
        '''
        

        return is_valid
  