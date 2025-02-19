from flask import Flask, request, render_template_string
import sqlite3
import pickle

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()
    conn.close()

init_db()

# 🚨 SQL Injection Vulnerability 🚨
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # 🚨 BAD: Directly inserting user input into the SQL query
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)  
        
        user = cursor.fetchone()
        conn.close()

        if user:
            return "Login successful!"
        else:
            return "Invalid credentials."

    return '''
    <form method="post">
        Username: <input type="text" name="username">
        Password: <input type="password" name="password">
 nbn       <input type="submit">
    </form>
    '''

# 🚨 XSS Vulnerability 🚨
@app.route("/profile")
def profile():
    name = request.args.get("name", "Guest")

    # 🚨 BAD: Rendering user input directly into HTML
    template = f"<h1>Welcome, {name}!</h1>"
    
    return render_template_string(template)

# 🚨 Insecure Deserialization 🚨
@app.route("/load", methods=["POST"])
def load_data():
    data = request.form.get("data")

    # 🚨 BAD: Loading untrusted input with pickle (Remote Code Execution Risk)
    obj = pickle.loads(bytes.fromhex(data))  

    return f"Loaded object: {obj}"

if __name__ == "__main__":
    app.run(debug=True)
