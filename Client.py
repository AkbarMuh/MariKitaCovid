import streamlit as st
import xmlrpc.client
import json
import requests

# Create an XML-RPC client
rpc_client = xmlrpc.client.ServerProxy("http://localhost:8000")

# Membuat function bernama post_report dengan beberapa parameter seperti NIK pelapor
# nama pelapor, nama terduga, alamat terduga, gejala terduga
def post_report(nik_pelapor, nama_pelapor, nama_terduga, alamat_terduga, gejala):
    # Mengecek validitas NIK menggunakan RPC
    is_valid_nik = rpc_client.is_valid_nik(nik_pelapor)

    # Jika NIK valid, maka kirim laporan ke server
    if is_valid_nik:
        # URL endpoint untuk mengirim laporan
        url = "http://localhost:5000/lapor"
        # data laporan yang akan dikirim dalam format json
        data = {
            "nik_pelapor": nik_pelapor,
            "nama_pelapor": nama_pelapor,
            "nama_terduga": nama_terduga,
            "alamat_terduga": alamat_terduga,
            "gejala": gejala
        }
        # menentukan type konten yang akan dikirim menjadi application/json pada headers
        headers = {'Content-Type': 'application/json'}

        try:
            # mengirim POST requests dengan data JSON ke dalam server
            response = requests.post(url, data=json.dumps(data), headers=headers)
            # ngereturn response dari server ke dalam format JSON
            return response.json()
        except requests.exceptions.RequestException as e:
            # ngereturn pesan error jika terjadi sebuah kesalahan pada requests
            return {"message": f"Error: {e}"}
    else:
        return {"message": "NIK tidak valid."}
    
def get_all_reports():
    # Membuat RPC call untuk mendapatkan semua data
    return rpc_client.get_all_reports()

def main():
    # set title dihalaman web
    st.title("Laporan COVID-19")

    # menggunakan input teks untuk mengambil informasi dari user
    nik_pelapor = st.text_input("NIK Pelapor:")
    nama_pelapor = st.text_input("Nama Pelapor:")
    nama_terduga = st.text_input("Nama Terduga COVID-19:")
    alamat_terduga = st.text_input("Alamat Terduga COVID-19:")
    gejala = st.text_input("Gejala yang Dirasakan:")

    # menampilkan tombol kirim laporan
    if st.button("Kirim Laporan"):
        #  melakukan pengecekan apakah ada field yang kosong
        if not all([nik_pelapor, nama_pelapor, nama_terduga, alamat_terduga, gejala]):
            st.error("Harap isi semua informasi.")
        #  melakukan pengecekan apakah ada awalan spasi, titik, atau simbol pada inputan
        elif not all(rpc_client.is_valid_string(value) for value in [nama_pelapor, nama_terduga, alamat_terduga, gejala]):
            st.error("Input tidak valid. Harap hindari awalan spasi, titik, atau simbol pada inputan.")
        else:
            #  mengirim laporan menggunakan function post_report 
            response = post_report(nik_pelapor, nama_pelapor, nama_terduga, alamat_terduga, gejala)
            
            # menampilkan pesan berhasil bersamaan dengan respon dari server
            st.success(f"Laporan terkirim! Respon dari server: {response}")
    
    if st.button("Tampilkan Semua Data"):
        reports = get_all_reports()
        st.table(reports)

if __name__ == "__main__":
    # running main function
    main()
