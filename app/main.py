from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import json

app = FastAPI(
    title="Patch Server",
    description="Patch upload, download, and version management",
    version="1.0",
    docs_url="/docs",
    redoc_url=None
)

# 서버 내부 패치 저장 폴더 (컨테이너에서 /app/patches와 연결)
PATCH_DIR = "patches"
os.makedirs(PATCH_DIR, exist_ok=True)

# version.json 경로
VERSION_FILE = os.path.join(PATCH_DIR, "version.json")
if not os.path.exists(VERSION_FILE):
    # 초기값 없으면 생성
    with open(VERSION_FILE, "w") as f:
        json.dump({"version": "0.0", "file": ""}, f)


@app.get("/")
def root():
    return {"message": "Patch Server Running"}


# ----------------------------
# 업로드 API (upload2)
# ----------------------------
@app.post("/patch/upload2")
async def upload_patch(file: UploadFile = File(...)):
    file_path = os.path.join(PATCH_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 업로드한 파일이 최신 버전으로 적용되도록 version.json도 업데이트 가능
    # (옵션: 필요하면 여기에 version 정보 입력)
    return {"message": "Patch uploaded", "filename": file.filename}


# ----------------------------
# 최신 버전 조회 API
# ----------------------------
@app.get("/patch/latest")
def get_latest_patch():
    with open(VERSION_FILE, "r") as f:
        data = json.load(f)
    return data


# ----------------------------
# 다운로드 API
# ----------------------------
@app.get("/patch/download/{filename}")
def download_patch(filename: str):
    file_path = os.path.join(PATCH_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Patch file not found")
    return FileResponse(file_path)