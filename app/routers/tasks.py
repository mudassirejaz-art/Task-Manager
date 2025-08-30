from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select as sql_select
from datetime import datetime
from typing import List
import asyncio

from app.db import get_session
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate, TaskOut
from app.pubsub import get_pubsub, PubSub

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_session),
    pubsub: PubSub = Depends(get_pubsub),
):
    task = Task(
        title=task_in.title,
        description=task_in.description,
        completed=task_in.completed
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)

    payload = {
        "type": "task.created",
        "task": {**task.dict(), "created_at": str(task.created_at), "updated_at": str(task.updated_at)}
    }
    asyncio.create_task(pubsub.publish("tasks", payload))
    return task

@router.get("", response_model=List[TaskOut])
async def list_tasks(session: AsyncSession = Depends(get_session)):
    result = await session.exec(sql_select(Task))
    return result.all()

@router.patch("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    task_in: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    pubsub: PubSub = Depends(get_pubsub),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    changed = False
    if task_in.title is not None:
        task.title = task_in.title; changed = True
    if task_in.description is not None:
        task.description = task_in.description; changed = True
    if task_in.completed is not None:
        task.completed = task_in.completed; changed = True

    if changed:
        task.updated_at = datetime.utcnow()
        session.add(task)
        await session.commit()
        await session.refresh(task)

        payload = {
            "type": "task.updated",
            "task": {**task.dict(), "created_at": str(task.created_at), "updated_at": str(task.updated_at)}
        }
        asyncio.create_task(pubsub.publish("tasks", payload))

    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    pubsub: PubSub = Depends(get_pubsub),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()

    payload = {"type": "task.deleted", "task": {"id": task_id}}
    asyncio.create_task(pubsub.publish("tasks", payload))
