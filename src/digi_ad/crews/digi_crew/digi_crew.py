from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from pydantic import BaseModel
from digi_ad.tools.custom_tool import FAQTool


class StandAloneOutput(BaseModel):
    question : str 
class QueryType(BaseModel):
    query_type : str 

@CrewBase
class StandAloneCrew:
    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def standalone_question_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["standalone_question_agent"],  
        )
   
    @task
    def standalone_question_task(self) -> Task:
        return Task(
            config=self.tasks_config["standalone_question_task"],  
            agent=self.standalone_question_agent(),
            output_pydantic=StandAloneOutput,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.sequential,
            verbose=True,
        )


@CrewBase
class RouterCrew:
    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def router_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["router_agent"],  
        )
   
    @task
    def route_task(self) -> Task:
        return Task(
            config=self.tasks_config["route_task"],  
            agent=self.router_agent(),
            output_pydantic=QueryType,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.sequential,
            verbose=True,
        )
@CrewBase
class FAQCrew:
    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def faq_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["faq_agent"], 
            tools=[FAQTool()], 
        )
   
    @task
    def faq_task(self) -> Task:
        return Task(
            config=self.tasks_config["faq_task"],  
            agent=self.faq_agent()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.sequential,
            verbose=True,
        )
    
@CrewBase
class BookDemoCrew:
    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def book_demo_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["demo_redirect_agent"],  
        )
   
    @task
    def book_demo_task(self) -> Task:
        return Task(
            config=self.tasks_config["demo_redirect_task"],  
            agent=self.book_demo_agent(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.sequential,
            verbose=True,
        )
    
    
