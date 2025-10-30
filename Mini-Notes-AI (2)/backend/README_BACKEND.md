Setup backend

cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

Endpoints:
POST /notes body {"title":"...","content":"..."}
GET /notes
POST /search body {"query":"...","top_k":3}
GET /health
