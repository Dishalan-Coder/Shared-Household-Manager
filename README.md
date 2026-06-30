# How to Run


### create .env file in backend folder

MONGODB_URL=mogodb url of yours
DB_NAME=household_manager
JWT_SECRET=shared-household-manager
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080

## 1.backend
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

The **Shared Household Manager** is a full-stack web application developed to help housemates manage shared responsibilities efficiently. It allows users to collaborate on chores, maintain a shared grocery list, and track expenses with automatic balance calculation.

---

##  Objectives

* Provide a centralized platform for housemates
* Improve task and responsibility management
* Ensure transparent expense tracking
* Reduce conflicts through clear financial insights

---

##  Technologies Used

### Frontend

* React.js
* Tailwind CSS

### Backend

* FastAPI (Python)

### Database

* MongoDB (with Motor for async operations)

### Other Tools

* Git & GitHub
* Postman (API testing)
* Uvicorn (ASGI server)

---

##  Key Features

*  User Authentication (Register/Login)
*  Household Creation & Joining System
*  Chore Assignment with Due Dates
*  Shared Grocery List (Add / Mark Complete)
*  Expense Tracking (Who Paid & Split Logic)
*  Automatic Balance Calculation (Who owes whom)

---

##  System Architecture

* **Frontend (React):** Handles UI and user interactions
* **Backend (FastAPI):** Manages API requests and business logic
* **Database (MongoDB):** Stores users, households, chores, groceries, and expenses

The system follows a **REST API architecture**, where the frontend communicates with the backend via HTTP requests.

---

##  Workflow

1. User registers and logs into the system
2. User creates or joins a household group
3. Members add and assign chores
4. Users update the shared grocery list
5. Expenses are recorded with payer details
6. The system calculates and displays balances





##  Challenges Faced

* Handling asynchronous database operations using Motor
* Designing accurate expense-splitting logic
* Managing authentication and session handling
* Ensuring proper API structure and error handling
* Backend and Frontend connecting



##  Future Improvements

* Mobile application (React Native)
* Real-time updates using WebSockets
* Notifications for chores and payments
* Integration with online payment systems

---

## Conclusion

The **Shared Household Manager** simplifies everyday household coordination by improving collaboration, transparency, and efficiency. It demonstrates strong full-stack development skills and practical problem-solving.

---

