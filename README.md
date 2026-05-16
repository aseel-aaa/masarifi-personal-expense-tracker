<p align="center">
  <h1 align="center">Masarifi — Personal Expense Tracker</h1>
  <p align="center">A full-stack web application for managing and tracking personal expenses</p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" />
</p>

---

## About

**Masarifi** is a fully Arabic, RTL web application for tracking and managing personal expenses. It allows users to log daily spending, organize expenses by category, and view detailed chart-based reports to analyze spending patterns.

## Features

- **Google Sign-In** — Secure authentication via Google OAuth 2.0
- **Interactive Dashboard** — Real-time overview with monthly statistics
- **Expense Management** — Quick entry with support for 20+ currencies (USD, ILS, SAR, EGP, and more)
- **Search & Filtering** — Full-text search and category-based filtering
- **Visual Reports** — Doughnut and horizontal bar charts with detailed category breakdown
- **Smart Categories** — Customizable categories with icons
- **Dark Theme UI** — Modern glassmorphism interface with smooth animations
- **Responsive Design** — Optimized for desktop, tablet, and mobile
- **Arabic RTL Layout** — Complete right-to-left interface with Tajawal typography
- **Toast Notifications** — Non-intrusive feedback for all user actions
- **Confirmation Dialogs** — Modal confirmation with backdrop blur before destructive actions

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, FastAPI, Uvicorn |
| **Database** | MongoDB Atlas (Motor async driver) |
| **Authentication** | Google OAuth 2.0, JWT (python-jose) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Charts** | Chart.js |
| **Typography** | Google Fonts (Tajawal) |

## Project Structure

```
personal-expense-tracker/
├── backend/
│   ├── main.py              # Entry point — FastAPI application
│   ├── database.py          # MongoDB connection
│   ├── models.py            # Data models (Pydantic)
│   ├── auth.py              # JWT authentication utilities
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── auth.py           # Authentication routes (Google OAuth)
│       ├── expenses.py       # Expense CRUD routes
│       └── categories.py     # Category management routes
├── frontend/
│   ├── login.html           # Login page
│   ├── index.html           # Dashboard
│   ├── add.html             # Add expense form
│   ├── list.html            # Expense list with search
│   ├── reports.html         # Reports and charts
│   └── css/
│       └── style.css        # Styles (dark theme, glassmorphism, animations)
├── .env                     # Environment variables
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A [MongoDB Atlas](https://www.mongodb.com/atlas) cluster
- A [Google Cloud Console](https://console.cloud.google.com/) project with OAuth 2.0 credentials

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/personal-expense-tracker.git
cd personal-expense-tracker
```

### 2. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
JWT_SECRET=your_jwt_secret_key
BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:8000
```

### 4. Run the Server

```bash
uvicorn backend.main:app --reload --port 8000
```

### 5. Open the Application

Navigate to `http://localhost:8000` in your browser.

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the **Google+ API**
4. Navigate to **Credentials** > **Create Credentials** > **OAuth Client ID**
5. Select **Web Application**
6. Add `http://localhost:8000/auth/callback` under **Authorized redirect URIs**
7. Copy the **Client ID** and **Client Secret** into your `.env` file

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/auth/google` | Initiate Google OAuth flow |
| `GET` | `/auth/callback` | Handle Google OAuth callback |
| `GET` | `/auth/me` | Retrieve current user info |
| `GET` | `/expenses/` | List all expenses |
| `POST` | `/expenses/` | Create a new expense |
| `DELETE` | `/expenses/{id}` | Delete an expense by ID |
| `GET` | `/expenses/stats` | Get monthly statistics |
| `GET` | `/expenses/reports/category` | Get spending report by category |
| `GET` | `/categories/` | List all categories |
| `POST` | `/categories/` | Create a new category |

## Contributing

Contributions are welcome. Feel free to open an **Issue** or submit a **Pull Request** for suggestions and improvements.

## License

This project is licensed under the [MIT License](LICENSE).
