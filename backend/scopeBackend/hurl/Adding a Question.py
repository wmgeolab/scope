# Delete the test workspace
DELETE http://{{host}}/api/workspaces/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test888",
    "password": "test888"
}
HTTP 200

# Create a workspace for testing
POST http://{{host}}/api/workspaces/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test888",
    "password": "test888"
}
HTTP 201
[Captures]
workspace_id: jsonpath "$.id"

# Add a question to the workspace
POST http://{{host}}/api/questions/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "workspace": {{workspace_id}},  
    "text": "What is the purpose of this workspace?",
    "source": "279"
}
HTTP 201
[Captures]
question_id: jsonpath "$.id"

# Retrieve all questions from the workspace
GET http://{{host}}/api/questions/?workspace={{workspace_id}}
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
HTTP 200

# Delete the question
DELETE http://{{host}}/api/questions/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "id": {{question_id}}
}
HTTP 200

# Delete the test workspace
DELETE http://{{host}}/api/workspaces/
Authorization: Token fadc41688e2228acb6c2cd435362f4eda6f4130d
Content-Type: application/json

{
    "name": "test888",
    "password": "test888"
}
HTTP 200
