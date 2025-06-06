from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, users, contact, travels, bookings
from api.database.connection import engine
from api.database.base import Base

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Accept requests from any origin (you can restrict to ["http://localhost:3000"] for dev)
    allow_credentials=True,        # Allow sending cookies/headers
    allow_methods=["*"],           # Accept all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],           # Accept all HTTP headers
)


app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# User Routes (User CRUD operations)
app.include_router(users.router, prefix="/users", tags=["Users"])

# Contact/Support Routes (Submit inquiries, messages)
app.include_router(contact.router, prefix="/contact", tags=["Contact"])

app.include_router(travels.router, prefix="/travels", tags=["Travels"])

app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])

