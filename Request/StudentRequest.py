from pydantic import BaseModel

class StudentRequest(BaseModel):
    Gender: str
    Age: float
    Academic_Pressure: float
    CGPA: float
    Study_Satisfaction: float
    Sleep_Duration: str
    Dietary_Habits: str
    Degree: str
    Suicidal_Thoughts: str
    Work_Study_Hours: float
    Financial_Stress: float
    Family_History_Mental_Illness: str