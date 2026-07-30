## Assembly Program Executor and Visual Simulator for 8085 Microprocessor

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)

## Overview

The **8085 Microprocessor Simulator** is a software-based application that simulates the architecture and instruction execution of the Intel 8085 microprocessor. It enables users to write, execute, and debug 8085 assembly language programs while visualizing the internal CPU operations in real time.

The simulator provides an interactive environment for understanding how 8085 microprocessor executes instructions through **Fetch–Decode–Execute** cycle. During execution, users can observe updates to registers, flags, memory, the Program Counter (PC), Stack Pointer (SP), Instruction Register (IR), and CPU status.

---

## Features

- Write and execute 8085 assembly language programs.
- Convert assembly instructions into machine code.
- Execute programs using the Fetch–Decode–Execute cycle.
- Step-by-step program execution.
- Real-time visualization of:
  - CPU Registers
  - Memory
  - Flags
  - Program Counter (PC)
  - Stack Pointer (SP)
  - Instruction Register (IR)
  - Execution Cycles
- Display instruction execution trace.
- Reset and reload programs.
- User-friendly web interface.

---

## Project Architecture

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

### Frontend
- React
- JavaScript
- HTML
- CSS
- Axios
- Vite

---

## Project Structure

```text
8085-microprocessor-simulator/
│
├── backend/
│   ├── app/
│   ├── venv/
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── docs/
├── tests/
├── .gitignore
├── conftest.py
├── package.json
├── package-lock.json
├── README.md
└── run_tests.bat
```

---

# How to Run the Project (Windows)

## Prerequisites

Install the following software before running the project.

- Python 3.12 or later
- Node.js (LTS Version)
- Git

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/bramhani007/8085-microprocessor-simulator.git

cd 8085-microprocessor-simulator-main
```

Or download the ZIP file from GitHub and extract it.

---

# Running the Backend

Open the **first terminal**.

### Navigate to the project

```powershell
cd 8085-microprocessor-simulator-main

cd backend
```

### Create a Virtual Environment (First Time Only)

```powershell
python -m venv venv
```

### Activate the Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### Install Required Packages (First Time Only)

```powershell
pip install -r requirements.txt
```

### Return to Project Root

```powershell
cd ..
```

### Start the Backend Server

```powershell
uvicorn backend.app.main:app --reload
```

### Backend API Documentation

Open:

```
http://127.0.0.1:8000/docs
```

---

# Running the Frontend

Open the **second terminal**.

### Navigate to the Frontend Folder

```powershell
cd 8085-microprocessor-simulator-main

cd frontend
```

### Install Dependencies (First Time Only)

```powershell
npm install
```

### Start the Frontend

```powershell
npm run dev
```

### Open the Application

```
http://localhost:5173
```

---

## Technologies Used

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Frontend Framework | React |
| Frontend Language | JavaScript |
| Build Tool | Vite |
| API Communication | Axios |
| Database | SQLite |
| ORM | SQLAlchemy |
| Data Validation | Pydantic |
| Web Server | Uvicorn |
| Version Control | Git |
| Repository | GitHub |

---


---

## Author

**S.Bramhani**

GitHub:
https://github.com/bramhani007
