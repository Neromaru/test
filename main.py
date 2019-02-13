from aiohttp import web
import os
import jinja2
import aiohttp_jinja2


base_path = os.path.dirname(os.path.abspath(__file__))
routes = web.RouteTableDef()
app = web.Application()

aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader(base_path + '/templates'),
                     )


def render_templ(request, root=True):
    context = dict(root=root)
    if root:
        context['folder'] = os.listdir(base_path)
        os.chdir(base_path)
    else:
        context['folder'] = os.listdir('.')
    response = aiohttp_jinja2.render_template('base.jinja2',
                                              request,
                                              context)
    return response


@routes.get('/')
async def index(request):
    return render_templ(request)


@routes.get('/up')
async def move_up(request):
    os.chdir('..')
    cur_dir = os.getcwd()
    if cur_dir == base_path or base_path.startswith(cur_dir):
        return web.HTTPFound('/')
    return render_templ(request, False)


@routes.get('/{path}')
async def handle(request):
    cur_dir = os.getcwd()
    path = request.match_info.get('path', base_path)
    selected = cur_dir+f'\\{path}'
    if os.path.isdir(selected):
        os.chdir(selected)
        return render_templ(request, False)

    else:
        return web.FileResponse(selected)

app.router.add_routes(routes)

web.run_app(app)
