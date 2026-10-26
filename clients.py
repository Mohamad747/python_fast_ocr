import json
import urllib.request



with open("config.json", encoding="utf-8") as f:
    config = json.load(f)



def call(endpoint, data, content_type):
    req = urllib.request.Request(
        config["api_url"] + endpoint,
        data=data,
        headers={"x-api-key": config["api_key"], "Content-Type": content_type},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def ocr(image_path):
    with open(image_path, "rb") as f:
        return call("/ocr", f.read(), "application/octet-stream")["text"]


def llm(prompt, text="", as_json=False):
    body = json.dumps({"prompt": prompt, "text": text, "as_json": as_json}).encode()
    return call("/llm", body, "application/json")["response"]


if __name__ == "__main__":
    img_path = r"C:\Users\mdakb\Downloads\Capture d'écran 2026-10-26 204110.png"
    texte = ocr(img_path)
    print(texte)
    print(llm("Extrais la date et le montant total en JSON.", texte, as_json=True))