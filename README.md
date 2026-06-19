# Campaign Analytics API

A full-stack web application for managing and analysing digital marketing campaigns. Built with Python, Flask, PostgreSQL, and vanilla JavaScript.

🔗 **Live App:** [campaign-api-production-ade3.up.railway.app](https://campaign-api-production-ade3.up.railway.app)

---

## Overview

CampaignIQ lets marketers track campaign performance in real time — CTR, CPL, ROAS, and budget utilisation — calculated automatically from raw campaign data. Built end-to-end: backend API, database design, authentication, and a fully interactive dashboard frontend.

## Features

**Backend**
- RESTful API with full CRUD operations for campaigns
- JWT authentication with bcrypt password hashing
- User ownership — each user only sees their own campaigns
- PostgreSQL with proper relational structure (foreign keys, auto-increment IDs)
- Input validation with detailed error messages
- Environment variable security

**Frontend**
- Dark-themed login/register page with data visualisation preview
- Interactive dashboard with live KPI summary cards
- CTR and Budget vs Spend charts (Chart.js)
- Add/Delete campaigns through a modal form
- Fully responsive, built with vanilla HTML/CSS/JavaScript (no framework)

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Flask-JWT-Extended, Flask-Bcrypt |
| Database | PostgreSQL, SQLAlchemy ORM |
| Frontend | HTML5, CSS3, JavaScript (Fetch API), Chart.js |
| Deployment | Railway (gunicorn production server) |
| Version Control | Git, GitHub |

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/register` | Create new user account | No |
| POST | `/login` | Login and receive JWT token | No |
| GET | `/me` | Get current user info | Yes |
| GET | `/campaigns` | List all campaigns for logged-in user | Yes |
| POST | `/campaigns` | Create a new campaign | Yes |
| GET | `/campaigns/<id>` | Get single campaign with KPIs | Yes |
| PUT | `/campaigns/<id>` | Full update of a campaign | Yes |
| PATCH | `/campaigns/<id>` | Partial update of a campaign | Yes |
| DELETE | `/campaigns/<id>` | Delete a campaign | Yes |

## Project Structure
week2_flask_api/

├── app.py                 # Entry point, routes

├── extensions.py          # db, bcrypt initialisation

├── models/

│   ├── campaign.py        # Campaign SQLAlchemy model

│   └── user.py             # User SQLAlchemy model

├── services/

│   └── analytics.py       # KPI calculations (CTR, CPL, ROAS)

├── utils/

│   └── validators.py      # Input validation

├── routes/

│   └── auth.py             # Register/login routes (Blueprint)

└── frontend/

├── index.html          # Login/register page

├── dashboard.html      # Main dashboard

└── css/style.css       # Shared styles


## Key Engineering Decisions

- **Separation of concerns** — models, services, utils, and routes each have a single responsibility
- **JWT identity-based ownership** — `user_id` is read from the token, never trusted from the request body
- **Auto-generated primary keys** — allows multiple users to have campaigns with the same name
- **Foreign key constraints** — enforced at the database level, not just application logic
- **CORS-enabled** — frontend and backend communicate cleanly across origins

## About the Developer

Built by Mohammad Farooq, a backend developer transitioning from 5+ years in digital marketing and tech consulting. This project applies real marketing domain knowledge (CTR, CPL, ROAS) to a production-style backend system.

[LinkedIn](https://www.linkedin.com/in/farooq11) · [GitHub](https://github.com/farooq1190)
