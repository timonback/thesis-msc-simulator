import waitress
from server.app import get_app


def serve():
    # windows specific
    # change to gunicorn for UNIX
    waitress.serve(get_app(), port=8888)


# Execute
if __name__ == "__main__":
    # execute only if run as a script
    serve()
