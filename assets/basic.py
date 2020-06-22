# -*- coding: utf-8 -*-
'''
Asset: basic data
=================
'''

ASSET = {
        "PERSONS":(
        # (tag / name / full / age (birth) / sex / job / call / info)
        ('man', '男', '', 30,(1,1), 'male', '会社員'),
        ('woman', '女', '', 30,(1,1), 'female', '会社員'),
        ),
        "STAGES":(
        # (tag / name / parent / (geometry) / info)
        # * basic area
        ('Japan', '日本', '', (135.00,35.00)),
        ('Tokyo', '東京', '', (139.67,35.76)),
        ),
        "DAYS":(
        # (tag / name / month / day / year)
        ('current', '現在', 4,1, 2020),
        ),
        "TIMES":(
        # (tag / name / hour / minute))
        ("earlymorning", "早朝", 6, 0),
        ("morning", "朝", 8, 0),
        ("midmorning", "午前", 10, 0),
        ("branch", "昼前", 11, 0),
        ("noon", "正午", 12, 0),
        ("afternoon", "午後", 14, 0),
        ("afterschool", "放課後", 16, 0),
        ("evening", "夕方", 17, 0),
        ("night", "夜", 20, 0),
        ("midnight", "深夜", 23, 0),
        ("deepnight", "真夜中", 2, 0),
        ),
        "ITEMS":(
        # (tag / name / cate / info)
        ),
        "WORDS":(
        # (tag / name / cate / info)
        ),
        "RUBIS":(
        # (origin / rubi / exclusions / always)
        ),
        }
