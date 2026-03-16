# APK Insight 🔍
### Web-Based APK Security Analysis Platform

APK Insight is a **security-focused web application** designed to analyze APK download sources available on the internet.  
The system uses **Google search scraping** to detect where an APK is distributed and classifies links into **Official, Third-Party, and High-Risk sources**.

The application calculates a **Trust Score** based on detected risky keywords and unofficial distribution platforms and visualizes the results in a **risk analysis dashboard**.

# 🚀 Features

• APK source detection using **Google SERP scraping**  
• Classification of sources into **Official, Third-Party, and Risky** categories  
• **Trust Score calculation** based on risk indicators  
• Interactive **risk distribution dashboard with charts**  
• **Scan history storage** using SQLite database  
• **CSV export** of scan results  
• Built-in **APK Security FAQ Chatbot**  
• Clean and responsive **web UI**

# 🧠 How It Works

1. User enters an **app name** in the search field.
2. The system performs a **Google search for APK download sources** using SerpAPI.(using you own APIs)
3. URLs are analyzed based on:
   - Trusted official domains
   - Risk keywords (mod, crack, hack, unlocked)
4. Sources are categorized into:
   - **Official**
   - **Third-Party**
   - **Risky**
5. A **Trust Score** is calculated.
6. Results are displayed in an **interactive dashboard** with charts and source lists.

# 🛠 Tech Stack

**Backend**
- Python
- FastAPI

**Frontend**
- HTML
- CSS
- JavaScript
- Jinja2 Templates
- Chart.js

**Database**
- SQLite

**APIs**
- SerpAPI (Google Search Results API)
  
# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

git clone https://github.com/TamannaDhanda28/apkinsight2.git

cd apkinsight2

## 2️⃣ Create Virtual Environment

python -m venv venv

## 3️⃣ Activate Virtual Environment

Windows

venv\Scripts\activate

## 4️⃣ Install Dependencies

pip install -r requirements.txt

If requirements file is not available install manually:

pip install fastapi uvicorn jinja2 google-search-results serpapi python-multipart groq

## 5️⃣ Run the Application

uvicorn main:app --reload

## 6️⃣ Open in Browser

http://127.0.0.1:8000

# 📊 Dashboard Features

The dashboard provides:

• Total APK source count  
• Official source detection  
• Third-party distribution analysis  
• Risky APK detection  
• Trust score visualization  
• Interactive chart distribution  

---

# 🤖 APK Security Chatbot

The platform includes a **built-in FAQ chatbot** that answers common APK security questions such as:

• What is APK?  
• Is third-party APK safe?  
• What is a risky APK?  
• Can I download mod APKs?  
• How does APK Insight detect official APKs?

# 🔐 Risk Detection Logic

The system detects risky APK sources using:

**Official Domain Detection**

play.google.com
apps.apple.com

**Risk Keywords**

mod
hack
crack
unlocked
pro

# 📤 Export Feature

Users can export scan results as a **CSV report**, which contains:

• Official URLs  
• Third-party URLs  
• Risky URLs  

# 📈 Future Improvements

• Malware detection integration  
• APK file hash verification  
• ML-based risk scoring  
• Live threat intelligence integration  
• User authentication system  

# 👩‍💻 Author

**Tamanna Dhanda**

GitHub  
https://github.com/TamannaDhanda28

# ⭐ If you like this project

Consider giving the repository a **star ⭐ on GitHub**.
