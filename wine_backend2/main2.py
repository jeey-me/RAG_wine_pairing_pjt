# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from wine_pairing2 import describe_chain, retrieve_chain, recommend_chain


# 체인 연결
r1 = describe_chain()
r2 = retrieve_chain()
r3 = recommend_chain()
chain = r1 | r2 | r3

# FastAPI 앱 생성
app = FastAPI()

class ImageRequest(BaseModel):
    image_urls: List[str]

@app.post("/recommend")
def recommend_wine(request: ImageRequest):
    res = chain.invoke({"image_urls": request.image_urls})
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main2:app", host="127.0.0.1", port=8000, reload=True)

