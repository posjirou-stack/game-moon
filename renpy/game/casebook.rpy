## 事件簿 — エンディング回収状況の一覧(要件定義書 8章の「進捗画面」)
## タイトル画面・ゲームメニューの「事件簿」ボタンから開く。
## 到達済みエンディングはタイトルを、未到達はヒントを表示する。

init python:

    ## 未到達エンディングのヒント(ネタバレしない程度の到達条件の示唆)
    ENDING_HINTS = {
        "01": "すべてを掴み、すべてを守り抜いた者だけが辿り着く結末。",
        "02": "儀式と黒幕を止めても、なお届かなかった手がある——。",
        "03": "レンズは奪った。だが“あの男”との対話は果たせなかった——。",
        "04": "儀式を止められずとも、この街の魂を守る術はある。",
        "05": "何も為せなかった夜に、月だけが輝いている。",
        "06": "真相を語る声に、最後まで耳を傾けた者だけが知る幕引き。",
        "07": "深淵を覗きすぎた者、敵を刺激しすぎた者の末路。",
    }

    def ending_seen(code):
        return (persistent.endings_seen is not None) and (code in persistent.endings_seen)


screen casebook():

    tag menu

    use game_menu(_("事件簿"), scroll="viewport"):

        vbox:
            spacing 18

            $ cb_count = len(persistent.endings_seen) if persistent.endings_seen else 0
            text "エンディング回収状況: [cb_count] / 7" size 26 color gui.accent_color

            null height 4

            for cb_code in ("01", "02", "03", "04", "05", "06", "07"):

                if ending_seen(cb_code):
                    $ cb_title = ENDING_TITLES[cb_code]
                    text "[cb_title]" size 24
                else:
                    $ cb_hint = ENDING_HINTS[cb_code]
                    text "？？？　——[cb_hint]" size 24 color "#666677"

            null height 12

            if cb_count >= 7:
                text "すべての結末が、事件簿に綴じられた。" size 24 color "#ffe08a"
            else:
                text "別の技能を伸ばし、別の選択をすれば、違う結末に辿り着く。" size 20 color "#8a8a99"
