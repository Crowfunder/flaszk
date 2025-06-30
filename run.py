from app.app import create_app
import os

app = create_app()
socketio = app.socketio

if __name__ == "__main__":
    if not os.getenv('FLASK_RUN_PORT'):
        os.environ['FLASK_RUN_PORT'] = "9002"
    port=os.getenv('FLASK_RUN_PORT')
    socketio.run(app, host="0.0.0.0", port=port, use_reloader=False)