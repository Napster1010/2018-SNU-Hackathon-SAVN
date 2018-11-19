from flask import Flask, request, url_for
import os
app = Flask(__name__)

@app.route('/user/login')
def verify_user():
    user = request.args.get('userId')
    password = request.args.get('password')
    if (user == 'u101' and password == 'pass@123'):
        return 'success'

if __name__ == '__main__':
    app.run(debug = True, port = 5000)
