import warnings
warnings.filterwarnings('ignore')

import sys
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from IPython.display import Markdown

load_dotenv()

planner = Agent(
    role="Code Planner",
    goal="Plan out the basis of efficient Python code on this topic: {request}",
    backstory="""You're planning out the basis of code about this topic: {request}.
    You will specify which libraries must be installed on the machine. (pip installs)
    You will specify which libraries must be imported. 
    You will form chapters that will be the basis for the Code Writer to write functional code on this topic.
    """,
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role="Code Writer",
    goal="Write efficient Python code on this topic: {request}",
    backstory="""You're writing efficient Python code, building up from the basis provided by
    Code Planner.
    Your code will follow the chapters and guidelines formed by Code Planner. 
    Your code must satisfy all requirements specified in {request}.
    Your code should be reasonably efficient and functional.
    """,
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    role="Code Editor",
    goal="Test and Polish the Python code on this topic: {request}",
    backstory="""You're testing and editing the Python code provided by Code Writer. 
    You will make sure the code runs without producing any error.
    You will make sure the code indeed meets all the requirements in {request}.
    You will make sure the code is efficient and functional.
    If any of these requirements fail, you shall edit and polish the code until it meets all requirements.
    """,
    allow_delegation=False,
    verbose=True
)

plan = Task(
    description=(
        """1. Prioritize efficient implementations over less efficient implementations.
        2. Utilize Python libraries to the fullest as long as it helps making the code simpler and easier to implement.
        3. Add explanations frequently.
        """
    ),
    expected_output="""A comprehensive code plan document with an outline, imports & pip installs, and brief explanations.""",
    agent=planner
)

write = Task(
    description=(
        """1. If a method from an already imported library can enhance the existing code in any way, use it.
        2. Add double-space and comments so that the finished code is readable to humans
        3. If there is a more efficient approach, take it over a less efficient approach
        """
    ),
    expected_output="""An efficient Python code that well-utilizes library methods to satisfy user requests""",
    agent=writer
)

edit = Task(
    description=("""1. If the code fails to satisfy any of the requirements, edit it until it satisfies them all.
        2. If there are imports or variables that are never used, remove them.
        """
    ),
    expected_output="""A final version of Python code that satisfies all specified requirements and produces 0 errors.""",
    agent=editor
)


crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)

result = crew.kickoff(inputs={"request": "a basic calculator program that can handle basic arithmetic operations"})
Markdown(result)
