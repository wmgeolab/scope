#Delete a workspace 
POST http://{{host}}/api/workspaces/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test888",
    "password": "test888"
}
HTTP 201

DELETE http://{{host}}/api/workspaces/ 
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test888",
    "password": "test888"
}
HTTP 200