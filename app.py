from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
db = SQLAlchemy(app)

class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    real_link = db.Column(db.String(100), nullable=True)
    local_link = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return 'Links %r' % self.id

def generate_local_link():
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    part_string = '/'
    uniq = True

    while uniq:
        for i in range(3):
            part_string += symbols[random.randint(0, len(symbols)-1)]
        
        local_link = "http://127.0.0.1:5000" + part_string
        rows = len(Links.query.all())
        for i in range(1, rows+1):
            uniq = False
            old_link = Links.query.get(i)
            old_local_link = old_link.local_link
            if old_local_link == local_link:
                uniq = True
                break

    return local_link

@app.route('/shortlinker', methods=["GET", "POST"])
def create_short_link():
    if request.method == "POST":
        real_link = request.form["real_link"]
        local_link = generate_local_link()
        try:
            links = Links(real_link=real_link, local_link=local_link)
            db.session.add(links)
            db.session.commit()
            return render_template('GetLink.html', link=local_link)
        except:
            return render_template('Error.html')
    else:
        return render_template('PostLink.html')

@app.route('/<string:short_link>')
def redirection(short_link):
    new_local_link = "http://127.0.0.1:5000/" + short_link
    is_correct = False
    rows = len(Links.query.all())
    for i in range(1, rows+1):
        link = Links.query.get(i)
        local_link = link.local_link

        if new_local_link == local_link:
            is_correct = True
            real_link = link.real_link
            break

    if is_correct:
        return redirect(real_link)
    else:
        return render_template('Error404.html')

if __name__ == "__main__":
    app.run(debug = True)
