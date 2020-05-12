import json
from jinja2 import Environment
from flask import Flask, render_template, request, Response

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/rend')
def rend():
    try:
        raw = '''template {{ test }}
        {% debug %}'''
        jinja_env = Environment(extensions=['jinja2.ext.debug'])
        template = jinja_env.from_string(raw)
        output = template.render()
        return output
    except Exception as e:
        return Response(response=f'Exception: {e}', status=500)


if __name__ == '__main__':
    app.run(debug=True)