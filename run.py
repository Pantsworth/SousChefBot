__author__ = 'DoctorWatson'
#!/usr/bin/env python
from project import app

if __name__ == "__main__":
    app.debug = True
    # Because we did not initialize Flask-SQLAlchemy with an application
    # it will use `current_app` instead.  Since we are not in an application
    # context right now, we will instead pass in the configured application
    # into our `create_all` call.
    app.run()
