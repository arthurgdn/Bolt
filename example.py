from Bolt import App, Router

# get route with html response
async def home(req,res):
    res.set_header('Content-Type', 'text/html')
    await res.send('<html><body><b>This is a test of Bolt framework</b></body></html>') 
    


# get route + params
async def welcome(req,res, name, lastname):
    await res.send("Welcome {}".format(name+lastname))

# post route with body
async def post_test(req,res):
    name = req.body.get('name','')[0]
    await res.send('sent name successfully !')

## application = router + http server
router = Router()
# defines the routes
router.get(r'/',home)
router.get(r'/welcome/{name}/{lastname}',welcome)
router.post(r'/post_test',post_test)

app = App(router)
app.start_server()