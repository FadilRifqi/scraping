import requests
from bs4 import BeautifulSoup
import json
import time
import uuid
import random
import sys

# Daftar sumber berita dengan konfigurasi CSS selector untuk scraping
SUMBER_BERITA = [
    {
        "nama": "ANTARA News",
        "base_url": "https://www.antaranews.com",
        "listing_url": "https://www.antaranews.com/terkini",
        "selectors": {
            "listing": {
                "item": "div.card__post",
                "judul": "h2",
                "link": "a"
            },
            "detail": {
                "tanggal": "div.wrap__article-detail-info span",
                "konten": "div.post-content",
                "paragraf": "p",
                "gambar": "div.wrap__article-detail-image img"
            }
        }
    },
    {
        "nama": "Kompas",
        "base_url": "https://www.kompas.com",
        "listing_url": "https://www.kompas.com/tren?source=link",
        "selectors": {
            "listing": {
                "item": "div.trenLatest__item",
                "judul": "h3.trenLatest__title",
                "link": "h3.trenLatest__title a"
            },
            "detail": {
                "tanggal": "div.read__time",
                "konten": "div.read__content",
                "paragraf": "p",
                "gambar": "div.photo__wrap img"
            }
        }
    },
    {
        "nama": "CNN Indonesia",
        "base_url": "https://www.cnnindonesia.com",
        "listing_url": "https://www.cnnindonesia.com/nasional",
        "selectors": {
            "listing": {
                "item": "article",
                "judul": "h2.text-cnn_black_light",
                "link": "article a"
            },
            "detail": {
                "tanggal": "div.text-cnn_grey.text-sm",
                "konten": "div.detail-text",
                "paragraf": "p",
                "gambar": "div.detail-image figure img"
            }
        }
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MyBot/1.0; +https://example.com/bot-info)"
}

def ambil_daftar_berita(sumber):
    """Mengambil daftar berita dari sumber tertentu"""
    try:
        response = requests.get(sumber["listing_url"], headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ Gagal mengakses {sumber['nama']}: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "lxml")
        selectors = sumber["selectors"]["listing"]

        daftar = soup.select(selectors["item"])
        hasil = []

        for item in daftar:
            link_tag = item.select_one(selectors["link"])
            judul_tag = item.select_one(selectors["judul"])

            if link_tag and judul_tag:
                judul = judul_tag.get_text(strip=True)
                link = link_tag.get("href", "")

                # Pastikan link adalah URL lengkap
                if not link.startswith(("http://", "https://")):
                    link = sumber["base_url"] + link

                hasil.append({
                    "judul": judul,
                    "link": link,
                    "sumber": sumber["nama"]  # Tambahkan informasi sumber berita
                })

        print(f"✅ Berhasil mengambil {len(hasil)} berita dari {sumber['nama']}")
        return hasil
    except Exception as e:
        print(f"❌ Error mengambil daftar berita dari {sumber['nama']}: {e}")
        return []

def ambil_detail(berita, sumber_berita):
    """Mengambil detail berita dari link dan sumber tertentu"""
    for sumber in sumber_berita:
        if sumber["nama"] == berita["sumber"]:
            selectors = sumber["selectors"]["detail"]
            break
    else:
        print(f"❌ Sumber berita tidak ditemukan: {berita['sumber']}")
        return None

    try:
        response = requests.get(berita["link"], headers=HEADERS)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "lxml")

        # Ambil tanggal
        tanggal_tag = soup.select_one(selectors["tanggal"])
        tanggal = tanggal_tag.get_text(strip=True) if tanggal_tag else ""

        # Skip berita yang tidak memiliki tanggal
        if not tanggal:
            print(f"❌ Berita tidak memiliki tanggal: {berita['link']}")
            return None

        # Ambil isi konten utama
        konten = soup.select_one(selectors["konten"])
        paragraf = konten.select(selectors["paragraf"]) if konten else []
        isi = "\n".join([p.get_text(strip=True) for p in paragraf])

        # Skip berita yang tidak memiliki isi
        if not isi:
            print(f"❌ Berita tidak memiliki isi: {berita['link']}")
            return None

        # Ambil URL gambar
        gambar_tag = soup.select_one(selectors["gambar"])
        gambar_url = ""
        if gambar_tag and gambar_tag.has_attr("src"):
            gambar_url = gambar_tag["src"]
            # Pastikan URL gambar lengkap
            if not gambar_url.startswith(("http://", "https://")):
                gambar_url = sumber["base_url"] + gambar_url

        return {
            "tanggal": tanggal,
            "isi": isi,
            "gambar_url": gambar_url
        }
    except Exception as e:
        print(f"❌ Gagal ambil detail dari {berita['link']}: {e}")
        return None

def simpan_ke_ts(data, filename="../frontend/database/berita_dengan_detail.ts"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("export const daftarBerita = ")
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write(";")
    print(f"\n✅ Data lengkap disimpan ke {filename}")

def scrape_semua(max_berita = 3):
    hasil = []

    # Ambil berita dari setiap sumber
    for sumber in SUMBER_BERITA:
        print(f"\n🔍 Mengambil berita dari {sumber['nama']}...")
        daftar = ambil_daftar_berita(sumber)

        # Ambil detail untuk setiap berita sampai max_berita item valid didapatkan
        valid_count = 0
        i = 0

        while valid_count < max_berita and i < len(daftar):
            berita = daftar[i]
            print(f"{i+1}. {berita['judul']} ({berita['sumber']}) Link: {berita['link']}")
            detail = ambil_detail(berita, SUMBER_BERITA)

            if detail:
                hasil.append({
                    "id": str(uuid.uuid4()),
                    "judul": berita["judul"],
                    "tanggal": detail["tanggal"],
                    "isi": detail["isi"],
                    "gambar_url": None if detail["gambar_url"] == "" else detail["gambar_url"],
                    "sumber": berita["sumber"]
                })
                valid_count += 1
                print(f"   ✅ Berhasil mengambil ({valid_count}/{max_berita})")
            else:
                print(f"   ⏩ Melewati berita (tidak valid/lengkap)")

            i += 1
            # Berikan jeda waktu acak untuk menghindari pemblokiran
            time.sleep(random.uniform(1.0, 3.0))

    return hasil

if __name__ == "__main__":
    max_berita = 3  # Default value
    if len(sys.argv) > 1:
        try:
            max_berita = int(sys.argv[1])
            print(f"🔢 Mengambil maksimal {max_berita} berita dari setiap sumber")
        except ValueError:
            print(f"❌ Argumen tidak valid: {sys.argv[1]}. Menggunakan nilai default: 3 berita")

    data = scrape_semua(max_berita)
    if data:
        simpan_ke_ts(data)
