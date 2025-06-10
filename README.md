# TaskHive - Intelligent Task Management System

TaskHive is a sophisticated task management system that uses AI-powered algorithms to intelligently assign tasks to employees based on their skills, experience, workload, and performance. The system features a modern Streamlit-based user interface for easy task and employee management.

## Features

### Task Management
- Create and manage tasks with detailed requirements
- Set task priorities (LOW, MEDIUM, HIGH, CRITICAL)
- Define required skills and expertise levels
- Track task deadlines and estimated hours
- Monitor task status and assignments

### Employee Management
- Add employees with their skill profiles
- Track employee workload and capacity
- Monitor employee performance and experience
- View assigned tasks and current workload

### Intelligent Task Assignment
- AI-powered task assignment recommendations
- Skill matching algorithm
- Workload balancing
- Experience-based scoring
- Performance-based prioritization

## Technical Stack
- Python 3.x
- Streamlit for the web interface
- Pandas for data handling
- Custom AI algorithms for task assignment

## Installation

1. Clone the repository:
```bash
git clone https://github.com/HarshBPGC/TaskHive.git
cd TaskHive
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to:
```
http://localhost:8501
```

### Adding Employees
1. Go to "Employee Management" page
2. Click "Add New Employee"
3. Fill in:
   - Employee ID
   - Name
   - Maximum workload hours
   - Skills and their levels
   - Years of experience for each skill

### Creating Tasks
1. Go to "Task Management" page
2. Click "Add New Task"
3. Fill in:
   - Task ID
   - Task Name
   - Priority level
   - Estimated hours
   - Deadline
   - Required skills and their levels

### Assigning Tasks
1. Go to "Task Assignment" page
2. Select an unassigned task
3. View AI-generated recommendations
4. Choose an employee from the recommendations or assign manually

## System Architecture

The system consists of three main components:

1. **Models** (`models.py`):
   - Employee class for managing employee data
   - Task class for task information
   - Skill and priority enums for standardization

2. **Task Assignment System** (`task_assignment.py`):
   - Intelligent task assignment algorithms
   - Skill matching calculations
   - Workload balancing
   - Performance scoring

3. **User Interface** (`app.py`):
   - Streamlit-based web interface
   - Interactive forms for data entry
   - Real-time task and employee management
   - Visual task assignment recommendations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Harsh Shah
- GitHub: [@HarshBPGC](https://github.com/HarshBPGC) 