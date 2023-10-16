
from fastapi import  FastAPI
# import psycopg2

# from psycopg2.extras import RealDictCursor
# import time
from . import  models
from .database import engine
from .routers import user,post,auth, vote
from fastapi.middleware.cors import CORSMiddleware
# models.Base.metadata.create_all(bind=engine)




app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

 

  
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="FastAPI",
#             user="postgres",
#             password="071139456",
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print('Database connection was successfull')
#         break
#     except psycopg2.Error as e:
#         print("Error: Unable to connect to the database")
#         print(e) 
#         time.sleep(4)   

@app.get("/")
def root():
    return {"message": "welcome to my API"}







