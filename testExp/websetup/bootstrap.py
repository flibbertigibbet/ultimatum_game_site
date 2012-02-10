# -*- coding: utf-8 -*-
"""Setup the testExp application"""

import logging
from tg import config
from testexp import model
import transaction

def bootstrap(command, conf, vars):
    """Place any commands to setup testexp here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = u'manager'
        u.display_name = u'Example manager'
        u.email_address = u'manager@somedomain.com'
        u.password = u'managepass'

        model.DBSession.add(u)

        g = model.Group()
        g.group_name = u'managers'
        g.display_name = u'Managers Group'

        g.users.append(u)

        model.DBSession.add(g)

        p = model.Permission()
        p.permission_name = u'manage'
        p.description = u'This permission give an administrative right to the bearer'
        p.groups.append(g)

        model.DBSession.add(p)

        u1 = model.User()
        u1.user_name = u'editor'
        u1.display_name = u'Example editor'
        u1.email_address = u'editor@somedomain.com'
        u1.password = u'editpass'

        model.DBSession.add(u1)

        #################################
        # add experiment bootstrap data
        g1 = model.ExpGroup()
        g1.exp_group_name = u'group one'
        model.DBSession.add(g1)

        g2 = model.ExpGroup()
        g2.exp_group_name = u'group two'
        model.DBSession.add(g2)

        # players are editor and manager
        p1 = model.Player()
        p1.user_id = 1
        p1.player_name = 'Tweedledee'
        p1.total_winnings = 0
        p1.group_id = 1
        model.DBSession.add(p1)

        p2 = model.Player()
        p2.user_id = 2
        p2.player_name = 'Tweedledum'
        p2.total_winnings = 0
        p2.group_id = 2
        model.DBSession.add(p2)

        game1 = model.Game()
        game1.player1_id = 1
        game1.player2_id = 2
        game1.total_sum = 4
        model.DBSession.add(game1)

        game2 = model.Game()
        game2.player1_id = 2
        game2.player2_id = 1
        game2.total_sum = 4
        model.DBSession.add(game2)
        
        players = model.Group()
        players.group_name = u'players'
        players.display_name = u'Players Group'

        players.users.append(u)
        players.users.append(u1)

        model.DBSession.add(players)
        
        play = model.Permission()
        play.permission_name = u'play'
        play.description = u'This permission allows users to play experiment games.'
        play.groups.append(players)

        model.DBSession.add(play)
        ##################################

        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print 'Warning, there was a problem adding your auth data, it may have already been added:'
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'

    # <websetup.bootstrap.after.auth>
