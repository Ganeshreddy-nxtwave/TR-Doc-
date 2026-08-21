# Introduction to Third-Party Packages

**Course:** Building Rest APIs with Flask  
**Topic:** Getting Started with Third-Party Packages  
**Unit ID:** `950f57b003b44cafadd4bc7cbe690499` | **Unit Number:** 4

---

# Introduction to Third-Party Packages in Python


## 1. Introduction to Third-Party Packages


- **Third-party packages** are software libraries developed by **external developers**.  
- They help **save time and effort** while building applications.
- These packages provide **additional functionality** that can be easily integrated into your own software projects.

## 2.Python Packages 


- **Third-party packages** are like **downloading new apps** that add **extra functionality** to Python.


### 2.1 Packages and Modules

- **Module**  
  - A **Python file** containing code with functions, classes, etc.
- **Package**  
  - A **collection of modules**.  
  - You can think of a package like a **folder** that contains multiple files (modules).

## 3. Third-Party Packages in Python – Examples

Python provides multiple packages to make development **faster**:

- requests
- pygame
- matplotlib
- pytorch
- tensorflow

These packages help in different areas such as **web requests**, **game development**, **data visualization**, and **machine learning**.


## 4. Introduction to API Calls in Python

### 4.1 Requests Package

- The **Python `requests` package** is used for **making HTTP requests** to a specified URL.
- It allows your Python program to **communicate with web servers** and work with **APIs**.


### 4.2 Installing `requests`

To install the `requests` package, run the following command in the **terminal/command prompt**:

```bash
!pip install requests
```


### 4.3 PIP and PyPI

* **PIP**

  * Python packages are typically installed via the Python package manager **`pip`**.
  * `pip` pulls libraries from repositories like **PyPI**.

* **PyPI (Python Package Index)**

  * PyPI is like a **big library or catalog** that holds thousands of Python packages.
  * Whenever you want to add new functionality to your Python programs, you can usually find a suitable package on **PyPI**.


## 5. Building a Simple Weather Application

### 5.1 Real-Time Weather Updates

We will build a simple **weather application** that displays the **current weather** of a given location.


### 5.2 Weather API URL

To get the weather information of **Mumbai**, we will use a **weather API URL**:

```python
url = "https://api.weatherapi.com/v1/current.json?key=e942dbeb75424295b4e94030242510&q={location}"
```

We will make an **API call** to this URL using the **`requests`** package.


### 5.3. Making a GET Request Using `requests`
* `requests.get()` is used to send a **GET request** to a specified URL for **retrieving data** from a server.

Basic syntax:

```python
requests.get(url, params, **kwargs)
```

* `url`: The URL of the resource.
* `params`: optional
* `kwargs`: optional


### 5.4 Making a GET Request

```python
import requests

# Getting weather data of Mumbai
url = "https://api.weatherapi.com/v1/current.json?key=e942dbeb75424295b4e94030242510&q=Mumbai"

response = requests.get(url)
```

Here:

* We import the `requests` package.
* Set the `url` for the weather API.
* Use `requests.get(url)` to send a GET request.


### 5.5. Understanding the Response Object

#### 5.5.1 Response Object

* `requests.get()` returns a **response object**.
* This object contains all the **data returned from the server** in response to the HTTP request.

#### 5.5.2 Response Object Data


* `.json()`

  * Parses the response payload as **JSON** and returns a **dictionary**.
* `.status_code`

  * Represents the **HTTP status code**.
* `.text`

  * Returns the **content** of the response as **Unicode text**.
* `.reason`

  * Textual reason for the HTTP status, e.g., `"Not Found"` or `"OK"`.
* `.headers`

  * A dictionary-like object containing the **response headers**.
* `.url`

  * The **URL** of the response.


### 5.6 Accessing JSON Data from the Response

#### 5.6.1 Using `.json()`

```python
import requests

# Getting weather data of Mumbai
url = "https://api.weatherapi.com/v1/current.json?key=e942dbeb75424295b4e94030242510&q=Mumbai"

response = requests.get(url)
data = response.json()

print(data)
```

* `response.json()` converts the response into a **Python dictionary**.
* `data` now holds all the weather information returned by the API.


### 5.7. Printing the Current Temperature

We can access specific fields from the JSON data, such as the **current temperature**:

```python
import requests

# Getting weather data of Mumbai
url = "https://api.weatherapi.com/v1/current.json?key=e942dbeb75424295b4e94030242510&q=Mumbai"

response = requests.get(url)
data = response.json()

print(f"Temperature: {data['current']['temp_c']}°C")
```

**Output:**

```text
Temperature: 29.1°C
```

## 6. Other Third-Party Packages in Python

In addition to `requests`, Python has many other useful third-party packages, such as:

### 6.1 pygame
* `pygame` – used to **design and build games** using Python

    * To install `pygame`:
    
      ```bash
      !pip install pygame
      ```

### 6.2 matplotlib

* `matplotlib` – an **open-source plotting package** for data visualization
   
    * To install `matplotlib`:

    ```bash
    !pip install matplotlib
    ```

## 7. Other useful python packages

* pytorch
* tensorflow
* Tkinter
* NumPy
* Pandas
* Pillow
* Scikit-learn
* Beautiful Soup