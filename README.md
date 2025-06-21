# Task Assignment System - Pattern Matching Algorithm

A simple task assignment system that uses pattern matching algorithms to assign tasks to employees based on their skills, experience, workload, and performance. The system features a clean Streamlit-based user interface for easy task and employee management.

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

### Pattern Matching Algorithm
- **Skill-based matching**: Matches employee skills to task requirements
- **Workload balancing**: Considers current workload vs. maximum capacity
- **Experience scoring**: Factors in years of experience for relevant skills
- **Performance-based prioritization**: Higher performing employees get priority for critical tasks
- **Multi-factor scoring**: Combines all factors using weighted algorithms

## Technical Stack
- Python 3.x
- Streamlit for the web interface
- Pandas for data handling
- Custom pattern matching algorithms for task assignment

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
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
   - Performance rating (0.1 to 1.0)
   - Skills and their levels (BEGINNER, INTERMEDIATE, ADVANCED, EXPERT)
   - Years of experience for each skill

### Creating Tasks
1. Go to "Task Management" page
2. Click "Add New Task"
3. Fill in:
   - Task ID
   - Task Name
   - Priority level
   - Estimated hours
   - Deadline (in days)
   - Required skills and their levels

### Using the Pattern Matching Algorithm
1. Go to "Task Assignment" page
2. Select an unassigned task
3. Click "Get Assignment Recommendations"
4. View the algorithm's recommendations with:
   - Assignment probability percentage
   - Skill match percentage
   - Availability percentage
   - Current workload details
   - Performance rating
5. Assign the task to the recommended employee or choose manually

## Algorithm Details

The pattern matching algorithm uses a weighted scoring system:

- **Skill Match (40%)**: How well employee skills match task requirements
- **Availability (25%)**: Current workload vs. maximum capacity
- **Experience (15%)**: Years of experience in required skills
- **Performance (10%)**: Employee performance rating
- **Priority Match (10%)**: How well employee performance matches task priority needs

The final probability is calculated using a sigmoid function to ensure values between 0 and 1.

## System Architecture

The system consists of three main components:

1. **Models** (`models.py`):
   - Employee class for managing employee data
   - Task class for task information
   - Skill and priority enums for standardization

2. **Task Assignment System** (`task_assignment.py`):
   - Pattern matching algorithms
   - Skill similarity calculations
   - Workload balancing logic
   - Multi-factor scoring system

3. **User Interface** (`app.py`):
   - Streamlit-based web interface
   - Interactive forms for data entry
   - Real-time task and employee management
   - Algorithm recommendations display

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 