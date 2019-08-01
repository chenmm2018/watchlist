from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import request, url_for, redirect, flash

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'dev'
@app.context_processor
def inject_user():
    user=User.query.get(3)
    return dict(user=user)

# ...
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        title=request.form.get('title')
        year=request.form.get('year')
        if not title or not year or len(year)>4 or len(title)>60:
            flash('Invalid input.')
            return redirect(url_for('index'))
        movie=Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash("Item create.")
        return redirect(url_for('index'))
    user =User.query.get(3)
    movies=Movie.query.all()
    return render_template('index.html',user=user, movies=movies)

# ...
@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
def edit(movie_id):
    movie=Movie.query.get_or_404(movie_id)
    if request.method=='POST':
        title=request.form['title']
        year=request.form['year']
        
        if not title or not year or len(year)>4 or len(title)>60:
            flash('Invalid input.')
            return redirect(url_for('edit',movie_id=movie_id))
            
        movie.title=title
        movie.year=year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))
    
    return render_template('edit.html', movie=movie)

@app.route('/movie/delete/<int:movie_id>',methods=['POST'])
def delete(movie_id):
    movie=Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))
    
@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e): # 接受异常对象作为参数
    return render_template('404.html'), 404 # 返回模板和状态码
    
db=SQLAlchemy(app)
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    
class Movie(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(20))
    year=db.Column(db.String(4))
   
   
import click
@app.cli.command() 
def forge():
    db.create_all()
    name = 'chenmiaomiao'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user=User(name=name)
    db.session.add(user)
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')

