# Simple Weather Forecast Web-App.

This is a small web-app written in *Python* with *Flask* that serves a 7-day weather forecast for a location given as input by a client user.
The App uses a public weather-forecast API service together with an I.P Geolocation API.

*This App is built and designed mainly for the use of testing DevOps environments of Pipelines and Automations.*

This repo includes a *Dockerfile* for running the app in a container.
The container runs the app behind a *Gunicorn WSGI* service for production environments.

Also included is a small Unit-Test Python file for running some HTTP request tests on the app using *Selenium* and *Unittest* Python Modules.

* Feel free to clone, edit and use as you wish
* Update your own API keys for the App to work properly.
* Container exposes *port 8080* for HTTP access to the web-app.
