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

## 背景と立ち絵の登録。
## game/images/ に該当ファイルがあればそれを使い、なければプレースホルダー
## (背景=単色、立ち絵=非表示)で動く。ファイル名の規約は docs/asset-list.md を参照。
## アセットを追加したら、ファイルを置くだけで次回起動時から反映される。

init python:

    def _register_bg(name, color):
        path = "images/bg/" + name + ".png"
        if renpy.loadable(path):
            renpy.image("bg " + name, path)
        else:
            renpy.image("bg " + name, Solid(color))

    _register_bg("izakaya", "#241611")       # 居酒屋「夜叉」
    _register_bg("street_night", "#0d1128")  # 夜の繁華街
    _register_bg("campus", "#233022")        # 光山大学
    _register_bg("alley", "#141019")         # 裏路地
    _register_bg("office", "#1c2430")        # 玲紀探偵事務所
    _register_bg("library", "#2a2620")       # 図書館・古崎堂
    _register_bg("park_night", "#0f1c14")    # 哲学堂公園(夜)
    _register_bg("ritual", "#1a0a1e")        # 儀式場・異空間
    _register_bg("house", "#2b2118")         # 東風谷家
    _register_bg("house_burnt", "#17120e")   # 東風谷家(焼け跡)
    _register_bg("bar", "#1f1520")           # Bar「雪国」
    _register_bg("basement", "#161a16")      # 久美啓太の地下室
    _register_bg("nagae", "#101418")         # 長江ビル
    _register_bg("apartment", "#1b1b22")     # 中西アパート
    _register_bg("church", "#100d16")        # 星の知恵派の教会
    _register_bg("lab", "#121a20")           # 遠藤研究所
    _register_bg("grave", "#151a12")         # 遠藤楓の墓
    _register_bg("villa", "#1a2016")         # 奥多摩の別荘
    _register_bg("tower", "#201a10")         # 東京タワー

    ## 立ち絵(キャラ×表情差分)。ファイルが無い間は Null(何も表示しない)として
    ## 登録するので、show/hide 文はアセット到着前から書いておける。
    CHAR_SPRITES = {
        "yuki":    ("normal", "smile", "fear", "sad"),
        "riku":    ("blank", "normal", "smile"),
        "mizuna":  ("normal", "serious"),
        "kumi":    ("normal",),
        "endo":    ("normal", "tired"),
        "sumire":  ("normal",),
    }

    for _c, _emotes in CHAR_SPRITES.items():
        for _e in _emotes:
            _p = "images/char/%s_%s.png" % (_c, _e)
            if renpy.loadable(_p):
                renpy.image(_c + " " + _e, _p)
            else:
                renpy.image(_c + " " + _e, Null())

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
