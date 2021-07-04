import os
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
from werkzeug.serving import run_simple

from data_adapter import DataStorage


class Posts:

    def __init__(self, config):
        self.storage = DataStorage(config['redis_host'], config['redis_port'])
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),
                                    autoescape=True)
        self.url_map = Map([
            Rule('/', endpoint='posts'),
            Rule('/create/', endpoint='create_post'),
            Rule('/<id>', endpoint='detail_view')
        ])

    def render_template(self, template_name, context):
        template = self.jinja_env.get_template(template_name)
        htmlout = template.render(data = context)
        return Response(htmlout, mimetype='text/html')

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, f'on_{endpoint}')(request, **values)
        except HTTPException as e:
            return e
    
    def on_create_post(self, request):
        if request.method == 'POST':
            if self.storage.is_valid(request):
                self.storage.save_post(request)
                return redirect("/")
        return self.render_template('create_post.html', None)


    def on_posts(self, request):
        posts = self.storage.get_posts()
        data = {"d": None}
        data['d'] = posts
        return self.render_template('posts.html', data)
    
    def on_detail_view(self, request, id):
        data = {"comments": None}
        data = {"post": None}
        data['post'] = self.storage.get_post(id)
        if request.method == 'POST':
            if self.storage.is_valid_comment(request):
                self.storage.save_comment(request, id)
        comments = self.storage.get_comments(id)
        data['comments'] = comments
        return self.render_template('detail_view.html', data)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    app = Posts({
        'redis_host': redis_host,
        'redis_port': redis_port
    })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app


if __name__ == '__main__':
    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=False, use_reloader=True)
