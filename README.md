# Campaign Analytics API

A REST API for managing and analysing digital marketing campaigns.

## Live URL
https://campaign-api-production-ade3.up.railway.app

## Tech Stack
- Python + Flask
- PostgreSQL + SQLAlchemy
- JWT Authentication
- Deployed on the railway

## Endpoints
- POST /register — create account
- POST /login — get JWT token
- GET /campaigns — list all campaigns
- POST /campaigns — create campaign (auth required)
- GET /campaigns/<id> — get campaign report
- PUT /campaigns/<id> — update campaign (auth required)
- PATCH /campaigns/<id> — partial update (auth required)
- DELETE /campaigns/<id> — delete campaign (auth required)
