from flask import Flask, render_template, request, redirect, session  
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app.models import user, recipe
from flask import flash


@app.route('/recipe/add', methods=['POST'])            
def add_recipe():  
    if 'user_id' not in session: 
        return redirect('/logout')    
    
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    
    recipe.Recipe.save_recipe(request.form)   
    return redirect("/dashboard")



@app.route('/recipes')         
def all_recipes():   
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':session['user_id']
    }
    recipes = Recipe.get_all_recipes_with_creator()
    
    return render_template("dashboard.html",user=User.get_user_by_id(data), all_recipes=recipes)

@app.route('/recipe/create', methods=['POST'])
def create_recipe():
    data={
        "name":request.form['name'],
        "user_id":session['user_id']
    }
    Recipe.save_recipe(data)

@app.route('/recipe/view/<recipe_id>')
def view_recipe(recipe_id,):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':session['user_id']
    }
    recipes = Recipe.get_all_recipes_with_creator()
    recipe_=recipe.Recipe.get_one_recipe_id(recipe_id)
    
    recipe_posted_by=Recipe.get_one_recipe_with_creator(recipe_id)
    

    return render_template('view_recipe.html',recipe_with_author=recipe_posted_by, recipe=recipe_, all_recipes=recipes, user=User.get_user_by_id(data))

@app.route('/recipe/edit/<recipe_id>')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/logout')  
    

    recipe_=recipe.Recipe.get_one_recipe_id(recipe_id)    
    return render_template('edit_recipe.html',recipe=recipe_)

@app.route('/recipe/update/<recipe_id>', methods=['POST'])         
def update_recipe(recipe_id):  
    if 'user_id' not in session:
        return redirect('/logout')
    
    recipe_=recipe.Recipe.get_one_recipe_id(recipe_id)

    if not Recipe.validate_recipe(request.form):
        return render_template('edit_recipe.html',recipe=recipe_)
    
    recipe.Recipe.update_recipe(request.form)   
    return redirect('/recipes')

 
@app.route('/recipe/delete/<recipe_id>')         
def delete_recipe(recipe_id):  
    if 'user_id' not in session:
        return redirect('/logout')
    
    recipe.Recipe.delete_recipe(recipe_id)
    return redirect('/dashboard')  

    
    
        

    
    
