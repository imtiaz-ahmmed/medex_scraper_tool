# MedEx Brand Scraper 💊

A web-based scraping tool to collect **medicine brand data from MedEx Bangladesh**
and export it into **Excel (.xlsx) and CSV** formats.

Built with **Python + FastAPI**, featuring a **simple and clean web UI** to control scraping
and download data easily.

---

## 📌 Features

- Scrape **medicine generics and their brand lists**
- Test mode: scrape **first 10 generics** safely
- Export data to:
  - Excel (`.xlsx`)
  - CSV (`.csv`)
- No database required
- Resume-safe using `progress.json`
- Clean UI (HTML + CSS + JavaScript)
- Robust URL handling (absolute & relative links)

---

## 📁 Project Structure

```
medex_scraper_tool/
│
├─ app.py                 # FastAPI application
├─ scraper.py             # Scraping logic
├─ exporter.py            # Excel & CSV export logic
├─ progress.json          # Progress tracker
├─ requirements.txt
│
├─ data/                  # Generated output files
│   ├─ medex_data.xlsx
│   └─ brands.csv
│
├─ static/
│   ├─ style.css          # UI styling
│   └─ app.js             # UI logic
│
└─ templates/
    └─ index.html         # Web interface
```

---

## ⚙️ Requirements

- Python **3.9+**
- pip
- Internet connection

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

```bash
uvicorn app:app --reload
```

Open your browser:

```
http://127.0.0.1:8000
```

---

## 🧪 How to Use

1. Open the web UI in your browser
2. Click **Start Scraping**
3. Monitor scraping logs in the terminal
4. Wait for status to show **Completed**
5. Click **Download Excel**
6. Open the downloaded file — data will be available

---

## 📊 Data Fields

- `generic_name`
- `brand_name`
- `strength`
- `company`
- `unit_price`

---

## 🔄 Progress Handling

Reset scraping progress by editing `progress.json`:

```json
{
  "completed_generics": []
}
```

---

## ⚠️ Disclaimer

This project is intended for **educational and research purposes only**.
Please respect MedEx’s terms of service.

---

## 📄 License

MIT License

---

## 👨‍💻 Author

**Imtiaz Ahmmed**
