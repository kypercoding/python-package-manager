# Python Package Manager

## Overview

The goal of this web application is to manage Python environments and packages on a high-level. This web application makes use of another project, the [package-manager-api]("https://github.com/kypercoding/package-manager-api"), as a backend service to store all Python environments and packages. The web application itself manages users through Flask-Login and JWT tokens, utilizing the Redis database to keep track of users' tokens.

A brief visual overview of the application's functionality can be seen below:

![](/Python%20Package%20Manager%20Diagram.jpg)

## Deployment

This web application was deployed on a DigitalOcean Droplet, configured with nginx, gunicorn, and Let's Encrypt. To access the deployed web application, click on: [LINK](https://www.ppm.kyperapps.com).

## Install

For users who desire to use this web application locally, this program requires the following:
* package-manager-api (see other repository for installation instructions)
* Redis
* Python, with pip requirements

To locally use the program:

1. Clone this repository into a directory of your choice.
2. Change to the directory of the repository (/python-package-manager).
3. Create a virtual Python environment and activate it.
4. With the environment activated, install the packages in the requirements.txt file (i.e. pip install -r requirements.txt).
5. Run the Redis server on a host, port, and database of your choice (remember these for the next step).
6. Run server.py with the command-line arguments:

```shell
python server.py BASE_URL HOST PORT DB
```

where BASE_URL is the base URL of the API (i.e. http://localhost:3000, if the API server is being run locally on a different port), the Redis host (i.e. "127.0.0.1" for a local Redis instance), the Redis port (i.e. 6379 for a local Redis instance) and the DB number (i.e. 0 for a local Redis instance). You can also call:

```
python server.py -h
```

for instructions. Note that Linux users may have to call "python3" instead of "python".

## Usage

When you click the web application's link (or run it on your local machine), you will be greeted by a simple screen with two buttons: "Registration" and "Login".

### Registration

To register an account, click on "Registration". Then, input a username and password combination. If successful, this should take you to the login screen. Otherwise, the page will clear and reload, making you register again.

### Login

To login, click on "Login" (or by now you will have been redirected there from the registration page). Input your username and password. This should take you to a page called "Dashboard".

### Dashboard

On the "Dashboard" page, you will be greeted by four inputs: a text box, "Create Environment" button, "Delete Environments" button, and "Logout" button.

### Create an environment

To create an environment, type an environment name in the text, such as "python-flask-environment". Then, click "Create Environment". You may need to reload to see a new clickable link labeled with the name of your environment.

### Add packages

To add packages to your environment, click on the clickable link labeled with the name of your environment. It should result in a pop-up appearing on your screen, with the name of the environment, a text box next to text "Add Packages", and a button labeled "Submit". To add packages, type in Python packages separated by spaces, and click "Submit" (i.e. "flask passlib flask-login"). Once you click "Submit", the page will redirect back to the dashboard. Click on the clickable link of your environment to see the packages under the environment name, separated by spaces, in a gray box. You may need to reload again if they don't appear. Now, the packages are available, for instance, to copy into the terminal and call a pip install command.

### Clear your environments

To delete all your environments, click "Delete Environments". This will clear all environments associated with your account.

### Logout

To logout, click "Logout".

## Tasks
- [x] Implemented basic creation of GET, POST, DELETE, and PUT endpoints of package-manager-api.
- [x] Created a functional front-end that takes in basic text input.
- [x] Implemented a basic Redis-based cache of users' JWT tokens.
- [x] Deployed on DigitalOcean Droplet.
- [ ] Handle inactive JWT tokens in the Redis cache.
- [ ] Significantly spruce up the front-end with more jQuery UI elements and/or other user-friendly elements.

More tasks may appear as time goes on.

## Notes

* This project was inspired by an older project called "py-pro-manager" (Python Project Manager). This web application, however, makes use of API calls to store environment data, allowing for higher-level programming in managing Python environments and packages (as opposed to a direct interaction between web application and database).
