from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from scraper import run_scraper
from exporter import export

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    return open("templates/index.html", encoding="utf-8").read()


@app.get("/start")
def start():
    rows = run_scraper()
    export(rows)
    return {"status": f"Completed. {len(rows)} brands scraped"}


@app.get("/download")
def download():
    return FileResponse(
        "data/medex_data.xlsx",
        filename="medex_brands_data.xlsx"
    )
