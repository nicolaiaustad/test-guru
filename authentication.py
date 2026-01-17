import pyotp
import qrcode
import io
import base64
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

users_db = {}

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Login</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    {% if error %}<p style="color: red;">{{ error }}</p>{% endif %}
</body>
</html>
'''

SETUP_2FA_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Setup 2FA</title></head>
<body>
    <h2>Setup Two-Factor Authentication</h2>
    <p>Scan this QR code with your authenticator app:</p>
    <img src="data:image/png;base64,{{ qr_code }}">
    <p>Or enter this secret manually: {{ secret }}</p>
    <form method="POST" action="/verify-setup">
        <input type="text" name="code" placeholder="Enter 6-digit code" required><br><br>
        <button type="submit">Verify and Enable 2FA</button>
    </form>
</body>
</html>
'''

VERIFY_2FA_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Verify 2FA</title></head>
<body>
    <h2>Two-Factor Authentication</h2>
    <form method="POST">
        <input type="text" name="code" placeholder="Enter 6-digit code" required><br><br>
        <button type="submit">Verify</button>
    </form>
    {% if error %}<p style="color: red;">{{ error }}</p>{% endif %}
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body>
    <h2>Welcome, {{ username }}!</h2>
    <p>You are logged in with 2FA enabled.</p>
    <a href="/logout">Logout</a>
</body>
</html>
'''

REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Register</title></head>
<body>
    <h2>Register</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Register</button>
    </form>
    {% if error %}<p style="color: red;">{{ error }}</p>{% endif %}
    <p>Already have an account? <a href="/login">Login</a></p>
</body>
</html>
'''

def generate_qr_code(provisioning_uri):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

@app.route('/')
def index():
    if 'username' in session and session.get('2fa_verified'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users_db:
            return render_template_string(REGISTER_TEMPLATE, error='Username already exists')

        users_db[username] = {
            'password': password,
            'totp_secret': None,
            '2fa_enabled': False
        }

        session['username'] = username
        session['2fa_verified'] = False
        return redirect(url_for('setup_2fa'))

    return render_template_string(REGISTER_TEMPLATE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users_db or users_db[username]['password'] != password:
            return render_template_string(LOGIN_TEMPLATE, error='Invalid credentials')

        session['username'] = username
        session['2fa_verified'] = False

        if users_db[username]['2fa_enabled']:
            return redirect(url_for('verify_2fa'))
        else:
            return redirect(url_for('setup_2fa'))

    return render_template_string(LOGIN_TEMPLATE)

@app.route('/setup-2fa')
def setup_2fa():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    secret = pyotp.random_base32()
    session['temp_secret'] = secret

    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(name=username, issuer_name="WebPortal")
    qr_code = generate_qr_code(provisioning_uri)

    return render_template_string(SETUP_2FA_TEMPLATE, qr_code=qr_code, secret=secret)

@app.route('/verify-setup', methods=['POST'])
def verify_setup():
    if 'username' not in session or 'temp_secret' not in session:
        return redirect(url_for('login'))

    code = request.form['code']
    secret = session['temp_secret']
    totp = pyotp.TOTP(secret)

    if totp.verify(code):
        username = session['username']
        users_db[username]['totp_secret'] = secret
        users_db[username]['2fa_enabled'] = True
        session.pop('temp_secret', None)
        session['2fa_verified'] = True
        return redirect(url_for('dashboard'))

    return redirect(url_for('setup_2fa'))

@app.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        code = request.form['code']
        username = session['username']
        secret = users_db[username]['totp_secret']
        totp = pyotp.TOTP(secret)

        if totp.verify(code):
            session['2fa_verified'] = True
            return redirect(url_for('dashboard'))

        return render_template_string(VERIFY_2FA_TEMPLATE, error='Invalid code')

    return render_template_string(VERIFY_2FA_TEMPLATE)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session or not session.get('2fa_verified'):
        return redirect(url_for('login'))

    return render_template_string(DASHBOARD_TEMPLATE, username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
