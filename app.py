from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from scraper.runner import run_scraper
from scraper.generics import scrape_generics
from scraper.brands import scrape_brands
from scraper.companies import scrape_companies
from scraper.dosage_forms import scrape_dosage_forms
from exporter.excel import export_excel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

LAST_FILE = None

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/scrape")
def scrape(
    section: str = Query(...),
    alphabets: str = Query("ALL"),
    limit: int | None = Query(None),
    herbal: int = Query(0),
):
    global LAST_FILE

    alpha_list = [] if alphabets == "ALL" else alphabets.split(",")

    if section == "generics":
        # We need to adapt scraper_generics later if needed, but for "Detailed" we might be using run_scraper?
        # The user's request implies scraping detailed generic data (brands/pack size).
        # Let's assume the main 'Detailed Search' or default scrape uses run_scraper
        # BUT wait, the UI calls /scrape?section=generics etc.
        # The prompt implies unified logic. The user wants to scrape "Generics" (alphabet wise) with detailed data.
        # run_scraper in scraper.py now does exactly that (generics -> brands).
        # We should map 'generics' section to THIS new logic if that's the intention.
        # Or maybe add a new section "all_details"?
        # User said: "generic wise download korbo".
        
        rows = run_scraper(alpha_list, limit)
        
    elif section == "brands":
        rows = scrape_brands(alpha_list, limit, herbal)
    elif section == "companies":
        rows = scrape_companies(alpha_list, limit, herbal)
    elif section == "dosage":
        rows = scrape_dosage_forms(limit)
    else:
        return JSONResponse({"error": "Invalid section"}, status_code=400)

    LAST_FILE = export_excel(rows, section)
    return {"status": "ok", "rows": len(rows)}

@app.get("/search")
def search_gen(q: str = Query(...)):
    from scraper.runner import search_generic
    results = search_generic(q)
    return results

@app.get("/scrape_single")
def scrape_single(url: str = Query(...), name: str = Query(...)):
    from scraper.runner import scrape_single_generic
    global LAST_FILE
    
    rows = scrape_single_generic(url, name)
    
    if not rows:
        return JSONResponse({"error": "No data scraped"}, status_code=400)
        
    LAST_FILE = export_excel(rows, f"Single_{name}")
    return {"status": "ok", "rows": len(rows)}

@app.get("/progress")
def get_progress():
    from scraper.runner import SCRAPE_STATUS
    return SCRAPE_STATUS



@app.get("/download")
def download():
    global LAST_FILE
    if not LAST_FILE:
        return JSONResponse({"error": "No file"}, status_code=400)
    return FileResponse(
        LAST_FILE,
        filename=LAST_FILE.split("/")[-1],
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
