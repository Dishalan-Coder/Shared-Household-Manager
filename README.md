# How to Run
## 1.backend

### create .env file in backend folder

MONGODB_URL=mogodb url of yours
DB_NAME=household_manager
JWT_SECRET=shared-household-manager
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080

```sh
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 2.frontend
```sh
cd frontend
npm install
npm run dev
```
