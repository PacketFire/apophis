""" Permissions Module """
from dataclasses import dataclass
from typing import List
from collections import namedtuple

PERMISSION = namedtuple('Permission', 'owner admin normal')

@dataclass(frozen=True)
class Permission:
    levels = List[str]


@dataclass(frozen=True)
class Owner(Permission):
    commands = ['theo', 'music', 'define', 'permission']


class Admin(Permission):
    commands = ['theo', 'music', 'define']


class Normal(Permission):
    commands = ['theo', 'define']
