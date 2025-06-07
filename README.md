# Task Assignment System

A Python-based task assignment system that intelligently matches employees with tasks based on their skills, experience, availability, and performance.

## Features

- Skill-based task matching
- Experience level consideration
- Workload management
- Performance-based assignments
- Priority-based task distribution
- Automatic and manual task assignment
- Assignment recommendations

## Project Structure

- `models.py`: Contains data models and enums (Skill, Task, Employee)
- `task_assignment.py`: Contains the TaskAssignmentSystem class with assignment logic
- `main.py`: Example usage of the system
- `requirements.txt`: Project dependencies

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the example:
```bash
python main.py
```

## How it Works

The system uses a weighted scoring system to match employees with tasks based on:
- Skill match (40%)
- Availability (25%)
- Experience (15%)
- Performance (10%)
- Priority match (10%)

The system calculates an assignment probability for each employee-task pair and recommends the best matches.

## Example

The example in `main.py` demonstrates:
1. Creating employees with different skills and experience levels
2. Creating tasks with specific requirements
3. Getting assignment recommendations
4. Automatically assigning tasks
5. Displaying final workload status 