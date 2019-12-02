# -*- coding: utf-8 -*-
"""Sample story for the momotaro.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append('builder')
from builder.world import World
import momotaro_config as cnf

################################################################
#
# Sample step:
# 1) Create the world
#       世界を作成する。
# 2) Create a new chapter
#       章の作成。
# 3) Create a episode
#       エピソード作成。
# 4) Create a new scene
#       シーン作成。物語のベース。ここに様々なActionを追加する。
# 5) Create a new stage
#       舞台作成。シーンに必須要素
# 6) Create a new day and time
#       日時作成。シーンのサブ要素
# 7) Add a scene plot
#       シーンプロットの作成。概要のないシーンは原則使えない
# 8) Add scene actions
#       シーンアクションの追加。
#
################################################################


## scenes
"""Scene は Action の塊。
"""
def sc_washing(w: World):
    s = w.scene("洗濯に", "おばあさんは洗濯に出かけて巨大な桃を見つけた")
    s.setCamera(w.granma)
    s.setStage(w.stage.river).setDay(w.day.getpeach).setTime(w.time.morning)
    s.add(
        w.comment("桃太郎誕生の話"),
        w.be(None, "昔あるところに子どものない老夫婦がいた").d("昔々あるところに子どものない老夫婦がいたそうだ"),
        w.move(w.granpa, "山へ芝刈りに行った").d("じいさんは山に芝刈りに出かけ、"),
        w.move(w.granma, "川に洗濯にくる").d("ばあさんは洗濯に川にやってきた"),
        w.look("大きな桃を見つける").d("と、川をどんぶらと大きな桃が流れてくるではないか"),
        w.think("思案する").d("どうしようかと考えたが、珍しいものだ、持ち帰ろうと決意する"),
        w.act("桃を拾って帰る").d("何とか木の棒で桃を引っ掛けてそれを寄せる",
            "川から拾い上げると思いのほか重く、ずっしりとしていた"),
        )
    return s

def sc_birth(w: World):
    s = w.scene("誕生", "桃太郎が生まれる")
    s.setCamera(w.granma)
    s.setStage(w.stage.home).setDay(w.day.birth).setTime(w.time.afternoon)
    s.add(
        w.be(None, "午後").d("その昼のことだ"),
        w.look(w.granma, "夫に桃のことを相談").d("$Sは桃を拾ったのだがどうすべきかと相談をしてみた"),
        w.talk(w.granpa, "中を見てみよう").t("こりゃあデカいな",
            "よし、切ってみるとしよう", "$meに任せておきなさい"),
        w.have("ナタを手に取る").d("表からナタを取ってきて、"),
        w.act("桃を割る").d("それを思い切り振り上げるとそのまま「えい！」と力強く桃に当てた"),
        w.look(w.granma, "桃から赤子が出てくる").d("桃はぱっくりと二つに割れ、中からは玉のような赤子が出てきて泣き声を上げた"),
        w.talk("どうしよう").t("あらあら。どうしましょうねえ"),
        w.talk(w.granpa, "どうしようって、喜ぶしかねえ！").same('t'),
        w.talk(w.granma, "そうよね").same('t'),
        w.think("二人とも神からの贈り物と喜ぶ").d("それでも二人は喜んでいた",
            "特に$Sの顔は涙でぐしゃぐしゃになり、真っ赤になっていたほどだった"),
        )
    return s

def sc_know_deamon(w: World):
    s = w.scene("悪事を知る", "村の人が鬼に色々とられて困っていると聞く")
    s.setCamera(w.taro)
    s.setStage(w.stage.vila).setDay(w.day.rumor).setTime(w.time.afternoon)
    s.add(
        w.be(None, "桃太郎は成長した").d("桃太郎はすくすく成長し、あっという間に大きくなった"),
        w.combine(
        w.act(w.taro, "村の中を歩いている").d("ある日、村の中を歩いていると、"),
        w.hear("鬼の噂を聞く").flag("鬼の噂").d("村人が集まってこそこそと何やら話している",
            "どうやら鬼に蔵に収めておいた宝物を盗まれたというのだ"),
        ),
        w.think("鬼をこらしめたい").d("$Sは鬼を退治しようと決意を固めた"),
        )
    return s

def sc_talk_buster(w: World):
    s = w.scene("鬼退治したい桃太郎", "鬼のことを両親に話して旅立ちの許可をもらう")
    s.setCamera(w.taro)
    s.setStage(w.stage.home).setDay(w.day.rumor).setTime(w.time.night)
    s.add(
        w.be(w.taro, "両親を前にじっと座っている").d("$Sはぎゅっと拳を握り締めて、両親を前にしていた"),
        w.act(w.taro, "鬼のことを相談する").deflag("鬼の噂"),
        w.combine(
        w.talk(w.taro, "実はずっと考えていたんだ").t("実はさ、"),
        w.talk(w.taro, "何か村の役に立ちたいって思ってた").t("$me、ずっと何か村の役に立ちたいって考えてたんだ"),
        ),
        w.think(w.granma, "返答に困る"),
        w.act(w.taro, "どうしても鬼が許せないと説得する"),
        w.talk(w.granma, "そこまで言うなら止めないよ"),
        )
    return s

def sc_dummyscene(w: World):
    s = w.scene("ダミーシーン", "テスト用です")
    return s.omit()

def sc_depature(w: World):
    s = w.scene("旅立ち", "鬼退治の旅に出る")
    s.setCamera(w.taro)
    s.setStage(w.stage.home).setDay(w.day.voyage).setTime(w.time.morning)
    s.add(
        w.symbol("◆"),
        w.be(w.taro, "ダミー冒頭").omit(),
        w.look(w.taro, "準備を終えて家の前にいる"),
        w.talk(w.granma, "これを").same(),
        w.have(w.taro, "$t_dangoを貰う").same(),
        w.move("出発する"),
        )
    return s

def sc_meetdog(w: World):
    s = w.scene("犬と出会う", "道端で犬に出会い仲間にする")
    s.setCamera(w.taro)
    s.setStage(w.stage.onstreet).setDay(w.day.meetdog).setTime(w.time.afternoon)
    s.add(
        w.layer("alley"),
        w.move(w.taro, "道を歩いていた"),
        w.look("犬と出会う"),
        w.talk(w.dog, "死にそうなので何か食べ物を下さい"),
        w.have(w.taro, "$t_dangoをやる"),
        w.act("$n_dogを仲間にした"),
        )
    return s

def sc_meetmonkey(w: World):
    s = w.scene("猿と出会う", "猿に出会い仲間にする")
    s.add(
        w.move(w.taro, "犬を連れて歩いていた"),
        w.look("猿と出会う"),
        w.talk(w.monkey, "腹減って死にそうなんだ。それくれ"),
        w.have(w.taro, "$t_dangoをやった"),
        w.act("$n_monkeyが仲間になった"),
        )
    return s

def sc_meetpheasant(w: World):
    s = w.scene("雉と出会う", "雉に出会い仲間にする")
    s.add(
        w.move(w.taro, "道を歩いていた"),
        w.look("雉と出会う"),
        w.talk(w.pheasant, "それ欲しい"),
        w.have(w.taro, "$t_dangoをやる"),
        w.act("$n_pheasantが仲間になった"),
        )
    return s

def sc_arrivedisland(w: World):
    s = w.scene("島に向かう", "鬼ヶ島に向かう")
    s.setCamera(w.taro)
    s.setStage(w.stage.onship).setDay(w.day.rideship).setTime(w.time.afternoon)
    s.add(
        w.move(w.taro, "船に乗り鬼ヶ島に向かう"),
        )
    return s

def sc_gotoisland(w: World):
    s = w.scene("鬼ヶ島", "鬼ヶ島にて鬼退治する")
    s.setCamera(w.taro)
    s.setStage(w.stage.island).setDay(w.day.arrived).setTime(w.time.morning)
    s.add(
        w.move(w.taro, "$w_islandにやってくる"),
        w.act("鬼を退治する"),
        w.have("鬼の宝物を手に入れる"),
        w.move("帰る"),
        )
    return s

def sc_backhome(w: World):
    s = w.scene("帰宅", "宝物を持って村に帰る")
    s.setCamera(w.taro)
    s.setStage(w.stage.vila).setDay(w.day.backhome).setTime(w.time.afternoon)
    s.add(
        w.move(w.taro, "村に戻ってくる"),
        w.be(w.granma, "村人たちみんな喜んで出迎える"),
        )
    return s

## episodes
"""Episode は Scene の塊。
"""
def ep_intro(w: World):
    return w.episode("桃太郎誕生",
            "拾った桃から赤子が生まれ、桃太郎に成長する",
            sc_washing(w),
            sc_birth(w),
            )

def ep_depature(w: World):
    return w.episode("鬼退治に出発",
            "桃太郎は鬼が悪さをしていると知り、鬼退治に出向く",
            sc_dummyscene(w),
            sc_know_deamon(w),
            sc_talk_buster(w),
            sc_depature(w),
            )

def ep_alley(w: World):
    return w.episode("味方ゲットだぜ",
            "旅の道中で家来を得る",
            sc_meetdog(w),
            sc_meetmonkey(w),
            sc_meetpheasant(w),
            )

def ep_bustered(w: World):
    return w.episode("そして鬼退治",
            "鬼ヶ島に渡って鬼退治をする",
            sc_gotoisland(w),
            sc_backhome(w),
            )

## chapters
"""Chapter は Episode の塊。
"""
def ch_main(w: World):
    return w.chapter("main story",
            ep_intro(w),
            ep_depature(w),
            ep_alley(w),
            ep_bustered(w),
            )

def ch_sub(w: World):
    return w.chapter("sub story",
            ).omit()

## setting
def set_stages(w: World):
    """Set stages.
    """
    return w

## main
def world():
    """Create a world.
    """
    w = World(2)
    w.set_db(cnf.PERSONS, cnf.CHARAS,
            cnf.STAGES,
            cnf.DAYS, cnf.TIMES,
            cnf.ITEMS,
            cnf.WORDS)
    set_stages(w)
    return w

def story(w: World):
    return w.story("桃太郎",
            ch_main(w),
            ch_sub(w),
            )

def main(): # pragma: no cover
    w = world()
    return w.build(story(w))


if __name__ == '__main__':
    import sys
    sys.exit(main())

