# -*- coding: utf-8 -*-
"""Basic config.
"""


################################################################
#
# Sample:
#
# 1) PERSONS
#       人物簡易設定
# 2) STAGES
#       舞台基本設定
# 3) DAYS
#       年月日設定
# 4) TIMES
#       時間帯基本設定
# 5) ITEMS
#       小道具設定
# 6) WORDS
#       辞書設定
# 7) RUBIS
#       ルビ設定
# 8) LAYERS
#       レイヤ設定
#
################################################################

ASSET = {
        "PERSONS":(
        # Tag / 氏,名 / 歳 / 性別 / 職業 / 呼称 / 紹介
        ("work_man", "男性会社員", "", 30, "male", "会社員", "me:俺"),
        ("work_woman", "女性会社員", "", 30, "female", "会社員", "me:私"),
        ("old_man", "老人", "", 70, "male", "無職", "me:儂"),
        ("old_woman", "老婦人", "", 70, "female", "無職", "me:私"),
        ("school_boy", "男子小学生", "", 10, "male", "小学生", "me:ぼく"),
        ("school_girl", "女子小学生", "", 10, "female", "小学生", "me:わたし"),
        ("student_boy", "男子学生", "", 15, "male", "学生", "me:僕"),
        ("student_girl", "女子学生", "", 15, "female", "学生", "me:私"),
        ),
        "STAGES":(
        # Tag / 名前 / 紹介
        ## 一般施設
        ("apart", "アパート"),
        ("manshion", "マンション"),
        ("supermarket", "スーパー"),
        ("department_store", "デパート"),
        ("commercial_facility", "総合商業施設"),
        ("conveni", "コンビニ"),
        ("office", "オフィス"),
        ("street", "路地"),
        ("crossroad", "交差点"),
        ## 施設内
        ("toilet", "トイレ"),
        ("kitchen", "キッチン"),
        ("dining", "食堂"),
        ("living", "リビング"),
        ## 公共施設
        ("school", "学校"),
        ("primaryschool", "小学校"),
        ("jrschool", "中学校"),
        ("highschool", "高校"),
        ("station", "駅"),
        ("busstop", "バス停"),
        ("port", "港"),
        ("airport", "空港"),
        ("park", "公園"),
        ## 乗り物
        ("elevator", "エレベータ"),
        ("bicycle", "自転車"),
        ("bike", "バイク"),
        ("train", "電車"),
        ("taxi", "タクシー"),
        ("bus", "バス"),
        ("car", "車"),
        ("ship", "船"),
        ("ferry", "フェリー"),
        ("airplane", "飛行機"),
        ),
        "DAYS":(
        # Tag / 名前 / 月 / 日 / 年
        ("meiji1", "明治元年", 1,25, 1868),
        ("taisho1", "大正元年", 7,30, 1912),
        ("showa1", "昭和元年", 12,25, 1926),
        ("heisei1", "平成元年", 1,8, 1989),
        ("911", "米国同時テロ事件", 9,11, 2001),
        ("311", "東日本大震災", 3,11, 2011),
        ("reiwa1", "令和元年", 5,1, 2019),
        ),
        "TIMES":(
        # Tag / 名前 / 時 / 分
        ("earlymorning", "早朝", 6, 0),
        ("morning", "朝", 8, 0),
        ("midmorning", "午前", 10, 0),
        ("noon", "正午", 12, 0),
        ("afternoon", "午後", 14, 0),
        ("afterschool", "放課後", 16, 0),
        ("evening", "夕方", 17, 0),
        ("night", "夜", 20, 0),
        ("midnight", "深夜", 23, 0),
        ("deepnight", "真夜中", 2, 0),
        ),
        "ITEMS":(
        # Tag / 名前 / 紹介
        ),
        "WORDS":(
        # Tag / 名前 / 紹介
        ),
        "RUBIS":(
        # Base / Rubi / Type
        ),
        "LAYERS":(
        ),
        }
