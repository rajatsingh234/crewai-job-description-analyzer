from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_job_description_analyzer.models.requirement_analysis import RequirementAnalysis
from crewai_job_description_analyzer.models.candidate_profile import CandidateProfile
from crewai_job_description_analyzer.models.match_analysis import MatchAnalysis
from crewai_job_description_analyzer.models.interview_preparation import InterviewPreparation



@CrewBase
class CrewaiJobDescriptionAnalyzer():
    """CrewaiJobDescriptionAnalyzer crew"""

    agents: list[BaseAgent]
    tasks: list[Task]


    @agent
    def requirement_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['requirement_analyst'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def candidate_profile_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['candidate_profile_analyst'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def matching_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['matching_analyst'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def interview_coach(self) -> Agent:
        return Agent(
            config=self.agents_config['interview_coach'], # type: ignore[index]
            verbose=True
        )

    @task
    def requirement_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['requirement_analysis_task'], # type: ignore[index]
            output_pydantic=RequirementAnalysis,
        )

    @task
    def candidate_profile_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['candidate_profile_analysis_task'], # type: ignore[index]
            output_pydantic=CandidateProfile,
        )
    
    @task
    def match_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['match_analysis_task'],
            output_pydantic=MatchAnalysis,
            context=[
                self.requirement_analysis_task(),
                self.candidate_profile_analysis_task(),
            ],
        )
    
    @task
    def interview_preparation_task(self) -> Task:
        return Task(
            config=self.tasks_config['interview_preparation_task'],
            output_pydantic=InterviewPreparation,
            context=[
                self.match_analysis_task(),
            ],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiJobDescriptionAnalyzer crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
