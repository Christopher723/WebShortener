from flask import Flask, request, jsonify, send_file, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, session
import random
import string
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
existing_db_path = 'URLS.db'

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'URLS.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

# URL Class/Model
class URLS(db.Model):
    LongUrl = db.Column(db.String(255))
    ShortUrl = db.Column(db.String(255), primary_key=True)


def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    LongUrl = request.form['longUrl']  # Use 'longUrl' to match the input name in the HTML form
    ShortUrl = generate_short_url()
    new_url = URLS(LongUrl=LongUrl, ShortUrl=ShortUrl)
    db.session.add(new_url)
    db.session.commit()
    return f'{request.host_url}{ShortUrl}'

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    url_entry = URLS.query.filter_by(ShortUrl=short_url).first()
    if url_entry:
        return redirect(url_entry.LongUrl)
    else:
        return 'URL not found', 404


@app.route('/')
def index():
    return render_template('index.html')


# Run server
if __name__ == '__main__':
    app.run(debug=True)
