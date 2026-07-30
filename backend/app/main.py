from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router


# =====================================================
# CREATE FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="8085 Microprocessor Simulator API",
    description=(
        "Assembly Program Executor and "
        "Visual Simulator for Intel 8085"
    ),
    version="1.0.0",
)


# =====================================================
# CORS CONFIGURATION
# =====================================================

app.add_middleware(
    CORSMiddleware,

    # Allow requests from all origins (for development and deployment)
    allow_origins=["*"],

    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# ROOT ENDPOINT
# =====================================================

@app.get("/")
def root():
    return {
        "project": "8085 Assembly Program Executor and Visual Simulator",
        "status": "running",
    }


# =====================================================
# HEALTH CHECK ENDPOINT
# =====================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "8085 Microprocessor Simulator API",
    }


# =====================================================
# REGISTER SIMULATOR API ROUTES
# =====================================================

app.include_router(router)