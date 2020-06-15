# Bolt
Bolt is a python asynchronous web framework designed to facilite the implementation of a backend service. This project was started with the aim of learning about asynchronous coding in Python. 

## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)
* [Example](#example)

## Technologies
Bolt is created with:
* Python : 3.8.2
* asyncio : 3.4.3
* dnspython : 1.16.0
* enum-compat : 0.0.3
* eventlet : 0.24
* greenlet : 0.4.15
* monotonic : 1.5
* six : 1.15.0
	
## Setup
This project cannot be installed using a package manager yet, to install it, download the Bolt folder and add it to your python scripts folder and import the module in your projects !
```python
from Bolt import App, Router
```

## Example

In this quick example you will see how to create your first route with Bolt.

You first have to define a controller to use when the route will be called, the controller is called with request and response objects, and here the response is sent as html : 
```python
async def home(req,res):
    res.set_header('Content-Type', 'text/html')
    await res.send('<html><body><b>This is a test of Bolt framework</b></body></html>') 
```
To add a route you first have to create a new router, define the path and the controller for the new route and finally create your web app and start the server to get going !
```python
router = Router()
router.get(r'/',home)
app = App(router)
app.start_server()
```
For more examples you can check out [example.py][https://github.com/arthurgdn/Bolt/blob/master/example.py]  