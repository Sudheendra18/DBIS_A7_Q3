from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
import re
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'Meghana@685')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'user_registration')

mysql = MySQL(app)

app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

def is_valid_mobile(mobile):
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, mobile) is not None

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        mobile_number = request.form['mobile_number']
        password = request.form['password']
        
        if not is_valid_mobile(mobile_number):
            flash('Invalid mobile number format', 'error')
            return redirect(url_for('register'))
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        
        cursor = mysql.connection.cursor()
        
        try:
            cursor.execute("INSERT INTO users (user_id, mobile_number, password) VALUES (%s, %s, %s)",
                           (user_id, mobile_number, hashed_password))
            mysql.connection.commit()
            flash('Registration successful!', 'success')
        except mysql.connection.IntegrityError:
            flash('User ID already exists', 'error')
        finally:
            cursor.close()
        
        return redirect(url_for('register'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)