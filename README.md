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

##  Project Overview

The **Shared Household Manager** is a full-stack web application designed to help housemates efficiently manage shared responsibilities such as chores, grocery lists, and expenses.

##  Objectives

* Simplify household task management
* Enable shared grocery tracking
* Manage and split expenses fairly
* Provide a clear financial balance view

---

##  Technologies Used

### Frontend

* React.js / HTML / CSS / Tailwind CSS

### Backend

* Node.js / FastAPI (if used)

### Database

* MySQL / MongoDB

### Other Tools

* Git & GitHub
* Postman
* Docker (if applicable)

---

##  Key Features

* 👤 User Registration & Login
* 🏠 Create / Join Household Groups
* 📋 Chore Assignment & Tracking
* 🛒 Shared Grocery List
* 💰 Expense Recording
* 📊 Balance Calculation (Who owes whom)

---

##  System Architecture

* Frontend communicates with backend via API
* Backend handles business logic
* Database stores users, chores, groceries, and expenses



##  Workflow

1. User registers/logs in
2. Creates or joins a household
3. Adds chores and assigns members
4. Updates grocery list collaboratively
5. Records shared expenses
6. System calculates balances



##  Challenges Faced

* Managing real-time updates
* Handling expense splitting logic
* Authentication and authorization
* Github workflow
* Backend Frondend connecting

##  Future Improvements

* Mobile application version
* Real-time notifications
* AI-based expense predictions
* Integration with payment gateways



##  Conclusion

This project demonstrates how technology can simplify everyday household management by improving collaboration, transparency, and efficiency among housemates.






## csv file format
```
description,amount,payer,date,split_between
Rent,12000,disha,2024-11-01,"dishalan, adsaya, thulasi"
```