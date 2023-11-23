from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# CORSミドルウェアの設定
origins = [
    "http://localhost:8000",
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイルのホスティング(javascript等が記述されているhtmlファイルの場合はここにhtmlファイルが入っているディレクトリを指定)
app.mount("/webapp", StaticFiles(directory="webapp"), name="webapp")

class TextItem(BaseModel):
    content: str

# テキストを保存するための変数
current_text = ""

@app.post("/send_text/")
async def send_text(item: TextItem):
    global current_text
    current_text = item.content
    return {"status": "success"}

@app.get("/get_text/")
def get_text():
    return {"content": current_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
