from fastapi import FastAPI

app = FastAPI()

@app.get("/suggest")
def suggest(query: str):
    if "đắng" in query:
        return {"suggestion": "Espresso - vị đậm đà cho gu mạnh"}
    if "ngọt" in query:
        return {"suggestion": "Latte - béo nhẹ, dễ uống"}
    return {"suggestion": "Cold Brew - thanh mát, hợp mùa hè"}
