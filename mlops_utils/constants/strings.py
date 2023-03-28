import os

# jwt
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")

# model
MODEL_NAME = os.environ.get("MLOPS_MODEL_NAME")
MODEL_STAGE = os.environ.get("MLOPS_MODEL_STAGE", "latest")

# exception messages
INVALID_TOKEN_OR_EXPIRED_TOKEN = "invalid token or expired"
INVALID_AUTHENTICATION_SCHEME = "invalid authentication scheme"
INVALID_AUTHORIZATION_CODE = "invalid authorization code"
AUTHENTICATION_REQUIRED = "authentication required"

# auth
BEARER = "Bearer"

# http
# ALLOWED_HOSTS = ["*"]
