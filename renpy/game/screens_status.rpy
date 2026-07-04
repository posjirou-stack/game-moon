## HUD(日付・SANの常時表示)とステータス画面(要件定義書 8章)
##
## - game_hud   : ゲーム中、画面右上に日付・時間帯・SANを常時表示するオーバーレイ。
##                プロローグ終了後に hud_visible = True で有効化される。
## - status_screen : スキル・SAN・関係値の一覧。HUDのボタンか F1 キーで開く。
## - notify    : gain_skill()/change_san() の通知表示に使う(標準テンプレート未導入のため自前定義)。

init python:

    config.overlay_screens.append("game_hud")

    def gauge(value, maximum, width=10):
        """テキスト製の簡易ゲージ(例: ■■■□□□□□□□)を返す。"""
        if maximum <= 0:
            return ""
        filled = int(round(float(max(0, min(value, maximum))) / maximum * width))
        return "■" * filled + "□" * (width - filled)


screen game_hud():

    zorder 90

    if hud_visible:

        frame:
            xalign 0.995
            yalign 0.01
            xpadding 16
            ypadding 8
            background "#000000b0"

            hbox:
                spacing 22

                text "[game_date]　[game_time]" size 22 color "#e8e8f0"
                text "SAN [san]" size 22 color "#c9e4ff"
                ## keyboard_focus False: 矢印キーでの選択肢操作がHUDに吸われないようにする
                textbutton "ステータス":
                    action ShowMenu("status_screen")
                    text_size 22
                    keyboard_focus False
                if config.developer:
                    textbutton "デバッグ":
                        action ShowMenu("debug_menu")
                        text_size 22
                        keyboard_focus False

        ## キーボードショートカット(HUD表示中のみ有効)
        key "K_F1" action ShowMenu("status_screen")
        if config.developer:
            key "K_F2" action ShowMenu("debug_menu")


screen status_screen():

    tag menu
    modal True

    ## 背景を暗く落とす
    add Solid("#000000cc")

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 48
        ypadding 36
        background "#14141ee6"

        vbox:
            spacing 14

            text "ステータス" size 34 color "#ffe08a"

            text "[mc_name]　／　[game_date]　[game_time]" size 24

            null height 6

            $ san_gauge = gauge(san, 60, 12)
            text "正気度(SAN)　[san_gauge]　[san]" size 24 color "#c9e4ff"

            null height 10

            text "◆ スキルライン" size 24 color "#ffe08a"

            $ g_knowledge = gauge(skill_knowledge, 10)
            $ g_investigation = gauge(skill_investigation, 10)
            $ g_negotiation = gauge(skill_negotiation, 10)
            $ g_combat = gauge(skill_combat, 10)

            text "知識・オカルト　[g_knowledge]　[skill_knowledge]" size 24
            text "探索　　　　　　[g_investigation]　[skill_investigation]" size 24
            text "交渉　　　　　　[g_negotiation]　[skill_negotiation]" size 24
            text "戦闘　　　　　　[g_combat]　[skill_combat]" size 24

            null height 10

            text "◆ 関係値" size 24 color "#ffe08a"

            text "東風谷 雪: [relationship_yuki]　　間宮 凛久: [relationship_rikuhisa]　　瑞名 慧: [relationship_mizuna]" size 24

            ## 開発環境でのみ、エンディング分岐フラグの内部状態を表示する
            if config.developer:

                null height 10

                text "◆ フラグ(開発環境のみ表示)" size 24 color "#ff9a9a"

                $ dbg_flags = "F1:%s F2:%s F3:%s F4:%s F5:%s 特殊:%s" % (
                    "○" if flag_f1_moonlens else "×",
                    "○" if flag_f2_yuki_saved else "×",
                    "○" if flag_f3_rikuhisa_saved else "×",
                    "○" if flag_f4_sign_removed else "×",
                    "○" if flag_f5_endo_stopped else "×",
                    "○" if flag_endo_route else "×")
                text "[dbg_flags]" size 24

                $ dbg_misc = "勢力:%s　注意度:%d　魔術師:%d人" % (
                    "/".join(sorted(allies)) if allies else "なし",
                    assassination_heat, magician_count())
                text "[dbg_misc]" size 24

            null height 16

            hbox:
                xalign 0.5
                spacing 30
                textbutton "資料庫" action ShowMenu("archive_screen")
                textbutton "閉じる" action Return()

    key "game_menu" action Return()
