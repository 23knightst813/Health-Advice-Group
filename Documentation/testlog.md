# Testing Log for Coder Dojo Web Application

## Test Case 1: Home Page

### Clock Functionality
- Event
    - Load Page
- Expected Result: Clock displayed successfully.
- Actual Result: Clock update very delayed
- Status: Fail
- Fix: Increase the Polling Rate
- Dependencies: None

### Digital Clock Funcitonality
- Event
    - Load Page
- Expected Result: Time Displayed Correctly in diigtal format
- Actual Result: 10:03 - Displayed as Ten Zero Three
- Status: Fail
- Fix: Edit Code to include O instead of Zero in the minitues collum
- Dependencies: None

### Nav Bar Funcitonality
- Event
    - Click Nav Bar
- Expected Result: Redirect to next page
- Actual Result: Redirect to next page
- Status: Pass
- Dependencies: None


## Test Case 2: User Registration

### Normal Data
- Input: 
    - Email: user@example.com
    - Password: P@ssw0rd1234
    - Password2: P@ssw0rd1234
    - CRD's: COPD
- Expected Result: User registered successfully.
- Actual Result: User registered successfully.
- Status: Pass
- Dependencies: User Database Table

### Erroneous Data
- Input: 
    - Email: user@example.com
    - Password: Password
    - Password2: Password
    - CRD's: COPD
- Expected Result: Error Message saying that the password isn't strong enough.
- Actual Result: No visible error message to the user, just logged in the console.
- Status: Fail
- Fix: Configure Flask Flash
- Dependencies: User Database Table

- Input: 
    - Email: user@example.com
    - Password: Password
    - Password2: Password2
    - CRD's: COPD
- Expected Result: Error Message saying that the passwords don't match.
- Actual Result: No visible error message to the user, just logged in the console.
- Status: Fail
- Fix: Configure Flask Flash
- Dependencies: User Database Table

### Boundary Data
- Input: 
    - Email: user@example.com
    - Password: P@ssw0rd123
    - Password2: P@ssw0rd123
    - CRD's: COPD
- Expected Result: User registered successfully.
- Actual Result: User registered successfully.
- Status: Pass
- Dependencies: User Database Table

### Presence Check
- Input: 
    - Email: 
    - Password: 
    - Password2: 
    - CRD's: 
- Expected Result: User registration stopped since fields are mandatory.
- Actual Result: User registration stopped.
- Status: Pass
- Dependencies: User Database Table

## Test Case 3: User Sign in

### Normal Data
- Input: 
    - Email: user@example.com
    - Password: P@ssw0rd1234
- Expected Result: User signed in successfully.
- Actual Result: User not found.
- Status: Fail
- Fix: Add missing sqlite3 syntax to add_user function
- Dependencies: User Database Table + Registration

### Erroneous Data
- Input: 
    - Email: user@example.com
    - Password: Password
- Expected Result: Password incorrect.
- Actual Result: Flask Flash telling the user that their password is incorrect.
- Status: Pass
- Dependencies: User Database Table + Registration

### Boundary Data
- Input: 
    - Email: user@example.com (valid email format)
    - Password: P@ssw0 (just below the minimum password length, e.g., 7 characters)
- Expected Result: Password is incorrect.
- Actual Result: Flask Flash message indicating the password is incorrect and too short.
- Status: Pass
- Dependencies: User Database Table + Registration

### Presence Check
- Input: 
    - Email: (empty)
    - Password: P@ssw0rd1234
- Expected Result: System prompts the user to enter an email address.
- Actual Result: Flask Flash message indicating the email field is required.
- Status: Pass
- Dependencies: User Database Table + Registration

- Input: 
    - Email: user@example.com
    - Password: (empty)
- Expected Result: System prompts the user to enter a password.
- Actual Result: Flask Flash message indicating the password field is required.
- Status: Pass
- Dependencies: User Database Table + Registration

## Test Case 4: Forecast
- Event:
    - Load Page
- Expected Result: Forecast and tips are displayed to the user
- Actual Result: Plage is blank
- Status: Fail
- Fix: Properly format the data before feeding into front end
- Dependencies: Weather API backend

- Event:
    - Load Page
- Expected Result: Styling and formating is correct
- Actual Result: Styling is layed out in rows not one collum
- Status: Fail
- Fix: Add Css to fix this issue
- Dependencies: Weather API backend

- Event:
    - Load Page
- Expected Result: Styling and formating is correct
- Actual Result:  Styling and formating is correct
- Status: Pass
- Dependencies: Weather API backend

## Test Case 5: Forecast - Tips
- Event:
    - Test the api
- Expected Result: Google API returns valid result
- Actual Result: Enter A Valid api key
- Status: Fail
- Fix: I was setting the api key to the string "api_key"

- Event:
    - Run Forcast function after refactor
- Expencted Result: Data is displayed to the website as normal
- Actual Result: TypeError: 'NoneType' object is not iterable
- Status: Fail
- Fix: Finsih Ai tips top return a formated response

- Event:
    - Run Forcast function after last fix
- Expencted Result: Data is displayed to the website as normal
- Actual Result: built-in method title of str object at 0x00000133A93D50F0
- Status: Fail
- Fix: Data Parsing

- Event:
    - Run Forcast function after last fix
- Expencted Result: Data is displayed to the website as normal
- Actual Result:  Data is displayed to the website as normal
- Status: Pass

## Test Case 7: Air Quality Dashbaord
- Event:
    - Load the page
- Expected Result: Page loads with live api data
- Actual Result: The data is not live and is hardcoded
- Status: Fail
- Fix: Add api calling and parse said data to the page

- Event:
    - Load the page
- Expected Result: Page loads with api data displayed
- Actual Result: JSON parsing failed: Expecting value: line 1 column 1 (char 0)
- Status: Fail
- Fix: Fix data parsing

- Event:
    - Load the page
- Expected Result: Page loads with api data displayed
- Actual Result: Page loads with api data displayed
- Status: Pass

## Test Case 8: Risk Assessment
- Event:
    - SUmbiting the form
- Expected Result: The form is saved to the database
- Actual Result: ImportError: cannot import name 'get_db_connection' from partially initialized module 'db' (most likely due to a circular import) (n:\Task 2\flaskr\app\db.py)
- Status Pass: No error
- Fix: Remove the get_db_connection function and replace the uses with  sqlite3.connect('Health.db')