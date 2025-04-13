#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from datetime import datetime
from todo import add_task, delete_task, toggle_task, get_filtered_tasks, load_tasks

st.set_page_config(page_title="To-Do List", page_icon="✅")

st.title("🧠 To-Do List Pro Max")
st.caption("Organize your chaos. One checkbox at a time.")

# --- Add a new task ---
with st.form("add_task_form", clear_on_submit=True):
    task_title = st.text_input("Task", placeholder="E.g. Complete ML project")
    due_date = st.date_input("Due Date", value=datetime.today())
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if task_title.strip():
            add_task(task_title.strip(), str(due_date), priority)
            st.success("Task added!")
        else:
            st.warning("Bruh, type the actual task.")

# --- Filter tasks ---
st.markdown("### Filters")
filter_type = st.radio("Show:", ["All", "Pending", "Completed"], horizontal=True)

# --- Load tasks ---
all_tasks = load_tasks()
filtered_tasks = get_filtered_tasks(filter_type)

# --- Initialize toggle session state ---
if "toggle_states" not in st.session_state:
    st.session_state.toggle_states = {}

# --- Display tasks ---
st.markdown("### Your Tasks")
if filtered_tasks:
    for task in filtered_tasks:
        task_id = all_tasks.index(task)

        # Sync checkbox state with actual task status
        if task_id not in st.session_state.toggle_states:
            st.session_state.toggle_states[task_id] = task["completed"]

        col1, col2, col3, col4 = st.columns([0.08, 0.55, 0.25, 0.12])

        with col1:
            checked = st.checkbox("", value=st.session_state.toggle_states[task_id], key=f"cb_{task_id}")
            if checked != task["completed"]:
                toggle_task(task_id)
                st.session_state.toggle_states[task_id] = checked
                st.experimental_rerun()

        with col2:
            title = f"~~{task['task']}~~" if task['completed'] else task['task']
            st.markdown(f"{title}  \n🗓️ {task['due_date']} | 🔥 {task['priority']}")

        with col3:
            status = "✅ Completed" if task["completed"] else "⏳ Pending"
            st.markdown(f"<span style='color:gray'>{status}</span>", unsafe_allow_html=True)

        with col4:
            if st.button("❌", key=f"delete_{task_id}"):
                delete_task(task_id)
                st.session_state.toggle_states.pop(task_id, None)
                st.experimental_rerun()
else:
    st.info("No tasks in this category yet. Go do something!")

st.markdown("---")
st.caption("Made by Hritik, polished by caffeine ☕")

