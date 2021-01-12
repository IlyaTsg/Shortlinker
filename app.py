from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pyshorteners

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
db = SQLAlchemy(app)

class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    real_link = db.Column(db.String(100), nullable=True)
    local_link = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return 'Links %r' % self.id

@app.route('/shortlinker', methods=["GET", "POST"])
def create_short_link():
    if request.method == "POST":
        try:
            real_link = request.form["real_link"]
            local_link = pyshorteners.Shortener().tinyurl.short(real_link)
            
            links = Links(real_link=real_link, local_link=local_link)
        except:
            return render_template('Error.html')
            
        try:
            db.session.add(links)
            db.session.commit()
            return render_template('GetLink.html', link=local_link)
        except:
            return render_template('Error.html')
    else:
        return render_template('PostLink.html')

if __name__ == "__main__":
    app.run(debug = True)
