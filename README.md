# 🎫 Support CRM with Auto-Triage Engine

A lightweight, production-ready Customer Support CRM built with FastAPI, SQLite, and Tailwind CSS. Automatically triages incoming tickets using keyword-based NLP — assigning urgency levels and categories without manual intervention.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)
![Tailwind](https://img.shields.io/badge/UI-Tailwind_CSS-38B2AC.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> 🚀 Live Demo: https://crm-5386.onrender.com

---

## ✨ Key Features

- 🤖 **Auto-Triage Engine** — Automatically assigns urgency (Critical/High/Normal) and category (Billing/Shipping/Product/Account/General) on ticket creation using keyword-based NLP.
- 📊 **Real-time Dashboard** — Live ticket counts across Open, In Progress, and Closed statuses with color-coded priority badges.
- 🔍 **Instant Search** — Dynamic client-side search across customer names, ticket IDs, and subjects.
- 📱 **Mobile Responsive** — Clean, responsive UI powered by Tailwind CSS.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+, FastAPI |
| Database | SQLite + SQLAlchemy ORM |
| Validation | Pydantic |
| Frontend | HTML5, Tailwind CSS (CDN), Vanilla JavaScript |
| API | RESTful with Fetch API |
| Deployment | Uvicorn, Render |

---

## 📁 Project Structure

CRM/
├── main.py                  # FastAPI app entry point & route definitions
├── database.py              # SQLite engine & database setup
├── models.py                # SQLAlchemy models (Tickets)
├── routes/
│   └── tickets.py           # Ticket API endpoints & auto-triage logic
├── frontend/                # Frontend layout templates
│   ├── index.html           # Main support CRM dashboard
│   └── create.html          # New ticket submission form
├── .env.example             # Template for environment configuration
├── .gitignore                # Git ignore rules
├── requirements.txt         # Dependency manifest
└── README.md

---

## 🤖 Auto-Triage Engine

When a ticket is submitted, the system automatically:

1. Analyzes the subject and description using keyword-based NLP rules.
2. Assigns Urgency Level:
   - 🔴 Critical — urgent, broken, refund, fraud, emergency
   - 🟠 High — delayed, wrong, missing, error, failed
   - 🟢 Normal — general inquiries and requests
3. Assigns Category:
   - 💳 Billing — payment, invoice, charge, refund
   - 📦 Shipping — delivery, tracking, courier, transit
   - 🔧 Product — defect, broken, quality, malfunction
   - 👤 Account — login, password, access, reset
   - 📋 General — everything else

This eliminates manual triage — reducing First Response Time (FRT) for high-priority tickets significantly.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/tickets | Create ticket with auto-triage |
| GET | /api/tickets | List all tickets (supports ?search=) |
| GET | /api/tickets/{ticket_id} | Get ticket details |
| PUT | /api/tickets/{ticket_id} | Update status and add notes |

### Example — Create Ticket Request:
POST /api/tickets
{
  "customer_name": "Rahul Sharma",
  "customer_email": "rahul@example.com",
  "subject": "Urgent: Refund not processed",
  "description": "I requested a refund 10 days ago and still haven't received it"
}

### Response:
{
  "ticket_id": "TKT-001",
  "created_at": "2026-08-16T09:30:00",
  "status": "Open",
  "urgency": "Critical",
  "category": "Billing"
}

---

## 💻 Local Setup

1. Clone the repository:
   git clone https://github.com/W-Yogita/CRM.git
   cd CRM

2. Create & activate virtual environment:
   # On Windows (PowerShell)
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # On Mac/Linux
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the application:
   uvicorn main:app --reload

5. Open in browser:
   Navigate to http://127.0.0.1:8000

---

## 🚀 Deployment

Deployed on Render:

1. Push code to GitHub repository (W-Yogita/CRM).
2. Go to render.com -> New Web Service.
3. Connect your CRM repository.
4. Set Build Command: pip install -r requirements.txt
5. Set Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
6. Click Create Web Service.

---

## 📋 Database Schema

Tickets Table:
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT UNIQUE,
    customer_name TEXT,
    customer_email TEXT,
    subject TEXT,
    description TEXT,
    status TEXT DEFAULT 'Open',
    urgency TEXT DEFAULT 'Normal',
    category TEXT DEFAULT 'General',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---

## 🎯 Design Decisions & Tradeoffs

- Why keyword-based NLP over LLM?  
  A rule-based keyword classifier provides deterministic, zero-latency triage without API costs or rate limits — making it highly reliable for high-volume support ticket processing.
- Why SQLite over PostgreSQL?  
  SQLite eliminates infrastructure complexity for this application. For enterprise scale (10,000+ tickets/day), PostgreSQL with connection pooling would be the natural upgrade path.
- Why Vanilla JS over React?  
  Keeps the frontend dependency-free, fast-loading, and simple to render directly alongside FastAPI templates.

---

## 🔮 Future Improvements

- [ ] Authentication and role-based access (Admin/Agent)
- [ ] Email notifications on ticket creation and status change
- [ ] Upgrade triage engine to fine-tuned ML classifier
- [ ] Analytics dashboard with resolution time metrics
- [ ] SLA tracking and breach alerts

---

## 👩‍💻 Built By

Yogita Wagh — CS Engineer specializing in AI systems and full-stack development

- GitHub: https://github.com/W-Yogita
- LinkedIn: https://linkedin.com/in/yogita-w-00b131319

---

## 📄 License         

MIT License — feel free to use and modify.                                                                                           
