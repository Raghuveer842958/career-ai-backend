from fastapi import APIRouter, HTTPException
from bson import ObjectId
from bson.errors import InvalidId


from app.database import users_collection
from app.models import User
from app.utils.helpers import serialize_user

router = APIRouter()

# -----------------------------------
# CREATE USER
# -----------------------------------
@router.post("/users")
def create_user(user: User):

    try:

        existing_user = users_collection.find_one({
            "email": user.email
        })

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        result = users_collection.insert_one(
            user.dict()
        )

        created_user = users_collection.find_one({
            "_id": result.inserted_id
        })

        return {
            "message": "User created successfully",
            "user": serialize_user(created_user)
        }

    except HTTPException as e:
        raise e

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -----------------------------------
# GET ALL USERS
# -----------------------------------
@router.get("/users")
def get_all_users():

    try:

        users = []

        for user in users_collection.find():
            users.append(
                serialize_user(user)
            )

        return {
            "users": users
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -----------------------------------
# GET SINGLE USER
# -----------------------------------
@router.get("/users/{user_id}")
def get_single_user(user_id: str):

    try:

        if not ObjectId.is_valid(user_id):

            raise HTTPException(
                status_code=400,
                detail="Invalid User ID"
            )

        user = users_collection.find_one({
            "_id": ObjectId(user_id)
        })

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "user": serialize_user(user)
        }

    except HTTPException as e:
        raise e

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -----------------------------------
# UPDATE USER
# -----------------------------------
@router.put("/users/{user_id}")
def update_user(user_id: str, updated_user: User):

    try:

        if not ObjectId.is_valid(user_id):

            raise HTTPException(
                status_code=400,
                detail="Invalid User ID"
            )

        existing_user = users_collection.find_one({
            "_id": ObjectId(user_id)
        })

        if not existing_user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": updated_user.dict()
            }
        )

        updated_data = users_collection.find_one({
            "_id": ObjectId(user_id)
        })

        return {
            "message": "User updated successfully",
            "user": serialize_user(updated_data)
        }

    except HTTPException as e:
        raise e

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -----------------------------------
# DELETE USER
# -----------------------------------
@router.delete("/users/{user_id}")
def delete_user(user_id: str):

    try:

        if not ObjectId.is_valid(user_id):

            raise HTTPException(
                status_code=400,
                detail="Invalid User ID"
            )

        existing_user = users_collection.find_one({
            "_id": ObjectId(user_id)
        })

        if not existing_user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        users_collection.delete_one({
            "_id": ObjectId(user_id)
        })

        return {
            "message": "User deleted successfully"
        }

    except HTTPException as e:
        raise e

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )