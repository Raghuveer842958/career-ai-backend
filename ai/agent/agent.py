from ai.factories.llm_factory import get_llm

from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from ai.tools.jobs_tools import (
    find_jobs, 
    suggest_job_role, 
    save_jobs, 
    get_saved_jobs, 
    recommend_matching_jobs
)

from ai.tools.resume_tools import (
    resume_strengths_tool,
    resume_weakness_tool,
    resume_projects_tool,
    resume_improvement_tool
)

from langchain_core.prompts import ChatPromptTemplate


def get_career_agent():

    llm = get_llm()

    tools = [
        resume_strengths_tool,
        resume_weakness_tool,
        resume_projects_tool,
        resume_improvement_tool,
        suggest_job_role,
        find_jobs,
        save_jobs,
        get_saved_jobs,
        recommend_matching_jobs,
    ]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are Career AI Assistant.

            Use Tools when required only
            """
        ),

        ("human", "{input}"),

        ("placeholder", "{agent_scratchpad}")
    ])

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True
    )

    return agent_executor

    # https://www.youtube.com/watch?v=ctHby5vhDqg&t=302s