# -*- coding: utf-8 -*-
## fashion common data


## common defines
__FASHION_LAYER__ = "__fashion__"

## meta data
FASHION_LAYERS = (
        (__FASHION_LAYER__ + "clothes", "服装",
            (
                "服", "七部丈", "半袖", "短パン",
                "着物", "和服", "襦袢", "帯",
                )),
        (__FASHION_LAYER__ + "tops", "トップ",
            (
                "上着", "セーター", "Ｔシャツ", "シャツ", "ジャンパー", "ジージャン", "コート",
                "スタジャン", "スカジャン", "ドレス", "ワンピース", "キャミソール", "キャミ",
                )),
        (__FASHION_LAYER__ + "bottoms", "ボトム",
            (
                "ズボン", "ジーパン", "デニム", "半ズボン", "ハーフパンツ",
                "ジャージ", "ツナギ", "つなぎ",
                )),
        (__FASHION_LAYER__ + "under", "下着",
            (
                "下着", "ブラ", "ブラジャー", "パンツ", "パンティ", "ショーツ", "トランクス", "ブリーフ",
                "ストッキング", "ニーハイ", "靴下", "レッグウォーマー", "アームウォーマー",
                )),
        (__FASHION_LAYER__ + "shoes", "靴",
            (
                "靴", "革靴", "ブーツ", "長靴", "シューズ",
                "ヒール", "スニーカー", "草履", "雪駄", "下駄",
                )),
        (__FASHION_LAYER__ + "items", "小物",
            (
                "帽子", "ハット", "キャップ", "ベレー帽", "ベレィ帽",
                "リストバンド",
                "手袋",
                "スカーフ", "ストール",
                "ネクタイ",
                "眼鏡", "サングラス", "グラス",
                "かんざし", "簪", "ヘアバンド", "カチューシャ", "リボン",
                )),
        (__FASHION_LAYER__ + "faces", "外見",
            (
                "髪",
                "肌",
                "目", "瞳", "眼",
                "鼻",
                "口", "唇",
                "体", "身体",
                "手",
                "足",
                )),
        )
