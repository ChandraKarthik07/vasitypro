# Project Name

Description of your project.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [User Registration](#user-registration)
  - [User Login](#user-login)
  - [Timesheet API](#timesheet-api)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_PROJECT_NAME.git
    ```

2. Navigate to the project directory:

    ```bash
    cd YOUR_PROJECT_NAME
    ```

3. Create a virtual environment:

    ```bash
    python -m venv YOUR_VIRTUAL_ENV
    ```

4. Activate the virtual environment:

    ```bash
    source YOUR_VIRTUAL_ENV/bin/activate  # On Windows: YOUR_VIRTUAL_ENV\Scripts\activate
    ```

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Apply migrations:

    ```bash
    python manage.py migrate
    ```

7. Run the development server:

    ```bash
    python manage.py runserver
    ```

Your project should now be running locally. Visit `http://localhost:8000` in your browser.

## Usage

### User Registration

1. Open your browser and navigate to `http://localhost:8000/api/signup/`.
2. Complete the registration form by providing a username, email, and password.
3. Click the "post" button.
4. You should receive a success message upon successful signup along with acess token.

#### 

### User Login

1. Open your browser and navigate to `http://localhost:8000/api/token/`.
2. Provide your username and password.
3. Click the "post" button.
4. You should be redirected to the home page upon successful login and aceess,refresh token as well .
5. -- use my existing creds in login user is kiran and password is 123
6. copy the acess token 
## API Endpoints

### Timesheet API

#### Creating a new timesheet entry

- **Endpoint:** `POST /api/timesheets/`
- **Data Format:**
  ```json
  {
    "user": 1,
    "projects": [1, 2],
    "hours_worked": 8.5,
    "week_start_date": "2023-12-01"
  }
#### Authorization: Bearer Token (Obtain after login)
#### Response: Returns the created timesheet entry.
#### Updating an existing timesheet entry
#### Endpoint: PUT /api/timesheets/{timesheet_id}/
Data Format:
json
Copy code
{
  "projects": [3, 4],
  "hours_worked": 10.0,
  "week_start_date": "2023-12-15"
}

### and most important there also other apis to login through google as well (oauth2) but you need to replace the creds of your own.
the apis are http://127.0.0.1:8000/api/auth/.... just need to code well..
