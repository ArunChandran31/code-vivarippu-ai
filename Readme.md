# Code விவரிப்பு AI

A modern AI‑powered code analysis tool that provides instant static analysis, AI‑generated feedback, and code insights using multi‑model backend support (OpenAI, Claude, Groq/Llama‑3, Mock mode).

---

## 🚀 Overview

**Code விவரிப்பு AI** is a full‑stack project built to intelligently analyze code and return meaningful insights such as:

* Summary of code
* Potential issues
* Complexity evaluation
* Style & best‑practice improvements
* Suggestions for cleaner, efficient code

The system combines **local static analysis + AI LLM evaluation**, providing a detailed merged result.

---

## ✨ Features

* 🔍 **Static Code Analysis** (local Python analyzer)
* 🤖 **AI‑Powered Review** (supports OpenAI, Claude, Groq Llama‑3)
* 🎭 **Mock Mode** (free use without API keys)
* 🖥️ **Beautiful Frontend UI** made with Vue 3 + Tailwind CSS
* 🧭 **Review Page** with JSON‑formatted outputs
* 📄 **PDF Export** (optional)
* 🔐 **Optional Firebase Auth**
* 📊 **Admin Page for Token Usage**
* 🍃 **MongoDB Database** for saving review history

---

## 🏗️ Tech Stack

### **Frontend**

* Vue 3 (Composition API)
* Vite
* Tailwind CSS
* Custom UI Components

### **Backend**

* FastAPI (Python)
* Async AI Engine
* MongoDB Atlas
* Groq / OpenAI / Claude API integrations

---

## 🖼️ Screenshots

### **Home Page UI**

!(../project_images/img1.png)
!(../project_images/img2.png)
---

## 📦 Installation

### **1. Backend Setup**

```bash
git clone <repo-url>
cd backend
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```

### **2. Environment Variables**

Create **backend/.env**:

```
MODEL_PROVIDER=groq
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama3-70b-versatile
MONGO_URI=your_mongo_uri
CORS_ORIGINS=http://localhost:5173
```

### **3. Run Backend**

```bash
uvicorn app:app --reload --port 8000
```

### **4. Run Frontend**

```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Mock Mode (No API Needed)

Enable mock mode by setting:

```
MODEL_PROVIDER=mock
```

This lets the app run **free** without external API keys.

---

## 📝 Project Functionality

* Paste your code into the big editor.
* Select programming language or auto‑detect.
* Click **→** to get:

  * Static analyzer results
  * AI model insights
  * Token usage
* View all results neatly displayed in Review Page.

---

## 👨‍💻 Author

**Arun Chandran**

* Portfolio: creviro.io
* Instagram: @creviro.io

---

## ⭐ Contribute

Feel free to fork the project and raise PRs.

If this helped you, give the repo a ⭐!

---

## 📄 License

This project is for educational & portfolio use.
