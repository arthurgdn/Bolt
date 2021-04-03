from Bolt import App, Router

#Defining various controllers for different routes
async def home(req,res):
    res.set_header('Content-Type', 'text/html')
    await res.send('<html><body><b>This is a test of Bolt framework</b></body></html>') 

# url params are passed as controller's arguments
async def welcome(req,res):
    name = req.query['name']
    lastname = req.query['lastname']
    await res.send("Welcome {}".format(name+lastname))

async def post_test(req,res):
    if 'name' in req.body:
        name = req.body['name']
        await res.send('sent name successfully ! name : ' + name)
    else:
        res.set_status(400)
        await res.send('Error: missing value in body: name')

# application = router + http server
router = Router()
# define the different routes
router.get(r'/',home)
router.get(r'/welcome',welcome)
router.post(r'/post_test',post_test)

# the app router is a collection of path and sub routers
appRouter = {
    '/' : router
}

app = App(appRouter, port=3000)
app.start_server()