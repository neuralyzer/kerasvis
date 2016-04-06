Keras live visualization
========================


This package visualizes ongoing Keras optimizations live in your browser.
Optimization runs are logged in a database. To use this visualization you have to
add `DBLogger` as callback to your optimization. 

Installation
------------

Install directly from github:

    pip install git+git://github.com/neuralyzer/kerasvis.git 


Quickstart example
------------------


    from kerasvis import DBLogger
    from keras.models import Sequential
    from keras.layers import Dense
    
    model = Sequential()
    model.add(Dense(input_dim=1, 200))
    model.compile("sgd", "binary_crossentropy", class_mode="binary")
    history = model.fit(X, y, nb_epoch=10, batch_size=64, verbose=0,
                        validation_split=0.2, show_accuracy=True, callbacks=[DBLogger(comment="comment")])

Start the keras visualization server with

    python -m kerasvis.runserver --port=5000 --db_path=/path/to/db 
    
to have the server listen to port 5000. Then point your browser to the server and check how your optimizations are doing.
You can also specify the database file to readout. Both part and db_path are optional arguments.

Delete runs from the database
-----------------------------

Runs can be deleted with the `DBLogger`. To delete the run with id 3 you do

    db_logger = DBLogger(id=3)
    db_logger.delete()
    
you will then be asked if you really want to delete and have to confirm with "yes".
