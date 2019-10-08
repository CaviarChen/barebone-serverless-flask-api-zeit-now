# app.py
from flask import Flask
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix
from database import db_session
from models import BlogPost
import urllib.request

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app,
          version='0.1',
          title='Our sample API',
          description='This is our sample API'
)

@api.route('/hello_world')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/test_http')
class HelloWorld(Resource):
    def get(self):
          fp = urllib.request.urlopen("http://www.python.org")
          html = fp.read().decode("utf8")
          fp.close()
          return {'html': html}

@api.route('/blog_posts')
class BlogPosts(Resource):
    model = api.model('BlogPost', {
        'id': fields.Integer,
        'title': fields.String,
        'post': fields.String,
    })
    @api.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return BlogPost.query.all()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)
