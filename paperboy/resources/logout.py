import falcon
import jinja2
from .base import BaseResource
from .html import read


class LogoutResource(BaseResource):
    auth_required = False

    def __init__(self, *args, **kwargs):
        super(LogoutResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        resp.content_type = 'text/html'
        file = read('logout.html')
        tpl = jinja2.Template(file).render(baseurl=self.config.baseurl,
                                           apiurl=self.config.apiurl,
                                           loginurl=self.config.loginurl,
                                           logouturl=self.config.logouturl)
        resp.body = tpl

    def on_post(self, req, resp):
        ret = self.db.users.logout(req, resp, self.session)
        req.context['user'] = None
        req.context['auth_token'] = None
        if ret:
            resp.unset_cookie('auth_token')
            resp.status = falcon.HTTP_302
            resp.set_header('Location', self.config.baseurl)
