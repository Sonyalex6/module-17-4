from fastapi import APIRouter, Depends, status, HTTPException, FastAPI
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import Task
from app.models.user import User
from app.schemas import CreateUser, UpdateUser, CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify
router = APIRouter(prefix='/task', tags=['task'])
@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
  tasks = db.scalars(select(Task)).all()
  if tasks is None:
    return HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='There are no users'
    )
  return tasks
@router.get('/task_id')
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
  task = db.scalars(select(User).where(User.id == task_id))
  if task_id is None:
    return HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='User was not found'
    )
  return task
@router.post('/create')
async def create_task(create: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
  user = db.scalars(select(User).where(User.id == user_id)).first()
  if user is None:
    return HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='User was not found'
    )
  db.execute(insert(Task).values(
    title=create.title,
    content=create.content,
    priority=create.priority,
    user_id=user_id,
    slug=slugify(create.title)
  ))
  db.commit()
  return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
@router.put('/update')
async def update_task(task_update: UpdateTask, id: int, db: Annotated[Session, Depends(get_db)]):
  update_task = db.scalars(select(Task).where(Task.user_id == id)).first()
  if update_task is None:
    return HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='User was not found'
    )
  db.execute(update(Task).where(Task.user_id == id).values(
    firstname=task_update.firstname,
    lastname=task_update.lastname,
    age=task_update.age
  ))
  db.commit()
  return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
@router.put('/delete')
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
  delete_task = db.scalars(select(Task).where(Task.id == task_id)).first()
  if delete_task is None:
    return HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='User was not found'
    )
  db.execute(delete(Task).where(Task.id == task_id))
  db.commit()
  return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is succ
