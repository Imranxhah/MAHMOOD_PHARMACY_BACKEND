<h1 align="center">Mahmood Pharmacy Backend 💊</h1>
<p align="center">
  <img src="https://img.shields.io/badge/Framework-Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Database-PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" />
</p>

## 📖 Overview
The robust, scalable backend powering **Mahmood Pharmacy** – one of the largest pharmacy chains in Lahore, Pakistan (with 31+ branches). Built on Python & Django REST Framework, this backend acts as the enterprise core, managing everything from inventory, real-time B2C order tracking, rider logistics, to complex analytical queries.

## ✨ Features
- **Enterprise Architecture**: Highly scalable REST API serving thousands of mobile app interactions daily.
- **Order & Logistics engine**: Real-time order processing paired with delivery pipeline updates.
- **Centralized Dashboard**: Extensive admin capabilities for branch and stock management.
- **Authentication**: Secure JWT token-based authentication.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Imranxhah/MAHMOOD_PHARMACY_BACKEND.git
   cd MAHMOOD_PHARMACY_BACKEND
   ```

2. **Set up a Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run Migrations & Start Server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## 🔐 Environment Variables
Make sure to create a `.env` file referencing your Secret Key, Database configuration, and Debug status.

---
*Created by [Imranxhah](https://github.com/Imranxhah)*
