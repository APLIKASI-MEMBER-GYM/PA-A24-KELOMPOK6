import json
import pwinput
from prettytable import PrettyTable
import datetime

akun_member_admin = "data_member_admin.json"
saldo_member = "saldo_member.json"
data_produk = "pricelist_produk.json"

#========================= MENU UTAMA ==============================
def menu_utama():
    print("\n《--- APLIKASI GYM AZELA ---》")
    print("1. Sign Up")
    print("2. Login")
    print("3. Keluar")
    opsi = input("\nSilahkan Pilih Menu (nomor): ")
    if opsi == "1":
        sign_up()
    elif opsi == "2":
        login()
    elif opsi == "3":
        keluar1()
    else:
        print("\nTidak Valid! Pilihan harus berupa angka/menu yang tersedia.")
        menu_utama()

def keluar1():
    kembali = input("\nApakah Anda ingin keluar dari Aplikasi Gym AZELA? (ya/tidak): ").lower()
    if kembali == "ya":
        print("\n≪•◦ Terima Kasih Telah Berkunjung ◦•≫")
    elif kembali == "tidak":
        menu_utama()
    else:
        print("\n== Input tidak valid. Silahkan input ya/tidak ==")
        keluar1()


#========================== SIGN UP ================================
def sign_up():
    print("\n=== Sign Up New Member ===")

    while True:
        username = input("Masukkan Username Anda: ").strip()
        if username:
            break
        print("Username tidak boleh kosong. Silakan masukkan username Anda.")

    while True:
        pw = pwinput.pwinput("Masukkan Password Anda: ").strip()
        if pw:
            break
        print("Password tidak boleh kosong. Silakan masukkan password Anda.")

    while True:
        no_hp = input("Masukkan No HP Anda: ").strip()
        if no_hp.isdigit():
            break
        else:
            print("No HP harus berupa angka. Silakan masukkan no HP Anda.")

    while True:
        try:
            TB = float(input("Tinggi badan (cm): "))
            BB = float(input("Berat badan (kg): "))
            break  
        except ValueError:
            print("Tinggi dan berat badan Anda harus berupa angka. Silakan coba lagi.")

    while True:
        JK = input("Jenis Kelamin Anda (L/P): ").lower().strip()
        if JK in ['l', 'p']:
            break
        else:
            print("Input tidak valid. Silakan pilih 'L' atau 'P'.")

    print("︵‿︵‿୨♡୧‿︵‿︵︵‿︵‿୨♡୧‿︵‿︵")

    try:
        with open(akun_member_admin, "r") as file:
            data_member = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        data_member = []

    for user in data_member:
        if isinstance(user, dict):  
            if user.get("username") == username or user.get("phone") == no_hp:
                print("\nAkun sudah ada. Silahkan login atau gunakan nomor lain.")
                menu_utama()  
                return

    data = {
        "username": username,
        "password": pw,
        "phone": no_hp,
        "tinggi badan": TB,
        "berat badan": BB,
        "jenis kelamin": JK,
        "role": "member"
    }
    data_member["member_admin"].append(data)

    with open(akun_member_admin, "w") as file:
        json.dump(data_member, file, indent=4)

    try:
        with open(saldo_member, "r") as file:
            data_saldo = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data_saldo = {"member gym": []}

    saldo_baru = {
        "username": username,
        "saldo": 0
    }
    data_saldo["member gym"].append(saldo_baru)

    with open(saldo_member, "w") as file:
        json.dump(data_saldo, file, indent=4)

    print("\nRegistrasi BERHASIL. Sekarang Anda merupakan member di GYM AZELA.")
    keluar2()

def keluar2():
    kembali = input("Apakah Anda ingin keluar dari Aplikasi Gym AZELA? (ya/tidak): ").lower()
    if kembali == "ya":
        print("\n≪•◦ Terima Kasih Telah Berkunjung ◦•≫")
    elif kembali == "tidak":
        menu_utama()
    else:
        print("\nInput tidak valid. Silahkan input ya/tidak")
        keluar2()


# =============================== LOGIN ====================================
def login():
    while True:
        username = input("\nMasukkan Username Anda: ").strip()
        if username:
            break
        else:
            print("Username tidak boleh kosong. Silakan masukkan username Anda.")
    while True:
        pw = pwinput.pwinput("Masukkan Password Anda: ").strip()
        if pw:
            break
        else:
            print("Password tidak boleh kosong. Silakan masukkan password Anda.")
    
    try:
        with open(akun_member_admin, "r") as file:
            data_akun = json.load(file)
            
            if "member_admin" not in data_akun or not isinstance(data_akun["member_admin"], list):
                print("Data akun tidak valid.")
                return menu_utama()
            
            for user in data_akun["member_admin"]:
                if user.get("username") == username and user.get("password") == pw:
                    if user.get("role") == "admin":
                        menu_admin()
                    elif user.get("role") == "member":
                        menu_member(username)
                    else:
                        print("Role tidak dikenali.")
                    return
            print("\nUsername atau password Anda salah. Silahkan coba lagi")
            login()

    except (json.JSONDecodeError, FileNotFoundError):
        print("Data akun tidak ditemukan.")
        login()


#================================== MENU ADMIN =============================
def menu_admin() :
    try :
        print("\n===== MENU ADMIN =====")
        print("1. Buat pricelist dan produk")
        print("2. Tampilkan pricelist dan produk")
        print("3. Update pricelist dan produk")
        print("4. Hapus pricelist, produk dan member")
        print("5. Keluar")
        opsi = input("\nSilahkan pilih menu (nomor): ")
        if opsi == '1' :
            create_produk()
        elif opsi == '2' :
            read_produk()
        elif opsi == '3' :
            update_produk()
        elif opsi == '4' :
            delete_produk_member()
        elif opsi == "5":
            keluar3()
        else:
            print("\nPilihan Anda tidak valid. Silakan coba lagi.")
            menu_admin()

    except (json.JSONDecodeError, FileNotFoundError):
        print("Data akun tidak ditemukan.")
        menu_admin()

def keluar3():
    kembali = input("Apakah Anda ingin keluar dari Aplikasi Gym AZELA? (ya/tidak): ").lower()
    if kembali == "ya":
        print("\n≪•◦ Terima Kasih Telah Berkunjung ◦•≫")
    elif kembali == "tidak":
        menu_admin()
    else:
        print("\nInput tidak valid. Silahkan input ya/tidak")
        keluar3()


#=================================== MENU MEMBER =====================================
def menu_member(username):
    try:
        print("\n===== MENU MEMBER =====")
        print("1. Pricelist dan Produk")
        print("2. Isi saldo")
        print("3. Cek saldo")
        print("4. Keluar")
        opsi = input("\nSilahkan pilih menu (nomor): ")
        if opsi == "1":
            pricelist_produk(username)
        elif opsi == "2":
            isi_saldo(username)
        elif opsi == "3":
            cek_saldo(username)
        elif opsi == "4":
            keluar4(username)
        else:
            print("\nPilihan Anda tidak valid. Silakan coba lagi.")
            menu_member(username)
            
    except (json.JSONDecodeError, FileNotFoundError):
        print("Data akun tidak ditemukan.")
        menu_member(username)

def keluar4(username):
    kembali = input("Apakah Anda ingin keluar dari Aplikasi Gym AZELA? (ya/tidak): ").lower()
    if kembali == "ya":
        print("\n≪•◦ Terima Kasih Telah Berkunjung ◦•≫")
    elif kembali == "tidak":
        menu_member(username)
    else:
        print("\nInput tidak valid. Silahkan input ya/tidak")
        keluar4(username)


#===================================== CREATE ===================================
def create_produk():
    print("\n=== Tambah Pricelist dan Jangka Waktu ===")
    jangka_waktu = input("Jangka Waktu: ")       

    while True:
        try:
            harga = int(input("Harga: "))
            if harga < 0:
                print("harga harus lebih dari 0!")
                menu_admin()
            break
        except ValueError:
            print("Harga harus berupa angka. Silakan coba lagi.")

    try:
        with open(data_produk, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"pricelist_produk": []}

    nomor_urut = len(data["pricelist_produk"]) + 1
    item_baru = {
        "nomor": nomor_urut,
        "jangka waktu": jangka_waktu,
        "harga": harga
    }

    data["pricelist_produk"].append(item_baru)

    with open(data_produk, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Data berhasil ditambahkan.")
    tampilkan_tabel_pricelist(data)
    keluar5()

def keluar5():
    kembali = input("Apakah Anda ingin keluar dari Aplikasi Gym AZELA? (ya/tidak): ").lower()
    if kembali == "ya":
        print("\n≪•◦ Terima Kasih Telah Berkunjung ◦•≫")
    elif kembali == "tidak":
        menu_admin()
    else:
        print("\nInput tidak valid. Silahkan input ya/tidak")
        keluar5()

def tampilkan_tabel_pricelist(data):
    table = PrettyTable()
    table.field_names = ["Nomor", "Jangka Waktu", "Harga"]
    for item in data["pricelist_produk"]:
        table.add_row([item["nomor"], item["jangka waktu"], item["harga"]])

    print("\n=== Pricelist Produk ===")
    print(table)


#================================ READ =========================================
def read_produk():
    with open(data_produk, "r") as file:
        data = json.load(file)["pricelist_produk"]

    table = PrettyTable(["Nomor", "Jangka Waktu", "Harga"])
    for item in data:
        table.add_row([item["nomor"], item["jangka waktu"], item["harga"]])

    print("\n=== Daftar Pricelist dan Produk ===")
    print(table)
    keluar6()

def keluar6():
    kembali = input("Apakah Anda ingin keluar dari Aplikasi Gym AZELA? (ya/tidak): ").lower()
    if kembali == "ya":
        print("\n≪•◦ Terima Kasih Telah Berkunjung ◦•≫")
    elif kembali == "tidak":
        menu_admin()
    else:
        print("\nInput tidak valid. Silahkan input ya/tidak")
        keluar6()


#=============================== UPDATE =======================================
def update_produk():
    print("\n=== Update Pricelist dan Produk ===")
    try:
        with open(data_produk, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Gagal memuat data pricelist produk.")
        return

    pricelist = data.get("pricelist_produk", [])

    if not pricelist:
        print("Tidak ada data produk yang tersedia untuk diperbarui.")
        return

    table = PrettyTable()
    table.field_names = ["Nomor", "Jangka Waktu", "Harga"]
    for item in pricelist:
        table.add_row([item["nomor"], item["jangka waktu"], item["harga"]])
    print(table)
    try:
        nomor_pilihan = int(input("Masukkan nomor produk yang ingin di-update: "))
        produk_dipilih = next((item for item in pricelist if item["nomor"] == nomor_pilihan), None)
        if not produk_dipilih:
            print("Nomor produk tidak ditemukan.")
            return
    except ValueError:
        print("Input tidak valid, harus berupa angka.")
        update_produk()
    print("\nPilih bagian yang ingin di-update:")
    print("1. Jangka Waktu")
    print("2. Harga")
    pilihan = input("Masukkan pilihan (1/2): ")

    if pilihan == "1":
        jangka_waktu_baru = input("Masukkan jangka waktu baru: ")
        produk_dipilih["jangka waktu"] = jangka_waktu_baru
        print("Jangka Waktu berhasil diperbarui.")
    elif pilihan == "2":
        try:
            harga_baru = int(input("Masukkan harga baru: "))
            if harga_baru < 0:
                print("harga harus lebih dari 0!")
                menu_admin()
            produk_dipilih["harga"] = harga_baru
            print("Harga berhasil diperbarui.")
        except ValueError:
            print("Harga harus berupa angka.")
            return
    else:
        print("Pilihan tidak valid.")
        update_produk()
    with open(data_produk, "w") as file:
        json.dump(data, file, indent=4)

    print("\nData berhasil diperbarui.")
    keluar7()

def keluar7():
    kembali = input("Apakah Anda ingin keluar dari Aplikasi Gym AZELA? (ya/tidak): ").lower()
    if kembali == "ya":
        print("\n≪•◦ Terima Kasih Telah Berkunjung ◦•≫")
    elif kembali == "tidak":
        menu_admin()
    else:
        print("\nInput tidak valid. Silahkan input ya/tidak")
        keluar7()


#=================================== DELETE ============================================
def delete_produk_member():
    print("\n=== Hapus Pricelist dan Produk ===")
    try:
        with open(data_produk, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Gagal memuat data pricelist produk.")
        return

    pricelist = data.get("pricelist_produk", [])

    if not pricelist:
        print("Tidak ada data produk yang tersedia untuk dihapus.")
        return
    print("\n=== Daftar Pricelist Produk ===")
    table = PrettyTable()
    table.field_names = ["Nomor", "Jangka Waktu", "Harga"]

    for item in pricelist:
        table.add_row([item["nomor"], item["jangka waktu"], f"Rp{item['harga']}"])

    print(table)

    try:
        nomor_pilihan = int(input("Masukkan nomor produk yang ingin dihapus: "))
        produk_dipilih = next((item for item in pricelist if item["nomor"] == nomor_pilihan), None)
        if not produk_dipilih:
            print("Nomor produk tidak ditemukan.")
            menu_admin()
    except ValueError:
        print("Input tidak valid, harus berupa angka.")
        delete_produk_member()

    pricelist.remove(produk_dipilih)

    for i, item in enumerate(pricelist, 1):
        item['nomor'] = i
    try:
        with open(data_produk, "w") as file:
            json.dump(data, file, indent=4)
        print(f"\nProduk dengan nomor {nomor_pilihan} berhasil dihapus.")
    except (FileNotFoundError, json.JSONDecodeError):
        print("Gagal menyimpan data setelah penghapusan.")

    table.clear_rows()

    for item in pricelist:
        table.add_row([item["nomor"], item["jangka waktu"], f"Rp{item['harga']}"])

    print(table)
    keluar8()

def keluar8():
    kembali = input("Apakah Anda ingin keluar dari Aplikasi Gym AZELA? (ya/tidak): ")
    if kembali == "ya":
        print("\n≪•◦ Terima Kasih Telah Berkunjung ◦•≫")
    elif kembali == "tidak":
        menu_admin()
    else:
        print("\nInput tidak valid. Silahkan input ya/tidak")
        keluar8()


#===============================  PRICELIST PRODUK ================================
def pricelist_produk(username):
    try:
        with open("pricelist_produk.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Gagal memuat data menu.")
        return

    pricelist = data.get("pricelist_produk", [])

    print("\n=== Pricelist dan Produk Gym ===")
    if pricelist:
        table = PrettyTable()
        table.field_names = ["Nomor", "Jangka Waktu", "Harga"]
        for item in pricelist:
            table.add_row([item["nomor"], item["jangka waktu"], item["harga"]])
        print(table)
    else:
        print("Pricelist dan produk tidak tersedia.")
        return
    
    while True:
        print("\nApakah Anda ingin:")
        print("1. Membeli produk")
        print("2. Kembali ke menu member")
        pilihan = input("Pilih opsi (1/2): ")

        if pilihan == "1":
            try:
                pilihan = int(input("\nSilahkan pilih produk yang ingin Anda beli (nomor): "))
                if 1 <= pilihan <= len(pricelist):
                    produk_dipilih = pricelist[pilihan - 1]
                    break  
                else:
                    print("Pilihan tidak valid.")
            except ValueError:
                print("Pilihan tidak valid.")
                continue 
        elif pilihan == "2":
            menu_member(username)  
            return
        else:
            print("Pilihan tidak valid.")
    
    try:
        with open(saldo_member, "r") as file:
            data_saldo = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Gagal memuat data saldo member.")
        return

    member = next((m for m in data_saldo.get("member gym", []) if m["username"] == username), None)

    if member and member.get("saldo", 0) >= produk_dipilih["harga"]:
        member["saldo"] -= produk_dipilih["harga"]
        with open(saldo_member, "w") as file:
            json.dump(data_saldo, file, indent=4)
        buat_invoice(username, produk_dipilih) 
    else:
        print("\nSaldo Anda tidak mencukupi. Silahkan Isi saldo terlebih dahulu")
        menu_member(username) 


#================================ INVOICE PEMBELIAN =============================
def buat_invoice(username, produk_dipilih):
    try:
        with open(saldo_member, "r") as file:
            data_saldo = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Gagal memuat data saldo member")
        return

    member = next((m for m in data_saldo.get("member gym", []) if m["username"] == username), None)

    if not member:
        print("Username tidak ditemukan")
        return

    saldo_sekarang = member.get("saldo", 0)
    waktu_transaksi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("╔════════════════════════════════════════════╗")
    print("║              INVOICE PEMBELIAN             ║")
    print("╠════════════════════════════════════════════╣")
    print(f" Username     : {username} ")
    print(f" Tanggal/Waktu: {waktu_transaksi}")
    print("╠════════════════════════════════════════════╣")
    print(f" Produk       : {produk_dipilih['jangka waktu']}")
    print(f" Harga        : Rp{produk_dipilih['harga']}")
    print(f" Saldo Awal   : Rp{saldo_sekarang + produk_dipilih['harga']}")  
    print(f" Saldo Akhir  : Rp{saldo_sekarang}")
    print("╚════════════════════════════════════════════╝")

    print("\nPembayaran berhasil dilakukan! Terima kasih atas transaksi Anda.")
    keluar9(username)

def keluar9(username):
    kembali = input("Apakah Anda ingin keluar dari Aplikasi Gym AZELA? (ya/tidak): ").lower()
    if kembali == "ya":
        print("\n≪•◦ Terima Kasih Telah Berkunjung ◦•≫")
    elif kembali == "tidak":
        menu_member(username)
    else:
        print("\nInput tidak valid. Silahkan input ya/tidak")
        keluar9(username)


#======================================= CEK SALDO ====================================
def cek_saldo(username):
    try:
        with open(saldo_member, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Gagal memuat data saldo member.")
        return

    member = next((member for member in data.get("member gym", []) if member["username"] == username), None)
    print("\n=== Saldo Anda ===")
    if member:
        saldo = member.get("saldo", 0)
        
        table = PrettyTable()
        table.field_names = ["Username", "Nominal Saldo"]
        table.add_row([username, f"Rp{saldo}"])
        
        print(table)
        keluar10(username)
    else:
        print("Username tidak ditemukan.")

def keluar10(username):
    kembali = input("Apakah Anda ingin keluar dari Aplikasi Gym AZELA? (ya/tidak): ").lower()
    if kembali == "ya":
        print("\n≪•◦ Terima Kasih Telah Berkunjung ◦•≫")
    elif kembali == "tidak":
        menu_member(username)
    else:
        print("\nInput tidak valid. Silahkan input ya/tidak")
        keluar10(username)


#========================================== ISI SALDO =================================
def isi_saldo(username):
    try:
        print(f"\n=== Isi Saldo ===")
        nominal = float(input("Masukkan nominal saldo yang ingin Anda isi (contoh: 100000): "))
        if nominal < 50000:
            print("\nPengisian saldo GAGAL. Minimal pengisian saldo adalah Rp50.000.")
            return isi_saldo(username)
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        return isi_saldo(username)

    try:
        with open(saldo_member, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Gagal memuat data saldo member.")
        return

    akun_ditemukan = False
    for member in data.get("member gym", []):
        if member["username"] == username:
            akun_ditemukan = True
            saldo_saat_ini = float(member.get("saldo", 0))
            member["saldo"] = saldo_saat_ini + nominal

            waktu_transaksi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("╔════════════════════════════════════════════╗")
            print("║         INVOICE PENGISIAN SALDO            ║")
            print("╠════════════════════════════════════════════╣")
            print(f"║ Username     : {username:<28}║")
            print(f"║ Tanggal/Waktu: {waktu_transaksi:<22}      ║")
            print(f"║ Nominal      : Rp{nominal:<20,.2f}      ║")
            print(f"║ Saldo Akhir  : Rp{member['saldo']:<20,.2f}      ║")
            print("╚════════════════════════════════════════════╝")

            try:
                with open(saldo_member, "w") as file:
                    json.dump(data, file, indent=4)
                keluar11(username)
            except IOError:
                print("Gagal memperbarui file saldo member.")
            return
    if not akun_ditemukan:
        print("Username tidak ditemukan.")

def keluar11(username):
    kembali = input("Apakah Anda ingin keluar dari Aplikasi Gym AZELA? (ya/tidak): ").lower()
    if kembali == "ya":
        print("\n≪•◦ Terima Kasih Telah Berkunjung ◦•≫")
    elif kembali == "tidak":
        menu_member(username)
    else:
        print("\nInput tidak valid. Silahkan input ya/tidak")
        keluar11(username)


if __name__ == "__main__":
    menu_utama()