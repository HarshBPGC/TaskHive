import streamlit as st
import pandas as pd
from models import Employee, Task, TaskPriority, Skill, SkillLevel
from task_assignment import TaskAssignmentSystem

# Initialize the task assignment system
if 'task_system' not in st.session_state:
    st.session_state.task_system = TaskAssignmentSystem()

# Set page configuration
st.set_page_config(
    page_title="Task Assignment System",
    page_icon="✨",
    layout="wide"
)

# Add custom CSS for white background and purple text
st.markdown("""
    <style>
    .stApp {
        background: #ffffff;
        color: #4B1FA6;
    }
    .stSidebar {
        background-color: #4B1FA6;
        color: #ffffff;
        transition: background-color 0.3s, color 0.3s;
    }
    .stSidebar * {
        color: #ffffff !important;
        transition: color 0.3s;
    }
    section[data-testid="stSidebar"] {
        min-width: 200px !important;
        max-width: 220px !important;
        width: 200px !important;
        transition: width 0.3s, background-color 0.3s;
    }
    .stButton>button {
        background-color: #4B1FA6;
        color: white;
        transition: background-color 0.3s, color 0.3s;
    }
    .stButton>button:hover {
        background-color: #32106b;
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #4B1FA6;
        transition: color 0.3s;
    }
    .stMarkdown, .stDataFrame, .stMetric {
        color: #4B1FA6;
        transition: color 0.3s;
    }
    header[data-testid="stHeader"] {
        background-color: #4B1FA6 !important;
        transition: background-color 0.3s;
    }
    header[data-testid="stHeader"] * {
        color: white !important;
        transition: color 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# Display the logo at the top of the app
logo_path = "noqs_logo.png"
st.image(logo_path, width=220)

# Add a title and description
st.title("Task Assignment System")
st.markdown("Intelligent task assignment using advanced algorithms")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Employee Management", "Task Management", "Task Assignment"])

# Dashboard page
if page == "Dashboard":
    st.header("📊 Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_employees = len(st.session_state.task_system.employees)
    total_tasks = len(st.session_state.task_system.tasks)
    assigned_tasks = sum(1 for task in st.session_state.task_system.tasks.values() if task.assigned_to)
    unassigned_tasks = total_tasks - assigned_tasks
    
    with col1:
        st.metric("👥 Total Employees", total_employees)
    with col2:
        st.metric("📋 Total Tasks", total_tasks)
    with col3:
        st.metric("✅ Assigned Tasks", assigned_tasks)
    with col4:
        st.metric("⏳ Unassigned Tasks", unassigned_tasks)
    
    # Charts section
    if st.session_state.task_system.employees or st.session_state.task_system.tasks:
        col1, col2 = st.columns(2)
        
        with col1:
            # Employee workload chart
            if st.session_state.task_system.employees:
                st.subheader("👥 Employee Workload Distribution")
                workload_data = []
                for emp in st.session_state.task_system.employees.values():
                    utilization = (emp.current_workload / emp.max_workload_hours) * 100 if emp.max_workload_hours > 0 else 0
                    workload_data.append({
                        "Employee": emp.name,
                        "Current Workload": emp.current_workload,
                        "Max Workload": emp.max_workload_hours,
                        "Utilization %": utilization
                    })
                
                workload_df = pd.DataFrame(workload_data)
                st.bar_chart(workload_df.set_index("Employee")["Utilization %"])
            
            # Skill distribution chart
            if st.session_state.task_system.employees:
                st.subheader("🛠️ Skill Distribution")
                skill_counts = {}
                for emp in st.session_state.task_system.employees.values():
                    for skill in emp.skills.values():
                        skill_name = skill.name
                        skill_counts[skill_name] = skill_counts.get(skill_name, 0) + 1
                
                if skill_counts:
                    skill_df = pd.DataFrame({
                        "Skill": list(skill_counts.keys()),
                        "Count": list(skill_counts.values())
                    })
                    st.bar_chart(skill_df.set_index("Skill"))
        
        with col2:
            # Task priority distribution
            if st.session_state.task_system.tasks:
                st.subheader("🎯 Task Priority Distribution")
                priority_counts = {}
                for task in st.session_state.task_system.tasks.values():
                    priority = task.priority.name
                    priority_counts[priority] = priority_counts.get(priority, 0) + 1
                
                priority_df = pd.DataFrame({
                    "Priority": list(priority_counts.keys()),
                    "Count": list(priority_counts.values())
                })
                st.bar_chart(priority_df.set_index("Priority"))
            
            # Task assignment status
            if st.session_state.task_system.tasks:
                st.subheader("📊 Task Assignment Status")
                status_data = {
                    "Status": ["Assigned", "Unassigned"],
                    "Count": [assigned_tasks, unassigned_tasks]
                }
                status_df = pd.DataFrame(status_data)
                st.bar_chart(status_df.set_index("Status"))
    
    # Recent activity table
    st.subheader("📈 Recent Activity")
    if st.session_state.task_system.tasks:
        activity_data = []
        for task in list(st.session_state.task_system.tasks.values())[-10:]:  # Show last 10 tasks
            activity_data.append({
                "Task ID": task.task_id,
                "Task Name": task.name,
                "Priority": task.priority.name,
                "Assigned To": task.assigned_to or "Unassigned",
                "Status": "✅ Completed" if task.is_completed else "⏳ Pending"
            })
        
        st.dataframe(pd.DataFrame(activity_data), use_container_width=True)
    else:
        st.info("No tasks available to display")

# Employee Management page
elif page == "Employee Management":
    st.header("👥 Employee Management")
    
    # Add new employee form
    with st.expander("➕ Add New Employee", expanded=True):
        st.subheader("📝 Employee Information")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Basic Details**")
            emp_id = st.text_input("Employee ID", placeholder="e.g., E001")
            emp_name = st.text_input("Employee Name", placeholder="e.g., John Doe")
            max_workload = st.number_input("Maximum Workload Hours", min_value=20.0, value=40.0, help="Maximum hours the employee can work per week")
            performance_rating = st.slider("Performance Rating", 0.1, 1.0, 0.8, 0.1, help="Employee performance rating (0.1 = poor, 1.0 = excellent)")
        
        with col2:
            st.markdown("**Skills & Experience**")
            skills = st.multiselect(
                "Select Skills",
                ["Python", "JavaScript", "SQL", "React", "Docker", "AWS", "Machine Learning", "Data Analysis", "Project Management", "Node.js"],
                default=[],
                help="Select all skills the employee possesses"
            )
            skill_details = {
                skill: {
                    "level": st.selectbox(
                        f"Skill Level for {skill}",
                        [level.name for level in SkillLevel],
                        key=f"emp_skill_{skill}",
                        help=f"Select proficiency level for {skill}"
                    ),
                    "experience": st.number_input(
                        f"Years of Experience in {skill}",
                        min_value=0.0,
                        value=1.0,
                        key=f"exp_{skill}",
                        help=f"Number of years working with {skill}"
                    )
                }
                for skill in skills
            }
        
        if st.button("➕ Add Employee", type="primary"):
            if emp_id and emp_name:
                employee_skills = [
                    Skill(skill, SkillLevel[details["level"]], details["experience"])
                    for skill, details in skill_details.items()
                ]
                employee = Employee(emp_id, emp_name, employee_skills, max_workload)
                employee.performance_rating = performance_rating
                
                st.session_state.task_system.add_employee(employee)
                st.success(f"✅ Employee '{emp_name}' added successfully!")
            else:
                st.error("❌ Please fill in Employee ID and Name")

    # Display existing employees
    st.subheader("📋 Current Employees")
    if st.session_state.task_system.employees:
        employees_data = []
        for emp in st.session_state.task_system.employees.values():
            skills_str = ", ".join([f"{s.name} ({s.level.name})" for s in emp.skills.values()])
            employees_data.append({
                "Employee ID": emp.emp_id,
                "Name": emp.name,
                "Skills": skills_str,
                "Current Workload": f"{emp.current_workload}/{emp.max_workload_hours} hours",
                "Performance": f"{emp.performance_rating:.2f}",
                "Assigned Tasks": len(emp.assigned_tasks)
            })
        
        st.dataframe(pd.DataFrame(employees_data), use_container_width=True)
    else:
        st.info("📝 No employees added yet. Add your first employee above!")

elif page == "Task Management":
    st.header("📋 Task Management")
    
    # Add new task form
    with st.expander("➕ Add New Task", expanded=True):
        st.subheader("📝 Task Information")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Basic Details**")
            task_id = st.text_input("Task ID", placeholder="e.g., T001")
            task_name = st.text_input("Task Name", placeholder="e.g., Develop Web Application")
            priority = st.selectbox("Priority Level", [p.name for p in TaskPriority], help="Select the urgency level of the task")
            estimated_hours = st.number_input("Estimated Hours", min_value=1.0, value=8.0, help="Estimated time to complete the task")
        
        with col2:
            st.markdown("**Requirements & Timeline**")
            deadline_days = st.number_input("Deadline (days)", min_value=1, value=7, help="Number of days to complete the task")
            required_skills = st.multiselect(
                "Required Skills",
                ["Python", "JavaScript", "SQL", "React", "Docker", "AWS", "Machine Learning", "Data Analysis", "Project Management", "Node.js"],
                default=[],
                help="Select skills required to complete this task"
            )
            skill_levels = {
                skill: st.selectbox(
                    f"Required Level for {skill}",
                    [level.name for level in SkillLevel],
                    key=f"skill_{skill}",
                    help=f"Select minimum skill level required for {skill}"
                )
                for skill in required_skills
            }
        
        if st.button("➕ Add Task", type="primary"):
            if task_id and task_name:
                required_skills_dict = {
                    skill: SkillLevel[level]
                    for skill, level in skill_levels.items()
                }
                task = Task(
                    task_id, 
                    task_name, 
                    required_skills_dict,
                    TaskPriority[priority],
                    estimated_hours,
                    deadline_days
                )
                
                st.session_state.task_system.add_task(task)
                st.success(f"✅ Task '{task_name}' added successfully!")
            else:
                st.error("❌ Please fill in Task ID and Name")

    # Display existing tasks
    st.subheader("📋 Current Tasks")
    if st.session_state.task_system.tasks:
        tasks_data = []
        for task in st.session_state.task_system.tasks.values():
            skills_str = ", ".join([f"{skill} ({level.name})" for skill, level in task.required_skills.items()])
            tasks_data.append({
                "Task ID": task.task_id,
                "Name": task.name,
                "Priority": task.priority.name,
                "Hours": task.estimated_hours,
                "Deadline": f"{task.deadline_days} days",
                "Required Skills": skills_str,
                "Assigned To": task.assigned_to or "Unassigned",
                "Status": "✅ Completed" if task.is_completed else "⏳ Pending"
            })
        
        st.dataframe(pd.DataFrame(tasks_data), use_container_width=True)
    else:
        st.info("📝 No tasks added yet. Add your first task above!")

elif page == "Task Assignment":
    st.header("🎯 Task Assignment")
    
    if not st.session_state.task_system.tasks:
        st.info("📝 Please add some tasks first in the Task Management section.")
    elif not st.session_state.task_system.employees:
        st.info("👥 Please add some employees first in the Employee Management section.")
    else:
        # Select task for assignment
        task_options = {f"{task.task_id} - {task.name}": task.task_id 
                       for task in st.session_state.task_system.tasks.values() 
                       if not task.assigned_to}
        
        if task_options:
            st.subheader("🔍 Select Task for Assignment")
            selected_task_key = st.selectbox("Choose an unassigned task", list(task_options.keys()), help="Select a task that needs to be assigned")
            selected_task_id = task_options[selected_task_key]
            
            if st.button("🎯 Get Assignment Recommendations", type="primary"):
                task = st.session_state.task_system.tasks[selected_task_id]
                matches = st.session_state.task_system.find_best_matches(task, top_n=5)
                
                st.subheader(f"📊 Assignment Recommendations for '{task.name}'")
                st.markdown(f"**Task Details:** Priority: {task.priority.name}, Hours: {task.estimated_hours}, Deadline: {task.deadline_days} days")
                
                for i, (employee, probability) in enumerate(matches, 1):
                    skill_match = st.session_state.task_system.calculate_skill_similarity(employee, task)
                    availability = employee.get_availability_ratio()
                    
                    with st.expander(f"🥇 {i}. {employee.name} (Match Probability: {probability:.1%})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("🎯 Skill Match", f"{skill_match:.1%}")
                            st.metric("⏰ Availability", f"{availability:.1%}")
                        with col2:
                            st.metric("📊 Current Workload", f"{employee.current_workload}/{employee.max_workload_hours} hours")
                            st.metric("⭐ Performance", f"{employee.performance_rating:.2f}")
                        
                        if st.button(f"✅ Assign to {employee.name}", key=f"assign_{i}"):
                            if st.session_state.task_system.assign_task(selected_task_id, employee.emp_id):
                                st.success(f"🎉 Task successfully assigned to {employee.name}!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to assign task.")
        else:
            st.success("🎉 All tasks are already assigned!")

# Add a footer
st.markdown("---")
st.markdown("*Task Assignment System - Intelligent task assignment using advanced algorithms*")
