import argparse
indent = "    "
def new(project_name):
    app = open(''+project_name+".py", "x")
    app.write('from Bolt import App, Router \n \n')
    app.write('async def home(req,res): \n')
    app.write(indent+ "res.set_header('Content-Type', 'text/html') \n")
    app.write(indent+ "await res.send('<html><body><b>Create Bolt App generated page</b></body></html>') \n \n")
    app.write('router = Router() \n')
    app.write("router.get(r'/', home)\n")
    app.write("app = App({ '/': router})\n")
    app.write("app.start_server()")
    app.close()

parser = argparse.ArgumentParser(description='CLI to generate Bolt apps')
parser.add_argument('init', type=str, action='store',
                    help='create new Bolt app')
parser.add_argument('app_name', type=str, action='store',
                    help='name of your app')
args = parser.parse_args()
new(args.app_name)

