#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import os
from datetime import datetime

TASK_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4, default=str)

def add_task(title, due_date, priority):
    tasks = load_tasks()
    tasks.append({
        "task": title,
        "completed": False,
        "due_date": due_date,
        "priority": priority
    })
    save_tasks(tasks)

def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)

def toggle_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = not tasks[index]["completed"]
        save_tasks(tasks)

def get_filtered_tasks(filter_type):
    tasks = load_tasks()
    if filter_type == "All":
        return tasks
    elif filter_type == "Completed":
        return [t for t in tasks if t["completed"]]
    elif filter_type == "Pending":
        return [t for t in tasks if not t["completed"]]
    return tasks

