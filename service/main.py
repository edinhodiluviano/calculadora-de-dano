import fastapi


def make_app():
    app = fastapi.FastAPI()

    @app.get("/ping2", status_code=fastapi.status.HTTP_200_OK)
    async def ping():
        return "ok"

    return app


app = make_app()
