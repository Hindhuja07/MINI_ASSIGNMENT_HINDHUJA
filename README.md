# MINI_ASSIGNMENT_HINDHUJA
README.md — Notes Manager with Semantic Search
Project Overview

This project is a small full-stack web application that allows users to create, store, and search their notes based on semantic similarity.
The goal is to demonstrate backend API design, database schema planning, text similarity logic, and frontend-backend integration using a simple, self-contained setup.

Tech Stack

Backend: FastAPI (Python)
Frontend: React.js
Database: SQLite using SQLModel
Search Logic: Text embedding and cosine similarity for semantic matching

Features

Create and store notes with title and content

View all saved notes

Search notes by meaning rather than just keywords

Store text representations in the database for later comparison

Minimal React frontend for adding and viewing notes

MINI-NOTES-AI/
│
├── backend/
│   ├── database.py
│   ├── main.py
│   ├── model.py
│   ├── requirements.txt
│   └── README_BACKEND.md
│
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
│
├── Declaration.md
├── notes.md
└── Readme.md


Setup Instructions
1. Clone the Repository
git clone https://github.com/Hindhuja07/notes-manager.git
cd notes-manager

2. Backend Setup (FastAPI)

Step 1: Create and activate a virtual environment

cd backend
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate


Step 2: Install dependencies

pip install -r requirements.txt


Your requirements.txt should include:

fastapi
uvicorn
sqlmodel
numpy
scikit-learn


Step 3: Run the backend

uvicorn main:app --reload


The backend will run at:
http://127.0.0.1:8000

API documentation is available at:
http://127.0.0.1:8000/docs

3. Frontend Setup (React.js)

Step 1: Install dependencies

cd ../frontend
npm install


Step 2: Start the frontend

npm start


The React app will be available at:
http://localhost:3000

Ensure the backend is running on port 8000 before using the frontend.

API Endpoints
Method  Endpoint    Descrip
tionPOST    /notes  Create a new note (title and 
content)GET /notes  Retrieve 
all notesPOST    /search Search notes using tex
t similarity

Search LogicEach note’s title and content are converted into a numerical vector representation based on te
xt features.These vectors are stored in the database as J
SON strings.When a search query is entered, it is converted into a similar vector rep
resentation.Cosine similarity is then calculated between the query vector and each note vector to determine how closely
 they match.The most relevant notes are returned in descending order of

 similarity.This simple semantic matching approach allows the search to understand meaning beyond exact keyw

ord matches.Improvements an

d Next StepsUse a vector database or optimized index for faster simila

rity search.Add user authentication (JWT o

r sessions).Add tagging or categorization for better note o

rganization.Include tests and containerization for easier

 deploy

ment.SummaryThe Notes Manager demonstrates how to design a clear backend API, plan a database schema, implement semantic search logic, and connect everything with a function
al frontend.The focus is on simplicity, correctness, and clarity of design rather than advanced infrastructure o
r libraries.
