# Introduction to Flask

**Course:** Building Rest APIs with Flask  
**Topic:** Building REST API's using Flask  
**Unit ID:** `365db4929eaf4d0bbe292eaaf6732b04` | **Unit Number:** 6

---

# Introduction

In previous units, we explored third party packages in Python. Now, we'll learn how to create the web applications that can power them. In this unit, we will learn about Flask, a popular Python framework used for building web applications and APIs. We will start from the basics and build our very first web application.

## Setting up Code Environment

To follow along with this material and develop Flask applications, you'll need to set up your development environment. This primarily involves installing Python and a suitable code editor like VS Code.

## 1. Install Python

Python is the programming language that Flask is built upon.

*   **Download Python:**
    *   Visit the official Python website: <a href="https://www.python.org/downloads/" target="_blank">https://www.python.org/downloads/</a>

    *   Download the latest stable version of Python for your operating system (Windows, macOS, Linux).
*   **Install Python:**
    *   **Windows:** Run the installer. Make sure to check the "Add Python X.X to PATH" option during installation. This is crucial for running Python commands from your terminal.
    *   **macOS:** Python might be pre-installed, but it's recommended to install the latest version from the official website or using a package manager like Homebrew (`brew install python`).
    *   **Linux:** Python is usually pre-installed. You can update it using your distribution's package manager (e.g., `sudo apt-get install python3` for Debian/Ubuntu).
*   **Verify Installation:** Open a new terminal or command prompt and type:

    ```bash
    python --version
    ```
    or
    
    ```bash
    python3 --version
    ```
    You should see the installed Python version.

## 2. Install Visual Studio Code (VS Code)

VS Code is a popular, lightweight, and powerful code editor that provides excellent support for Python development.

*   **Download VS Code:**
    *   Visit the official VS Code website: <a href="https://code.visualstudio.com/" target="_blank">https://code.visualstudio.com/</a>
    *   Download the installer for your operating system.
*   **Install VS Code:**
    *   Run the installer and follow the instructions. It's generally recommended to keep the default settings.
*   **Install Python Extension for VS Code:**
    *   Open VS Code.
    *   Go to the Extensions view by clicking on the square icon on the sidebar or pressing `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (macOS).
    *   Search for "Python" and install the extension provided by Microsoft. This extension provides features like IntelliSense, linting, debugging, and more.

With Python and VS Code set up, you're ready to start building your Flask applications!

## Python: A Versatile Language
Python is a programming language known for its simplicity, readability, and versatility. It is used in almost every field and is a widely used programming language that can be used for both frontend and backend development. The capacity of the computer of performing more than one task at the same time is called the versatility.

### Python can be used in:
- **AI / Machine Learning**
- **Big Data**
- **Smart Device / IOT**
- **Game Developement**
- **Backend Developement**

## Python in Web Applications

Python is a versatile programming language known for its simplicity and readability. It's used in nearly every field, including web development, where it can be used for both frontend and backend tasks.

### Python Frameworks

A Python framework is a collection of tools and libraries that provide a common structure to build applications more quickly and efficiently. They offer reusable code and a defined architecture so you don't have to start from scratch.

### Popular Python frameworks include:

- **Flask**
- **Django**
- **FastAPI**
- **CherryPy**


## Flask

Flask is mainly used for building Web Applications and RESTful APIs.

- **Popularity:** Flask is one of the most popular and widely used web frameworks by developers, according to developer surveys.
- **Companies Using Flask:** Major companies like **Netflix, CRED, Reddit, and Lyft** use Flask to power their applications.

### Installing Flask

Just like any other Python package, Flask can be installed using `pip`.

Open your terminal and run the following command:

```bash
    pip install flask
```

## Building Your First Flask Application

Let's build a simple web application that responds with "Hello World!" when a user visits it.

### The Flow
1.  A **Client** (like a web browser) sends an HTTP Request to a URL.
2.  Our **Flask Server** receives the request.
3.  The server processes the request and sends back an HTTP Response containing the text "Hello World!".

<details>
<summary><strong>Step 1: Create a Python File</strong></summary>
<br>
Create a new Python file and name it `hello_world.py`.
</details>

<details>
<summary><strong>Step 2: Write the Flask Code</strong></summary>
<br>
Add the following code to your `hello_world.py` file. Each part is explained below.

```python
# 1. Import the Flask class
from flask import Flask

# 2. Create an instance of the Flask class
app = Flask(__name__)

# 3. Define a route and the function to handle it
@app.route('/', methods=['GET'])
def home():
   return "Hello World!"

# 4. Run the application server
if __name__ == '__main__':
    app.run(debug=True)
```

**Code Explained:**

1.  **`from flask import Flask`**: This line imports the main `Flask` class from the `flask` package.
2.  **`app = Flask(__name__)`**: This creates an instance of the Flask application. `__name__` is a special Python variable that gives Flask information about where the application is located. The `app` variable represents our web application.
3.  **`@app.route('/', methods=['GET'])`**: This is a decorator that tells Flask which URL should trigger our function.
    -   The first argument (`'/'`) is the **path** of the URL (the root of our website).
    -   The `methods` argument specifies which HTTP methods this route responds to. If not specified, it defaults to `GET`.
4.  **`def home(): ...`**: This is the function that will be executed when a user visits the `/` route. It returns the string "Hello World!", which will be sent back to the browser.
5.  **`app.run(debug=True)`**: This line starts the Flask development server.
    -   `debug=True` is a helpful parameter that automatically reloads the server when you make code changes and provides detailed error pages if something goes wrong.

</details>

<details>
<summary><strong>Step 3: Run the Flask Server</strong></summary>
<br>
To start your application, open a terminal in the same directory as your `hello_world.py` file and run the following command:

```bash
python hello_world.py
```

You will see output indicating that the Flask server is running and listening for connections, typically on `http://127.0.0.1:5000/`.

</details>

<details>
<summary><strong>Step 4: Access Your Application</strong></summary>
<br>
Open your web browser and navigate to `http://127.0.0.1:5000/`. You should see the "Hello World!" message displayed on the page.

</details>


## Flask Routing

Routing is the process of mapping URLs to specific functions. You can define multiple routes in your application.

Let's add another route that responds with a name.

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
   return "Hello World!"

# New route for the path '/name'
@app.route('/name')
def get_name():
   return "Rahul"

if __name__ == '__main__':
    app.run(debug=True)
```

Now, if you run the server and visit `http://127.0.0.1:5000/name`, the browser will display "Rahul".