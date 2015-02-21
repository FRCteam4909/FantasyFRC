#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging

import globals
from globals import get_team_list

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import ndb
from google.appengine.api import users

from datastore_classes import league_key, Choice, root_event_key, choice_key, account_key, Account

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Help(webapp2.RequestHandler):

    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()

        #Check if user is logged in
        if user is None:
            #Send html data to browser
            template_values = {'logged_out': users.create_login_url('/help/')}
            template = JINJA_ENVIRONMENT.get_template('templates/help.html')
            self.response.write(template.render(template_values))
        else:
            #Current user's id, used to identify their data
            user_id = user.user_id()
            logout_url = users.create_logout_url('/')

            #Make global call to get the user data
            account = globals.get_or_create_account(user)
            league_id = account.league

            #Proccess league info
            if league_id != '0':
                league_name = league_key(league_id).get().name
            else:
                league_name = ""

            #Send html data to browser
            template_values = {
                        'user': user.nickname(),
                        'logout_url': logout_url,
                        'league_name': league_name
                        }
            template = JINJA_ENVIRONMENT.get_template('templates/help.html')
            self.response.write(template.render(template_values))

class PointsPage(webapp2.RequestHandler):

    def get(self):
        # Checks for active Google account session
        user = users.get_current_user()

        #Check if user is logged in
        if user is None:
            #Send html data to browser
            template_values = {'logged_out': users.create_login_url('/help/points')}
            template = JINJA_ENVIRONMENT.get_template('templates/points_detail.html')
            self.response.write(template.render(template_values))
        else:
            #Current user's id, used to identify their data
            user_id = user.user_id()
            logout_url = users.create_logout_url('/')

            account = globals.get_or_create_account(user)
            league_id = account.league

            logging.info(account)
            if league_id != '0':
                league_name = league_key(league_id).get().name
            else:
                league_name = ""

            #Send html data to browser
            template_values = {
                        'user': user.nickname(),
                        'logout_url': logout_url,
                        'league_name': league_name
                        }
            template = JINJA_ENVIRONMENT.get_template('templates/points_detail.html')
            self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
                                       ('/help/', Help),
                                       ('/help/points', PointsPage),
                                       ], debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()