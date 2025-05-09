import requests
from bs4 import BeautifulSoup
import json
import time
import uuid

BASE_URL = "https://www.antaranews.com"
LISTING_URL = f"{BASE_URL}/terkini"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MyBot/1.0; +https://example.com/bot-info)"
}

def ambil_daftar_berita():
    response = requests.get(LISTING_URL, headers=HEADERS)
    if response.status_code != 200:
        print("❌ Gagal mengakses halaman listing.")
        return []

    soup = BeautifulSoup(response.text, "lxml")
    daftar = soup.find_all("div", class_="card__post")
    hasil = []

    for item in daftar:
        link_tag = item.find("a")
        judul_tag = item.find("h3")
        if link_tag and judul_tag:
            judul = judul_tag.get_text(strip=True)
            link = link_tag["href"]
            hasil.append({
                "judul": judul,
                "link": link  # link disimpan sementara untuk ambil detail
            })
    return hasil

def ambil_detail(link):
    try:
        response = requests.get(link, headers=HEADERS)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "lxml")

        # Ambil tanggal dari <span> pertama dalam <div class="wrap__article-detail-info">
        tanggal_tag = soup.find("div", class_="wrap__article-detail-info")
        tanggal = ""
        if tanggal_tag:
            span_tag = tanggal_tag.find("span")
            if span_tag:
                tanggal = span_tag.get_text(strip=True)

        # Ambil isi konten utama
        konten = soup.find("div", class_="post-content")
        paragraf = konten.find_all("p") if konten else []
        isi = "\n".join([p.get_text(strip=True) for p in paragraf])

        # Ambil URL gambar dari <div class="wrap__article-detail-image">
        gambar_tag = soup.find("div", class_="wrap__article-detail-image")
        gambar_url = ""
        if gambar_tag:
            img_tag = gambar_tag.find("img")
            if img_tag and img_tag.has_attr("src"):
                gambar_url = img_tag["src"]

        return {
            "tanggal": tanggal,
            "isi": isi,
            "gambar_url": gambar_url
        }
    except Exception as e:
        print(f"❌ Gagal ambil detail dari {link}: {e}")
        return None

def simpan_ke_ts(data, filename="../frontend/database/berita_dengan_detail.ts"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("export const daftarBerita = ")
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write(";")
    print(f"\n✅ Data lengkap disimpan ke {filename}")


def scrape_semua():
    daftar = ambil_daftar_berita()
    hasil = []

    print(f"🔍 Mengambil {len(daftar)} berita...")

    for i, berita in enumerate(daftar, start=1):
        print(f"{i}. {berita['judul']} Link: {berita['link']}")
        detail = ambil_detail(berita["link"])
        if detail:
            hasil.append({
                "id": str(uuid.uuid4()),  # id unik untuk setiap berita
                "judul": berita["judul"],
                "tanggal": detail["tanggal"],
                "isi": detail["isi"],
                "gambar_url": None if detail["gambar_url"] == "" else detail["gambar_url"]  # Menambahkan URL gambar

            })
        time.sleep(1)  # Hindari membanjiri server

    return hasil

def simpan_ke_json(data, filename="../frontend/database/berita_dengan_detail.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Data lengkap disimpan ke {filename}")

if __name__ == "__main__":
    data = scrape_semua()
    if data:
        simpan_ke_ts(data)
