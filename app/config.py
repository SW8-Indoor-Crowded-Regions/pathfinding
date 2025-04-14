# from fastapi.middleware.cors import CORSMiddleware


# Allowed CORS origins
ALLOWED_ORIGINS = [
	'http://localhost:8000',  # Only allows requests from gateway
]


CORS_SETTINGS = {
	'allow_origins': ALLOWED_ORIGINS,
	'allow_credentials': True,
	'allow_methods': ['*'],  # Allow all methods (GET, POST, etc...)
	'allow_headers': ['*'],  # Allow all headers
}
