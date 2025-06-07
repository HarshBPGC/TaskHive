import math
from typing import Dict, List, Tuple
from models import Employee, Task, TaskPriority

class TaskAssignmentSystem:
    def __init__(self):
        self.employees = {}
        self.tasks = {}
        self.assignment_weights = {
            'skill_match': 0.4,
            'availability': 0.25,
            'experience': 0.15,
            'performance': 0.1,
            'priority_match': 0.1
        }

    def add_employee(self, employee: Employee):
        self.employees[employee.emp_id] = employee

    def add_task(self, task: Task):
        self.tasks[task.task_id] = task

    def calculate_skill_similarity(self, employee: Employee, task: Task) -> float:
        """Calculate how well employee's skills match task requirements (0-1)"""
        if not task.required_skills:
            return 0.5  # Neutral score if no specific skills required
        
        total_match = 0
        max_possible_match = 0
        
        for skill_name, required_level in task.required_skills.items():
            employee_level = employee.get_skill_level(skill_name)
            required_level_val = required_level.value
            
            # Calculate match score for this skill
            if employee_level >= required_level_val:
                # Employee meets or exceeds requirement
                skill_match = 1.0 + (employee_level - required_level_val) * 0.1
            else:
                # Employee doesn't meet requirement - penalize based on gap
                skill_match = max(0, employee_level / required_level_val * 0.7)
            
            total_match += skill_match
            max_possible_match += 1.2  # Max possible score per skill
        
        return min(1.0, total_match / max_possible_match)

    def calculate_experience_score(self, employee: Employee, task: Task) -> float:
        """Calculate experience relevance score (0-1)"""
        if not task.required_skills:
            return 0.5
        
        total_experience = 0
        skill_count = 0
        
        for skill_name in task.required_skills.keys():
            if skill_name in employee.skills:
                total_experience += employee.skills[skill_name].experience_years
                skill_count += 1
        
        if skill_count == 0:
            return 0.1  # Low score if no relevant experience
        
        avg_experience = total_experience / skill_count
        # Normalize experience score (assuming 10+ years is maximum relevant)
        return min(1.0, avg_experience / 10.0)

    def calculate_priority_match_score(self, employee: Employee, task: Task) -> float:
        """Calculate how well employee matches task priority needs"""
        # Higher priority tasks should go to higher performing employees
        performance_threshold = {
            TaskPriority.CRITICAL: 0.9,
            TaskPriority.HIGH: 0.7,
            TaskPriority.MEDIUM: 0.5,
            TaskPriority.LOW: 0.3
        }
        
        required_performance = performance_threshold[task.priority]
        if employee.performance_rating >= required_performance:
            return 1.0
        else:
            return employee.performance_rating / required_performance

    def calculate_assignment_probability(self, employee: Employee, task: Task) -> float:
        """Calculate probability of assigning task to employee"""
        # Check if employee can handle the workload
        if employee.current_workload + task.estimated_hours > employee.max_workload_hours:
            return 0.0  # Cannot assign if it exceeds capacity
        
        # Calculate individual scores
        skill_similarity = self.calculate_skill_similarity(employee, task)
        availability = employee.get_availability_ratio()
        experience = self.calculate_experience_score(employee, task)
        performance = min(1.0, employee.performance_rating)
        priority_match = self.calculate_priority_match_score(employee, task)
        
        # Calculate weighted score
        weighted_score = (
            skill_similarity * self.assignment_weights['skill_match'] +
            availability * self.assignment_weights['availability'] +
            experience * self.assignment_weights['experience'] +
            performance * self.assignment_weights['performance'] +
            priority_match * self.assignment_weights['priority_match']
        )
        
        # Convert to probability using sigmoid function
        probability = 1 / (1 + math.exp(-5 * (weighted_score - 0.5)))
        return probability

    def find_best_matches(self, task: Task, top_n: int = 3) -> List[Tuple[Employee, float]]:
        """Find the best employee matches for a task"""
        matches = []
        
        for employee in self.employees.values():
            probability = self.calculate_assignment_probability(employee, task)
            if probability > 0:
                matches.append((employee, probability))
        
        # Sort by probability (descending)
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_n]

    def assign_task(self, task_id: str, employee_id: str = None) -> bool:
        """Assign a task to an employee (auto-assign if employee_id not provided)"""
        if task_id not in self.tasks:
            print(f"Task {task_id} not found")
            return False
        
        task = self.tasks[task_id]
        
        if task.assigned_to:
            print(f"Task {task_id} is already assigned to {task.assigned_to}")
            return False
        
        if employee_id:
            # Manual assignment
            if employee_id not in self.employees:
                print(f"Employee {employee_id} not found")
                return False
            
            employee = self.employees[employee_id]
            if employee.current_workload + task.estimated_hours > employee.max_workload_hours:
                print(f"Employee {employee.name} doesn't have enough capacity")
                return False
        else:
            # Auto assignment - find best match
            matches = self.find_best_matches(task)
            if not matches:
                print(f"No suitable employee found for task {task_id}")
                return False
            
            employee = matches[0][0]  # Best match
        
        # Make the assignment
        task.assigned_to = employee.emp_id
        employee.current_workload += task.estimated_hours
        employee.assigned_tasks.append(task_id)
        
        print(f"Task '{task.name}' assigned to {employee.name}")
        return True

    def get_assignment_recommendations(self, task_id: str) -> None:
        """Display assignment recommendations for a task"""
        if task_id not in self.tasks:
            print(f"Task {task_id} not found")
            return
        
        task = self.tasks[task_id]
        matches = self.find_best_matches(task, top_n=5)
        
        print(f"\nAssignment recommendations for task '{task.name}':")
        print("-" * 60)
        
        for i, (employee, probability) in enumerate(matches, 1):
            skill_match = self.calculate_skill_similarity(employee, task)
            availability = employee.get_availability_ratio()
            
            print(f"{i}. {employee.name}")
            print(f"   Probability: {probability:.2%}")
            print(f"   Skill Match: {skill_match:.2%}")
            print(f"   Availability: {availability:.2%}")
            print(f"   Current Workload: {employee.current_workload}/{employee.max_workload_hours} hours")
            print() 