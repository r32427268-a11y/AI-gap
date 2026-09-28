from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
def interview_test():
    return {
        "message": "Interview route is working"
    }
