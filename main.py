from models import Employee, Skill, SkillLevel, Task, TaskPriority
from task_assignment import TaskAssignmentSystem

def main():
    # Create the assignment system
    system = TaskAssignmentSystem()
    
    # Create employees with different skills
    emp1 = Employee("E001", "Alice Johnson", [
        Skill("Python", SkillLevel.EXPERT, 5.0),
        Skill("Machine Learning", SkillLevel.ADVANCED, 3.0),
        Skill("Data Analysis", SkillLevel.EXPERT, 4.0)
    ])
    emp1.performance_rating = 0.95
    
    emp2 = Employee("E002", "Bob Smith", [
        Skill("JavaScript", SkillLevel.EXPERT, 6.0),
        Skill("React", SkillLevel.ADVANCED, 4.0),
        Skill("Node.js", SkillLevel.INTERMEDIATE, 2.0),
        Skill("Python", SkillLevel.INTERMEDIATE, 2.0)
    ])
    emp2.performance_rating = 0.85
    
    emp3 = Employee("E003", "Carol Wilson", [
        Skill("Project Management", SkillLevel.EXPERT, 8.0),
        Skill("Data Analysis", SkillLevel.INTERMEDIATE, 3.0),
        Skill("Python", SkillLevel.BEGINNER, 1.0)
    ])
    emp3.performance_rating = 0.90
    
    # Add employees to system
    system.add_employee(emp1)
    system.add_employee(emp2)
    system.add_employee(emp3)
    
    # Create tasks
    task1 = Task("T001", "Develop ML Model", 
                {"Python": SkillLevel.ADVANCED, "Machine Learning": SkillLevel.ADVANCED}, 
                TaskPriority.HIGH, 20.0, 14)
    
    task2 = Task("T002", "Build Web Dashboard", 
                {"JavaScript": SkillLevel.ADVANCED, "React": SkillLevel.INTERMEDIATE}, 
                TaskPriority.MEDIUM, 15.0, 10)
    
    task3 = Task("T003", "Data Analysis Report", 
                {"Data Analysis": SkillLevel.INTERMEDIATE, "Python": SkillLevel.INTERMEDIATE}, 
                TaskPriority.LOW, 10.0, 7)
    
    # Add tasks to system
    system.add_task(task1)
    system.add_task(task2)
    system.add_task(task3)
    
    # Show recommendations and assign tasks
    system.get_assignment_recommendations("T001")
    system.assign_task("T001")
    
    print("\n" + "="*60 + "\n")
    
    system.get_assignment_recommendations("T002")
    system.assign_task("T002")
    
    print("\n" + "="*60 + "\n")
    
    system.get_assignment_recommendations("T003")
    system.assign_task("T003")
    
    # Show final workload status
    print("\n" + "="*60)
    print("FINAL WORKLOAD STATUS")
    print("="*60)
    for emp in system.employees.values():
        print(f"{emp.name}: {emp.current_workload}/{emp.max_workload_hours} hours "
              f"({emp.current_workload/emp.max_workload_hours:.1%} capacity)")
        print(f"  Assigned tasks: {emp.assigned_tasks}")
        print()

if __name__ == "__main__":
    main() 