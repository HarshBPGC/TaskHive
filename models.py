from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

class SkillLevel(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Skill:
    name: str
    level: SkillLevel
    experience_years: float

class Task:
    def __init__(self, task_id: str, name: str, required_skills: Dict[str, SkillLevel], 
                 priority: TaskPriority, estimated_hours: float, deadline_days: int):
        self.task_id = task_id
        self.name = name
        self.required_skills = required_skills
        self.priority = priority
        self.estimated_hours = estimated_hours
        self.deadline_days = deadline_days
        self.assigned_to = None
        self.is_completed = False

class Employee:
    def __init__(self, emp_id: str, name: str, skills: List[Skill], 
                 max_workload_hours: float = 40.0):
        self.emp_id = emp_id
        self.name = name
        self.skills = {skill.name: skill for skill in skills}
        self.max_workload_hours = max_workload_hours
        self.current_workload = 0.0
        self.assigned_tasks = []
        self.performance_rating = 1.0  # Default performance multiplier

    def add_skill(self, skill: Skill):
        self.skills[skill.name] = skill

    def get_skill_level(self, skill_name: str) -> int:
        if skill_name in self.skills:
            return self.skills[skill_name].level.value
        return 0

    def get_availability_ratio(self) -> float:
        return max(0, (self.max_workload_hours - self.current_workload) / self.max_workload_hours) 