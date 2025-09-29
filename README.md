
# sendEmailPy

Welcome to the `sendEmailPy` project! This repository contains the source code for our Python application.

Follow the instructions below to set up your local development environment and run the application.

## 🚀 Getting Started

First, **clone the repository** to your local machine:

```bash
git clone git@github.com:kharazian/sendEmailPy.git
cd sendEmailPy
````

-----

## 🛠️ Local Setup

We recommend using a Python virtual environment to manage dependencies.

1.  **Create and Activate Virtual Environment**
    Create the environment (named `.venv`):

    ```bash
    python3 -m venv .venv
    ```

    Activate the virtual environment:

    ```bash
    source .venv/bin/activate
    ```

2.  **Install Dependencies**
    Install all required packages using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

-----

## ⚙️ Configuration

The application requires specific configuration variables, which are loaded from a **`.env`** file.

1.  **Create `.env` File**
    Copy the example file to create your working environment file:

    ```bash
    cp .env.example .env
    ```
2.  **Generate a Secure Secret Key**
    Generate a random 32-byte hexadecimal string to use for the SECRET_KEY:

    ```Bash
    openssl rand -hex 32
    Copy the output of this command.
    ```

2.  **Populate `.env` Data**
    Edit the newly created **`.env`** file and fill in the values based on the required settings below:

    ```ini
    # --- Email Configuration ---
    MAIL_USERNAME=your_email@example.com
    MAIL_PASSWORD=your_email_password
    MAIL_FROM=your_email@example.com
    MAIL_SERVER=smtp.example.com
    MAIL_PORT=587
    MAIL_TLS=True
    MAIL_SSL=False

    # --- User Credentials (for initial setup/admin) ---
    USER_USERNAME=username
    USER_PASSWORD_HASH=hash_of_password

    # --- JWT Settings ---
    SECRET_KEY=your-super-secret-key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

-----

## 🏃 Running the Application

### Production (Recommended)

Run the application using **Uvicorn**:

```bash
    .venv/bin/gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Debugging/Local Development

Run your application's entry script directly:

```bash
uvicorn app.main:app --reload

Or

python myapp.py
```
