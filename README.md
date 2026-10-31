# Vanguard Scanner 🛡️

Vanguard Scanner, ağ güvenliği analizi ve port tarama işlemlerini otomatikleştirmek için geliştirilmiş, grafik arayüze (GUI) sahip bir siber güvenlik aracıdır. Asenkron port taraması yapar, yerel ağdaki cihazları keşfeder ve Vulners API entegrasyonu ile tespit edilen servislerdeki bilinen zafiyetleri (CVE) anlık olarak sorgular.

### Özellikler
* **Hızlı Port Tarama:** Threading altyapısı ile saniyeler içinde asenkron port analizi.
* **Ağ Keşfi (Network Discovery):** Modeme bağlı tüm cihazları IP ve MAC adresleriyle listeleme.
* **Zafiyet Tespiti:** Vulners API üzerinden gerçek zamanlı CVE (Ortak Zafiyetler ve Açıklar) sorgulaması.
* **Güvenli Kullanım:** API anahtarlarının kod içinde saklanmasını önleyen dinamik giriş arayüzü.

### Kurulum ve Kullanım

**Bağımsız Sürüm (Windows .exe)**
Projeyi Python ortamı kurmadan çalıştırmak için sağ taraftaki **Releases** bölümünden `Vanguard.exe` dosyasını indirin ve çalıştırın.

**Geliştirici Sürümü (Python)**
1. Depoyu klonlayın:
   git clone https://github.com/MushroomReis/vanguard-scanner.git
2. Gerekli bağımlılıkları yükleyin:
   pip install requests
3. Aracı başlatın:
   python scanner.py

### Yasal Uyarı ⚠️
Bu araç yalnızca eğitim ve yetkili sistemlerin denetimi amacıyla geliştirilmiştir. İzinsiz tarama yapmak yasa dışıdır. Tüm sorumluluk kullanıcıya aittir.
