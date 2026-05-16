from fastapi import APIRouter, Request, HTTPException, Depends
from starlette.responses import RedirectResponse
from ..auth import oauth, create_access_token, get_current_user
from ..database import get_database
import os

router = APIRouter(prefix="/auth", tags=["auth"])
db = get_database()

@router.get("/google")
async def google_login(request: Request):
    redirect_uri = os.getenv("BASE_URL") + "/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        if not user_info:
             raise HTTPException(status_code=400, detail="Failed to fetch user info")
        
        email = user_info['email']
        name = user_info['name']
        google_id = user_info['sub']

        # Save or update user in DB
        await db.users.update_one(
            {"google_id": google_id},
            {"$set": {"email": email, "name": name, "google_id": google_id}},
            upsert=True
        )

        # Create JWT
        access_token = create_access_token(data={"sub": email})
        
        # Redirect to frontend with token in URL (simple way for vanilla frontend)
        # Or better, redirect to a static page that saves it to localStorage
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8000/login.html")
        return RedirectResponse(url=f"{frontend_url}?token={access_token}")
    except Exception as e:
        print(f"Auth error: {e}")
        raise HTTPException(status_code=400, detail="Authentication failed")

@router.get("/me")
async def get_me(current_user: str = Depends(get_current_user)):
    user = await db.users.find_one({"email": current_user})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user['_id'] = str(user['_id'])
    return user
