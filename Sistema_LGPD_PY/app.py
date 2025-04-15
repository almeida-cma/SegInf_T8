from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import User, DataRequest
from datetime import datetime
import uuid
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or str(uuid.uuid4())

# Middleware para registrar acessos
@app.before_request
def log_request():
    if 'user_id' in session:
        user_id = session['user_id']
        action = f"{request.method} {request.path}"
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        User.log_access(user_id, action, ip_address, user_agent)

# Rotas principais
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Verificar consentimento LGPD
        if 'lgpd_consent' not in request.form:
            flash('Você deve concordar com nossa Política de Privacidade para se registrar', 'error')
            return redirect(url_for('register'))
        
        try:
            new_user = User(username, email, password)
            user_id = new_user.save()
            
            # Registrar login
            session['user_id'] = user_id
            session['username'] = username
            flash('Registro realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        except ValueError as e:
            flash(str(e), 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user, user_id = User.get_by_username(username)  # Agora recebe ambos
        if user and user.check_password(password):
            session['user_id'] = user_id
            session['username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorretos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado com sucesso', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    return render_template('dashboard.html', username=session['username'])

# Rotas LGPD - Direitos do Titular
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/request-data', methods=['POST'])
def request_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    user_id = session['user_id']
    request_type = request.json.get('type')
    
    if request_type not in ['access', 'rectification', 'deletion', 'portability']:
        return jsonify({'error': 'Tipo de solicitação inválido'}), 400
    
    DataRequest.create_request(user_id, request_type)
    return jsonify({'success': True})

@app.route('/my-requests')
def my_requests():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    requests = DataRequest.get_user_requests(user_id)
    return render_template('my_requests.html', requests=requests)

if __name__ == '__main__':
    from database import init_db
    init_db()
    app.run(debug=True)