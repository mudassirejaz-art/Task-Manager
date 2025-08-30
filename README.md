# 📌 Task Manager

A simple **Task Manager App** built with **FastAPI (backend)** and **Vanilla JavaScript + HTML + CSS (frontend)**. It supports real-time updates using **WebSockets**.

---

## 🚀 Features

* ➕ Add new tasks (title + description)
* ✅ Mark tasks as completed / ❌ pending (toggle)
* 🗑️ Delete tasks
* 🔄 Real-time updates with WebSocket
* 🎨 Clean UI with filters:

  * All tasks
  * Completed tasks
  * Pending tasks

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python)
* **Frontend:** HTML, CSS, Vanilla JavaScript
* **Database:** SQLite (default)
* **Real-time:** WebSockets

---

## 📂 Project Structure

```
📦 task-manager
├── app
│   ├── main.py         # FastAPI app entry point
│   ├── models.py       # Database models
│   ├── database.py     # DB setup (SQLite)
│   └── schemas.py      # Pydantic schemas
├── static
│   └── app.js          # Frontend logic
├── templates
│   └── index.html      # Main UI
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/mudassirejaz-art/Task-Manager.git
cd task-manager
```

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

Server will start at 👉 `http://127.0.0.1:8000`

---

## 🖥️ Usage

1. Open browser and go to `http://127.0.0.1:8000`
2. Add a new task (title + description)
3. Click on a task to toggle between completed ✅ / pending ❌
4. Use delete button to remove a task
5. Use filters to view All / Completed / Pending tasks

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo and submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License**.
