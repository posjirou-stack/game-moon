## デバッグメニュー(開発用)
##
## config.developer が有効な環境(SDKから直接起動した場合)でのみ、
## HUDの「デバッグ」ボタンまたは F2 キーから開ける。
## 配布ビルドでは config.developer が自動的に False になるため、プレイヤーからは見えない。
##
## できること:
## - 任意のシーン・エンディングへのジャンプ
## - スキル・SAN・関係値の増減
## - エンディング分岐フラグ(F1〜F5・特殊ルート)のON/OFF
## - カレンダーの時間送り

init python:

    def debug_add(var, delta):
        """デバッグ用: ストア変数を無検証で増減する。"""
        setattr(store, var, getattr(store, var) + delta)

    DEBUG_FLAG_LIST = [
        ("flag_f1_moonlens",       "F1 ムーンレンズ奪取"),
        ("flag_f2_yuki_saved",     "F2 雪 救出"),
        ("flag_f3_rikuhisa_saved", "F3 凛久 救出"),
        ("flag_f4_sign_removed",   "F4 印 解除"),
        ("flag_f5_endo_stopped",   "F5 遠藤 阻止"),
        ("flag_endo_route",        "特殊 遠藤ルート"),
    ]


screen debug_menu():

    tag menu
    modal True

    add Solid("#000000cc")

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 40
        ypadding 28
        background "#221418e6"

        vbox:
            spacing 12

            text "デバッグメニュー(開発環境のみ)" size 30 color "#ff9a9a"

            text "◆ シーンジャンプ" size 22 color "#ffe08a"

            hbox:
                spacing 8
                textbutton "1章:夜叉" action Jump("chapter1_izakaya") text_size 20
                textbutton "1章:新木場" action Jump("chapter1_campus") text_size 20
                textbutton "1章:遭遇" action Jump("chapter1_encounter") text_size 20
                textbutton "行動選択" action Jump("calendar_start") text_size 20
                textbutton "儀式" action Jump("climax_ritual") text_size 20

            hbox:
                spacing 8
                textbutton "END①" action Jump("ending_01_true") text_size 20
                textbutton "END②" action Jump("ending_02_good") text_size 20
                textbutton "END③" action Jump("ending_03_normal") text_size 20
                textbutton "END④" action Jump("ending_04_limited") text_size 20
                textbutton "END⑤" action Jump("ending_05_worst") text_size 20
                textbutton "END⑥" action Jump("ending_06_endo") text_size 20
                textbutton "END⑦" action Jump("ending_07_early_exit") text_size 20

            text "◆ スキル・SAN" size 22 color "#ffe08a"

            for dbg_line in ("knowledge", "investigation", "negotiation", "combat"):
                hbox:
                    spacing 8
                    $ dbg_name = skill_name(dbg_line)
                    $ dbg_val = get_skill(dbg_line)
                    $ dbg_var = SKILL_LINES[dbg_line][1]
                    text "[dbg_name]: [dbg_val]" min_width 280 size 22
                    textbutton "−1" action Function(debug_add, dbg_var, -1) text_size 20
                    textbutton "＋1" action Function(debug_add, dbg_var, 1) text_size 20

            hbox:
                spacing 8
                text "SAN: [san]" min_width 280 size 22
                textbutton "−10" action Function(debug_add, "san", -10) text_size 20
                textbutton "＋10" action Function(debug_add, "san", 10) text_size 20

            text "◆ エンディング分岐フラグ" size 22 color "#ffe08a"

            hbox:
                spacing 8
                for dbg_flag_var, dbg_flag_name in DEBUG_FLAG_LIST[:3]:
                    $ dbg_flag_state = "○" if getattr(store, dbg_flag_var) else "×"
                    textbutton "[dbg_flag_name] [dbg_flag_state]" action ToggleVariable(dbg_flag_var) text_size 20

            hbox:
                spacing 8
                for dbg_flag_var, dbg_flag_name in DEBUG_FLAG_LIST[3:]:
                    $ dbg_flag_state = "○" if getattr(store, dbg_flag_var) else "×"
                    textbutton "[dbg_flag_name] [dbg_flag_state]" action ToggleVariable(dbg_flag_var) text_size 20

            text "◆ カレンダー" size 22 color "#ffe08a"

            hbox:
                spacing 8
                text "[game_date]　[game_time]" min_width 280 size 22
                textbutton "時間帯を1つ進める" action Function(advance_slot) text_size 20

            null height 8

            textbutton "閉じる" action Return() xalign 0.5

    key "game_menu" action Return()
