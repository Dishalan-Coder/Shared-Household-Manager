from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Flatten pydantic's error list into a single readable message so the
    # frontend (which reads err.response.data.detail as plain text) can
    # display it directly under the relevant field/banner.
    messages = []
    for err in exc.errors():
        field = err["loc"][-1] if err.get("loc") else ""
        msg = err.get("msg", "Invalid value")
        # Pydantic v2 prefixes custom ValueErrors with "Value error, "
        msg = msg.replace("Value error, ", "")
        messages.append(f"{field}: {msg}" if field else msg)
    return JSONResponse(status_code=422, content={"detail": "; ".join(messages)})


app.include_router(auth_routes.router)
app.include_router(household_routes.router)
app.include_router(chore_routes.router)
app.include_router(grocery_routes.router)
app.include_router(expense_routes.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "shared-household-manager"}