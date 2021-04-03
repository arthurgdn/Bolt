from Bolt import App, Router

#Defining various controllers for different routes
async def home(req,res):
    res.set_header('Content-Type', 'text/html')
    await res.send('<html><body><b>This is a test of Bolt framework</b></body></html>') 

# url params are passed as controller's arguments
async def welcome(req,res, name, lastname):
    await res.send("Welcome {}".format(name+lastname))

async def post_test(req,res):
    name = req.body.get('name','')[0]
    await res.send('sent name successfully !')

# application = router + http server
router = Router()
# define the different routes
router.get(r'/',home)
router.get(r'/welcome/{name}/{lastname}',welcome)
router.post(r'/post_test',post_test)

# the app router is a collection of path and sub routers
appRouter = {
    '/' : router
}

app = App(appRouter, port=3000)
app.start_server()