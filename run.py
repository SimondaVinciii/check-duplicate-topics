
from dupliapp.main import create_app
from dupliapp.config import settings


app = create_app()

if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT)