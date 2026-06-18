from fastapi import APIRouter, HTTPException
from bson import ObjectId
from bson.errors import InvalidId
from typing import List
from bson import ObjectId
from pydantic import BaseModel

from app.models import Job
from app.utils.helpers import serialize_job
# from app.database import jobs_collection
import app.database as database

router = APIRouter()

class JobInput(BaseModel):
    job_id: str
    title: str
    company: str
    location: str | None = None
    link: str | None = None


@router.post('/')
async def create_job(job: Job):
    try:

        existing_job = await database.jobs_collection.find_one({
            'job_id': job.job_id
        })

        print("existing_job is :", existing_job)

        if existing_job:
            raise HTTPException(
                status_code=404,
                detail="job already exist"
            )

        result = await database.jobs_collection.insert_one(
            job.dict()
        )

        print("resulet is :", result)

        created_job = await database.jobs_collection.find_one({
            '_id': result.inserted_id
        })

        print("created_job is :", created_job)

        return {
            'message': 'job created successfully',
            'job': serialize_job(created_job)
        }

    except HTTPException as e:
        raise e

    except Exception as e:

        print("errror is :", e)

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.post("/many")
async def create_many_jobs(job: List[JobInput]):
    try:
        # convert Pydantic models → dicts
        job_dicts = [j.model_dump() for j in job]

        result = await database.jobs_collection.insert_many(job_dicts)

        print("jobs_collection:", database.jobs_collection)
        
        print("result is :-", result)

        created_jobs = []

        for id in result.inserted_ids:
            new_job = await database.jobs_collection.find_one({'_id': id})
            if new_job:
                new_job["_id"] = str(new_job["_id"])
                created_jobs.append(new_job)


        return {
            "message": "Jobs inserted successfully",
            "jobs": created_jobs
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    

@router.get('/')
async def get_all_jobs():

    print("Hello-1")

    try:

        jobs = []

        # MongoDB does NOT fetch all records immediately.
        # cursor object, Think of Cursor Like Iterator
        # cursor lazily fetches documents one by one
        # This is memory efficient.

        # all_jobs = jobs_collection.find()

        all_jobs = database.jobs_collection.find().sort("_id", -1).limit(5)
        
        print("all jobs are :", all_jobs)

        # for i, job in enumerate(all_jobs):
        #     print(f"user {i+1} -> {job}")

        async for job in all_jobs:

            jobs.append(
                serialize_job(job)
            )

        return {
            'jobs': jobs
        }

    except HTTPException as e:
        raise e

    except Exception as e:

        print("error is :", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get('/{job_id}')
async def get_job_by_id(job_id: str):

    print("job_id is :", job_id)

    if not ObjectId.is_valid(job_id):

        raise HTTPException(
            status_code=404,
            detail="Invalid job id"
        )

    job = await database.jobs_collection.find_one({
        '_id': ObjectId(job_id)
    })

    print("job is :", job)

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not fond"
        )

    return {
        'job': serialize_job(job)
    }


@router.put('/{job_id}')
async def update_job(job_id: str, updated_job: Job):

    try:

        if not ObjectId.is_valid(job_id):

            raise HTTPException(
                status_code=404,
                detail="Invalid job id"
            )

        existing_job = await database.jobs_collection.find_one({
            '_id': ObjectId(job_id)
        })

        if not existing_job:

            raise HTTPException(
                status_code=404,
                detail='Job not found'
            )

        temp = await database.jobs_collection.update_one(
            {'_id': ObjectId(job_id)},
            {
                "$set": updated_job.dict()
            }
        )

        print("temp is :", temp)

        new_updated_job = await database.jobs_collection.find_one({
            '_id': ObjectId(job_id)
        })

        return {
            "message": "Job updated successfully",
            "updated_job": serialize_job(new_updated_job)
        }

    except HTTPException as e:
        raise e

    except Exception as e:

        print("error is :", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete('/{job_id}')
async def delete_job(job_id: str):

    try:

        if not ObjectId.is_valid(job_id):

            raise HTTPException(
                status_code=404,
                detail="Id not found"
            )

        existing_job = await database.jobs_collection.find_one({
            '_id': ObjectId(job_id)
        })

        if not existing_job:

            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        deleted_job = await database.jobs_collection.delete_one({
            '_id': ObjectId(job_id)
        })

        print("deleted job is :", deleted_job)

        return {
            'message': "job deleted successfully",
        }

    except HTTPException as e:
        raise e

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail="Internal server Error"
        )