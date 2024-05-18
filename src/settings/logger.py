import logging
import os
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    ログファイルを日付ごとにローテーションするためのクラス
    ログファイルの保存先は、logs/Ymd/ファイル名となる
    """

    def __init__(
        self,
        log_dir,
        filename,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding=None,
        delay=False,
        utc=False,
        atTime=None,
    ):
        self.log_dir = log_dir
        self.filename = filename
        super().__init__(
            self._get_log_file_path(),
            when,
            interval,
            backupCount,
            encoding,
            delay,
            utc,
            atTime,
        )

    def _get_log_file_path(self):
        date_str = datetime.now().strftime("%Y%m%d")
        dated_log_dir = os.path.join(self.log_dir, date_str)
        os.makedirs(dated_log_dir, exist_ok=True)  # ディレクトリ作成
        return os.path.join(dated_log_dir, self.filename)


# フィルタの設定
class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level):
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level


log_dir = "src/logs"

logger = logging.getLogger("uvicorn")

logger.setLevel(logging.INFO)

# フォーマッタの設定
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s in %(pathname)s:%(lineno)d",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ストリームハンドラーの設定
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# アプリケーションログ用ファイルハンドラーの設定（毎日ローテーション）
app_handler = CustomTimedRotatingFileHandler(
    log_dir, "app.log", when="midnight", interval=1, backupCount=30
)
app_handler.setFormatter(formatter)
app_handler.setLevel(logging.INFO)

# エラーログ用ファイルハンドラーの設定（毎日ローテーション）
error_handler = CustomTimedRotatingFileHandler(
    log_dir, "error.log", when="midnight", interval=1, backupCount=30
)
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.WARNING)

# app_handlerにフィルタを追加してWARNINGレベル未満のログのみを記録
app_handler.addFilter(MaxLevelFilter(logging.INFO))

# ハンドラーをロガーに追加
logger.addHandler(stream_handler)
logger.addHandler(app_handler)
logger.addHandler(error_handler)
