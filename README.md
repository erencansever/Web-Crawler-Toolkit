# 🎯 Web Crawler Toolkit

🕷️ **Web Crawler Toolkit**, dinamik ve kompleks web sitelerinden (örneğin: **Biletix**, **Etkinlik siteleri**, **JS-heavy sayfalar**) veri çekmek isteyenler için hazır Python betiklerinden oluşan modern bir araç kutusudur.

Karmaşık DOM yapıları, JavaScript-render edilmiş içerikler, pagination ve sitemap analizi gibi birçok gerçek dünya problemini hedefler.

---

## 📁 İçerik

| Dosya                           | Açıklama |
|--------------------------------|----------|
| `biletix_event_scraper.py`     | Biletix gibi JavaScript tabanlı sitelerden etkinlik bilgisi çeker (Selenium ile). |
| `dynamic_scraper_selenium.py` | JavaScript içeriği yükleyen tüm siteler için genel dinamik scraper |
| `sitemap_parser.py`           | XML sitemap dosyalarından link çıkarır |
| `simple_static_scraper.py`    | Basit HTML sayfalarından veri çeker (requests + BeautifulSoup) |
| `utils/headers.py`            | Header spoofing, User-Agent randomizer |

---

## 🚀 Hedeflenen Senaryolar

- 🎫 **Etkinlik sitelerinden** (ör. Biletix) etkinlik adı, tarih ve yer çekme
- 🧭 **Sitemap üzerinden** tüm sayfaları keşfetme
- 🕵️‍♂️ JavaScript ile render edilen sayfalardan bilgi çıkarma
- ⏳ Otomatik sayfa kaydırmalı ve tıklamalı gezintiler

---

## ⚙️ Kurulum

Python bağımlılıklarını yüklemek için:

```bash
pip install -r requirements.txt
