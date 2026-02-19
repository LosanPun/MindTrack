"""
Project initialization hooks.

This applies a compatibility patch for Django 5.1 running on Python 3.14,
where django.template.context BaseContext.__copy__ triggers an AttributeError.
"""

from copy import copy as _copy
import sys

import django


def _patch_django_context_copy_for_py314():
    if not django.get_version().startswith("5.1"):
        return
    if sys.version_info < (3, 14):
        return

    from django.template.context import BaseContext, Context

    def _base_context_copy(self):
        duplicate = object.__new__(self.__class__)
        duplicate.__dict__ = self.__dict__.copy()
        duplicate.dicts = self.dicts[:]
        return duplicate

    def _context_copy(self):
        duplicate = _base_context_copy(self)
        duplicate.render_context = _copy(self.render_context)
        return duplicate

    BaseContext.__copy__ = _base_context_copy
    Context.__copy__ = _context_copy


_patch_django_context_copy_for_py314()
