import getpass
import os
import sqlite3
import warnings
import json


class DBLogger:
    """
    Log Keras optimization to a database and delete runs.

    Parameters
    ----------

    comment: str
        A comment which helps to identify the optimization run

    id : int
        Supply this argument if you want to continue an optimization with the given id.

    db_path: str, default=None
        If not supplied the db is stored in ~/tmp/keras_logs.db
    """
    def __init__(self, *, comment="No Comment", db_folder=None, id=None):
        super().__init__()
        if db_folder is None:
            db_folder = os.path.join(os.path.expanduser("~"), "tmp")
        try:
            os.makedirs(db_folder)
        except FileExistsError:
            pass
        db_path = os.path.join(db_folder, "keras_logs.db")
        self.connection = sqlite3.connect(db_path, timeout=60)
        self._create_tables()
        self._init_record(id, comment)
        print(self, flush=True)

    def delete(self):
        res = input("Really delete id={}? Confirm with \"yes\"".format(self.id))
        if res == "yes":
            with self.connection:
                self.connection.execute("DELETE FROM run WHERE id=?", (self.id,))
                self.connection.execute("DELETE FROM log WHERE runid=?", (self.id,))
            print("Deleted")
        else:
            print("Nothing done")

    def _init_record(self, id, comment):
        user = getpass.getuser()
        with self.connection:
            if id is not None:  # continue optimization
                self.id = id
                comment = self.comment
                if comment is not None:
                    warnings.warn("Comment loaded from database. Supplied comment ignored.")
            else:  # start new optimization
                cursor = self.connection.execute("INSERT INTO run (comment, user) VALUES (?,?)", (comment, user))
                self.id = cursor.lastrowid

    @property
    def comment(self):
        with self.connection:
            comment = self.connection.execute("SELECT comment from run WHERE id=?", (self.id,)).fetchone()[0]
        return comment

    @comment.setter
    def comment(self, value):
        with self.connection:
            self.connection.execute("UPDATE run SET comment=? WHERE id=?", (value, self.id))

    @property
    def config(self):
        with self.connection:
            config = self.connection.execute("SELECT config from run WHERE id=?", (self.id,)).fetchone()[0]
        return config

    def _create_tables(self):
        with self.connection:
            self.connection.execute("""CREATE TABLE IF NOT EXISTS
                                       run (id INTEGER PRIMARY KEY, comment TEXT, user TEXT, config TEXT)""")
            self.connection.execute("""CREATE TABLE IF NOT EXISTS
                                       log (id INTEGER PRIMARY KEY, runid INTEGER, loss REAL, acc REAL,
                                            val_loss REAL, val_acc REAL, epoch INTEGER,
                                            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)""")

    def __repr__(self):
        return "{}({}, \"{}\")".format(self.__class__.__name__, self.id, self.comment)

    def on_train_begin(self, logs={}):
        self._store_config()

    def on_epoch_end(self, epoch, logs=None):
        loss = logs['loss']
        acc = logs.get('acc', None)
        val_loss = logs.get("val_loss", None)
        val_acc = logs.get("val_acc", None)
        self._write(loss, acc, epoch, val_loss, val_acc)

    def _store_config(self):
        if self.config is None:
            if hasattr(self, "model"):
                try:
                    config = self.model.to_json()
                except Exception:
                    config = str(self.model.get_config())
                optimizer_config = json.dumps(self.model.optimizer.get_config())
                config = config[:-1] + ", \"optimizer\":" + optimizer_config + " }"
                with self.connection:
                    self.connection.execute("UPDATE run set config=? WHERE id=?", (config, self.id))
        else:
            warnings.warn("Config already exists. Config was NOT overwritten.")

    def _write(self, loss, acc, epoch, val_loss, val_acc):
        with self.connection:
            self.connection.execute("INSERT INTO log (runid, loss, acc, epoch, val_loss, val_acc) VALUES (?,?,?,?,?,?)",
                                    (self.id, loss, acc, epoch, val_loss, val_acc))


    # these her are copief from keras.callback to avoid the keras import
    # and the initialization of theano caused by it
    def _set_params(self, params):
        self.params = params

    def _set_model(self, model):
        self.model = model

    def on_epoch_begin(self, epoch, logs={}):
        pass

    def on_batch_begin(self, batch, logs={}):
        pass

    def on_batch_end(self, batch, logs={}):
        pass

    def on_train_end(self, logs={}):
        pass
