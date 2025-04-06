from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langchain_experimental.utilities import PythonREPL
from dotenv import load_dotenv
from crewai.tools import BaseTool
import os
from lead_generator.tools.custom_tool import OrganizationSearchTool, PeopleSearchTool
from crewai.telemetry import Telemetry

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

load_dotenv()

def noop(*args, **kwargs):
    # with open("./logfile.txt", "a") as f:
    #     f.write("Telemetry method called and noop'd\n")
    pass


for attr in dir(Telemetry):
    if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
        setattr(Telemetry, attr, noop)
        
SERPER_API_KEY=os.getenv("SERPER_API_KEY")

class PythonREPLTool(BaseTool):
    name: str = "python_repl"
    description: str = "A Python shell. Use this to execute Python commands. Input should be a valid Python command. If you want to see the output of a value, you should print it out with `print(...)`."
    python_repl: PythonREPL = PythonREPL()

    def _run(self, query: str) -> str:
        return self.python_repl.run(query)

# Instantiate the custom tool
repl_tool = PythonREPLTool()

@CrewBase
class LeadGenerator():
    """LeadGenerator crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def business(self) -> Agent:
        return Agent(
            config=self.agents_config['business'],
            verbose=True,
            tools=[SerperDevTool(), repl_tool]
        )

    @agent
    def apollo_fetcher(self) -> Agent:
        return Agent(
            config=self.agents_config['apollo_fetcher'],
            verbose=True,
            tools=[PeopleSearchTool(), OrganizationSearchTool(), repl_tool]
        )
    
    @agent
    def response_formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['response_formatter'],
            verbose=True,
            tools=[repl_tool]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def extract_business_and_icp(self) -> Task:
        return Task(
            config=self.tasks_config['extract_business_and_icp'],
        )

    @task
    def fetch_leads(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_leads'],
            output_file='report.md'
        )
    
    def format_response(self) -> Task:
        return Task(
            config=self.tasks_config['format_response'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LeadGenerator crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
