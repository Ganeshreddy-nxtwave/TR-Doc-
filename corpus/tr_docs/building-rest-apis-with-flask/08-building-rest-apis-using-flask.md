# Building Rest APIs using Flask

**Course:** Building Rest APIs with Flask  
**Topic:** Building REST API's using Flask  
**Unit ID:** `983b92ff338f47ca9cba52189161f5fd` | **Unit Number:** 8

---

# Introduction

In the previous unit, we learned the fundamentals of Flask by building a simple web application. Now, we will take the next step and use Flask to build a **REST API**. We'll create several endpoints to manage a list of products, simulating a real-world e-commerce application like Zepto.


## What is an API?

An **API (Application Programming Interface)** is a software intermediary that allows two applications to talk to each other. While a user interacts with a website through its User Interface (buttons, forms), applications and servers interact with each other through APIs.

For our project, we will build a few APIs for a "Zepto Clone" to manage product data.

### APIs We Will Build:
- **Get Products**: Fetches a list of all available products.
- **Get a Single Product**: Fetches the details of one specific product using its ID.
- **Add a Product**: Adds a new product to our list.

### API Testing Tools
To test our API endpoints, we need a special tool. While there are many options like Insomnia and Swagger, we will use **Postman**, one of the most popular tools for API testing.

> **Action:** Before you begin, please create a free account on [Postman](https://www.postman.com/) and create a new, empty workspace.


## 1. Get All Products API

Our first endpoint will return a list of all products.

<details>
<summary><strong>Step 1: Setting up Sam
In this unit, we successfully built a basic REST API using Flask, covering essential operations like fetching all products, retrieving a single product by ID, and adding new products.ple Data</strong></summary>
<br>
First, let's create a new `app.py` file. In a real application, this data would come from a database, but for now, we'll use a simple Python list of dictionaries as our sample data.

```python
from flask import Flask

app = Flask(__name__)

# Sample product data
products = [
   {"id": 1, "name": "Chopping Board", "price": 360},
   {"id": 2, "name": "Sketch Pens", "price": 30},
   {"id": 3, "name": "Shoes", "price": 519}
]

if __name__ == '__main__':
    app.run(debug=True)
```
</details>

<details>
<summary><strong>Step 2: Creating the GET /products Route</strong></summary>
<br>
Now, let's create the Flask route that will return our list of products. Flask automatically converts Python lists returned from routes into JSON responses.

```python
from flask import Flask

app = Flask(__name__)

products = [
   {"id": 1, "name": "Chopping Board", "price": 360},
   {"id": 2, "name": "Sketch Pens", "price": 30},
   {"id": 3, "name": "Shoes", "price": 519}
]

## Route to get all products
@app.route('/products', methods=['GET'])
def get_products():
  return products

if __name__ == '__main__':
    app.run(debug=True)
```
</details>

<details>
<summary><strong>Step 3: Testing with Postman</strong></summary>
<br>
1.  Run your Flask application: `python app.py`.
2.  Open Postman and create a new request.
3.  Set the request method to **GET**.
4.  Enter the URL: `http://127.0.0.1:5000/products`.
5.  Click **Send**.

You should see the JSON array of products in the response body.
</details>


## 2. Get a Single Product API

Next, we'll create an endpoint to fetch a single product by its unique ID.

<details>
<summary><strong>Step 1: Understanding Path Parameters</strong></summary>
<br>
To identify a specific product, we need to pass its ID in the URL. We can achieve this using a **path parameter**. The URL will look like this: `/products/<product_id>`.

Flask will capture the value from the URL and pass it as an argument to our view function.

Examples:

- `/products/1` will fetch the product with `id = 1`.
- `/products/3` will fetch the product with `id = 3`.
</details>

<details>
<summary><strong>Step 2: Implementing the Route</strong></summary>
<br>
Let's add the new route to our `app.py`. The function will loop through the `products` list to find a match.

> **Note:** By default, URL parameters are strings. Since our product IDs are integers, we need to convert `product_id` to an `int` before comparing.

```python
# ... (previous code remains the same)

# Route to get a single product by ID
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
  product_id = int(product_id)
  for product in products:
    if product['id'] == product_id:
      return product
  # Return an error if the product is not found
  return {"error": "Product not found"}, 404

# ... (app.run remains the same)
```
</details>

<details>
<summary><strong>Step 3: Testing the Endpoint</strong></summary>
<br>
1.  Make sure your Flask server is running.
2.  In Postman, create a new **GET** request.
3.  Enter the URL for a specific product, for example: `http://127.0.0.1:5000/products/2`.
4.  Click **Send**.

</details>


## 3. Add a New Product API

Finally, let's create a **POST** endpoint to add a new product to our list.

<details>
<summary><strong>Step 1: Understanding the Request Body</strong></summary>
<br>
When creating a new resource, the client needs to send the data for that resource. This data is sent in the **request body**, typically in JSON format.

A sample JSON request body to add a new product would look like this:

```json
{
  "name": "Laptop Bag",
  "price": 800
}
```
</details>

<details>
<summary><strong>Step 2: Using the 'request' Object</strong></summary>
<br>
To access incoming request data in Flask, we need to import the `request` object. The `request.get_json()` method will parse the JSON body from the request and return it as a Python dictionary.

Update your imports to include `request`.

```python
from flask import Flask, request
```
</details>

<details>
<summary><strong>Step 3: Implementing the POST Route</strong></summary>
<br>
This route will listen for `POST` requests on the `/products` endpoint. It will read the new product data, assign it a new ID, and add it to our list.

```python
# ... (previous code remains the same)

# Route to add a new product
@app.route('/products', methods=['POST'])
def add_product():
   new_product = request.get_json()
   
   # Generate a new ID (in a real app, a database would handle this)
   new_product['id'] = len(products) + 1
   products.append(new_product)
   
   return {"message": "Product added!", "product": new_product}, 201

# ... (app.run remains the same)
```
</details>

<details>
<summary><strong>Step 4: Testing the POST Endpoint</strong></summary>
<br>
1.  Make sure your Flask server is running.
2.  In Postman, create a new request.
3.  Set the method to **POST** and the URL to `http://127.0.0.1:5000/products`.
4.  Go to the **Body** tab, select **raw**, and choose **JSON** from the dropdown.
5.  Paste the new product JSON into the text area:

    ```json
    {
      "name": "Laptop Bag",
      "price": 800
    }
    ```
6.  Click **Send**.

You should receive a "Product added!" message. You can verify this by making another `GET` request to `/products` to see the newly added item in the list.
</details>


## Conclusion

In this unit, we successfully built a basic REST API using Flask, covering essential operations like fetching all products, retrieving a single product by ID, and adding new products.