import time
from flask import Flask, render_template
from kerasvis.server.plots import empty_plot, loss_accuracy_plot
from kerasvis.server.dataloader import LogDataLoader, to_dict


app = Flask(__name__)


@app.route("/")
def main():
    try:
        log = LogDataLoader(path=app._keras_log_db_path)
        return render_template("overview.html", data=zip(*log.get_overview()))
    except ValueError:
        return render_template("nodb.html")


@app.route("/id/<int:id>")
def detail(id):
    start_time = time.time()
    log = LogDataLoader(path=app._keras_log_db_path)
    if not log.id_exists(id):
        return render_template("idnotfound.html", id=id)
    comment = log.get_comment(id)
    df = log.get_data(id)
    last_update_time = log.get_last_update_time(id)
    config_string = log.get_config(id)
    config_dict = to_dict(config_string)
    duration = time.time() - start_time
    return render_template("detail.html",
                           loss=loss_accuracy_plot(df, "epoch", [["loss", "val_loss"], ["acc", "val_acc"]]) if log.id_exists(id) and len(df) > 0 else empty_plot,
                           comment=comment,
                           id=id,
                           config_data=config_string,
                           layers=config_dict["layers"],
                           general={key: value for key, value in config_dict.items()if key != "layers"},
                           last_update_time=last_update_time,
                           runs=zip(*log.get_overview()[:2]),
                           db_load_time=str(round(duration, 2)) + " s")


app.debug = True
