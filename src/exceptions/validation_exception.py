from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def translate_error_message(errors):
    translated_errors = []

    for error in errors:
        # フィールド名を取得
        loc = error["loc"][-1]

        # フロントで使用しやすいようにエラーメッセージを整形
        translated_error = {"loc": loc, "msg": error["msg"]}

        # エラーメッセージを追加
        translated_errors.append(translated_error)

    return translated_errors


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422, content={"detail": translate_error_message(exc.errors())}
    )
