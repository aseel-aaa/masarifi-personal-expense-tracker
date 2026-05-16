<p align="center">
  <h1 align="center">Masarifi — Personal Expense Tracker</h1>
  <p align="center">A modern, Arabic-first full-stack web application for managing personal expenses.</p>
</p>

## Overview

**Masarifi** is a RTL (Right-to-Left) expense tracker built with FastAPI and MongoDB. It features a sleek glassmorphism dark theme and helps users visualize their spending habits through interactive charts.

## Key Features

- **Arabic RTL Interface** — Optimized for Arabic speakers with Tajawal typography.
- **Google Authentication** — Secure login via OAuth 2.0.
- **Visual Analytics** — Spending reports using Chart.js.
- **Expense Management** — Easy tracking with multi-currency support.
- **Modern UI** — Responsive design with dark mode and smooth animations.

## Tech Stack

- **Backend:** Python (FastAPI), MongoDB
- **Frontend:** HTML/CSS/JS (Vanilla)
- **Design:** Glassmorphism, Dark Theme, RTL

## Getting Started

1. **Clone & Setup:**
   ```bash
   git clone https://github.com/aseel-aaa/masarifi-personal-expense-tracker.git
   cd personal-expense-tracker
   pip install -r backend/requirements.txt
   ```

2. **Configure:**
   Create a `.env` file with your `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `MONGODB_URL`, and `JWT_SECRET`.

3. **Run:**
   ```bash
   uvicorn backend.main:app --reload
   ```

Open `http://localhost:8000` to start tracking!


## License

This project is licensed under the [MIT License](LICENSE).
