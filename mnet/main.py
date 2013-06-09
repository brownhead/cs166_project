#!/usr/bin/env python

# Create the application
from mnet.application import app

# Load up all of the views
import mnet.views

if __name__ == "__main__":
    app.run()
