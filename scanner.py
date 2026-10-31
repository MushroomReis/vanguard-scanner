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
        self.root.title("Vanguard Scanner - Zafiyet ve Ağ Analiz Aracı v3.2")
        self.root.geometry("780x600")
        self.root.configure(bg="#0c0c0c")
        
        # Ana pencereyi başta gizliyoruz
        self.root.withdraw()
        
        # Yasal uyarı penceresini çağırıyoruz
        self.yasal_uyari_goster()

        top_frame = tk.Frame(root, bg="#0c0c0c")
        top_frame.pack(pady=15)

        tk.Label(top_frame, text="Hedef IP:", fg="#00ff00", bg="#0c0c0c", font=("Consolas", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = tk.Entry(top_frame, font=("Consolas", 12), bg="#1a1a1a", fg="#00ff00", insertbackground="white", width=18)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ip_entry.insert(0, "127.0.0.1")

        self.start_btn = tk.Button(top_frame, text="PORT TARAMA", bg="#004d00", fg="#00ff00", font=("Consolas", 10, "bold"), command=self.start_scan_thread)
        self.start_btn.grid(row=0, column=2, padx=5, pady=5)

        self.discover_btn = tk.Button(top_frame, text="AĞDAKİ CİHAZLARI BUL", bg="#00004d", fg="#00ffff", font=("Consolas", 10, "bold"), command=self.start_discovery_thread)
        self.discover_btn.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(top_frame, text="Vulners API Key:", fg="#00ff00", bg="#0c0c0c", font=("Consolas", 10)).grid(row=1, column=0, padx=5, pady=5)
        self.api_entry = tk.Entry(top_frame, font=("Consolas", 10), bg="#1a1a1a", fg="#00ff00", insertbackground="white", width=30, show="*")
        self.api_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        self.save_btn = tk.Button(top_frame, text="SONUÇLARI KAYDET", bg="#4d4d00", fg="#ffff00", font=("Consolas", 10, "bold"), command=self.sonuclari_kaydet, state=tk.DISABLED)
        self.save_btn.grid(row=1, column=3, padx=5, pady=5)

        self.log_area = scrolledtext.ScrolledText(root, width=90, height=22, bg="#000000", fg="#00ff00", font=("Consolas", 10))
        self.log_area.pack(padx=15, pady=10)
        
        self.log_yaz("Vanguard Scanner v3.2 Başlatıldı...\n- Belli bir cihazda açık aramak için 'PORT TARAMA'yı kullanın.\n- Wi-Fi ağınıza bağlı cihazları görmek için 'AĞDAKİ CİHAZLARI BUL'a tıklayın.\n" + "-"*70 + "\n")

    # --- YASAL UYARI MODÜLÜ ---
    def yasal_uyari_goster(self):
        self.uyari_penceresi = tk.Toplevel()
        self.uyari_penceresi.title("⚠️ Yasal Uyarı ve Sorumluluk Reddi")
        self.uyari_penceresi.geometry("550x300")
        self.uyari_penceresi.configure(bg="#0c0c0c")
        self.uyari_penceresi.resizable(False, False)
        
        # Kullanıcı "X" tuşuna basarsa programı tamamen kapatır
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
        tk.Button(btn_frame, text="REDDEDİYORUM (ÇIKIŞ)", bg="#4d0000", fg="#ff0000", font=("Consolas", 10, "bold"), command=self.reddet).pack(side="right", padx=15)

    def kabul_et(self):
        self.uyari_penceresi.destroy()
        self.root.deiconify() # Ana pencereyi göster

    def reddet(self):
        self.root.destroy()
        sys.exit()

    # --- PORT, ZAFİYET VE AĞ KEŞFİ KODLARI AYNEN KORUNDU ---
    def log_yaz(self, mesaj):
        self.log_area.insert(tk.END, mesaj + "\n")
        self.log_area.see(tk.END)

    def sonuclari_kaydet(self):
        dosya_yolu = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Metin Dosyası", "*.txt")], title="Sonuçları Kaydet")
        if dosya_yolu:
            with open(dosya_yolu, "w", encoding="utf-8") as dosya:
                dosya.write(self.log_area.get("1.0", tk.END))
            messagebox.showinfo("Başarılı", f"Sonuçlar kaydedildi:\n{dosya_yolu}")

    def start_discovery_thread(self):
        self.discover_btn.config(state=tk.DISABLED, text="AĞ TARANIYOR...")
        self.start_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.log_area.delete('1.0', tk.END)
        threading.Thread(target=self.ag_kesfi_yap, daemon=True).start()

    def ag_kesfi_yap(self):
        self.log_yaz("-" * 70)
        self.log_yaz("[*] Wi-Fi Ağındaki Cihazlar Taranıyor... (Bu işlem 10-15 saniye sürebilir)")
        self.log_yaz("-" * 70 + "\n")
        
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
                subprocess.call(['ping', '-n', '1', '-w', '200', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.call(['ping', '-c', '1', '-W', '1', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
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
        
        self.log_yaz(f"Senin Cihaz IP Adresin: {local_ip}")
        self.log_yaz(f"{'IP ADRESİ':<18} | {'MAC ADRESİ':<20} | {'DURUM'}")
        self.log_yaz("-" * 70)
        
        for line in output.split('\n'):
            if base_ip in line and ("dinamik" in line.lower() or "dynamic" in line.lower()):
                parts = line.split()
                if len(parts) >= 2:
                    ip = parts[0]
                    mac = parts[1].replace('-', ':').upper()
                    if ip != local_ip and ip != base_ip + "255":
                        self.log_yaz(f"{ip:<18} | {mac:<20} | Wi-Fi'ye Bağlı Cihaz")
                        bulunan_cihazlar += 1
                        
        self.log_yaz("-" * 70)
        self.log_yaz(f"[*] Tarama Tamamlandı! Ağda tespit edilen toplam cihaz: {bulunan_cihazlar + 1} (Senin Cihazın Dahil)")
        
        self.discover_btn.config(state=tk.NORMAL, text="AĞDAKİ CİHAZLARI BUL")
        self.start_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)

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
        if not banner or banner == "Servis yaniti bos":
            return "Kontrol edilemedi"
        
        api_key = self.api_entry.get().strip()
        if not api_key:
            return "API Anahtarı Eksik (Açık kontrolü yapılamadı)"
        
        yazilim = banner.split('/')[0].split()[0].strip()
        url = "https://vulners.com/api/v3/search/lucene/"
        payload = {"query": f'type:cve AND software:"{yazilim}"', "apiKey": api_key, "size": 1}
        
        try:
            response = requests.post(url, json=payload, timeout=4)
            if response.status_code == 200:
                data = response.json()
                if data.get("result") == "OK" and data["data"]["search"]:
                    en_kritik = data["data"]["search"][0]
                    cve_id = en_kritik.get("_source", {}).get("id", "Bilinmeyen CVE")
                    cvss = en_kritik.get("_source", {}).get("cvss", {}).get("score", "Skor Yok")
                    return f"AÇIK TESPİT EDİLDİ (Skor: {cvss}): {cve_id}"
                return "Temiz (Bilinen açık bulunamadı)"
        except:
            return "API Bağlantı Hatası"
        return "Temiz (Bilinen açık bulunamadı)"

    def grab_banner(self, ip, port):
        try:
            s = socket.socket()
            s.settimeout(1.5)
            s.connect((ip, port))
            if port in [80, 8080, 443]:
                s.send(b"GET / HTTP/1.1\r\n\r\n")
            banner = s.recv(1024).decode(errors='ignore').strip()
            s.close()
            return banner if banner else "Servis yaniti bos"
        except:
            return "Tespit edilemedi"

    def port_tara(self, ip, port):
        try:
            soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soket.settimeout(0.5)
            sonuc = soket.connect_ex((ip, port))
            
            if sonuc == 0:
                banner = self.grab_banner(ip, port)
                zafiyet = self.api_zafiyet_sorgula(banner)
                self.log_yaz(f"[+] PORT {port} AÇIK | Servis: {banner[:25]}... \n ↳ Zafiyet Durumu: {zafiyet}\n")
            soket.close()
        except:
            pass

    def is_parcacigi(self, ip, kuyruk):
        while not kuyruk.empty():
            port = kuyruk.get()
            self.port_tara(ip, port)
            kuyruk.task_done()

    def start_scan_thread(self):
        ip = self.ip_entry.get()
        if not ip:
            messagebox.showerror("Hata", "Lütfen bir IP adresi girin!")
            return
            
        self.start_btn.config(state=tk.DISABLED, text="TARANIYOR...")
        self.discover_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.log_area.delete('1.0', tk.END)
        threading.Thread(target=self.tarama_yap, args=(ip,), daemon=True).start()

    def tarama_yap(self, ip):
        baslangic = datetime.now()
        mac = self.get_mac_address(ip)
        
        self.log_yaz("-" * 70)
        self.log_yaz(f"[*] Hedef IP: {ip} | MAC: {mac}")
        self.log_yaz(f"[*] Vanguard Scanner Portları Tarıyor ve Vulners'ı Sorguluyor...")
        self.log_yaz("-" * 70 + "\n")

        port_kuyrugu = Queue()
        for port in range(1, 1025):
            port_kuyrugu.put(port)

        threads = []
        for _ in range(100):
            t = threading.Thread(target=self.is_parcacigi, args=(ip, port_kuyrugu))
            t.daemon = True
            t.start()
            threads.append(t)

        port_kuyrugu.join()
        
        bitis = datetime.now()
        self.log_yaz("-" * 70)
        self.log_yaz(f"[*] Tarama Tamamlandı! Geçen Süre: {bitis - baslangic}")
        
        self.start_btn.config(state=tk.NORMAL, text="PORT TARAMA")
        self.discover_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = VanguardScannerGUI(root)
    root.mainloop()