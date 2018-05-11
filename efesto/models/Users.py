# -*- coding: utf-8 -*-
from peewee import BooleanField, CharField

from .Base import Base


class Users(Base):
    identifier = CharField(unique=True)
    superuser = BooleanField(default=False)

    def login(identifier):
        """
        Logs in an user, when provided with a valid identifer
        """
        try:
            return Users.get(Users.identifier == identifier)
        except Users.DoesNotExist:
            return None

    def _apply_permissions(self, query, model, level):
        """
        Applies the requested permission level to a query
        """
        lhs = (model.others_permission >= level)
        rhs_left_right = (model.owner_permission >= level)
        if model == Users:
            rhs_left = ((model.id == self.id) & rhs_left_right)
        else:
            rhs_left = ((model.owner == self.id) & rhs_left_right)
        rhs_right_right = (model.group_permission >= level)
        rhs_right = ((model.group == self.group) & rhs_right_right)
        return query.where(lhs | (rhs_left | rhs_right))

    def do(self, action, query, model):
        """
        Does an action with a query, on a model
        """
        actions = {
            'read': 1,
            'edit': 2,
            'eliminate': 3
        }
        return self._apply_permissions(query, model, actions[action])
