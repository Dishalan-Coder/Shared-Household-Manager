from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth_routes, household_routes, chore_routes, grocery_routes, expense_routes

app = FastAPI(title="Shared-Household Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(household_routes.router)
app.include_router(chore_routes.router)
app.include_router(grocery_routes.router)
app.include_router(expense_routes.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "shared-household-manager"}