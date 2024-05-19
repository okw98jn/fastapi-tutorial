from src.utils.environment import get_env_variable

# JWTシークレットキー
JWT_SECRET_KEY = get_env_variable("JWT_SECRET_KEY")

# JWTトークンの署名に使用するアルゴリズム
ALGORITHM = "HS256"

# トークンの有効期限
ACCESS_TOKEN_EXPIRE_MINUTES = 30
