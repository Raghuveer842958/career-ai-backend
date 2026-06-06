from fastapi import APIRouter, HTTPException
from bson import ObjectId
from bson.errors import InvalidId

from models import Job
from utils.helpers import serialize_job
from database import jobs_collection

router = APIRouter()

@router.post('/')
def create_job(job: Job):

    try:

        existing_job = jobs_collection.find_one({
            'job_id': job.job_id
        })

        print("existing_job is :", existing_job)

        if existing_job:
            raise HTTPException(
                status_code= 404,
                detail= "job already exist"
            )
        
        result = jobs_collection.insert_one(job.dict())
        print("resulet is :", result)
        created_job = jobs_collection.find_one({'_id': result.inserted_id})
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


@router.get('/')
def get_all_jobs():
    try:
        jobs = []
        # MongoDB does NOT fetch all records immediately.
        # cursor object, Think of Cursor Like Iterator
        # cursor lazily fetches documents one by one
        # This is memory efficient.
        all_jobs = jobs_collection.find()
        
        # for i, job in enumerate(all_jobs):
        #     print(f"user {i+1} -> {job}")

        for job in jobs_collection.find():
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
def get_job_by_id(job_id: str):

    print("job_id is :", job_id)

    if not ObjectId.is_valid(job_id):
        raise HTTPException(
            status_code=404,
            detail= "Invalid job id"
        )
    
    job = jobs_collection.find_one({'_id': ObjectId(job_id)})
    print("job is :", job)

    if not job:
        raise HTTPException(
            satus_code=404,
            detail= "Job not fond"
        )
    
    return {
        'job': serialize_job(job)
    }


@router.put('/{job_id}')
def update_job(job_id: str, updated_job: Job):

    try:

        if not ObjectId.is_valid(job_id):
            raise HTTPException(
                status_code=404,
                detail= "Invalid job id"
            )
    
        existing_job = jobs_collection.find_one({'_id': ObjectId(job_id)})

        if not existing_job:
            raise HTTPException(
                status_code= 404,
                detail= 'Job not found'
            )
        
    
        temp = jobs_collection.update_one(
            {'_id': ObjectId(job_id)}, 
            {
                "$set": updated_job.dict()
            }
        )

        print("temp is :", temp)
        new_updated_job = jobs_collection.find_one({'_id': ObjectId(job_id)})

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
def delete_job(job_id: str):
    try:

        if not ObjectId.is_valid(job_id):
            raise HTTPException(
                stauts_code=404,
                detail= "Id not found"
            )
        
        existing_job = jobs_collection.find_one({'_id': ObjectId(job_id)})

        if not existing_job:
            raise HTTPException(
                status_code= 404,
                detail= "Job not found"
            )
        
        deleted_job = jobs_collection.delete_one({'_id': ObjectId(job_id)})
        print("deleted job is :",deleted_job)

        return {
            'message': "job deleted successfully",
        }

    except HTTPException as e:
        raise e


    except Exception as e:
        raise HTTPException(
            status_code= 500,
            detail= "Internal server Error"
        )