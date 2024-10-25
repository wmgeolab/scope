#Create a workspace 
POST http://127.0.0.1:8000/api/workspaces/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test222",
    "password": "test222"
}
HTTP 201

DELETE http://127.0.0.1:8000/api/workspaces/ 
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test222",
    "password": "test222"
}
HTTP 200

#Get all workspaces that a user is in 
GET http://127.0.0.1:8000/api/workspaces/ 
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json
HTTP 201

#Delete a workspace 
POST http://127.0.0.1:8000/api/workspaces/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test222",
    "password": "test222"
}
HTTP 201

DELETE http://127.0.0.1:8000/api/workspaces/ 
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test222",
    "password": "test222"
}
HTTP 200

#Add a tag to a workspace 
POST http://127.0.0.1:8000/api/workspaces/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test222",
    "password": "test222"
}
HTTP 201
[Captures]
workspace: jsonpath "$.workspace"

POST http://127.0.0.1:8000/api/tags/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "workspace": {{workspace}}, 
    "tag": "tag"
}
HTTP 201

DELETE http://127.0.0.1:8000/api/workspaces/ 
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test222",
    "password": "test222"
}
HTTP 200

#Joining a workspace 
POST http://127.0.0.1:8000/api/workspaces/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test222",
    "password": "test222"
}
HTTP 201

GET http://127.0.0.1:8000/api/workspaces/join/  
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json
{
    "name": "test222",
    "password": "test222"
}
HTTP 201

DELETE http://127.0.0.1:8000/api/workspaces/ 
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test222",
    "password": "test222"
}
HTTP 200