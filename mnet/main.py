#!/usr/bin/env python

# Create the application
from mnet.application import app
import auth

app.secret_key = 'SUPER SECRET KEY (dont tell)'

# Load up all of the views
import mnet.views

if __name__ == "__main__":
    app.debug = True
    app.run()
