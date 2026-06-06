from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Literal

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ai.factories.llm_factory import get_llm
from ai.rag.retriever import retrieve_resume_context
from typing import Optional

class ResumeInsightInput(BaseModel):
    query: str = Field(..., description="User question about resume")

class ResumeStrengthsInput(BaseModel):
    query: Optional[str] = Field(
        default="",
        description="Optional user question about strengths"
    )

class ResumeWeaknessInput(BaseModel):
    query: Optional[str] = Field(
        default="",
        description="Optional user question about weaknesses or gaps"
    )

class ResumeProjectsInput(BaseModel):
    query: Optional[str] = Field(
        default="",
        description="Optional user question about projects."
    )

class ResumeImprovementInput(BaseModel):
    query: Optional[str] = Field(
        default="",
        description="Optional user question about resume improvements."
    )

@tool(args_schema=ResumeStrengthsInput)
def resume_strengths_tool(query: str = ""):
    """
    Analyze resume strengths, skills, achievements, and hiring advantages.

    Use for questions about:
    - strengths
    - strongest skills
    - recruiter appeal
    - hiring potential
    - standout qualities

    Do not use for weaknesses, projects, resume improvements, or jobs.
    """

    llm = get_llm()

    docs = retrieve_resume_context("skills achievements strengths experience")
    context = "\n\n".join([d.page_content for d in docs])

    prompt = PromptTemplate(
        template="""
        You are a career coach.

        Identify ONLY strengths from the resume.

        Context:
        {context}

        Instructions:
        - Focus on technical + soft strengths
        - Be concise
        - No hallucination
        """,
        input_variables=["context"]
    )

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"context": context})


@tool(args_schema=ResumeWeaknessInput)
def resume_weakness_tool(query: str = ""):
    """
    Analyze resume weaknesses, skill gaps, missing experience, and factors
    that may reduce competitiveness for target roles.

    Use for:
    - weaknesses
    - skill gaps
    - missing skills
    - missing technologies
    - reasons for rejection
    - missing experience

    Return constructive weaknesses based only on the resume.
    """

    llm = get_llm()

    docs = retrieve_resume_context("experience missing skills gaps improvements")
    context = "\n\n".join([d.page_content for d in docs])

    prompt = PromptTemplate(
        template="""
        You are a senior career advisor.

        Identify weaknesses or gaps in the resume.

        Context:
        {context}

        Rules:
        - Be honest but constructive
        - Suggest gaps in skills or experience
        - Do NOT demotivate user
        """,
        input_variables=["context"]
    )

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"context": context})

# Q1. Can you identify my skill gaps?



@tool(args_schema=ResumeProjectsInput)
def resume_projects_tool(query: str = ""):
    """
    Analyze and explain projects from the resume.

    Use for:
    - projects
    - applications built
    - project experience
    - portfolio work
    - tech stack used
    - project impact

    Examples:
    - What projects have I built?
    - Tell me about my projects.
    - What is my best project?
    - Which project is most relevant for backend roles?
    - What technologies have I used in my projects?

    Do not use for strengths, weaknesses, resume improvements,
    job search, or job recommendations.

    Return project summaries based only on the resume.
    """

    llm = get_llm()

    docs = retrieve_resume_context("projects built applications work experience")
    context = "\n\n".join([d.page_content for d in docs])

    prompt = PromptTemplate(
        template="""
        You are a technical recruiter.

        Explain the projects in the resume clearly.

        Context:
        {context}

        Instructions:
        - Describe each project clearly
        - Highlight tech stack
        - Show impact
        """,
        input_variables=["context"]
    )

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"context": context})


@tool(args_schema=ResumeImprovementInput)
def resume_improvement_tool(query: str = ""):
    """
    Suggest ways to improve the resume, skills, career profile, and
    job readiness.

    Use for:
    - resume improvements
    - profile improvement
    - career growth advice
    - upskilling recommendations
    - interview readiness
    - increasing shortlist chances

    Examples:
    - How can I improve my resume?
    - What should I learn next?
    - How can I get more interviews?
    - What should I do to get shortlisted?

    Do not use for strengths, weaknesses, project summaries,
    job search, or job recommendations.

    Return practical improvement suggestions based on the resume.
    """

    llm = get_llm()

    docs = retrieve_resume_context("resume skills experience projects gaps")
    context = "\n\n".join([d.page_content for d in docs])

    prompt = PromptTemplate(
        template="""
        You are a senior FAANG recruiter.

        Suggest improvements for this resume.

        Context:
        {context}

        Rules:
        - Be practical
        - Suggest missing skills
        - Suggest resume structure improvements
        - Suggest career growth steps
        """,
        input_variables=["context"]
    )

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"context": context})



# resume_ats_score_tool
# resume_skill_gap_tool
# resume_job_match_tool