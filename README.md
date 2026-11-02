Vanguard Scanner 🛡️ (v2.0)
Vanguard Scanner; ağ güvenliği analizi, zafiyet tespiti, saldırı tespiti (IDS) ve kişisel dijital gizlilik kontrolünü tek bir masaüstü arayüzünde birleştiren Python tabanlı açık kaynaklı bir siber güvenlik kalkanıdır.

🚀 Öne Çıkan Özellikler
⚡ Asenkron Port Tarama: Multi-threading altyapısı ile hedef IP üzerindeki 1000+ portu saniyeler içinde tara.

🔍 Zafiyet Tespiti (CVE): Vulners API entegrasyonu ile açık portlardaki servislerin bilinen güncel güvenlik açıklarını anlık sorgula.

📡 Hassas Ağ Keşfi: Ping Sweep ve ARP tablosu analizi ile hayalet/sanal cihazları eleyerek Wi-Fi ağına bağlı gerçek cihazları (IP & MAC) doğru şekilde listele.

🛡️ Saldırı Tespit Sistemi (IDS): Ağda gerçekleşebilecek Man-in-the-Middle (Ortadaki Adam) ve ARP Zehirlenmesi (ARP Spoofing) saldırılarını kırmızı alarmla tespit et.

☣️ Dark Web Kimlik Taraması: XposedOrNot API entegrasyonu ile e-posta adreslerinin geçmiş veritabanı sızıntılarında (breach) yer alıp almadığını kontrol et.

🌐 IP Sızıntı & Anonimlik Testi: Dış IP, konum ve ISP analizi ile VPN/Proxy kullanımını ve internet ayak izini doğrula.

📶 Modem Şifreleme Analizi: Windows ağ servisleri üzerinden bağlı olunan Wi-Fi ağının güvenlik protokolünü (WPA2/WPA3/WEP) ve şifreleme direncini raporla.

⚖️ Zorunlu Yasal Uyarı Ekranı: Kullanıcı sorumluluğunu göz göz önüne alan TCK 243-244 maddeleri kapsamındaki katmanlı sorumluluk reddi penceresi.

🛠️ Kurulum ve Çalıştırma
Gereksinimler
Python 3.8+

requests kütüphanesi

Bash
# Depoyu klonlayın
git clone https://github.com/MushroomReis/vanguard-scanner.git

# Proje klasörüne girin
cd vanguard-scanner

# Gerekli bağımlılığı yükleyin
pip install requests

# Uygulamayı çalıştırın
python scanner.py
📦 .exe Olarak Derleme (PyInstaller)
Uygulamayı bağımsız bir Windows çalıştırılabilir dosyasına dönüştürmek için:

Bash
pip install pyinstaller
python -m PyInstaller --onefile --noconsole --noconfirm --name "Vanguard" --icon="vanguard.ico" scanner.py
Derleme tamamlandığında çalıştırılabilir dosya dist/Vanguard.exe dizininde oluşacaktır.

⚖️ Yasal Uyarı / Disclaimer
Bu yazılım yalnızca eğitim, savunma amaçlı analizler ve izin alınmış sistemlerde test yapılmak üzere geliştirilmiştir. İzinsiz ağlarda veya sistemlerde yetkisiz tarama yapmak yasaktır ve yasal sorumluluk tamamen kullanıcıya aittir.
