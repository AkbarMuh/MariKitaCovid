import json
import os
from datetime import datetime
from flask import Flask, request, jsonify
from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread

# Fungsi untuk memeriksa validitas NIK
def is_valid_nik(nik):
    return len(nik) >= 4 and nik.isdigit()

def is_valid_string(s):
    return s.strip() and s[0].isalpha()
# Fungsi untuk menampilkan semua data dari file
def get_all_reports():
    with open('laporan_covid.txt', 'r') as file:
        reports = [json.loads(line) for line in file]

    return reports

# Fungsi untuk menyimpan laporan dalam file
def save_report(report):
    with open('laporan_covid.txt', 'a') as file:
        file.write(json.dumps(report) + '\n')

# Fungsi untuk merespon dengan informasi penjemputan
def respond_pickup_info():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = {
        'waktu': current_time,
        'nama': 'Tim Penanganan Covid-19',
        'jumlah_orang_penjemput': 2
    }
    return response

# Fungsi untuk menghandle laporan dari client
def handle_report(data):
    try:
        report = json.loads(data)
        save_report(report)
        response = respond_pickup_info()
    except json.JSONDecodeError:
        response = {'message': 'Format JSON tidak valid.'}
    
    return json.dumps(response)

# Fungsi untuk RPC - Validasi NIK
def rpc_is_valid_nik(nik):
    return is_valid_nik(nik)

def rpc_is_valid_string(s):
    return is_valid_string(s)

# Fungsi untuk RPC - Mendapatkan semua data
def rpc_get_all_reports():
    return get_all_reports()

def run_flask_app():
    app = Flask(__name__)

    @app.route('/lapor', methods=['POST'])
    def lapor():
        data = request.data.decode('utf-8')
        response = handle_report(data)
        return response

    @app.route('/list', methods=['GET'])
    def list_reports():
        reports = get_all_reports()
        return jsonify(reports)

    if not os.path.exists('laporan_covid.txt'):
        open('laporan_covid.txt', 'w').close()

    # Use run_simple from Werkzeug to run the Flask app
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app, use_reloader=False, use_debugger=True)

def run_rpc_server():
    # Create an XML-RPC server
    rpc_server = SimpleXMLRPCServer(('localhost', 8000))
    
    # Register functions for RPC
    rpc_server.register_function(rpc_is_valid_nik, 'is_valid_nik')
    rpc_server.register_function(rpc_is_valid_string, 'is_valid_string')
    rpc_server.register_function(rpc_get_all_reports, 'get_all_reports')

    # Run the XML-RPC server
    rpc_server.serve_forever()

if __name__ == "__main__":
    # Run Flask app in a separate thread
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()

    # Run XML-RPC server in the main thread
    run_rpc_server()
