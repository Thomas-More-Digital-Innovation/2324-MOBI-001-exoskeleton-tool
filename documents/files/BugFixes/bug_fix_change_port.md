# Bug Fix: Changing the Port for a Flask Application

## Issue Description
Sometimes, when running a Flask application, you may encounter the need to change the default port on which the application runs. This document outlines the steps to change the port for your Flask application. I encountered this issue on my laptop, it was outlined by the following error message:
```
* Serving Flask app 'app'
* Debug mode: on
An attempt was made to access a socket in a way forbidden by its access permissions
```

## Prerequisites
* Python and Flask are installed on your system.
* You have a Flask application script (e.g., app.py) that you want to modify.

## Steps to Change the Port
### 1. Open Your Flask Application Script:
Open the Python script that contains your Flask application code in a text editor. This script is typically named app.py.
### 2. Locate the app.run() Function:
In your Python script, find the line that includes the app.run() function. It usually looks like this:
```py
if __name__ == '__main__':
    app.run(debug=True)
```

### 3. Modify the app.run() Function:
Modify the app.run() function to include the port parameter with your desired port number. For example, to change the port to 8080, modify it as follows:
```py
if __name__ == '__main__':
    app.run(debug=True, port=8080)
```

### 4. Save Your Changes:
Save the changes you made to your Python script.

### 5. Activate Your Virtual Environment (if applicable):
If you are using a virtual environment, activate it in your terminal by running one of the following commands:
* for windows:
```
.\venv\Scripts\activate
```
* for macOS/Linux
```
source venv/bin/activate
```

### 6. Run Your Flask Application:
In your terminal, navigate to the directory where your Flask application is located and run the application again:
```
python app.py
```
Your Flask application will now run on the specified port (in this example, port 8080). Make sure to update any URLs or references in your application code or configurations to reflect the new port if necessary.

## Conclusion
By following these steps, you can change the port on which your Flask application runs, allowing you to adapt it to your specific requirements.
