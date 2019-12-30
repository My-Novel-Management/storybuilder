# -*- coding: utf-8 -*-
"""Example story
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append('builder')
## public libs
## local libs
from builder.drawer import Drawer
from builder.world import World
from builder.writer import Writer
## local files
from assets import basic
from config import DAYS, ITEMS, LAYERS, PERSONS, RUBIS, STAGES, TIMES, WORDS

D = Drawer()
W = Writer
_ = Writer.getWho()
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
def sc_getpeach(w: World):
    granma, granpa = W(w.granma), W(w.granpa)
    peach = W(w.peach)
    return w.scene("大きな桃", w.comment("桃を拾う"),
            w.comment("流れてきた桃を拾う", "おばあさんとおじいさんの簡単な状況説明とか"),
            granma.be(D.p("昔々あるところに$n_granpaと$n_granmaがいた")),
            granpa.be(),
            granma.explain("子どもがいない", D.p("老夫婦には子どもがおらず、")),
            _.feel("寂しい", D.pT("寂しい暮らしを送っていた")),
            granpa.go("芝刈り", D.p("$Sは山に芝刈りに、")),
            granma.come("洗濯", D.pT("$Sは川へ洗濯に出かけた")),
            w.load("river"),
            w.load("granma_base"),
            granma.look("hair", "白髪混じりで細い髪質"),
            granma.look(D.p("川へやってきた$Sは")),
            peach.come(D.pT("桃が流れてくるのに気づいた")),
            peach.look("size", "人間が二人掛かりで持てそうな大きさ",
                D.p("それはとても大きく、とても細腕の老婆一人では持ち上げられそうにないほどで、")),
            peach.look("mate", "しっかりと色づき美味しそう",
                D.pT("水に浮かびながらその色づいた表面を見せ、どんぶらことやってくる")),
            granma.do("pickup", "桃を", D.p("$Sは流れてきた桃を木の棒で引き寄せると、")),
            _.do("get", D.pT("手を伸ばしてそれを何とか岸に引き上げた"),),
            granma.talk("まあ、なんて大きな桃だこと！", "これを持って帰ったら$granpaもさぞ驚くことだろうね"),
            granma.go(D.pT("紐で結びつけて「よいしょ」と背負うと、ほうほうのていで何とか家まで持ち帰った")),
            camera=w.granma,
            stage=w.on_river,
            day=w.in_getpeach, time=w.at_morning,
            )

def sc_birth(w: World):
    granma, granpa = W(w.granma), W(w.granpa)
    return w.scene("誕生", w.comment("$taroの誕生秘話"),
            granma.be(), granpa.be(),
            w.load("living"),
            w.load("granma_base"),
            granma.talk("$n_taroだ。そうだ。$n_taroだよ"),
            stage=w.on_home,
            time=w.at_midmorning,
            )

def sc_known(w: World):
    return w.scene("鬼の悪事を知る", w.comment("村人から鬼の悪事を聞く"),
            camera=w.taro,
            stage=w.on_vila,
            day=w.in_rumor, time=w.at_afternoon,
            )

def sc_desicion(w: World):
    return w.scene("決意", w.comment("鬼退治の決意をする"),
            stage=w.on_home,
            time=w.at_night,
            )

def sc_voyage(w: World):
    return w.scene("旅立ち", w.comment("旅立つ$taro"),
            )

def sc_meetdog(w: World):
    return w.scene("犬と会う", w.comment("犬を味方にする"),
            camera=w.taro,
            stage=w.on_street,
            day=w.in_meetdog, time=w.at_afternoon,
            )

def sc_meetmonkey(w: World):
    return w.scene("猿と会う", w.comment("猿を味方にする"),
            camera=w.taro,
            stage=w.on_street,
            day=w.in_meetmonkey, time=w.at_evening,
            )

def sc_meetbird(w: World):
    return w.scene("雉と会う", w.comment("雉を味方にする"),
            camera=w.taro,
            stage=w.on_street,
            day=w.in_meetbird, time=w.at_midmorning,
            )

def sc_island(w: World):
    return w.scene("鬼ヶ島", w.comment("鬼ヶ島で鬼退治をする"),
            w.load("oni_island"),
            camera=w.taro,
            stage=w.on_island,
            day=w.in_arrived, time=w.at_afternoon,
            )

def sc_busteroni(w: World):
    return w.scene("鬼退治",
            camera=w.taro,
            stage=w.on_island,
            day=w.in_arrived, time=w.at_afternoon,
            )

def sc_backhome(w: World):
    taro, dog, monkey, bird = W(w.taro), W(w.dog), W(w.monkey), W(w.bird)
    granma, granpa = W(w.granma), W(w.granpa)
    vilaman = W(w.vilaman)
    return w.scene("村に戻る", w.comment("宝物と共に村に戻った"),
            w.load("vila"),
            granma.be(), granpa.be(),
            vilaman.be(20),
            taro.come(),taro.have(w.treasure),
            dog.come(), monkey.come(), bird.come(),
            taro.talk("無事に帰ったよ！"),
            granma.talk("おお$taroが！"),
            granpa.talk("本当によく帰ってきた"),
            dog.do("smile"),
            monkey.do("laugh"),
            bird.do("smile"),
            taro.explain("宝物を"),
            camera=w.taro,
            stage=w.on_vila,
            day=w.in_backhome, time=w.at_morning,
            )

## episodes
def ep_birth(w: World):
    return w.episode("$taro誕生",
            sc_getpeach(w),
            sc_birth(w),
            sc_known(w),
            sc_desicion(w),
            sc_voyage(w),
            )

def ep_ally(w: World):
    return w.episode("味方を得る",
            sc_meetdog(w),
            sc_meetmonkey(w),
            sc_meetbird(w),
            )

def ep_buster(w: World):
    return w.episode("鬼退治",
            sc_island(w),
            sc_busteroni(w),
            sc_backhome(w),
            )

## persons
def set_persons(w: World):
    taro = W(w.taro)
    granma = W(w.granma)
    return (
        w.block("taro_base",
            taro.have(w.cloth_momo1),
            ),
        w.block("taro_battle",
            taro.have(w.cloth_momo2),
            taro.have(w.katana),
            taro.have(w.flag),
            ),
        w.block("granma_base",
            granma.have(w.cloth_boro),
            ),
        )

## stages
def set_stages(w: World):
    floor, ceil, wall = W(w.floor), W(w.ceil), W(w.wall)
    water, tree, land = W(w.water), W(w.tree), W(w.land)
    house = W(w.house)
    fort = W(w.fort)
    return (
        w.block("living",
            ceil.be(),
            floor.be(),
            wall.be(),
            ceil.wear("梁が露出した寒々としたもの"),
            floor.wear("板張りでところどころ穴が空いている粗末なもの"),
            wall.wear("漆喰で塗られている"),
            ),
        w.block("river",
            water.be(), land.be(), tree.be(2),
            water.wear("綺麗で透き通っている"),
            ),
        w.block("oni_island",
            land.be(),
            fort.be(),
            fort.wear("石を積んで造られた巨大な城"),
            ),
        w.block("in_onifort",
            wall.be(),
            floor.be(),
            wall.wear("じっとり湿った石が積まれた壁"),
            floor.wear("そこここを苔が覆っている"),
            ),
        w.block("vila",
            house.be(10),
            house.wear("木の板を貼り付け、屋根は茅葺き"),
            )
        )

## items

## main
def ch_main(w: World):
    return w.chapter("main",
            ep_birth(w),
            ep_ally(w),
            ep_buster(w),
            )

def world():
    w = World("桃太郎")
    w.setCommonData()
    w.setAssets(basic.ASSET)
    w.buildDB(PERSONS,
            STAGES, ITEMS, DAYS, TIMES, WORDS,
            RUBIS, LAYERS)
    w.entryBlock(
            *set_persons(w),
            *set_stages(w),
            )
    return w

def main(): # pragma: no cover
    w = world()
    return w.build(
            ch_main(w),
            )


if __name__ == '__main__':
    import sys
    sys.exit(main())

