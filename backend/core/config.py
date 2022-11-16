# import jwt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    root_path="/api",
    title="FLOW-MONITORING",
    description="Exploring seed flow monitoring datapoint",
    version="1.0.0",
    contact={
        "name": "Akvo",
        "url": "https://akvo.org",
        "email": "dev@akvo.org",
    },
    license_info={
        "name": "AGPL3",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    },
)

origins = ["http://localhost:3000"]
methods = ["GET"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
)

# app.include_router(hint_route)


@app.get("/", tags=["Dev"])
def read_main():
    return "OK"


@app.get("/health-check", tags=["Dev"])
def health_check():
    return "OK"


@app.get("/hello")
def read_root():
    return {"Hello": "World"}


# @app.middleware("http")
# async def route_middleware(request: Request, call_next):
#     auth = request.headers.get('Authorization')
#     if auth:
#         auth = jwt.decode(
#             auth.replace("Bearer ", ""), options={"verify_signature": False})
#         request.state.authenticated = auth
#     response = await call_next(request)
#     return response
