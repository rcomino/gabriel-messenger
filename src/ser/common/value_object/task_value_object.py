"""Task Value Object Module"""

from asyncio import Task, Queue
from dataclasses import dataclass
from typing import Optional


@dataclass
class TaskValueObject:
    """Task Value Object. This include task and info of this task. Name is the instance name that is executing in this
    task. State Change Queue is a Queue used to change state of the instance, for example stop the task. Publication
    Queue is queue used by:
        receiver: will put publications (receivers not create a Queue but use Senders queue)
        sender: will get publications of this Queue."""
    name: str
    task: Task
    state_change_queue: Queue
    publication_queue: Optional[Queue] = None
