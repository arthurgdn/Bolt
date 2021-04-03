import re
from ..router import Router


def generate_router(routers):
    router = Router()
    for sub_routers_path in routers.keys():
        sub_routers_routes = routers[sub_routers_path].routes
        reg_exp_paths = sub_routers_routes.keys()
        for reg_exp_path in reg_exp_paths:
            if sub_routers_path.startswith('/'):
                if sub_routers_path != '/':
                    if reg_exp_path.pattern == '^/$':
                        router.routes[re.compile('^'+sub_routers_path+reg_exp_path.pattern[2:])] = sub_routers_routes[reg_exp_path]
                    else:
                        router.routes[re.compile('^'+sub_routers_path+reg_exp_path.pattern[1:])] = sub_routers_routes[reg_exp_path]
                else:
                    router.routes[re.compile(reg_exp_path.pattern)] = sub_routers_routes[reg_exp_path]
    return router