### Portal Berita

Portal Berita adalah aplikasi web yang mengumpulkan berita dari berbagai sumber berita Indonesia seperti Kompas.com, CNN Indonesia, dan ANTARA News menggunakan teknik web scraping.

#### Fitur Utama

- Scraping berita dari berbagai sumber
- Tampilan berita modern dengan Next.js
- Autentikasi Google untuk akses login

#### Struktur Proyek

```
portalberita/
├── scraping/            # Kode Python untuk scraping
│   └── app.py           # Scraper utama
├── frontend/            # Aplikasi Next.js
│   ├── app/             # Pages dan components
│   ├── database/        # Data hasil scraping
│   └── .env             # File untuk env variables
├── README.md            # Dokumentasi proyek
```

#### Persyaratan

- Python 3.8+
- Node.js 16+
- NPM atau Yarn
- Google Cloud Console account (untuk OAuth)

#### Instalasi

1. Clone repositori:

```bash
git clone https://github.com/username/portalberita.git
cd portalberita
```

2. Install dependencies Python untuk scraper:

```bash
cd scraping
pip install -r requirements.txt
```

3. Install dependencies Next.js untuk frontend:

```bash
cd ../frontend
npm install
# atau
yarn install
```

### Menjalankan Web Scraper

1. Jalankan scraper untuk mengumpulkan berita:

```bash
cd scraping
python app.py 5  # 5 adalah jumlah berita yang diambil per sumber
```

2. Data berita akan disimpan di [berita_dengan_detail.ts](frontend/database/berita_dengan_detail.ts)

### Menjalankan Frontend Next.js

1. Siapkan file .env di folder [frontend](frontend/) dengan isi:

```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
NEXTAUTH_SECRET=your-random-secret
```

2. Untuk mendapatkan Google Client ID dan Secret:

- Buka [Google Cloud Console](https://console.cloud.google.com/)
- Buat project baru atau gunakan yang sudah ada
- ke "APIs & Services" > "Credentials"
- Klik "Create Credentials" > "OAuth client ID"
- Pilih "Web application"
- Tambahkan "[http://localhost:3000](http://localhost:3000)" sebagai "Authorized JavaScript origins"
  Tambahkan "[http://localhost:3000/api/auth/callback/google](http://localhost:3000/api/auth/callback/google)" sebagai "Authorized redirect URIs"
  Salin Client ID dan Client Secret ke .

3. Jalankan server development Next.js:

```bash
cd frontend
npm run dev
# atau
yarn dev
```

4. Buka http://localhost:3000 di browser Anda

### Deployment

Untuk deployment production:

1. Build frontend:

```bash
cd frontend
npm run build
# atau
yarn build
```

2. Jalankan dalam mode production:

```bash
npm start
# atau
yarn start
```

