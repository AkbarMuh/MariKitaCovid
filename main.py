# Import modul json untuk mengelola data dalam format JSON.
import json
# Import modul os agar bisa berkomunikasi dengan sistem operasi.
import os
# Import class datetime dari modul datetime untuk beroperasi dengan informasi waktu dan tanggal.
from datetime import datetime
# Import class Flask dari modul flask untuk membuat aplikasi web
from flask import Flask, request, jsonify
# Import class SimpleXMLRPCServer dari modul xmlrpc.server untuk membuat server XML-RPC
from xmlrpc.server import SimpleXMLRPCServer
# Import class Thread dari modul threading untuk melakukan pemrograman paralel
from threading import Thread
# Import modul json untuk merandom angka
import random

# Fungsi untuk membaca file NIK_Valid.txt dan memeriksa password
def read_valid_nik_and_check_password(password):
    # Ganti dengan password yang Anda inginkan
    correct_password = "password123"

    # Mengecek password
    is_password_correct = password == correct_password

    # Membaca file NIK_Valid.txt jika password benar
    if is_password_correct:
        with open("NIK_Valid.txt", "r") as file:
            valid_nik_list = [line.strip() for line in file]
        return is_password_correct, valid_nik_list
    else:
        return is_password_correct, None
    

# Fungsi untuk memeriksa validitas NIK
def is_valid_nik(nik):
    with open('NIK_Valid.txt', 'r') as file:
        content = file.readlines()
    NIK = [line.strip() for line in content]
    print(NIK)
    return nik in NIK

# Fungsi untuk memeriksa format string yang valid
def is_valid_string(s):
    # Mereturn hasil true atau false berdasarkan kondisi
    # Memeriksa apakah karakter pertama dari string 's' adalah huruf.
    return s.strip() and s[0].isalpha()

# Fungsi untuk menampilkan semua data dari file
def get_all_reports():
    with open('laporan_covid.txt', 'r') as file:
        reports = [json.loads(line) for line in file]

    return reports

# Fungsi untuk menyimpan laporan dalam file
def save_report(report):
    # Membuka file 'laporan_covid.txt' dengan mode 'a' atau append
    with open('laporan_covid.txt', 'a') as file:
        # Menggunakan json.dumps untuk mengonversi objek report menjadi string JSON
        # kemudian menuliskannya ke dalam file, diikuti dengan karakter \n untuk membuat baris baru
        file.write(json.dumps(report) + '\n')

# Fungsi untuk merespon dengan informasi penjemputan
def respond_pickup_info():
    # Mendapatkan waktu saat ini dan memformatnya
    current_time = datetime.now().strftime("%A, %d %B %Y %H:%M:%S")
    
    # Menyiapkan variasi nama tim yang kreatif
    team_names = ['Pahlawan Kesehatan', 'Guardians of Well-being', 'Covid Crusaders', 'Health Protectors']
    team_name = random.choice(team_names)
    
    # Menghasilkan jumlah orang penjemput secara acak antara 1 dan 5
    jumlah_orang_penjemput = random.randint(1, 5)
    
    # Membuat pesan sambutan yang lebih personal, positif, dan humoris
    greetings = ['Terimakasih atas dedikasinya!', 'Anda adalah pahlawan sejati!', 'Bersama kita melawan pandemi!']
    greeting = random.choice(greetings)
    
    # Menambahkan elemen kejutan dan humor
    surprises = ['Tetap semangat!', 'Ada hadiah kecil untuk Anda!', 'Kami sangat menghargai bantuan Anda.']
    surprise = random.choice(surprises)
    
    jokes = ['Kenapa virus tidak suka pergi ke pesta? Karena selalu ada penanganan cepat!', 'Apa makanan favorit virus? Byte!', 'Bagaimana virus komputer pergi ke dokter? Dengan mencari solusi antivirus!']
    joke = random.choice(jokes)
    
    # Membuat objek dictionary response
    response = {
        'waktu': current_time,
        'nama': team_name,
        'jumlah_orang_penjemput': jumlah_orang_penjemput,
        'pesan': f"{greeting} {surprise} 😄 {joke}"
    }
    
    # Mereturn objek dictionary response
    return response

# Fungsi untuk menghandle laporan dari client
def handle_report(data):
    # Menggunakan try except untuk antisipasi Error
    try:
        # Memuat data JSON yang diterima dan kemudian disimpan ke variabel report
        report = json.loads(data)
        # Simpan report dengan fungsi save_report()
        save_report(report)
        # Memanggil fungsi respond_pickup_info() untuk membuat response
        # dan menyimpannya ke dalam variabel response
        response = respond_pickup_info()
    # Block kode except untuk menangani error jika data JSON tidak valid
    except json.JSONDecodeError:
        # Membuat response jika JSON tidak valid
        response = {'message': 'Format JSON tidak valid.'}
    
    # Mereturn response sebagai string JSON
    return json.dumps(response)

# Fungsi untuk RPC - Validasi NIK
def rpc_is_valid_nik(nik):
    return is_valid_nik(nik)

# Fungsi untuk RPC - Validasi Inputan String
def rpc_is_valid_string(s):
    return is_valid_string(s)

# Fungsi untuk RPC - Mendapatkan semua data
def rpc_get_all_reports():
    return get_all_reports()

# Fungsi untuk RPC - Memeriksa password dan mendapatkan NIK valid
def rpc_check_password_and_get_valid_nik(password):
    is_password_correct, valid_nik_list = read_valid_nik_and_check_password(password)
    return is_password_correct, valid_nik_list

# Fungsi untuk menjalankan flask
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
    rpc_server.register_function(rpc_check_password_and_get_valid_nik, 'check_password_and_get_valid_nik')

    # Run the XML-RPC server
    rpc_server.serve_forever()

if __name__ == "__main__":
    # Run Flask app in a separate thread
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()

    # Run XML-RPC server in the main thread
    run_rpc_server()
