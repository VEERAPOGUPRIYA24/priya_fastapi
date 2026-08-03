import jwt
from fastapi import Request, HTTPException

SECRET_KEY = "abcdefghijklmnopqrtuvwxyz"
ALGORITHM = "HS256"


# Check whether the user is logged in
def authenticated_user(request: Request):

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Login required"
        )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )


# Admin only
def admin_only(user):

    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can access"
        )


# Admin or Developer
def admin_or_dev(user):

    if user["role"] not in ["admin", "dev"]:
        raise HTTPException(
            status_code=403,
            detail="Only Admin or Developer can access"
        )


# Any logged-in user (Admin, Dev, Intern)
def all_users(user):

    if user["role"] not in ["admin", "dev", "intern"]:
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )