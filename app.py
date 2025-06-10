import streamlit as st
import pandas as pd
import numpy as np
from models import Employee, Task, TaskPriority, Skill, SkillLevel
from task_assignment import TaskAssignmentSystem

# Initialize the task assignment system
if 'task_system' not in st.session_state:
    st.session_state.task_system = TaskAssignmentSystem()

# Set page configuration
st.set_page_config(
    page_title="Task Management System",
    page_icon="✨",
    layout="wide"
)

# Add a title and description
st.title("Task Management System")
st.markdown("Manage employees and tasks efficiently")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Task Management", "Employee Management", "Task Assignment"])

# Main content area
if page == "Task Management":
    st.header("Task Management")
    
    # Add new task form
    with st.expander("Add New Task", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            task_id = st.text_input("Task ID")
            task_name = st.text_input("Task Name")
            priority = st.selectbox("Priority", [p.name for p in TaskPriority])
            estimated_hours = st.number_input("Estimated Hours", min_value=1.0, value=8.0)
        
        with col2:
            deadline_days = st.number_input("Deadline (days)", min_value=1, value=7)
            required_skills = st.multiselect(
                "Required Skills",
                ["Python", "JavaScript", "SQL", "React", "Docker", "AWS"],
                default=[]
            )
            skill_levels = {
                skill: st.selectbox(
                    f"{skill} Level",
                    [level.name for level in SkillLevel],
                    key=f"skill_{skill}"
                )
                for skill in required_skills
            }
        
        if st.button("Add Task"):
            if task_id and task_name:
                required_skills_dict = {
                    skill: SkillLevel[level]
                    for skill, level in skill_levels.items()
                }
                task = Task(
                    task_id=task_id,
                    name=task_name,
                    required_skills=required_skills_dict,
                    priority=TaskPriority[priority],
                    estimated_hours=estimated_hours,
                    deadline_days=deadline_days
                )
                st.session_state.task_system.add_task(task)
                st.success(f"Task '{task_name}' added successfully!")
            else:
                st.error("Please fill in all required fields")

    # Display existing tasks
    st.subheader("Current Tasks")
    tasks_data = []
    for task in st.session_state.task_system.tasks.values():
        tasks_data.append({
            "Task ID": task.task_id,
            "Name": task.name,
            "Priority": task.priority.name,
            "Hours": task.estimated_hours,
            "Deadline": f"{task.deadline_days} days",
            "Assigned To": task.assigned_to or "Unassigned",
            "Status": "Completed" if task.is_completed else "Pending"
        })
    
    if tasks_data:
        st.dataframe(pd.DataFrame(tasks_data))
    else:
        st.info("No tasks added yet")

elif page == "Employee Management":
    st.header("Employee Management")
    
    # Add new employee form
    with st.expander("Add New Employee", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            emp_id = st.text_input("Employee ID")
            emp_name = st.text_input("Employee Name")
            max_workload = st.number_input("Max Workload Hours", min_value=20.0, value=40.0)
        
        with col2:
            skills = st.multiselect(
                "Skills",
                ["Python", "JavaScript", "SQL", "React", "Docker", "AWS"],
                default=[]
            )
            skill_details = {
                skill: {
                    "level": st.selectbox(
                        f"{skill} Level",
                        [level.name for level in SkillLevel],
                        key=f"emp_skill_{skill}"
                    ),
                    "experience": st.number_input(
                        f"{skill} Experience (years)",
                        min_value=0.0,
                        value=1.0,
                        key=f"exp_{skill}"
                    )
                }
                for skill in skills
            }
        
        if st.button("Add Employee"):
            if emp_id and emp_name:
                employee_skills = [
                    Skill(
                        name=skill,
                        level=SkillLevel[details["level"]],
                        experience_years=details["experience"]
                    )
                    for skill, details in skill_details.items()
                ]
                employee = Employee(
                    emp_id=emp_id,
                    name=emp_name,
                    skills=employee_skills,
                    max_workload_hours=max_workload
                )
                st.session_state.task_system.add_employee(employee)
                st.success(f"Employee '{emp_name}' added successfully!")
            else:
                st.error("Please fill in all required fields")

    # Display existing employees
    st.subheader("Current Employees")
    employees_data = []
    for emp in st.session_state.task_system.employees.values():
        employees_data.append({
            "Employee ID": emp.emp_id,
            "Name": emp.name,
            "Skills": ", ".join(emp.skills.keys()),
            "Current Workload": f"{emp.current_workload}/{emp.max_workload_hours} hours",
            "Assigned Tasks": len(emp.assigned_tasks)
        })
    
    if employees_data:
        st.dataframe(pd.DataFrame(employees_data))
    else:
        st.info("No employees added yet")

elif page == "Task Assignment":
    st.header("Task Assignment")
    
    # Task assignment interface
    if st.session_state.task_system.tasks:
        task_id = st.selectbox(
            "Select Task",
            [task.task_id for task in st.session_state.task_system.tasks.values() if not task.assigned_to]
        )
        
        if task_id:
            st.subheader("Assignment Recommendations")
            task = st.session_state.task_system.tasks[task_id]
            matches = st.session_state.task_system.find_best_matches(task)
            
            for i, (employee, probability) in enumerate(matches, 1):
                with st.expander(f"{i}. {employee.name} (Match: {probability:.1%})"):
                    st.write(f"Current Workload: {employee.current_workload}/{employee.max_workload_hours} hours")
                    st.write(f"Skills: {', '.join(employee.skills.keys())}")
                    
                    if st.button(f"Assign to {employee.name}", key=f"assign_{i}"):
                        if st.session_state.task_system.assign_task(task_id, employee.emp_id):
                            st.success(f"Task assigned to {employee.name}")
                            st.rerun()
                        else:
                            st.error("Assignment failed")
    else:
        st.info("No unassigned tasks available")

# Add a footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit") 