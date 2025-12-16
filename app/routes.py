
from fastapi import APIRouter, HTTPException, status
from app.schemas import TodoCreate, TodoUpdate, TodoResponse
from app.data import todos, counter

router = APIRouter(prefix="/api/v1")

@router.get("/ping")
def ping():
    return {"pong": True}

@router.get("/todos", response_model=list[TodoResponse])
def list_todos():
    return todos

@router.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)
def create_todo(todo: TodoCreate):
    global counter

    new_todo = {
        "id": counter,
        "title": todo.title,
        "completed": todo.completed
    }
    counter += 1
    todos.append(new_todo)
    return new_todo

@router.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo não encontrado")

@router.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, data: TodoUpdate):
    for todo in todos:
        if todo["id"] == todo_id:
            if data.title is not None:
                todo["title"] = data.title
            if data.completed is not None:
                todo["completed"] = data.completed
            return todo
    raise HTTPException(status_code=404, detail="Todo não encontrado")

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(index)
            return
    raise HTTPException(status_code=404, detail="Todo não encontrado")
