#   Copyright (C) 2018  Jacopo Cascioli
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
from peewee import BooleanField, CharField

from .Base import Base


class Users(Base):
    identifier = CharField(unique=True)
    superuser = BooleanField(default=False)

    @staticmethod
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
        if self.superuser:
            return query
        actions = {'read': 1, 'edit': 2, 'eliminate': 3}
        return self._apply_permissions(query, model, actions[action])
