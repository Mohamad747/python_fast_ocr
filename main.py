import os, json, urllib.request
from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
from rapidocr_onnxruntime import RapidOCR

app = FastAPI()
engine = RapidOCR()
API_KEY = os.environ["API_KEY"]

class LLMIn(BaseModel):
    prompt: str
    text: str = ""
    as_json: bool = False  # true = force une réponse JSON

def check(key):
    if key != API_KEY:
        raise HTTPException(status_code=401)

@app.post("/ocr")
async def ocr(request: Request, x_api_key: str = Header()):
    check(x_api_key)
    result, _ = engine(await request.body())
    return {"text": " ".join(l[1] for l in result or [])}

@app.post("/llm")
def llm(body: LLMIn, x_api_key: str = Header()):
    check(x_api_key)
    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": body.prompt + "\n\n" + body.text,
        "stream": False,
        "keep_alive": -1,
        "options": {"temperature": 0},
    }
    if body.as_json:
        payload["format"] = "json"
    req = urllib.request.Request("http://localhost:11434/api/generate",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        reponse = json.loads(r.read())["response"]
    return {"response": json.loads(reponse) if body.as_json else reponse}