
# EcoDev App

This app can serve as a template. It includes some basic functionalities such as user login,
customisable components such as navbar menus, and customised component builders such as

### Usage

Go to <APP_URL> to view the app.

Got to <API_URL>/docs to view the API documentation (with Swagger)

If encountering a `404 page not found`, [contact the CDA team](https://teams.microsoft.com/l/channel/19%3a82ee44fd11e248febedc478307bf9239%40thread.tacv2/CDA%2520Hotline?groupId=0c6b8357-7a2e-49d9-9c10-143c7cb9b5d4&tenantId=33440fc6-b7c7-412c-bb73-0e70b0198d5a)

### Help, Bugs & Feedback

Product Owners: Thomas Epelbaum, Amaury Salles & Yoann Diep

If encountering any bugs, feel free to browse the issue list & contribute!

Use the docs/issues_template whenever possible. It will greatly help the developper team understand the full extent of your bug or feature request.


### Local development

1. Clone the repo and build the docker image:

    ```git
    git clone git@github.com:FR-PAR-ECOACT/ecodev-front.git
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
