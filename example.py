from Bolt import App, Router
from Bolt.response import Response


async def home(request,rsp):
    rsp.set_header('Content-Type', 'text/html')
    rsp.send('<html><body><b>test</b></body></html>') 
    


# get route + params
async def welcome(r,res, name, lastname):
   res.send("Welcome {}".format(name+lastname))



async def test(req,res):
    i=4
    
# post route + body param
async def parse_form(r):
    if r.method == 'GET':
        return 'form'
    else:
        print(r.body)
        name = r.body.get('name', '')[0]
        password = r.body.get('password', '')[0]

        return "{0}:{1}".format(name, password)

## application = router + http server
router = Router()
router.add_routes({
    r'/welcome/{name}/{lastname}': welcome,
    r'/': home,
    r'/login': parse_form,
    r'/test':test,
    })

app = App(router)
app.start_server()