from flask import Flask, request, render_template
import jwt
import datetime

app = Flask(__name__)

flag = "Securinets{JWT_1s_s0_34sy_t0_f4K3}"
secret_key = "3v1l_M0rtY_H4s_Th3_Fl4G"

@app.route('/api', methods=['POST'])
def api():
    token = request.headers.get('Authorization')
    print(f"Received token: {token}")
    if token is None:
        return "Authorization token missing", 401
    payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    if payload['isAdmin'] == 'true':
        return flag
    else:
        return "You must be an admin and your token must not have expired to access this resource", 403

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    data = request.json
    if data and 'username' in data and 'password' in data:
        if data['username'] == 'admin' and data['password'] == 'rick123':
            payload = {'isAdmin': 'false'}
            token = jwt.encode(payload, secret_key, algorithm='HS256')
            return token
    return "Invalid credentials", 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
