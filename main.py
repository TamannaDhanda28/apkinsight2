from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, JSONResponse
from serpapi import GoogleSearch
from urllib.parse import urlparse
from datetime import date
import sqlite3, json, csv, io

app = FastAPI()
templates = Jinja2Templates(directory="templates")

SERP_API_KEY = "7ebd6ed5e1999a5ae05917ed0fe8733643137d7b05afdea7ba89f8ca42a820f0"

conn = sqlite3.connect("apkinsight.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scan_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name TEXT,
    official INTEGER,
    third_party INTEGER,
    risky INTEGER,
    trust_score INTEGER,
    scanned_at TEXT,
    raw_data TEXT
)
""")
conn.commit()

OFFICIAL_STORES = ["play.google.com", "apps.apple.com"]
RISKY_KEYWORDS = ["mod", "hack", "crack", "unlocked", "pro"]

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search")
def search(request: Request, app_name: str = Form(...)):

    params = {
        "engine": "google",
        "q": f"{app_name} apk",
        "num": 20,
        "api_key": SERP_API_KEY
    }

    data = GoogleSearch(params).get_dict()

    official, third_party, risky = [], [], []
    seen = set()

    for r in data.get("organic_results", []):
        url = r.get("link")
        if not url or url in seen:
            continue
        seen.add(url)

        domain = urlparse(url).netloc.lower()

        if any(store in domain for store in OFFICIAL_STORES):
            official.append(url)
        elif any(word in url.lower() for word in RISKY_KEYWORDS):
            risky.append(url)
        else:
            third_party.append(url)

    trust_score = max(0, 100 - (len(risky) * 15) - (len(third_party) * 5))
    checked_date = date.today().strftime("%d %b %Y")

    cursor.execute("""
        INSERT INTO scan_history
        (app_name, official, third_party, risky, trust_score, scanned_at, raw_data)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        app_name,
        len(official),
        len(third_party),
        len(risky),
        trust_score,
        checked_date,
        json.dumps({
            "official": official,
            "third_party": third_party,
            "risky": risky
        })
    ))
    conn.commit()

    scan_id = cursor.lastrowid

    return templates.TemplateResponse(
    "dashboard.html",
    {
        "request": request,
        "app": app_name,
        "official": official,
        "third_party": third_party,
        "risky": risky,
        "total": len(seen),
        "trust_score": trust_score,
        "checked_date": checked_date,
        "scan_id": scan_id  
    }
)



@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/history")
def history(request: Request):
    cursor.execute("SELECT * FROM scan_history ORDER BY id DESC")
    rows = cursor.fetchall()
    return templates.TemplateResponse(
        "history.html",
        {"request": request, "records": rows}
    )

@app.delete("/delete-history/{scan_id}")
def delete_history(scan_id: int):
    cursor.execute("DELETE FROM scan_history WHERE id = ?", (scan_id,))
    conn.commit()
    return JSONResponse({"status": "deleted"})

@app.get("/export/{scan_id}")
def export_csv(scan_id: int):
    cursor.execute(
        "SELECT raw_data, app_name FROM scan_history WHERE id = ?",
        (scan_id,)
    )
    row = cursor.fetchone()

    if not row:
        return JSONResponse({"error": "Record not found"}, status_code=404)

    raw_data, app_name = row
    raw = json.loads(raw_data)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Category", "URL"])

    for category, urls in raw.items():
        for url in urls:
            writer.writerow([category, url])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={app_name}_report.csv"
        }
    )
