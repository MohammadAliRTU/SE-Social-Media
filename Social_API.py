from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi.responses import JSONResponse
from Social_Backend import Social_Backend

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key="result_key")

@app.get("/")
async def baseic(request: Request):
    response_json = {"status": 200, "data": "OK"}
    response_str = json.dumps(response_json)
    response = JSONResponse(content=response_str, status_code=200)
    return response

@app.post("/sign-up")
async def sign_up(request: Request):
    form_data = await request.json()
    email = form_data["data"].get("email")
    password = form_data["data"].get("password")
    username = form_data["data"].get("username")
    common_id = form_data["data"].get("common_id")
    name = form_data["data"].get("name")
    city = form_data["data"].get("city")
    age = form_data["data"].get("age")
    social_backend = Social_Backend()
    result = social_backend.signup(email, password, username, common_id, name, city, age)
    if result == "Authentication completed":
        response_json = {"status": 200, "data": "User added to the system successfuly"}
        response_str = json.dumps(response_json)
        response = JSONResponse(content=response_str, status_code=422)
        return response
    else:
        response_json = {"status": 422, "data": "Email address or password is not valid."}
        response_str = json.dumps(response_json)
        response = JSONResponse(content=response_str, status_code=422)
        return response
    

@app.post("/sign-in")
async def sign_in(request: Request):
    form_data = await request.json()
    username = form_data["data"].get("email")
    password = form_data["data"].get("password")
    social_backend = Social_Backend()
    result = social_backend.signin(username, password)
    if result == "Authentication completed":
        response_json = {"status": 200, "data": "User signed in successfuly"}
        response_str = json.dumps(response_json)
        response = JSONResponse(content=response_str, status_code=200)
        return response
    else:
        response_json = {"status": 422, "data": "Email address or password is not valid."}
        response_str = json.dumps(response_json)
        response = JSONResponse(content=response_str, status_code=422)
        return response
    
@app.post("/tweet")
async def tweet(request: Request):
    form_data = await request.json()
    tweet = form_data["data"].get("tweet")
    common_id = form_data["data"].get("common_id")
    social_backend = Social_Backend()
    result = social_backend.tweet(common_id, tweet)
    response_json = {"status": 200, "data": result}
    response_str = json.dumps(response_json)
    response = JSONResponse(content=response_str, status_code=200)
    return response

@app.post("/like")
async def like(request: Request):
    form_data = await request.json()
    tweet_number = form_data["data"].get("tweet_number")
    common_id = form_data["data"].get("common_id")
    social_backend = Social_Backend()
    result = social_backend.like(common_id, tweet_number)
    response_json = {"status": 200, "data": result}
    response_str = json.dumps(response_json)
    response = JSONResponse(content=response_str, status_code=200)
    return response

@app.post("/comment")
async def comment(request: Request):
    form_data = await request.json()
    tweet_number = form_data["data"].get("tweet_number")
    comment = form_data["data"].get("comment")
    common_id = form_data["data"].get("common_id")
    social_backend = Social_Backend()
    result = social_backend.comment(common_id, tweet_number, comment)
    response_json = {"status": 200, "data": result}
    response_str = json.dumps(response_json)
    response = JSONResponse(content=response_str, status_code=200)
    return response

@app.post("/follow")
async def follow(request: Request):
    form_data = await request.json()
    follower_common_id = form_data["data"].get("follower_common_id")
    following_common_id = form_data["data"].get("following_common_id")
    social_backend = Social_Backend()
    result = social_backend.follow(follower_common_id, following_common_id)
    response_json = {"status": 200, "data": result}
    response_str = json.dumps(response_json)
    response = JSONResponse(content=response_str, status_code=200)
    return response

@app.post("/search-username")
async def search_username(request: Request):
    form_data = await request.json()
    username = form_data["data"].get("username")
    social_backend = Social_Backend()
    result = social_backend.search_username(username)
    response_json = {"status": 200, "data": result}
    response_str = json.dumps(response_json)
    response = JSONResponse(content=response_str, status_code=200)
    return response

@app.post("/feed-page")
async def feed_page(request: Request):
    form_data = await request.json()
    common_id = form_data["data"].get("common_id")
    social_backend = Social_Backend()
    result = social_backend.feed_page(common_id)
    response_json = {"status": 200, "data": result}
    response_str = json.dumps(response_json)
    response = JSONResponse(content=response_str, status_code=200)
    return response

@app.post("/home-page")
async def home_page(request: Request):
    form_data = await request.json()
    common_id = form_data["data"].get("common_id")
    social_backend = Social_Backend()
    result = social_backend.home_page(common_id)
    response_json = {"status": 200, "data": result}
    response_str = json.dumps(response_json)
    response = JSONResponse(content=response_str, status_code=200)
    return response

@app.post("/tweet-page")
async def tweet_page(request: Request):
    form_data = await request.json()
    tweet_number = form_data["data"].get("tweet_number")
    social_backend = Social_Backend()
    result = social_backend.tweet_page(tweet_number)
    response_json = {"status": 200, "data": result}
    response_str = json.dumps(response_json)
    response = JSONResponse(content=response_str, status_code=200)
    return response


