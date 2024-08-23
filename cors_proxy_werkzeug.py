from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple

def application(environ, start_response):
    request = Request(environ)

    target_url = 'http://localhost:4000'

    response = request.get(target_url)

    headers = [('Access-Control-Allow-Origin', '*')]  # Allow requests from any origin
    start_response(response.status_code, headers)
    return [response.content]

rules = [
    Rule('/', endpoint='proxy'),
]

app = Map(rules)

if __name__ == '__main__':
    run_simple('localhost', 6000, application)