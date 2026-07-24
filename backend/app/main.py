from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router


app = FastAPI(

    title="8085 Microprocessor Simulator API",

    description=(

        "Assembly Language Debugger and "

        "Visual Simulator for Intel 8085"

    ),

    version="1.0.0"

)


# =====================================================
# CORS CONFIGURATION
# =====================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:5173",

        "http://127.0.0.1:5173"

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# =====================================================
# ROOT ENDPOINT
# =====================================================

@app.get("/")
def root():

    return {

        "project": (

            "8085 Assembly Language "

            "Debugger and Visual Simulator"

        ),

        "status": "running"

    }


# =====================================================
# REGISTER ROUTES
# =====================================================

app.include_router(router)