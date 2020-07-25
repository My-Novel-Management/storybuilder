# -*- coding: utf-8 -*-
'''
Sample Story #001: Momotaro
'''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append('builder')
from builder.world import World
from assets import basic
from assets import common_rubi


# DB
PERSONS = [
        # (tag / name / full / age / birth / sex / job / calling / info)
        ('taro', '桃太郎', '', 15,(4,10), 'm', '村人', 'me:私'),
        ('mam', '絹江', '', 60,(1,1), 'f', '農家', 'me:わたし'),
        ('dad', '源三', '', 67,(1,1), 'm', '農家', 'me:わし'),
        ('dog', '犬', '', 10,(1,1), 'm', '動物'),
        ('monkey', '猿', '', 10,(1,1), 'm', '動物'),
        ('bird', '雉', '', 10,(1,1), 'm', '動物'),
        ('oni', '鬼', '', 30,(1,1), 'm', '鬼'),
        ]
STAGES = [
        # (tag / name / parent / geometry / info)
        ('Vila', '太郎の村', '', (100,100)),
        ('home', '太郎の家', 'on_Vila'),
        ('river', '村近くの川', '', (150,100)),
        ('field', '街道', '', (50,50)),
        ('Island', '鬼ヶ島', '', (500,50)),
        ('ship', '船', '', (200,50)),
        ]
DAYS = [
        # (tag / name / month / day / year)
        ('birthtaro', '桃太郎誕生', 4,10, 100),
        ('know_oni', '鬼の悪事を知る', 5,10, 103),
        ('start_voyage', '鬼退治出発', 5,20, 103),
        ('buster_oni', '鬼退治', 6,10, 103),
        ]
TIMES = [
        # (tag / name / hour / minute)
        ('morning', '朝', 8,00),
        ('noon', '昼', 12,00),
        ('afternoon', '午後', 14,00),
        ('night', '夜', 20,00),
        ]
ITEMS = [
        # (tag / name / category / info)
        ('dango', '吉備団子', 'food'),
        ('katana', '刀', 'weapon'),
        ]
WORDS = [
        # (tag / name / info)
        ("dogrun", "犬走り"),
        ("memo", "手帳"),
        ]
RUBIS = [
        # (origin / rubi / exclusions / always)
        ("桃太郎", "｜桃太郎《ももたろう》"),
        ]

## scenes
# NOTE:
#   create each scenes
def sc_get_peach(w: World):
    mam = w.get('mam')
    return w.scene("桃を拾う",
            w.comment("序盤。おばあさんが桃を拾う"),
            w.cmd.change_camera('mam'),
            w.cmd.change_stage('on_river'),
            "これは桃太郎の物語だ",
            w.plot_setup("昔、おじいさんとおばあさんがいた", "二人には子どもがない"),
            mam.be("あるところにおじいさんとおばあさんがいました", "&"),
            mam.explain("おじいさんは山へ芝刈りに、おばあさんは川へ洗濯に出かけました"),
            mam.wear("渋染の着物にほつれた草履", "ぼさぼさの白髪"),
            mam.wear("目は小豆のよう"),
            mam.wear("肌はシミが目立つ"),
            mam.come("洗濯物を籠に入れ、河原にやってきた$Sでしたが、", "&"),
            mam.do("川の上流からどんぶらこと大きな桃が流れてくるのを見つけました。それを見て思います"),
            mam.do("じっと立って桃を見つめて"),
            w.motif("桃", "大きな桃"),
            mam.talk("あれまあ、なんて大きな桃なんでしょう"),
            mam.think("おじいさんが好きそうだと思った", "&"),
            mam.think("拾って帰って、おじいさんと一緒に食べようかしらね", "#桃をゲット"),
            w.foreshadow("桃を拾う"),
            mam.do("そう考え、何とか木の棒を使ってこちらに引き寄せ、ひと抱えもある桃を手に入れました"),
            mam.do("$memoを手にして、それを忘れないように書き込んでおいた"),
            mam.go("それを籠に入れ、家に帰りました"),
            )

def sc_birth_taro(w: World):
    mam, dad = w.get('mam'), w.get('dad')
    taro = w.get('taro')
    return w.scene("誕生",
            w.br(),
            w.cmd.change_stage('on_home'),
            "部屋の様子を少し書いておく",
            mam.be("#居間に座っていた"),
            dad.be(),
            mam.talk("おじいさん見ておくれよ、この大きな桃"),
            dad.talk("ありゃまあ、なんてぇ大きな桃だよ",
                "早速$meが切ってやろう"),
            dad.do("ナタを手にした$Sは大きく振り上げると、一気に桃に向かってブスリ、とやりました"),
            taro.be("#$S誕生する", "桃はパカーと真っ二つに割れて、中から玉のような赤子が出てきました"),
            w.payoff("桃から桃太郎が誕生"),
            mam.wear("たすき掛け"),
            mam.talk("おじいさん、こりゃあ人の子だ！？　なんてことだ！"),
            mam.talk("子どもがいない$meに神様が授けて下さったんだよぉ"),
            dad.talk("よし！", "$taroと名付けよう",
                "今日からお前は$taroだ"),
            taro.explain("こうして$Sは生まれました"),
            w.comment("桃太郎誕生"),
            )

def sc_voyage(w: World):
    taro = w.get('taro')
    mam, dad = w.get('mam'), w.get('dad')
    dango = w.get('dango')
    return w.scene("旅立ち",
            w.symbol("　　　　◆"),
            w.cmd.change_camera('taro'),
            w.cmd.change_date('start_voyage'),
            w.cmd.change_time('morning'),
            taro.be(),
            taro.explain("$Sはすくすくと育ち、あっという間に大きく逞しく成長しました"),
            taro.do("ある日、村人から鬼の悪行を聞いた$Sは考えました"),
            w.plot_turnpoint("鬼の話を聞く"),
            w.plot_develop("$taroは鬼退治に出発する"),
            taro.think("――何とか鬼を退治して村に恩返しがしたい"),
            taro.explain("そこでおじいさんとおばあさんを前にして、鬼退治をしたいと言い出したのです"),
            mam.be(),
            dad.be(),
            mam.look("#神妙な顔で座っている"),
            mam.talk("どうしても行くというのかい？"),
            taro.talk("$meの決意は固いです", "何よりここまで育ててくれたあなたたちや村の人たちに恩返しがしたい"),
            dad.talk("ばあさんや、男の子というのはいつか自分のやることを見つけて旅立つものだ",
                "行かせてやろうじゃないか"),
            dad.do("そう言うと$Sは$katanaを持ってきて、$taroに渡します"),
            dad.talk("これをお持ちなさい", '&'),
            dad.talk("かつて鬼を切ったと言われる名刀だ"),
            taro.talk("こんな大切なものを", "$meは絶対に鬼をやっつけてきます"),
            mam.talk("それじゃあ$meは、", "$dangoでも作ろうかね"),
            taro.talk("ありがとうございます"),
            mam.do("団子を作って"),
            taro.do("おばあさんからは$dangoを貰った"),
            dango.wear("きな粉がまぶされ、美味しそうだ"),
            taro.explain("こうして$Sは翌朝早くに旅立っていきました"),
            w.comment("鬼退治"),
            taro.go(),
            )

def sc_ally(w: World):
    taro = w.get('taro')
    dog, monkey, bird = w.get('dog'), w.get('monkey'), w.get('bird')
    return w.scene("家来",
            w.plot_develop("$taroは道中で家来を得る"),
            w.tag.title('家来その１'),
            w.cmd.change_stage('field'),
            taro.come('$Sが道を歩いていると、', '&'),
            w.plot_setup("犬が歩いてきた", about="犬の家来"),
            dog.come('向こうから$Sが歩いてきた'),
            dog.look('その$Sはなんともひどい有様で、そのうちに道端に倒れてしまった'),
            taro.talk('大丈夫ですか？'),
            dog.talk('お腹をすかせてしまって'),
            taro.talk('それならこれを食べて下さい'),
            taro.do('$dangoを一つあげました'),
            dog.talk("助かりました", "ところで$taroさんはどこに行くのですか？"),
            taro.talk("鬼を退治しに行くところなんだ"),
            dog.talk("それなら$meがお供しましょう", "鬼はこの牙が苦手と言います"),
            taro.explain("こうして犬は$Sの家来となりました"),
            taro.do("犬が$dogrunを走り回っているのを見ていた"),
            w.br(),
            w.tag.title('家来その２'),
            taro.hear("誰かの話しかける声"),
            taro.do("またしばらく歩いていきます。今度は猿が木の上から話しかけます"),
            monkey.be("#木の上に"),
            monkey.talk("おい、なんか美味そうなもん持ってるな"),
            taro.talk("ああ、これか", "おばあさんが作ってくれた$dangoだ"),
            monkey.talk("一つ$meにくれねえか？"),
            taro.talk("いいけれども、ただでという訳にはいかないな"),
            taro.do("$Sが猿を見て渋ると、猿はこう返しました"),
            monkey.talk("それなら何でも一つ言うことを聞いてやろう",
                "$meは力こそないが、知恵はよく働く",
                "悪評高い鬼のやつらにだって知恵比べなら負けはしねえ"),
            taro.talk("それなら$meと一緒に鬼退治に来てくれませんか？"),
            monkey.do("二つ返事で頷くと、$Sは$dangoを貰って一気に口に放り込んだ"),
            taro.explain("こうして犬に続き猿も家来にした$Sだったが、その行く手を阻むように川が横たわっていた"),
            w.br(),
            w.tag.title('家来その３'),
            taro.talk("困ったなあ"),
            bird.come("そこに$Sが優雅に翼を広げてやってくる"),
            bird.talk("おや、噂の$taroさんじゃありませんか", "どうかされましたか？"),
            taro.talk("いや、実は川が渡れずに困っていたんだ"),
            bird.talk("それなら$meが仲間たちを呼んで渡してあげましょう"),
            bird.do("そう言うと$Sはピーと鳴き、仲間を沢山集め、$taroたちを向こう岸へと運んでくれた"),
            taro.do("$Sはお礼にと$dangoを渡したが、$birdは鬼退治に行くという話を聞き、一緒に行ってくれることになった"),
            taro.explain("$Sは家来として犬、猿、雉とそれぞれ引き連れ、$on_Islandを目指しました"),
            w.br(),
            w.tag.title('船で渡る'),
            taro.explain('$Sたちは船で$Islandに渡りました'),
            )

def sc_island(w: World):
    taro = w.get('taro')
    oni = w.get('oni')
    return w.scene("$on_Island",
            w.cmd.change_stage('on_Island'),
            w.plot_resolve("$taroは鬼退治をした"),
            w.comment("$taroは鬼退治をする"),
            taro.come("$Sは家来と共に$on_Islandへとやってきた"),
            oni.be("酒とご馳走で祝勝会をしている"),
            taro.talk("やい！", "村の人たちから奪った宝物は返してもらうぞ"),
            oni.talk("うるさいわ。一体何だというんだ？"),
            taro.talk("$meは$taroだ。お前らを成敗する！"),
            taro.do("$Sは家来と共にその場にいた鬼たちをあっという間に組み伏せた"),
            oni.talk("参りました。どうか、命だけは……"),
            taro.talk("もうこれ以上村の人に悪さをするんじゃないぞ？", "いいな？"),
            taro.explain("こうして鬼たちから宝物を巻き上げ、村に持ち帰りました"),
            )

# episodes
def ep_birth_momotaro(w: World):
    return w.episode("$taro誕生",
            w.plot_note("桃太郎が誕生するところ"),
            sc_get_peach(w),
            sc_birth_taro(w),
            outline="流れてきた大きな桃には赤子（$taro）が入っていた",
            )

def ep_ally(w: World):
    return w.episode("味方",
            w.plot_note("鬼退治の旅に出る桃太郎"),
            w.plot_note("行く先々で仲間を手に入れ、いざ鬼ヶ島に向かう"),
            sc_voyage(w),
            sc_ally(w),
            outline='鬼退治の旅に出た$taroは道中で仲間を得る')

def ep_buster_daemon(w: World):
    return w.episode("$oni退治",
            w.plot_note("鬼退治を行う桃太郎"),
            w.plot_note("奪われた宝物を村へと持ち帰る"),
            sc_island(w),
            outline="鬼ヶ島にやってきた$taroは鬼退治をし、村に宝物を持って帰った",
            )

# main
def writernote(w: World):
    return w.writer_note('企画意図',
            "これはサンプルとして「桃太郎」を使って説明するものである",
            "作品についての企画意図や、企画の方向性、応募要項などをここにまとめておく",
            )

def ch_1st(w: World):
    return w.chapter("前半",
            ep_birth_momotaro(w),
            )

def ch_2nd(w: World):
    return w.chapter("後半",
            ep_ally(w),
            )

def ch_ending(w: World):
    return w.chapter("エピローグ",
            ep_buster_daemon(w),
            )

def chara_momotaro(w: World):
    return w.chara_note('$taroの履歴書',
            "おばあさんの手により川を流れていた桃が拾われ、その中から生まれた異端児",
            "通常の人間よりも早くに大きく育ち、怪力と誠実さ、正義感を備えていた",
            "ある時、村の人から鬼が宝物を奪っていった話を聞き、鬼退治を決意するのだった",
            )

def main(): # pragma: no cover
    w = World.create_world('桃太郎')
    w.config.set_outline('桃から生まれた$taroが鬼退治をする')
    w.db.set_from_asset(basic.ASSET)
    w.db.set_persons(PERSONS)
    w.db.set_stages(STAGES)
    w.db.set_days(DAYS)
    w.db.set_times(TIMES)
    w.db.set_items(ITEMS)
    w.db.set_words(WORDS)
    w.db.set_rubis(RUBIS)
    w.db.set_from_asset(common_rubi.ASSET)
    w.config.set_base_date(4,10, 100)
    w.config.set_base_time(8,00)
    w.config.set_sites("エブリスタ", "小説家になろう")
    w.config.set_taginfos('昔話', "男主人公", "動物", "ファンタジィ")
    return w.run(
            writernote(w),
            ch_1st(w),
            ch_2nd(w),
            ch_ending(w),
            chara_momotaro(w),
            )


if __name__ == '__main__':
    import sys
    sys.exit(main())

