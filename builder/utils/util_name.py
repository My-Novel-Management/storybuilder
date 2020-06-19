# -*- coding: utf-8 -*-
'''
Name Utility methods
====================
'''

__all__ = (
        'name_set_from',
        )


from builder.utils import assertion


def name_set_from(basename: str, name: str) -> tuple:
    lastname = firstname = fullname = exfullname = ''
    tmp = assertion.is_str(basename) if basename else assertion.is_str(name)
    if ',' in tmp:
        lastname, firstname = tmp.split(',')
    else:
        lastname = firstname = tmp
    fullname = tmp.replace(',', '')
    exfullname = f'{firstname}・{lastname}' if firstname != lastname else tmp
    return (firstname, lastname, fullname, exfullname)

