<div align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Python-3670A0?logo=python&logoColor=ffdd54" alt="Python">
    </a>
    <a href="https://fastapi.tiangolo.com/">
        <img src="https://img.shields.io/badge/FastAPI-005571?logo=fastapi" alt="Fastapi">
    </a>
    <a href="https://www.postgresql.org/">
        <img src="https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white" alt="PostgreSQL">
    </a>
</div>

<br/>

# 🛒 Real-Time Product Reservation System

A robust backend service for managing product reservations with concurrency-safe logic, reservation timeouts, and atomic stock management.

---

## 📁 Project Structure

```bash
product_reservation/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── reservation.py
│   │   │   │   ├── product.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── scheduler.py         # for reservation timeouts
│   │
│   ├── domain/
│   │   ├── models/
│   │   │   ├── product.py
│   │   │   ├── reservation.py
│   │   │   ├── order.py
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── reservation_service.py
│   │   │   ├── stock_service.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── repositories/
│   │   ├── product_repository.py
│   │   ├── reservation_repository.py
│   │   ├── order_repository.py
│   │   └── __init__.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── product.py
│   │   ├── reservation.py
│   │   ├── order.py
│   │   └── __init__.py
│   │
│   ├── main.py
│   └── __init__.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── requirements.txt
└── README.md

## ⚙️ Requirements
- [Python 3.11](https://www.python.org/downloads/release/python-3110/)

## 🔌 Run Locally

Prerequisite installations
- python3.9 or higher
- virtual environment (venv)

Clone the project

```bash
  git clone https://github.com/shivambits2021/ReservationService.git
```

Create virtual environment

```bash
  virtualenv venv
```

Activate venv in linux

```bash
  source venv/bin/activate
```

Activate venv in windows

```bash
  venv\Scripts\activate
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Start the server

```bash
  uvicorn app.main:app
```

## 👷 Authors

- [Shivam Pratap](https://www.linkedin.com/in/shivam-p-64a17615a)