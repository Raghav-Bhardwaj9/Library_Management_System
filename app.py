from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy data for demonstration
users = {'admin': 'admin123', 'user': 'user123'}
membership_data = {}

# Routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return 'Invalid username/password combination'

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        if username == 'admin':
            return render_template('admin_dashboard.html')
        else:
            return render_template('user_dashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Membership related routes
@app.route('/add_membership', methods=['GET', 'POST'])
def add_membership():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        email = request.form['email']
        duration = request.form['duration']
        membership_data[email] = {'name': name, 'duration': duration}
        return redirect(url_for('dashboard'))

    return render_template('add_membership.html')

@app.route('/update_membership', methods=['GET', 'POST'])
def update_membership():
    if request.method == 'POST':
        # Handle form submission
        membership_number = request.form['membership_number']
        duration = request.form['duration']
        if membership_number in membership_data:
            membership_data[membership_number]['duration'] = duration
        return redirect(url_for('dashboard'))

    return render_template('update_membership.html')

if __name__ == '__main__':
    app.run(debug=True)
