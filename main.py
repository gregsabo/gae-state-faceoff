#!/usr/bin/env python

import webapp2
from state import State
import random
from state_list import STATE_LIST
from google.appengine.ext.webapp import template


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(template.render('index.html', {}))


class FaceoffHandler(webapp2.RequestHandler):
    def get(self):
        a_key = random.choice(STATE_LIST.keys())
        b_key = random.choice(STATE_LIST.keys())
        self.response.write(template.render('faceoff.html', dict(
            a_key=a_key,
            a_name=STATE_LIST[a_key],
            b_key=b_key,
            b_name=STATE_LIST[b_key]
        )))


class WinnerHandler(webapp2.RequestHandler):
    def post(self):
        winner_code = self.request.get('winner')
        loser_code = self.request.get('loser')

        winner = State.get_or_create(winner_code)
        loser = State.get_or_create(loser_code)

        winner.record_win_against(loser).put()
        loser.record_loss_against(winner).put()

        self.redirect('/faceoff')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/faceoff', FaceoffHandler),
    ('/winner', WinnerHandler),
], debug=True)
