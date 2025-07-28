import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

try:
    base_url = "https://www.biletix.com/category/OTHER/ISTANBUL/tr"
    logging.info(f"Opening base URL: {base_url}")
    driver.get(base_url)
    time.sleep(2)

    kategori_linkleri = []
    logging.info("Finding category elements...")
    kategori_etiketleri = driver.find_elements(By.CSS_SELECTOR, "a.subcat_item")
    for etiket in kategori_etiketleri:
        href = etiket.get_attribute("href")
        if href and "/search/" in href:
            kategori_linkleri.append(href)

    logging.info(f"{len(kategori_linkleri)} kategori bulundu.")

    etkinlik_verileri = []
    non_event_urls = []  

    for kategori_url in kategori_linkleri:  
        logging.info(f"Kategori: {kategori_url}")
        try:
            logging.info(f"Opening category URL: {kategori_url}")
            driver.get(kategori_url)
            time.sleep(2)
        except Exception as e:
            logging.error(f"Kategoriye gidilemedi: {kategori_url} - {e}")
            continue

        while True:
            try:
                logging.info("Looking for 'load more' button...")
                btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.search_load_more"))
                )
                logging.info("Clicking 'load more' button...")
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(1.5)
            except Exception:
                logging.info("No more 'load more' button or error occurred.")
                break

        logging.info("Finding event divs...")
        etkinlik_divleri = driver.find_elements(By.CSS_SELECTOR, "div.searchLinkDiv")
        etkinlik_linkleri = []
        for div in etkinlik_divleri:
            onclick = div.get_attribute("onclick")
            if onclick and "window.location=" in onclick:
                event_url = onclick.split("'")[1]
                if event_url.startswith("http"):
                    url = event_url
                else:
                    url = "https://www.biletix.com" + event_url
                if ("/etkinlik/" in url and "/etkinlik-grup/" not in url):
                    etkinlik_linkleri.append(url)
                else:
                    non_event_urls.append(url)
                    logging.info(f"Non-event URL stored: {url}")

        logging.info(f"{len(etkinlik_linkleri)} etkinlik bulundu.")

        for etkinlik_url in etkinlik_linkleri: 
            logging.info(f"Etkinlik: {etkinlik_url}")
            try:
                logging.info(f"Opening event URL: {etkinlik_url}")
                driver.get(etkinlik_url)
                time.sleep(2)

                try:
                    gun = driver.find_element(By.CSS_SELECTOR, ".date-box .day").text.strip()
                    aylar_ve_saat = driver.find_elements(By.CSS_SELECTOR, ".date-box .month")
                    if len(aylar_ve_saat) >= 2 and ":" in aylar_ve_saat[1].text:
                        ay = aylar_ve_saat[0].text.strip()
                        saat = aylar_ve_saat[1].text.strip()
                        tarih_saat = f"{gun} {ay} {saat}"
                    elif len(aylar_ve_saat) >= 1:
                        ay = aylar_ve_saat[0].text.strip()
                        tarih_saat = f"{gun} {ay} bilinmiyor"
                    else:
                        tarih_saat = "bilinmiyor"
                except Exception as e:
                    logging.error(f"Tarih/saat çekilemedi: {e}")
                    tarih_saat = "bilinmiyor"

                try:
                    mekan = driver.find_element(By.CSS_SELECTOR, ".performance-listing-venue").text.strip()
                except Exception as e:
                    logging.error(f"Mekan çekilemedi: {e}")
                    mekan = "bilinmiyor"

                etkinlik_verileri.append({
                    "Etkinlik URL": etkinlik_url,
                    "Tarih-Saat": tarih_saat,
                    "Mekan": mekan
                })

            except Exception as e:
                logging.error(f"Etkinlikte hata: {etkinlik_url} - {e}")
                continue

    df = pd.DataFrame(etkinlik_verileri)
    csv_path = "/Users/boraberkercansever/Desktop/biletix_detaylar4.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    logging.info(f"CSV yazıldı: {csv_path}")

    if non_event_urls:
        pd.DataFrame({'non_event_url': non_event_urls}).to_csv('/Users/boraberkercansever/Desktop/non_event_urls4.csv', index=False)
        logging.info("Non-event URLs saved to /Users/boraberkercansever/Desktop/non_event_urls4.csv")

except Exception as e:
    logging.critical(f"Beklenmeyen hata: {e}")
finally:
    driver.quit()
    logging.info("Driver kapatıldı.")
