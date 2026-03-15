from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import json

app = FastAPI()

PATCH_DIR = "patch_files"
os.makedirs(PATCH_DIR, exist_ok=True)



@app.get("/")
def root():
    return {"message": "Patch Server Running"}


PATCH_DIR = "patch_files"
os.makedirs(PATCH_DIR, exist_ok=True)

@app.post("/patch/upload")
async def upload_patch(file: UploadFile = File(...)):
    file_path = os.path.join(PATCH_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"message": "patch uploaded", "filename": file.filename}

PATCH_DIR = "/app/patches"
VERSION_FILE = os.path.join(PATCH_DIR, "version.json")

@app.get("/patch/latest")
def get_latest_patch():
    with open(VERSION_FILE, "r") as f:
        data = json.load(f)
    return data


@app.get("/patch/download/{filename}")
def download_patch(filename: str):
    file_path = os.path.join(PATCH_DIR, filename)
    return FileResponse(file_path)