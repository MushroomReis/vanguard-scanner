import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import socket
import threading
from queue import Queue
import subprocess
import re
from datetime import datetime
import requests
import platform
import sys

class VanguardScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vanguard Scanner - Kapsamlı Siber Güvenlik Kalkanı v5.0")
        self.root.geometry("900x650")
        self.root.configure(bg="#0c0c0c")
        
        self.root.withdraw()
        self.yasal_uyari_goster()

        top_frame = tk.Frame(root, bg="#0c0c0c")
        top_frame.pack(pady=15)

        # 1. SATIR: Ağ Tarama İşlemleri
        tk.Label(top_frame, text="Hedef IP:", fg="#00ff00", bg="#0c0c0c", font=("Consolas", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ip_entry = tk.Entry(top_frame, font=("Consolas", 10), bg="#1a1a1a", fg="#00ff00", insertbackground="white", width=18)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ip_entry.insert(0, "127.0.0.1")

        self.start_btn = tk.Button(top_frame, text="PORT TARAMA", bg="#004d00", fg="#00ff00", font=("Consolas", 9, "bold"), command=self.start_scan_thread, width=16)
        self.start_btn.grid(row=0, column=2, padx=5, pady=5)

        self.discover_btn = tk.Button(top_frame, text="CİHAZLARI BUL", bg="#00004d", fg="#00ffff", font=("Consolas", 9, "bold"), command=self.start_discovery_thread, width=16)
        self.discover_btn.grid(row=0, column=3, padx=5, pady=5)

        self.ids_btn = tk.Button(top_frame, text="AĞ GÜVENLİĞİ (IDS)", bg="#4d0000", fg="#ff4d4d", font=("Consolas", 9, "bold"), command=self.start_ids_thread, width=20)
        self.ids_btn.grid(row=0, column=4, padx=5, pady=5)

        # 2. SATIR: Kimlik ve Gizlilik Modülleri
        tk.Label(top_frame, text="Hedef E-Posta:", fg="#00ffff", bg="#0c0c0c", font=("Consolas", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.email_entry = tk.Entry(top_frame, font=("Consolas", 10), bg="#1a1a1a", fg="#00ffff", insertbackground="white", width=18)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        self.darkweb_btn = tk.Button(top_frame, text="DARK WEB TARAMA", bg="#330033", fg="#ff00ff", font=("Consolas", 9, "bold"), command=self.start_darkweb_thread, width=16)
        self.darkweb_btn.grid(row=1, column=2, padx=5, pady=5)

        self.ipleak_btn = tk.Button(top_frame, text="IP SIZINTI TESTİ", bg="#333300", fg="#ffff00", font=("Consolas", 9, "bold"), command=self.start_ipleak_thread, width=16)
        self.ipleak_btn.grid(row=1, column=3, padx=5, pady=5)

        self.modem_btn = tk.Button(top_frame, text="MODEM ANALİZİ", bg="#003333", fg="#00ffff", font=("Consolas", 9, "bold"), command=self.start_modem_thread, width=20)
        self.modem_btn.grid(row=1, column=4, padx=5, pady=5)

        # 3. SATIR: API ve Kaydetme
        tk.Label(top_frame, text="Vulners API Key:", fg="#00ff00", bg="#0c0c0c", font=("Consolas", 10)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.api_entry = tk.Entry(top_frame, font=("Consolas", 10), bg="#1a1a1a", fg="#00ff00", insertbackground="white", width=38, show="*")
        self.api_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        self.save_btn = tk.Button(top_frame, text="SONUÇLARI KAYDET", bg="#1a1a1a", fg="#ffffff", font=("Consolas", 9, "bold"), command=self.sonuclari_kaydet, width=20)
        self.save_btn.grid(row=2, column=4, padx=5, pady=5)

        # LOG ALANI
        self.log_area = scrolledtext.ScrolledText(root, width=105, height=22, bg="#000000", fg="#00ff00", font=("Consolas", 10))
        self.log_area.pack(padx=15, pady=10)
        
        acilis_mesaji = (
            "Vanguard Scanner v5.0 - Mega Sürüm Başlatıldı...\n"
            " [1] Ağdaki cihazları, açık portları ve hackerları (IDS) analiz edebilirsiniz.\n"
            " [2] Yeni modüllerle Dark Web e-posta ihlallerini, IP gizliliğinizi ve Modem şifrelemenizi test edebilirsiniz.\n"
            + "-"*85 + "\n"
        )
        self.log_yaz(acilis_mesaji)

    def yasal_uyari_goster(self):
        self.uyari_penceresi = tk.Toplevel()
        self.uyari_penceresi.title("⚠️ Yasal Uyarı ve Sorumluluk Reddi")
        self.uyari_penceresi.geometry("550x300")
        self.uyari_penceresi.configure(bg="#0c0c0c")
        self.uyari_penceresi.resizable(False, False)
        self.uyari_penceresi.protocol("WM_DELETE_WINDOW", self.reddet)

        metin = (
            "VANGUARD SCANNER - SORUMLULUK REDDİ\n\n"
            "Bu yazılım yalnızca eğitim, savunma amaçlı analizler ve sahibinden \n"
            "açık izin alınmış sistemler üzerinde kullanılmak üzere geliştirilmiştir.\n\n"
            "İzinsiz ağlara bağlanmak, tarama yapmak veya zafiyet aramak \n"
            "Türk Ceza Kanunu (TCK Madde 243-244) kapsamında bilişim suçudur.\n\n"
            "Bu aracı kullanarak, doğabilecek her türlü hukuki ve cezai \n"
            "sorumluluğun tamamen size ait olduğunu kabul etmiş olursunuz."
        )
        
        tk.Label(self.uyari_penceresi, text=metin, fg="#00ff00", bg="#0c0c0c", font=("Consolas", 10), justify="center").pack(pady=30)
        btn_frame = tk.Frame(self.uyari_penceresi, bg="#0c0c0c")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="KABUL EDİYORUM", bg="#004d00", fg="#00ff00", font=("Consolas", 10, "bold"), command=self.kabul_et).pack(side="left", padx=15)
        tk.Button(btn_frame, text="REDDEDİYORUM", bg="#4d0000", fg="#ff0000", font=("Consolas", 10, "bold"), command=self.reddet).pack(side="right", padx=15)

    def kabul_et(self):
        self.uyari_penceresi.destroy()
        self.root.deiconify()

    def reddet(self):
        self.root.destroy()
        sys.exit()

    def log_yaz(self, mesaj):
        self.log_area.insert(tk.END, mesaj + "\n")
        self.log_area.see(tk.END)

    def sonuclari_kaydet(self):
        dosya_yolu = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Metin Dosyası", "*.txt")], title="Sonuçları Kaydet")
        if dosya_yolu:
            with open(dosya_yolu, "w", encoding="utf-8") as dosya:
                dosya.write(self.log_area.get("1.0", tk.END))
            messagebox.showinfo("Başarılı", f"Sonuçlar kaydedildi:\n{dosya_yolu}")

    # --- 1. DARK WEB VERİ İHLALİ (XposedOrNot API) ---
    def start_darkweb_thread(self):
        threading.Thread(target=self.darkweb_tara, daemon=True).start()

    def darkweb_tara(self):
        email = self.email_entry.get().strip()
        if not email:
            self.log_yaz("[-] HATA: Dark Web araması için lütfen 'Hedef E-Posta' kısmını doldurun.")
            return
            
        self.log_yaz("-" * 85)
        self.log_yaz(f"[*] Dark Web Veri İhlali Taranıyor: {email}...")
        try:
            req = requests.get(f"https://api.xposedornot.com/v1/check-email/{email}", timeout=6)
            if req.status_code == 200:
                data = req.json()
                breaches = data.get("breaches", [[]])[0]
                self.log_yaz(f"[🚨 KRİTİK İHLAL] Bu e-posta {len(breaches)} farklı veritabanı sızıntısında bulundu!")
                self.log_yaz(f" ↳ Sızan Platformlar: {', '.join(breaches)}")
                self.log_yaz(" ↳ TAVSİYE: Bu platformlarda kullandığınız şifreleri acilen değiştirin.")
            elif req.status_code == 404:
                self.log_yaz("[✅] GÜVENLİ: Bu e-posta adresi bilinen hiçbir veri ihlalinde bulunamadı.")
            else:
                self.log_yaz("[-] API yanıt vermedi veya çok fazla istek atıldı. Daha sonra tekrar deneyin.")
        except Exception as e:
            self.log_yaz(f"[-] Dark Web bağlantı hatası: {e}")
        self.log_yaz("-" * 85 + "\n")

    # --- 2. IP SIZINTI VE ANONİMLİK TESTİ (Güncellendi) ---
    def start_ipleak_thread(self):
        threading.Thread(target=self.ipleak_tara, daemon=True).start()

    def ipleak_tara(self):
        self.log_yaz("-" * 85)
        self.log_yaz("[*] Dış Ağ (IP Sızıntı) ve Anonimlik Testi Başlıyor...")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
            req = requests.get("https://ipapi.co/json/", headers=headers, timeout=5)
            
            if req.status_code == 200:
                data = req.json()
                ip = data.get("ip", "Bilinmiyor")
                sehir = data.get("city", "Bilinmiyor")
                ulke = data.get("country_name", "Bilinmiyor")
                isp = data.get("org", "Bilinmiyor")
                
                self.log_yaz(f" ↳ Dışa Yansıyan IP Adresiniz: {ip}")
                self.log_yaz(f" ↳ Tespit Edilen Konum: {sehir}, {ulke}")
                self.log_yaz(f" ↳ Servis Sağlayıcı (ISP): {isp}")
                
                if "vpn" in isp.lower() or "hosting" in isp.lower() or "cloud" in isp.lower():
                    self.log_yaz("[✅] GİZLİLİK AKTİF: Trafiğinizin maskelendiği (VPN/Proxy) tespit edildi.")
                else:
                    self.log_yaz("[⚠️] AÇIKTASINIZ: Bağlantınız doğrudan modeme bağlı. Gerçek konumunuz izlenebilir.")
            else:
                self.log_yaz(f"[-] API Engeli (Hata Kodu: {req.status_code}): Servis geçici olarak yanıt vermiyor.")
        except Exception as e:
            self.log_yaz(f"[-] IP servisine ulaşılamadı: {e}")
        self.log_yaz("-" * 85 + "\n")

    # --- 3. MODEM ŞİFRELEME ANALİZİ ---
    def start_modem_thread(self):
        threading.Thread(target=self.modem_analizi_yap, daemon=True).start()

    def modem_analizi_yap(self):
        self.log_yaz("-" * 85)
        self.log_yaz("[*] Modem Şifreleme ve Ağ Güvenliği Analizi Başlıyor...")
        if platform.system() == "Windows":
            try:
                output = subprocess.getoutput("netsh wlan show interfaces")
                if "Authentication" in output or "Kimlik doğrulaması" in output:
                    lines = output.split('\n')
                    auth, cipher = "Bilinmiyor", "Bilinmiyor"
                    for line in lines:
                        if "Authentication" in line or "Kimlik doğrulaması" in line:
                            auth = line.split(":")[-1].strip()
                        if "Cipher" in line or "Şifreleme" in line:
                            cipher = line.split(":")[-1].strip()
                    
                    self.log_yaz(f" ↳ Wi-Fi Kimlik Doğrulama: {auth}")
                    self.log_yaz(f" ↳ Şifreleme Algoritması: {cipher}")
                    
                    if "WPA3" in auth:
                        self.log_yaz("[✅] MÜKEMMEL GÜVENLİK: Modeminiz yeni nesil WPA3 protokolünü kullanıyor.")
                    elif "WPA2" in auth:
                        self.log_yaz("[✅] GÜVENLİ: Modeminiz WPA2 standardında, günlük kullanım için yeterli.")
                    elif "WEP" in auth or "WPA" in auth and "WPA2" not in auth:
                        self.log_yaz("[🚨 KRİTİK ZAFİYET] Modeminiz ESKİ bir teknoloji kullanıyor! Modeminizi güncelleyin.")
                    elif "Open" in auth or "Açık" in auth:
                        self.log_yaz("[🚨 KRİTİK ZAFİYET] Bu Wi-Fi ağı şifresiz!")
                else:
                    self.log_yaz("[-] Wi-Fi arabirimi bulunamadı. Kablolu ağa (Ethernet) bağlı olabilirsiniz.")
            except Exception as e:
                self.log_yaz(f"[-] Modem verisi okunamadı: {e}")
        else:
            self.log_yaz("[-] Bu özellik yalnızca Windows'ta çalışmaktadır.")
        self.log_yaz("-" * 85 + "\n")

    # --- DİĞER MODÜLLER (IDS, Ağ Keşfi, Port Tarama) ---
    def start_ids_thread(self):
        threading.Thread(target=self.ids_taramasi_yap, daemon=True).start()

    def ids_taramasi_yap(self):
        self.log_yaz("-" * 85)
        self.log_yaz("[🛡️] Vanguard IDS Aktif! Ağda Man-in-the-Middle (Ortadaki Adam) Saldırısı Aranıyor...")
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            mac_ip_haritasi = {}
            tehdit_bulundu = False

            for line in result.stdout.split('\n'):
                line = line.strip()
                if "dinamik" in line.lower() or "dynamic" in line.lower():
                    parts = line.split()
                    if len(parts) >= 2:
                        ip, mac = parts[0], parts[1].replace('-', ':').upper()
                        if mac in mac_ip_haritasi:
                            tehdit_bulundu = True
                            self.log_yaz(f"[🚨 KRİTİK TEHDİT] ARP Zehirlenmesi Tespit Edildi!")
                            self.log_yaz(f" ↳ DİKKAT: '{mac}' MAC Adresi hem {mac_ip_haritasi[mac]} hem de {ip} IP'leri tarafından kullanılıyor.")
                        else:
                            mac_ip_haritasi[mac] = ip

            if not tehdit_bulundu:
                self.log_yaz("[✅] AĞ GÜVENLİ: Herhangi bir ARP Zehirlenmesi tespit edilmedi.")
        except Exception as e:
            self.log_yaz(f"[-] IDS Tarama Hatası: {e}")
        self.log_yaz("-" * 85 + "\n")

    def start_discovery_thread(self):
        threading.Thread(target=self.ag_kesfi_yap, daemon=True).start()

    def ag_kesfi_yap(self):
        self.log_yaz("-" * 85)
        self.log_yaz("[*] Wi-Fi Ağındaki Cihazlar Hassas Taranıyor... (Yaklaşık 15-20 saniye)")
        try:
            s = socket.socket(socket.AF_INET, socket.socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "192.168.1.1"
            
        ip_parts = local_ip.split('.')
        base_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}."
        
        def ping_ip(ip):
            if platform.system() == "Windows":
                subprocess.call(['ping', '-n', '2', '-w', '500', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.call(['ping', '-c', '2', '-W', '1', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        threads = []
        for i in range(1, 255):
            t = threading.Thread(target=ping_ip, args=(base_ip + str(i),))
            t.start()
            threads.append(t)
            
        for t in threads:
            t.join()
            
        if platform.system() == "Windows":
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            
        output = result.stdout
        bulunan_cihazlar = 0
        dogru_arabirim = False
        
        self.log_yaz("-" * 85)
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith('Interface:') or line.startswith('Arabirim:'):
                dogru_arabirim = (local_ip in line)
                continue
            if dogru_arabirim and (base_ip in line) and ("dinamik" in line.lower() or "dynamic" in line.lower()):
                parts = line.split()
                if len(parts) >= 2:
                    ip, mac = parts[0], parts[1].replace('-', ':').upper()
                    if ip != local_ip and ip != base_ip + "255":
                        self.log_yaz(f"{ip:<18} | {mac:<20} | Wi-Fi'ye Bağlı Cihaz")
                        bulunan_cihazlar += 1
                        
        self.log_yaz(f"[*] Hassas Tarama Tamamlandı! Ağda tespit edilen cihaz: {bulunan_cihazlar + 1}")
        self.log_yaz("-" * 85 + "\n")

    def get_mac_address(self, ip):
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['arp', '-a', ip], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                result = subprocess.run(['arp', '-a', ip], capture_output=True, text=True)
            mac = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", result.stdout)
            return mac.group(0).replace('-', ':').upper() if mac else "Bulunamadi"
        except:
            return "Tespit edilemedi"

    def api_zafiyet_sorgula(self, banner):
        if not banner or banner == "Servis yaniti bos": return "Kontrol edilemedi"
        api_key = self.api_entry.get().strip()
        if not api_key: return "API Anahtarı Eksik"
        
        yazilim = banner.split('/')[0].split()[0].strip()
        try:
            req = requests.post("https://vulners.com/api/v3/search/lucene/", json={"query": f'type:cve AND software:"{yazilim}"', "apiKey": api_key, "size": 1}, timeout=4)
            if req.status_code == 200 and req.json().get("data", {}).get("search"):
                en_kritik = req.json()["data"]["search"][0]
                cve_id = en_kritik.get("_source", {}).get("id", "Bilinmeyen")
                cvss = en_kritik.get("_source", {}).get("cvss", {}).get("score", "Yok")
                return f"AÇIK TESPİT EDİLDİ (Skor: {cvss}): {cve_id}"
            return "Temiz"
        except: return "API Bağlantı Hatası"

    def grab_banner(self, ip, port):
        try:
            s = socket.socket()
            s.settimeout(1.5)
            s.connect((ip, port))
            if port in [80, 8080, 443]: s.send(b"GET / HTTP/1.1\r\n\r\n")
            banner = s.recv(1024).decode(errors='ignore').strip()
            s.close()
            return banner if banner else "Servis yaniti bos"
        except: return "Tespit edilemedi"

    def port_tara(self, ip, port):
        try:
            soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soket.settimeout(0.5)
            if soket.connect_ex((ip, port)) == 0:
                banner = self.grab_banner(ip, port)
                zafiyet = self.api_zafiyet_sorgula(banner)
                self.log_yaz(f"[+] PORT {port} AÇIK | Servis: {banner[:25]}... \n ↳ Zafiyet: {zafiyet}\n")
            soket.close()
        except: pass

    def is_parcacigi(self, ip, kuyruk):
        while not kuyruk.empty():
            self.port_tara(ip, kuyruk.get())
            kuyruk.task_done()

    def start_scan_thread(self):
        ip = self.ip_entry.get()
        if ip: threading.Thread(target=self.tarama_yap, args=(ip,), daemon=True).start()

    def tarama_yap(self, ip):
        baslangic = datetime.now()
        self.log_yaz("-" * 85)
        self.log_yaz(f"[*] Hedef IP: {ip} | MAC: {self.get_mac_address(ip)}")
        self.log_yaz(f"[*] Vanguard Portları Tarıyor...")
        
        kuyruk = Queue()
        for p in range(1, 1025): kuyruk.put(p)
        threads = [threading.Thread(target=self.is_parcacigi, args=(ip, kuyruk), daemon=True) for _ in range(100)]
        for t in threads: t.start()
        kuyruk.join()
        
        self.log_yaz(f"[*] Tarama Tamamlandı! Geçen Süre: {datetime.now() - baslangic}")
        self.log_yaz("-" * 85 + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = VanguardScannerGUI(root)
    root.mainloop()