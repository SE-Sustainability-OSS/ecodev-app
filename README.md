
# EcoDev App

This app can serve as a template. It includes some basic functionalities such as user login,
customisable components such as navbar menus, and customised component builders such as

### Usage
1. First create a `<new-repository>` in your GitHub, then follow these commands, replacing any mention of `<new-repository>`, with your repo name:

    ```bash
    # Create new folder where you would like your repo to be located on your machine
    mkdir <new-repository>; cd <new-repository>

    # Make a bare clone of this repository
    git clone https://github.com/SE-Sustainability-OSS/ecodev-app

    # Move files to parent directory
    cd .. ; mv <new-repository>/ecodev-app/* <new-repository>/

    # Delete remaining ecodev-app files
    cd <new-repository> ; rm -rf ecodev-app/

    # Remove git file
    rm -rf .git

    # Create new .git file (and optionally rename master to main)
    git init ; git branch -M main

    # Add new remote
    git remote add origin https://github.com/<user>/<new-repository>
    ```


2. Search for and replace any references to `ecodev-app` and `ecodev_app` within the repo, with your own app name.

    - `docker-compose.yml`
    - `docker-compose.override.yml`
    - `Makefile`

    :warning: Do keep the respective `-` and `_` used throughout


3. Update this `README.md` with your own. A template is provided in `README-template.md`

    _Feel free to remove any other markdown file (e.g. `SECURITY.md`, `CODE_OF_CONDUCT.md`, etc.) that are not applicable._

4. Once done, create your first commit and push to your new repo, as you would normally do.
    ```bash
    git add . ; git commit -m 'Initial commit'
    git push origin main
    ```

5. To run your app, follow the `Local development` steps below (also available in the `README-template.md` file)


### Help, Bugs & Feedback

Product Owners: Thomas Epelbaum, Amaury Salles & Yoann Diep

If encountering any bugs, feel free to browse the issue list & contribute!

Use the docs/issues_template whenever possible. It will greatly help the developper team understand the full extent of your bug or feature request.


### Local development

1. Clone the repo and build the docker image:

    ```git
    git clone git@github.com:FR-PAR-ECOACT/ecodev-app.git
    ```

2. Create an `.env` file and save it under the application's root folder. It must contain the following (you have an `env_template` to help you):
    ```.env
    # App name
    app_name= template # Name of the app. Will appear on the app header.

    # API app
    app_port=8000 # API app port number. Remove this entry in production
    fastapi_url= # API app web url. Fill only in production.

    # Dash app
    dash_app_port=8071 # Dash app port number. Remove this entry in production
    dash_url= # Dash app web url.  Fill only in production.

    # Jupyter app
    jupyter_port=5000 # Jupyter notebook port number. Remove this entry in production

    # Database access
    db_port=5432 # Database port number
    db_host=db # Database server name
    db_name=db # Database name
    db_username=user # Database login username. Change to a real username.
    db_password=password # Database login password. Change to a secured password.

    # Hashing secrets
    secret_key=azertyuiopqdfghjklmwxcvbn134567890azertyuiopqsdfghjklmwxcvbn1234567890 # App secret key (for hashing purposed)
    algorithm=HS256 # Password hashing algorithm

    # Other
    access_token_expire_minutes=1440 # App JWT access token expiry duration

    # App mailbox
    email_sender= # Mailbox email address. Put to the real email sender
    email_password= # Mailbox password. Put to the real email sender password
    email_smtp= # Mailbox SMTP (like smtp.gmail.com or mail.outlook.com). Put your smtp provider here

    # gunicorn/uvicorn setup
    gunicorn_setup=false # Should be True in production. Simpler to only with uvicorn for local dev
    debug=false # Put to true if you want to be in dash debug mode
    ```


3. Run `make setup` to install the pre-commits

4. Build the docker image
    ```bash
    make dev-build
    ```

5. Open your [local PGAdmin](http://localhost:5054) and login using the admin credentials.

    ⚠️ You may encounter login issues if using Firefox browser.

6. Connect to the database server using the admin credentials

7. Create a new database `<YOUR_DB_NAME>_db`, as per your .env file (`db`) in the example.

8. Add a user.json file under data, if you'd like to initialise a few users. It should contain:
    ```json
    [
        {
            "id": null,
            "user": "user_name",
            "password": "hashed_password",
            "permission": "permission_level",
            "client": "project_name",
            "application": "application_name"
        }
    ]
    ```


9. Run the docker container

    ```bash
    docker compose up -d
    ```

10. The app should be running under http://localhost: <YOUR_ENV_DASH_APP_PORT>:


10. To check for any issues, you can check the logs with:

    ```bash
    docker logs <YOUR_APP_CONTAINER_NAME> --tail=100 -f
    ```

    Use `Ctrl+C` to exit the logs
