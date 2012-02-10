# -*- coding: utf-8 -*-
"""Game controller."""

from testexp.lib.base import BaseController
from tg import abort, expose, flash, require, url, request, redirect
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission
from testexp.model import *
from sqlalchemy import or_
#from tg import tmpl_context
from testexp.widgets import make_offer, accept_offer

__all__ = ['PlayController']


class PlayController(BaseController):
    """
    controller-wide authorization
    """
    
    # The predicate that must be met for all the actions in this controller:
    allow_only = has_permission('play',
                                msg=l_('Only for people with the "play" permission'))
                                
    @expose('testexp.templates.index')
    def index(self):
        """Let the user know that's visiting a protected controller."""
        flash(_("Player Controller here"))
        return dict(page='index')
    
    @expose('testexp.templates.index')
    def some_where(self):
        """Let the user know that this action is protected too."""
        return dict(page='some_where')
        
    @expose('testexp.templates.start')
    def start(self, came_from=url('/')):
        if not request.identity:
                login_counter = request.environ['repoze.who.logins'] + 1
                redirect('/login', came_from=came_from, __logins=login_counter)
                
        username = request.identity['repoze.who.userid']
        userid = DBSession.query(User.user_id).filter_by(user_name=username).first()[0]
        your = DBSession.query(Player).filter_by(user_id=userid).first()
        games = DBSession.query(Game).filter(or_(Game.player1_id == your.player_id, \
                Game.player2_id == your.player_id))
        #player_name = DBSession.query(Player.player_name).filter_by(user_id=userid).first()[0]
        exp_grps = DBSession.query(ExpGroup)
        
        return dict(your=your, exp_grps=exp_grps, games=games, page='start')
        
    @expose('testexp.templates.mygames')
    def mygames(self, came_from=url('/')):
        if not request.identity:
                login_counter = request.environ['repoze.who.logins'] + 1
                redirect('/login', came_from=came_from, __logins=login_counter)
                
        username = request.identity['repoze.who.userid']
        userid = DBSession.query(User.user_id).filter_by(user_name=username).first()[0]
        your = DBSession.query(Player).filter_by(user_id=userid).first()
        games = DBSession.query(Game).filter(or_(Game.player1_id == your.player_id, \
                Game.player2_id == your.player_id))
        user_grp = DBSession.query(ExpGroup.exp_group_name).filter_by( \
                exp_group_id=your.group_id).first()[0]
                
        game_status = {} # text description of current game status
        play_forms = {} # forms for making a play
        same_group = {} # whether the other player is in the same experiment group
        all_done = True # change to false if any games incomplete
        
        for game in games:
            game_form = None
            if game.player1_id == your.player_id:
                mygroup = 'Other player belongs to your group!'
                if game.accepted == True:
                    status = "Game is over.  Your offer was accepted."
                elif game.accepted == False:
                    status = "Game is over.  Your offer was refused."
                elif game.proposal_amt != None:
                    status = "Waiting for the other player to accept or reject the offer."
                    all_done = False
                else:
                    status = "Your turn:  make an offer."
                    all_done = False
                    game_form = make_offer.MakeOfferForm("make_offer_form", \
                        action='save_offer')
            else:
                mygroup = 'Other player does NOT belong to your group.'
                if game.accepted == True:
                    status = "Game is over.  You have accepted the offer."
                elif game.accepted == False:
                    status = "Game is over.  You have refused the offer."
                elif game.proposal_amt != None:
                    status = "Your turn:  choose to accept or reject the offer."
                    all_done = False
                    game_form = accept_offer.AcceptOfferForm("accept_offer_form", \
                        action='accept_offer')
                else:
                    status = "Waiting for the other player to make an offer."
                    all_done = False
            
            game_status[game.game_id] = status
            play_forms[game.game_id] = game_form
            same_group[game.game_id] = mygroup
        
        return dict(your=your, user_grp=user_grp, games=games, same_group=same_group, \
            game_status=game_status, play_forms=play_forms, all_done=all_done, page='mygames')
    
    @expose()
    def save_offer(self, **kw):
        if request.method != 'POST':
            raise Exception('save_offer must be a POST request')
        else:
            game = DBSession.query(Game).filter_by(game_id=kw['game_id']).first()
            game.proposal_amt = kw['proposal_amt']
            
            flash("saved offer of $" + kw['proposal_amt'] + " for game #" + kw['game_id'])
        redirect('mygames')
        
    @expose()
    def accept_offer(self, **kw):
        if request.method != 'POST':
            raise Exception('accept_offer must be a POST request')
        else:
            game = DBSession.query(Game).filter_by(game_id=kw['game_id']).first()
            p1 = DBSession.query(Player).filter_by(player_id=game.player1_id).first()
            p2 = DBSession.query(Player).filter_by(player_id=game.player2_id).first()
            
            if kw['accept'] == 'Yes':
                game.accepted = 1
                p1.total_winnings += (game.total_sum - game.proposal_amt)
                p2.total_winnings += game.proposal_amt
            elif kw['accept'] == 'No':
                game.accepted = 0
            else:
                accept_val = None
            
        flash("saved offer response of '" + kw['accept'] + "' for game #" + kw['game_id'])
        redirect('mygames')
        
    @expose()
    def simple(self, came_from=url('/')):
        if not request.identity:
                login_counter = request.environ['repoze.who.logins'] + 1
                redirect('/login', came_from=came_from, __logins=login_counter)
                
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, player %s!') % userid)
        redirect(came_from)
    
    def view(self, url):
        """Abort the request with a 404 HTTP status code."""
        abort(404)

