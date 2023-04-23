#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception):
    """Closes the database session after each request."""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def display_states_list():
    """Displays a HTML page with a list of all the State objects."""
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=states_sorted)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
