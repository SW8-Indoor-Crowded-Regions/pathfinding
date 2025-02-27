from fastapi import FastAPI
from app.routes.routing import router
from app.config import CORS_SETTINGS
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Routing")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_SETTINGS["allow_origins"],
    allow_credentials=CORS_SETTINGS["allow_credentials"],
    allow_methods=CORS_SETTINGS["allow_methods"],
    allow_headers=CORS_SETTINGS["allow_headers"],
)


# ROUTING ROUTER
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)

# In production use Gunicorn to run Uvicorn with workers
# Below is an example with -w 4 meaning 4 workers processes assigned
#
# pip install gunicorn
# gunicorn -k uvicorn.workers.UvicornWorker -w 4 app.main:app
