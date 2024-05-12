import logging
import os
import sys

log_dir: str = "src/logs"

# ディレクトリが存在しない場合に作成
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger()

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s in %(pathname)s:%(lineno)d",
    datefmt="%Y-%m-%d %H:%M:%S",
)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

app_handler = logging.FileHandler(log_dir + "/app.log")
app_handler.setFormatter(formatter)
app_handler.setLevel(logging.INFO)

error_handler = logging.FileHandler(log_dir + "/error.log")
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.ERROR)

logger.handlers = [stream_handler, app_handler, error_handler]
