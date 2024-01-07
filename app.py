from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify

db = SQLAlchemy()

class AccountPassword(db.Model):
    __tablename__ = 'account password'

    ID = db.Column(db.String(255), primary_key=True)
    PASSWORD = db.Column(db.String(255), nullable=False)
    UC = db.Column(db.String(255), nullable=False)
    UN = db.Column(db.String(255), nullable=False)
    FC = db.Column(db.String(20), nullable=False)



app = Flask(__name__)

# Database connection settings
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pydb'
mysql = MySQL(app)

def check_database_connection():
    with app.app_context():
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT 1")
            data = cur.fetchone()
            cur.close()
            print("Connected to the database successfully.")
        except Exception as e:
            print(f"Error connecting to the database: {str(e)}")

check_database_connection()

@app.route('/api/items/post', methods=['POST'])
def create_item():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO items (name) VALUES (%s)", [data['name']])
    mysql.connection.commit()
    return jsonify({'status': 'Item created'}), 201

@app.route('/api/items/get', methods=['GET'])
def get_items():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    items = cur.fetchall()
    return jsonify(items)

@app.route('/api/items/<int:item_id>/put', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE items SET name = %s WHERE id = %s", (data['name'], item_id))
    mysql.connection.commit()
    return jsonify({'status': 'Item updated'}), 200

@app.route('/api/items/<int:item_id>/delete', methods=['DELETE'])
def delete_item(item_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM items WHERE id = %s", [item_id])
    mysql.connection.commit()
    return jsonify({'status': 'Item deleted'}), 200

@app.route('/', methods=['GET'])
def home():
    return "Welcome to my API!"

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(KeyError)
def handle_key_error(e):
    return jsonify(error='Key not found in request data'), 400

if __name__ == '__main__':
    app.run(debug=True)