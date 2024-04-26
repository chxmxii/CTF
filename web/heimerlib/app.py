from flask import Flask, render_template, abort, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mystical_library.db'
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default_secret_key")
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    magic_points = db.Column(db.Integer, default=0)
    spells = db.relationship('Spell', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Spell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Spell {self.name}>'

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    spells = db.relationship('Spell', backref='library', lazy=True)

    def __repr__(self):
        return f'<Library {self.name}>'
        
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/learn_spell', methods=['POST'])
def learn_spell():
    spell_name = request.form.get('spell_name')
    user = User.query.filter_by(username=request.form.get('username')).first()
    if user and user.magic_points >= 10: # Assuming learning a spell costs 10 magic points
        spell = Spell(name=spell_name, description="A mystical incantation", user_id=user.id)
        db.session.add(spell)
        user.magic_points -= 10
        db.session.commit()
        return redirect(url_for('home'))
    else:
        abort(403)

@app.route('/cast_spell')
def cast_spell():
    spell_name = request.args.get('spell_name')
    user = User.query.filter_by(username=request.args.get('username')).first()
    if user and any(spell.name == spell_name for spell in user.spells):
        return render_template('cast_spell.html', spell_name=spell_name)
    else:
        abort(403)
        
def main() -> None:
    with app.app_context():
        db.create_all()
    app.run(debug=True)

if __name__ == '__main__':
    main()
