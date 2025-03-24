#Getting all tags from a specified workspace 
POST http://{{host}}/api/workspaces/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test888",
    "password": "test888"
}
HTTP 201
[Captures]
id: jsonpath "$.id"

POST http://{{host}}/api/tags/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "workspace": {{id}}, 
    "tag": "tag1",
    "tag": "tag2"
}
HTTP 201


GET http://{{host}}/api/tags/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "workspace": {{id}}
}

HTTP 200

DELETE http://{{host}}/api/tags/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "workspace": {{id}}, 
    "tag": "tag1",
    "tag": "tag2"
}
HTTP 200

DELETE http://{{host}}/api/workspaces/ 
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test888",
    "password": "test888"
}
HTTP 200