import uvicorn
from fastapi import FastAPI ,Body, Depends
from app.auth.auth_bearer import JWTBearer
from app.model import UserLoginSchema , UserSchema , PostSchema
from app.auth.auth_handler import signJWT

posts = [
    {
        "id" : 1,
        "title" : "login user",
        "content": "how to login user",
    }
]

users = []

app = FastAPI()



def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False


@app.get("/" , tags=["test"])
def greet():
    return {"Hello" : "World"}

@app.get("/post" , tags = ["get"])
def get_post():
    return {"data" : posts}

@app.get("/post/{id}", tags = ["get"])
def get_one_post(id : int):
    if id>len(posts):
        return {
            "error" : "post with this id does not exist!"
        }
    
    for post in posts:
        if post["id"] == id:
            return {
                "data" : post
            }
        
@app.post("/posts" ,dependencies=[Depends(JWTBearer())],tags= ["posts"])
def add_post(post : PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "info" : "post_added!"
    }

#user signup


@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)


@app.post("/user/login" , tags=["user"])
def user_login(user: UserLoginSchema = Body()):
    if check_user (user):
        return signJWT(user.email)
    else:
        return {
            "error":"invalid login"
        }