# 🔐 Enigma I Machine

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)

A modern web-based implementation of the historic Enigma machine, built with FastAPI and Python. This project brings the fascinating world of WWII cryptography to life in a user-friendly interface.

## ✨ Features

- **Authentic Enigma Implementation**: 
  - Complete rotor mechanism with historically accurate configurations
  - Multiple rotor selections (I-V)
  - Reflectors (A, B, C)
  - Configurable ring settings
  - Plugboard connections

- **Modern Web Interface**:
  - Interactive web-based UI
  - Real-time encoding/decoding
  - Mobile-responsive design

## 🛠️ Technology Stack

- **Backend**:
  - FastAPI (v0.115.11) - Modern, fast web framework
  - Python 3.x
  - Mangum (v0.19.0) - AWS Lambda compatibility
  - Jinja2 (v3.1.4) - Template engine

- **Frontend**:
  - HTML/CSS
  - Jinja2 Templates

## 🚀 Getting Started

1. **Clone the repository**
```bash
git clone https://github.com/Jventajas/enigma-machine.git
cd enigma-machine
```

2. **Set up a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
uvicorn main:app --reload
```

5. **Visit the application**
   - Open your browser and navigate to `http://localhost:8000`

## 🎯 How It Works

The Enigma machine consists of several key components:

1. **Rotors**: The machine uses three rotors chosen from five available options (I-V). Each rotor performs a substitution cipher and rotates with each keystroke.

2. **Reflector**: After passing through all three rotors, the signal is reflected back through the rotors in reverse order, ensuring the encryption is reciprocal.

3. **Plugboard**: Allows for additional letter swapping before and after the main encryption process.
