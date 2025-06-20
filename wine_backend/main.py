from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from wine_pairing import describe_chain, retrieve_chain, recommend_chain

load_dotenv()
app = FastAPI()

# 체인 구성
r1 = describe_chain()
r2 = retrieve_chain()
r3 = recommend_chain()
chain = r1 | r2 | r3

class ImageRequest(BaseModel):
    image_urls: List[str]

@app.post("/recommend")
def recommend_wine(request: ImageRequest):
    res = chain.invoke({"image_urls": request.image_urls})
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
