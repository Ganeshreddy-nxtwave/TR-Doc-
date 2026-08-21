# Integrating Flask APIs in Frontend

**Course:** Building Rest APIs with Flask  
**Topic:** Building REST API's using Flask  
**Unit ID:** `3541116a652d409e93cc74ef0d0c43f2` | **Unit Number:** 10

---

# Introduction

In the previous session, we created a **Flask API backend** for a Zepto-like app. We built API endpoints such as **`/products`** and **`/product/<id>`** to fetch product data, and tested the responses using **Postman**.

In this session, we are going to build **NxtExpress**, an e-commerce web page that showcases products with **images, prices, and descriptions**. The project is already partially built with HTML, CSS, and JavaScript, but the **frontend is not yet connected** to the backend API.

---

## NxtExpress - An E-commerce Webpage

The main goal of this session is to **integrate our existing NxtExpress UI with the Flask API** so that product data is fetched **dynamically** and displayed beautifully as **interactive product cards**.

---

### Prerequisite

- **VS Code**  
- **Python**  
- **Flask**

---


### Session Initial Code

The session’s initial code contains both the **frontend** and **backend** inside the same project folder:  

- **Backend — Flask API:** Handles API routes  
- **Frontend — UI:** Built with HTML, CSS, and JavaScript to display product cards  
- **Resource.md:** Contains the required JSON data  

Download session initial code : <a href="https://nkb-backend-ccbp-media-static.s3-ap-south-1.amazonaws.com/ccbp_beta/media/content_loading/uploads/dcb093a3-b8ea-420a-ada5-d6d0d1e4f010_Nxt_Express.zip" target="_blank" >NxtExpress Initial Code</a>

When we run this code in the browser, we won’t see any product cards because the frontend is **not yet connected** to the backend.  

What we are going to build next is the **integration of the frontend with the Flask API** so that the UI displays real product data as **product cards**.

---

### Steps to Integrate Flask APIs with Frontend
<details> 
<summary>**Update Products Data in Flask**</summary>

- We will add more products with **description** and **image** fields.  
- This JSON data is provided in **Resource.md**.

```json
[
  {
    "id": 1,
    "name": "Chopping Board",
    "price": 360,
    "description": "A durable wooden chopping board for daily kitchen use.",
    "image": "https://bit.ly/3XCmlH5"
  },
  {
    "id": 2,
    "name": "Sketch Pens",
    "price": 30,
    "description": "12 bright colors perfect for school and art projects.",
    "image": "https://bit.ly/3X8Tb2d"
  },
  {
    "id": 3,
    "name": "Shoes",
    "price": 519,
    "description": "Comfortable running shoes with breathable mesh.",
    "image": "https://bit.ly/4r5FnTX"
  },
  {
    "id": 4,
    "name": "Water Bottle",
    "price": 199,
    "description": "1-litre stainless steel insulated bottle.",
    "image": "https://bit.ly/48oQWy3"
  },
  {
    "id": 5,
    "name": "Notebook",
    "price": 85,
    "description": "200-page ruled notebook for study & office use.",
    "image": "https://images.unsplash.com/photo-1519682337058-a94d519337bc"
  },
  {
    "id": 6,
    "name": "Earphones",
    "price": 299,
    "description": "High-quality wired earphones with mic.",
    "image": "https://bit.ly/4i705i2"
  },
  {
    "id": 7,
    "name": "Backpack",
    "price": 899,
    "description": "Lightweight waterproof backpack with 3 compartments.",
    "image": "https://bit.ly/4ocvZuZ"
  },
  {
    "id": 8,
    "name": "LED Bulb",
    "price": 120,
    "description": "9W energy-efficient LED bulb.",
    "image": "https://bit.ly/49oKyI9"
  },
  {
    "id": 9,
    "name": "Coffee Mug",
    "price": 250,
    "description": "Ceramic mug with heat insulation and stylish print.",
    "image": "https://bit.ly/48uDdov"
  },
  {
    "id": 10,
    "name": "Keyboard",
    "price": 750,
    "description": "USB keyboard with smooth keys and long durability.",
    "image": "https://bit.ly/3X6DtEU"
  }
]

```
</details> <details> 
<summary>**Run Flask API in VS Code and Copy the Endpoint URL**</summary>

- Open **backend folder**  
- Inside it, create **app.py**  

**Add Flask Code**

- Add below Flask code in app.py
- Update products data with the new JSON data provided.

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Add new JSON data
products = [
    {...},{...},...
]

@app.route('/products')
def get_products():
    return products

app.run(debug=True)

```

### ** Frontend and Backend Cannot Talk to Each Other**

- Our frontend and backend **run on different ports/domains**, so the **browser blocks the API request** , and the products do not load on the page.
- Result: **API call fails**, products do not load, and the console shows **CORS errors**.

---

### **Turn On CORS**

To allow the frontend and backend to communicate, we need to **enable CORS** in the backend.

---

### **What is CORS?**

**CORS (Cross-Origin Resource Sharing)** allows the backend to **give permission** to the frontend so it can access data.

<details><summary>**Steps to Enable CORS**</summary>

- **Install Required Package**




```bash
pip install flask-cors
```

- **Apply CORS in Flask**

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows all origins by default


...
```
</details>
### ** Run the Flask App**

```bash
python3 app.py
```



### **Access API**

- Flask server runs at : **http ://127.0.0.1:5000/**

- Get API endpoint: **http ://127.0.0.1:5000/products**

- Test in browser → **JSON data of products will be returned**

</details> <details> <summary>**Connect Frontend to Flask Using Fetch API**</summary>
- We will add our public API endpoint as a parameter and send a **GET request** to the backend using the **JavaScript Fetch API**.

```JavaScript
async function fetchProducts() {
    try {
        const response = await fetch('http://127.0.0.1:5000/products');
        if (!response.ok) throw new Error('Failed to fetch');
        const products = await response.json();
        renderProducts(products);
    } catch (error) {
        console.warn('Failed to fetch products:', error);
        renderProducts([]);
    }
}
```

</details>
The existing HTML, CSS, and JavaScript will be used to dynamically create product cards that will be displayed in the UI.