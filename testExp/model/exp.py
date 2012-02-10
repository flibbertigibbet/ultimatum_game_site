# -*- coding: utf-8 -*-
"""experiment model module.  Bootstrap data in websetup/bootstrap.py."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, Numeric, Boolean
from sqlalchemy.orm import relation, backref

from testexp.model import DeclarativeBase, metadata, DBSession

__all__ = ['ExpGroup', 'Player', 'Game']


class ExpGroup(DeclarativeBase):
    __tablename__ = 'exp_group'
    
    #{ Columns
    
    exp_group_id = Column(Integer, autoincrement=True, primary_key=True)
    
    exp_group_name = Column(Unicode(255), unique=True, nullable=False)
    
    #}
    
    #{ Relations
    
    players = relation('Player', backref='parent_group')
    
    #}
    
    #{ Special methods

    def __repr__(self):
        return ('<Group: name=%r>' % self.exp_group_name).encode('utf-8')

    def __unicode__(self):
        return self.exp_group_name

    #}

# player
class Player(DeclarativeBase):
    __tablename__ = 'player'
    
    player_id = Column(Integer, autoincrement=True, primary_key=True)
    
    user_id = Column(Integer, ForeignKey('tg_user.user_id'), unique=True)
    
    player_name = Column(Unicode(255), unique=True, nullable=False)
    
    total_winnings = Column(Numeric, nullable=False, default=0)
    
    group_id = Column(Integer, ForeignKey('exp_group.exp_group_id'), nullable=False)
    
    #{ Special methods

    def __repr__(self):
        return ('<Player: name=%r>' % self.player_name).encode('utf-8')

    def __unicode__(self):
        return self.player_name

    #}

# game
class Game(DeclarativeBase):
    __tablename__ = 'game'
    
    game_id = Column(Integer, autoincrement=True, primary_key=True)
    
    player1_id = Column(Integer, ForeignKey('player.player_id'))
    
    player2_id = Column(Integer, ForeignKey('player.player_id'))
    
    total_sum = Column(Numeric, nullable=False, default=4)
    
    proposal_amt = Column(Numeric)
    
    accepted = Column(Boolean, nullable=True)

