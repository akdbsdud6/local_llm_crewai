import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew
from dotenv import load_dotenv

load_dotenv()

def write_to_file(content, filename):
    with open(filename, 'w') as file:
        file.write(content)
    return filename

reader = Agent(
    role="Code Reader",
    goal="Open and read provided code in this location: {location}, then point out parts that can be fixed or improved, based on {program_requirements}.",
    backstory="""You're a code reader that will read code and give feedback on potential improvements you find, based on the requirements stated in {program_requirements}.
    You will carefully read the provided code line by line, interpreting its ultimate goal and how each part of the code contributes to the goal. 

    You will check if library imports and corresponding pip installs are made correctly.
    You will check if the current version of the installed libraries can correctly handle the provided code.

    You will check if the code follows SOLID development principles. 
    If it doesn't, you will specify that it doesn't so Code Fixer can make the code follow SOLID development principles. 

    You will check if the code is easily readable by humans.

    If the code returns errors, you will find and specify the lines that are causing the errors.
    Your response will be the basis for Code Fixer to modify the code provided by user.
    """,
    allow_delegation=False,
    verbose=True
)

fixer = Agent(
    role="Code Fixer",
    goal="Fix or improve the code provided in this location: {location}",
    backstory="""You're fixing/improving a given code, building up from the basis provided by
    Code Reader.
    The fixed code will follow the potential improvements Code Reader has found.
    The fixed code must satisfy all requirements specified in {program_requirements}.
    The fixed code should be reasonably efficient and functional.
    The fixed code must follow SOLID development principles.
    The fixed code must be easily readable by humans.
    The fixed code should have comments that navigate user through its implementations
    You may pip install or import new libraries as long as they ultimately help enhance the code.
    """,
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    role="Code Editor",
    goal="Test, Polish, and save the code on this topic: {program_requirements}",
    backstory="""You're testing and editing the Python code provided by Code Fixer. 
    You will make sure the code runs without producing any error.
    You will make sure the code indeed meets all the requirements in {program_requirements}.
    You will make sure the code is efficient and functional.
    You will make sure the code follows SOLID development principles.
    You will make sure the code is easily readable to humans.
    You will make sure the code has plenty of helpful comments.
    If any of these requirements fail, you shall edit and polish the code until it meets all requirements.
    """,
    allow_delegation=False,
    verbose=True,
    function_calling=True
)

read = Task(
    description=(
        """1. Read the code carefully, going line by line and understandinng the ultimate goal.
        2. Find room of improvement: whether it be readability, efficiency, or functionality.
        """
    ),
    expected_output="""A comprehensive code fix plan document with an outline on points of potential improvement and brief explanations.""",
    agent=reader
)

fix = Task(
    description=(
        """1. If a method from a library can enhance the existing code in any way, use it.
        2. Add double-spaces and comments so that the finished code is readable to humans
        3. Specify any part that has been fixed, by adding a commend beside the line.
        4. If there is a more efficient approach, take it over a less efficient approach
        """
    ),
    expected_output="""An efficient Python code that well-utilizes library methods to satisfy user-given requirements""",
    agent=fixer
)

edit = Task(
    description=("""1. If the code fails to satisfy any of the requirements, edit it until it satisfies them all.
        2. If there are imports or variables that are never used, remove them.
        3. When presenting the final version, start any line of explanation that isn't "code" with a # symbol so it becomes a comment.
        4. Don't wrap up the final version of code with ''', just present it straight
        """
    ),
    expected_output="""The filename of a python code that contains the final version of Python code that satisfies all specified requirements and produces 0 errors.""",
    agent=editor
)


crew = Crew(
    agents=[reader, fixer, editor],
    tasks=[read, fix, edit],
    verbose=2
)

result = crew.kickoff(
    inputs={
        "location":"EditThis.py",
        "program_requirements":"""1. The provided code doesn't have user interface GUI. Change this so the new code has great user interface GUI
        2. A basic calculator that can handle addition, subtraction, multiplication, division of many digits
        3. Code should be readable to human""",
        "output_file":"code_output.py"
    })

output_file = "code_output.py"
with open(output_file, 'w') as file:
    file.write(result)

print(f"The improved code has been saved to: {output_file}")

#Markdown(result)
