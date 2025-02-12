from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200))
   

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    todo_list =Todo.query.all()
   
    return render_template('base.html',todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    #add new item
    with app.app_context():
        title=request.form.get("title")
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #delete 
    with app.app_context():
        todo =Todo.query.filter_by(id=todo_id).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("index"))

@app.route("/deleteall")
def delete_all():
    with app.app_context():
        db.session.query(Todo).delete()  
        db.session.commit()
    return redirect(url_for("index"))

if __name__=="__main__":
    app.run(debug=False,host='0.0.0.0')
