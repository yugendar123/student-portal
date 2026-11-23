from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from dotenv import load_dotenv
import os
from database import get_db, engine, Base
from models import User


load_dotenv()


app = FastAPI()


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv(
        "SESSION_SECRET",
        "dev-only-change-this-secret"
    ),
    session_cookie="student_portal_session",
    max_age=3600,
    same_site="lax",
    https_only=False
)


templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return password_hash.verify(
        plain_password,
        hashed_password
    )




Base.metadata.create_all(bind=engine)



def get_current_user(
    request: Request,
    db: Session
):
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    return db.query(User).filter(
        User.id == user_id
    ).first()


@app.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_current_user(request, db)

    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "user": user
        }
    )



@app.get("/register")
def register_page(request: Request):

    return templates.TemplateResponse(
        request,
        "register.html",
        {}
    )



@app.post("/register")
def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:

        return templates.TemplateResponse(
            request,
            "register.html",
            {
                "error": "All fields are required.",
                "name": name,
                "email": email
            },
            status_code=400
        )
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:

        return templates.TemplateResponse(
            request,
            "register.html",
            {
                "error": "Email already registered.",
                "name": name,
                "email": email
            },
            status_code=400
        )

    hashed_password = hash_password(password)

    new_user = User(
        name=name,
        email=email,
        password_hash=hashed_password,
        role="student"
    )

    try:

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception:

        db.rollback()
        raise

    return RedirectResponse(
        url="/login?registered=1",
        status_code=303
    )



@app.get("/login")
def login_page(
    request: Request,
    registered: int = 0
):

    return templates.TemplateResponse(
        request,
        "login.html",
        {
            "registered": registered
        }
    )



@app.post("/login")
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    email = email.strip().lower()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user or not verify_password(
        password,
        user.password_hash
    ):

        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "error": "Invalid email or password."
            },
            status_code=401
        )

    request.session.clear()

    request.session["user_id"] = int(user.id)

    if user.role == "admin":

        return RedirectResponse(
            url="/admin",
            status_code=303
        )

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )



@app.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_current_user(request, db)

    if not user:

        request.session.clear()

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    # Admin should use admin page

    if user.role == "admin":

        return RedirectResponse(
            url="/admin",
            status_code=303
        )

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "user": user
        }
    )



# ==========================================
# ADMIN DASHBOARD - VIEW ALL USERS
# ==========================================

@app.get("/admin")
def admin_page(
    request: Request,
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)

    if not user:
        return RedirectResponse("/login", status_code=303)

    if user.role != "admin":
        return templates.TemplateResponse(
            request,
            "access_denied.html",
            {"user": user},
            status_code=403
        )

    # Get all registered users
    users = db.query(User).order_by(User.id.desc()).all()

    # Count students
    total_students = db.query(User).filter(
        User.role == "student"
    ).count()

    total_users = db.query(User).count()

    return templates.TemplateResponse(
        request,
        "admin.html",
        {
            "user": user,
            "users": users,
            "total_students": total_students,
            "total_users": total_users
        }
    )


# ==========================================
# CHANGE USER ROLE
# ==========================================

@app.post("/admin/users/{user_id}/role")
def change_user_role(
    user_id: int,
    request: Request,
    role: str = Form(...),
    db: Session = Depends(get_db)
):
    admin = get_current_user(request, db)

    if not admin:
        return RedirectResponse("/login", status_code=303)

    if admin.role != "admin":
        return templates.TemplateResponse(
            request,
            "access_denied.html",
            {"user": admin},
            status_code=403
        )

    # Only allow these roles
    if role not in ["student", "admin"]:
        return RedirectResponse("/admin", status_code=303)

    target_user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not target_user:
        return RedirectResponse("/admin", status_code=303)

    # Admin cannot change their own role
    if target_user.id == admin.id:
        return RedirectResponse("/admin", status_code=303)

    # Do not remove the last administrator
    if target_user.role == "admin" and role == "student":
        admin_count = db.query(User).filter(
            User.role == "admin"
        ).count()

        if admin_count <= 1:
            return RedirectResponse("/admin", status_code=303)

    target_user.role = role
    db.commit()

    return RedirectResponse("/admin", status_code=303)


# ==========================================
# DELETE USER
# ==========================================

@app.post("/admin/users/{user_id}/delete")
def delete_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    admin = get_current_user(request, db)

    if not admin:
        return RedirectResponse("/login", status_code=303)

    if admin.role != "admin":
        return templates.TemplateResponse(
            request,
            "access_denied.html",
            {"user": admin},
            status_code=403
        )

    target_user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not target_user:
        return RedirectResponse("/admin", status_code=303)

    # Admin cannot delete their own account
    if target_user.id == admin.id:
        return RedirectResponse("/admin", status_code=303)

    # Protect the last administrator
    if target_user.role == "admin":
        admin_count = db.query(User).filter(
            User.role == "admin"
        ).count()

        if admin_count <= 1:
            return RedirectResponse("/admin", status_code=303)

    db.delete(target_user)
    db.commit()

    return RedirectResponse("/admin", status_code=303)
@app.get("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )