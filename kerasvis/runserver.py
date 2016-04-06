import argparse

argument_parser = argparse.ArgumentParser(description="Keras optimization run visualization")
argument_parser.add_argument("--port", type=int, default=5000, help="Port to run the server on. Defaults to 5000")
argument_parser.add_argument("--db_path",  default=None, help="Path to db. Defaults to ~/tmp/keras_logs.db")
args = argument_parser.parse_args()


if __name__ == "__main__":
    from kerasvis.server.main import app
    if args.db_path is not None:
        app._keras_log_db_path = "sqlite:///" + args.db_path
    else:
        app._keras_log_db_path = None
    app.run(threaded=True, port=args.port)
