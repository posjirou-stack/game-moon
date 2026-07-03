## 「月夜が魅せる物語 -Fated Moonlight-」
## エントリポイント: キャラクター定義・背景プレースホルダー・プロローグ(性別選択)のみを置く。
## 各章の本文は chapter*.rpy、行動選択ループは calendar.rpy、エンディングは endings.rpy を参照。
##
## 原作: 「月夜が魅せる物語」(作:唯燐 / 文:じゃこ缶・きりぅ)を原作とする二次創作。
## 非公開・身内プレイ用プロトタイプ。

define mizuna = Character("瑞名 慧", color="#8fb8ff")
define yuki = Character("東風谷 雪", color="#ffc9e3")
define rikuhisa = Character("間宮 凛久", color="#a8e6a1")
define endo = Character("遠藤 啓介", color="#d0a0ff")
define m = DynamicCharacter("mc_name", color="#ffe08a")

## 背景はまだアセット未着手のため、単色のプレースホルダーで場面転換を表現する。
image bg izakaya = Solid("#241611")
image bg street_night = Solid("#0d1128")
image bg campus = Solid("#233022")
image bg alley = Solid("#141019")
image bg office = Solid("#1c2430")
image bg library = Solid("#2a2620")
image bg park_night = Solid("#0f1c14")
image bg ritual = Solid("#1a0a1e")
image bg black = Solid("#000000")

label start:

    scene bg black

    "――これは、とある高校生が「運命」に出会うまでの、ほんの数日間の記録。"

    menu:
        "主人公の性別を選んでください。"

        "男性":
            $ gender = "male"
            $ first_person = "僕"

        "女性":
            $ gender = "female"
            $ first_person = "私"

    "名前は神来杜湊（からいと みなと）。18歳、私立高校の3年生。"

    "そして、[mc_name]にはもうひとつの顔がある。"

    "私立探偵事務所「玲紀探偵事務所」で、駆け出しの調査助手として働いているのだ。"

    ## ここから日付・SANのHUDを表示する
    $ hud_visible = True

    jump chapter1_izakaya
