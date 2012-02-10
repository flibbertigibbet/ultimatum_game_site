# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from repoze.what import predicates

from testexp.lib.base import BaseController
from testexp.model import DBSession, metadata
from testexp import model
from testexp.controllers.secure import SecureController

from testexp.controllers.error import ErrorController

from testexp.controllers.play import PlayController

##########
from testexp.model import *
##########

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the testExp application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::em

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    
    play = PlayController()

    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()
    
    #####################
    @expose('testexp.templates.test')
    def test(self):
        exp_grps = DBSession.query(ExpGroup)
        return dict(
            page='test',
            exp_grps = exp_grps
        )    
        
    @expose('testexp.templates.simple')
    def simple(self):
        return dict(page='simple')
    #####################

    @expose('testexp.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('testexp.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('testexp.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('testexp.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)

    @expose('testexp.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('testexp.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('testexp.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('testexp.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from='/'):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login', came_from=came_from, __logins=login_counter)
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
