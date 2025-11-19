from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from jose import jwt, JWTError
import pandas as pd
import os


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
DATA_DIR = os.getenv("DATA_DIR", "./data")
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="Elden Ring Dataset API")

@app.get("/")
def root():
    return {"message": "Welcome to my ELDEN RING API!"}

# Hardcoded demo users
VALID_USERS = {
    "admin": "password123"
}


# ---------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime


# ---------------------------------------------------------
# JWT Utility
# ---------------------------------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generates a signed JWT token."""
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    ))
    to_encode.update({"exp": expire})

    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded, expire


# ---------------------------------------------------------
# Authentication
# ---------------------------------------------------------
@app.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint → Returns JWT access token."""
    username, password = form_data.username, form_data.password

    if username not in VALID_USERS or VALID_USERS[username] != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token, expires = create_access_token({"sub": username})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_at=expires
    )


def verify_token(authorization: Optional[str] = Header(None)) -> str:
    """Extracts and validates the Bearer token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = parts[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ---------------------------------------------------------
# File Discovery
# ---------------------------------------------------------
@app.get("/files", response_model=List[str])
def list_csv_files(user: str = Depends(verify_token)):
    """
    Recursively lists all CSV files under the data directory.
    Returns paths relative to /data (e.g. 'armors.csv', 'items/consumables.csv')
    """
    csv_files = []

    for root, _, files in os.walk(DATA_DIR):
        for f in files:
            if f.lower().endswith(".csv"):

                full_path = os.path.join(root, f)

                rel_path = os.path.relpath(full_path, DATA_DIR)
                rel_path = rel_path.replace("\\", "/")  # Normalize Windows paths

                csv_files.append(rel_path)

    return sorted(csv_files)


# ---------------------------------------------------------
# CSV Data Access
# ---------------------------------------------------------
@app.get("/data")
def get_data(
    file: str,
    page: int = 1,
    page_size: int = 100,
    q: Optional[str] = None,
    user: str = Depends(verify_token)
):
    """
    Reads a CSV file and returns its data with pagination and optional search.
    Supports nested paths like 'items/consumables.csv'.
    """

    # Build safe normalized path
    safe_path = os.path.normpath(os.path.join(DATA_DIR, file))
    base_path = os.path.normpath(DATA_DIR)

    # Prevent path traversal attacks
    if not safe_path.startswith(base_path):
        raise HTTPException(status_code=400, detail="Invalid file path")

    # Check existence
    if not os.path.isfile(safe_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Load CSV
    try:
        df = pd.read_csv(safe_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read CSV: {e}")

    # Search filter
    if q:
        q_lower = q.lower()
        mask = df.astype(str).apply(
            lambda col: col.str.lower().str.contains(q_lower, na=False)
        )
        df = df[mask.any(axis=1)]

    total_rows = len(df)
    start = (page - 1) * page_size
    rows = df.iloc[start:start + page_size].fillna("").to_dict(orient="records")

    return {
        "file": file,
        "total_rows": total_rows,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_rows + page_size - 1) // page_size,
        "rows": rows
    }
