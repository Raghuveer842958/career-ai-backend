def serialize_user(user) -> dict:

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user["age"]
    }

def serialize_job(job) -> dict:
    return {
        'id': str(job['_id']),
        'job_id': job["job_id"],
        'title': job["title"],
        'company': job["company"],
        'location': job["location"],
        'link': job["link"],
    }


def serialize_job2(job) -> dict:
    return {
        'id': str(job['_id']),
        'job_id': job["job_id"],
        'job_title': job["job_title"],
        'employer_name': job["employer_name"],
        'employer_logo': job["employer_logo"],
        'employer_website': job["employer_website"],
        'job_apply_link': job["job_apply_link"]
    }