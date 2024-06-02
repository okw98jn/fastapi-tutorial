from src.utils.environment import get_env_variable

# JWTシークレットキー
JWT_SECRET_KEY = get_env_variable("JWT_SECRET_KEY")

# JWTトークンの署名に使用するアルゴリズム
ALGORITHM = "HS256"

# トークンの有効期限
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Google認証URL
GOOGLE_AUTHORIZATION_URL = get_env_variable("GOOGLE_AUTHORIZATION_URL")

# GoogleクライアントID
GOOGLE_CLIENT_ID = get_env_variable("GOOGLE_CLIENT_ID")

# Googleクライアントシークレット
GOOGLE_CLIENT_SECRET = get_env_variable("GOOGLE_CLIENT_SECRET")

# GoogleコールバックURL
GOOGLE_CALLBACK_URL = get_env_variable("GOOGLE_CALLBACK_URL")
