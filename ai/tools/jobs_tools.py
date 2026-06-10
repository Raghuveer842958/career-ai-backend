from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser

import os
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional
from requests.exceptions import RequestException

from ai.factories.llm_factory import get_llm
from ai.rag.retriever import retrieve_resume_context


load_dotenv()

BASE_URL  = "http://127.0.0.1:8000/jobs/many"


class JobSearchInput(BaseModel):
    position: str = Field(
        ...,
        description="Job role to search for. ig: Python developer"
    )
    location: Optional[str] = Field(
        default="India",
        description="Preferred job location"
    )


class Job(BaseModel):
    job_id: str
    title: str
    company: str
    location: Optional[str] = None


class JobList(BaseModel):
    jobs: List[Job]


class SaveJobsInput(BaseModel):
    jobs: List[Job]


class RecommendedJob(BaseModel):
    job_id: str = Field(description="Unique job identifier")
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    location: Optional[str] = Field(
        default=None,
        description="Job location"
    )
    match_score: int = Field(
        description="Job match score from 0 to 100"
    )
    reason: str = Field(
        description="Short reason why this job matches the resume"
    )


class RecommendedJobsResponse(BaseModel):
    recommended_jobs: List[RecommendedJob]



@tool
def suggest_job_role():
    """
    Use for generating a job profile name based on user skills and experience.
    Example: Full Stack Developer, Backend Developer
    """

    docs = retrieve_resume_context(
        "Skills Framework Frontend Backend Programming Language Experience"
    )

    context = "\n\n".join([
        doc.page_content
        for doc in docs
    ])

    prompt = PromptTemplate(
        template="""
        Generate a suitable professional job profile name based on the provided resume context.

        Resume Context:
        {context}
        """,
        input_variables=["context"]
    )

    llm = get_llm()

    parser = StrOutputParser()

    chain = prompt | llm | parser

    # ✅ FIXED
    response = chain.invoke({
        "context": context
    })

    return response


@tool(args_schema=JobSearchInput)
def find_jobs(position: str, location: Optional[str] = "India"):
    """
    Search for job openings based on a job title or role.
    """

    try:

        url = "https://jsearch.p.rapidapi.com/search"

        querystring = {
            "query": f"{position} in {location}",
            "page": "1",
            "num_pages": "1"
        }

        headers = {
            "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        response = requests.get(
            url,
            headers=headers,
            params=querystring,
            timeout=40
        )

        response.raise_for_status()

        data = response.json()

        jobs = data.get("data", [])[:5]

        optimized_jobs = []

        for job in jobs:

            optimized_jobs.append(
                Job(
                    job_id=job.get("job_id"),
                    title=job.get("job_title"),
                    company=job.get("employer_name"),
                    location=job.get("job_location"),
                )
            )

        return {
            "jobs": [
                job.model_dump()
                for job in optimized_jobs
            ]
        }

    except RequestException as e:

        return {
            "error": f"Failed to fetch jobs: {str(e)}",
            "jobs": []
        }


@tool(args_schema=SaveJobsInput)
def save_jobs(jobs: List[Job]):
    """
    Save jobs into database.
    """

    payload = [
        job.model_dump()
        for job in jobs
    ]

    response = requests.post(
        "http://127.0.0.1:8000/jobs/many",
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return {
        "message": data["message"],
        "saved_count": len(data["jobs"])
    }


@tool
def get_saved_jobs():
    """
    Retrieve saved jobs from the database.
    """

    response = requests.get(
        "http://127.0.0.1:8000/jobs/",
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return {
        "jobs": data["jobs"]
    }


@tool(args_schema=JobList)
def recommend_matching_jobs(jobs: List[Job]):
    """
    Recommend best matching jobs according to
    user skills and experience.
    """


    docs = retrieve_resume_context(
        "skills frontend backend full stack devops projects experience"
    )

    context = "\n\n".join([
        doc.page_content
        for doc in docs
    ])

    jobs_text = "\n\n".join([
        f"""
        Job ID: {job.job_id}
        Title: {job.title}
        Company: {job.company}
        Location: {job.location}
        """
        for job in jobs
    ])

    parser = PydanticOutputParser(
        pydantic_object=RecommendedJobsResponse
    )

    prompt = PromptTemplate(
        template="""
        You are an AI job recommendation engine.

        Analyze the resume and compare it with the provided jobs.

        Instructions:
        - Calculate a match score from 0 to 100
        - Consider skills, experience, projects, and technologies
        - Provide a short reason for the score
        - Return top matching jobs first

        Resume:
        {context}

        Jobs:
        {jobs}

        {format_instructions}
        """,
        input_variables=[
            "context",
            "jobs"
        ],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )

    llm = get_llm()

    chain = prompt | llm | parser

    response = chain.invoke({
        "context": context,
        "jobs": jobs_text
    })

    return response.model_dump()
