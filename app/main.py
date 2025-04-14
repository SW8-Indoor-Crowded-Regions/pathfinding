from fastapi import FastAPI
from app.routes import routers
from app.config import CORS_SETTINGS
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title='Routing')

# CORS
app.add_middleware(
	CORSMiddleware,
	allow_origins=CORS_SETTINGS['allow_origins'],
	allow_credentials=CORS_SETTINGS['allow_credentials'],
	allow_methods=CORS_SETTINGS['allow_methods'],
	allow_headers=CORS_SETTINGS['allow_headers'],
)

for router in routers:
	app.include_router(router)


if __name__ == '__main__':
	uvicorn.run('app.main:app', host='0.0.0.0', port=8001, reload=True)
