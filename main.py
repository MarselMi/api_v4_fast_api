from fastapi import FastAPI
import uvicorn

from core.config import settings
from api_v4 import router as router_v4

app = FastAPI()
app.include_router(router=router_v4, prefix=settings.api_v4_prefix)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
