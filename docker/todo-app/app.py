from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
import json
from fastapi.middleware.cors import CORSMiddleware

DATA_DIR = Path("/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

todo_file_path = DATA_DIR / "todos.json"

# Initialize FastAPI app
app = FastAPI(title="ToDo API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for ToDo items
class TodoItem(BaseModel):
    id: Optional[int] = None
    title: str
    completed: bool = False

# Helper functions
def load_todos() -> List[dict]:
    try:
        with open(todo_file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_todos(todos: List[dict]):
    with open(todo_file_path, "w") as f:
        json.dump(todos, f, indent=4)

# API endpoints
@app.get("/todos", response_model=List[TodoItem])
async def get_todos():
    return load_todos()

@app.post("/todos", response_model=TodoItem)
async def create_todo(todo: TodoItem):
    todos = load_todos()
    
    # Generate new ID
    if todos:
        new_id = max(todo["id"] for todo in todos) + 1
    else:
        new_id = 1
    
    todo_dict = todo.model_dump()
    todo_dict["id"] = new_id
    todos.append(todo_dict)
    save_todos(todos)
    return todo_dict

@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, todo: TodoItem):
    todos = load_todos()
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            todo_dict = todo.model_dump()
            todo_dict["id"] = todo_id
            todos[i] = todo_dict
            save_todos(todos)
            return todo_dict
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    todos = load_todos()
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            save_todos(todos)
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
