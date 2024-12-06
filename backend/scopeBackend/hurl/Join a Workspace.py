#Joining a workspace 
POST http://127.0.0.1:8000/api/workspaces/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test888",
    "password": "test888"
}
HTTP 201

POST http://127.0.0.1:8000/api/workspaces/join/  
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json
{
    "name": "test888",
    "password": "test888"
}
HTTP 200

DELETE http://127.0.0.1:8000/api/workspaces/ 
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test888",
    "password": "test888"
}
HTTP 200