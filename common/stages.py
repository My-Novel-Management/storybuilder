# -*- coding: utf-8 -*-
## stage common datas

## common defines
__STAGE_LAYER__ = "__stage__"

## meta data
STAGE_LAYERS = (
        (__STAGE_LAYER__ + "building", "建物",
            (
                "家",
                "壁",
                "天井",
                "床",
                "屋根",
                ),),
        (__STAGE_LAYER__ + "outside", "屋外",
            (
                "道路", "路", "路地",
                "ビル", "テナント",
                "アパート",
                "マンション",
                "一軒家",
                "スーパー", "商店", "店",
                "噴水",)),
        (__STAGE_LAYER__ + "inside", "屋内",
            (
                "畳",
                "本棚",
                "キッチン", "台所",
                "リビング", "居間",
                "ダイニング", "食堂",
                )),
        (__STAGE_LAYER__ + "fantasy", "ファンタジー",
            (
                "城",
                "砦",
                ),),
        )

