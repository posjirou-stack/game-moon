## 育成/シミュレーション要素の土台(要件定義書 6.3, 7.1章を参照)
## 変数定義と、スキル判定・SAN増減・フラグ管理の共通関数をここに集約する。
##
## ファイル構成の規約は renpy/README.md を参照。

default gender = None          # "male" / "female"
default first_person = "僕"
default mc_name = "神来杜湊"    # 苗字:神来杜(からいと) 名:湊(みなと)

## 4方向スキルライン(7.1章)。初期値はハンドアウト4寄り(知識・オカルト)を高めに設定。
default skill_knowledge = 3      # 知識・オカルト(初期タイプ)
default skill_investigation = 1  # 探索(HO1由来)
default skill_negotiation = 1    # 交渉(HO2由来)
default skill_combat = 1         # 戦闘(HO3由来)

## 正気度(SAN)。0になると早期離脱エンド(⑦)へ直行する。
default san = 60

## 主要NPCとの関係値(5章のエンディング分岐で使用する想定)
default relationship_yuki = 0      # 東風谷雪
default relationship_rikuhisa = 0  # 間宮凛久
default relationship_mizuna = 0    # 瑞名慧

## エンディング分岐フラグ F1〜F5(要件定義書 5.2章)
default flag_f1_moonlens = False        # F1: ムーンレンズ奪取
default flag_f2_yuki_saved = False      # F2: 東風谷雪 救出
default flag_f3_rikuhisa_saved = False  # F3: 間宮凛久 救出(12/28 21:00まで)
default flag_f4_sign_removed = False    # F4: 死へと誘う印 解除
default flag_f5_endo_stopped = False    # F5: 遠藤啓介の野望阻止
default flag_endo_route = False         # ⑥特殊エンド: 遠藤啓介ルートに入ったか

## カレンダー表示用(HUD・ステータス画面が参照する)。
## 12/21〜12/22はチャプター1が advance_time() で直接更新し、
## 12/23以降は calendar.rpy の行動選択ループが更新する。
default game_date = "12月21日(水)"
default game_time = "夜"

## HUD(日付・SANの常時表示)の可視状態。プロローグ終了後にONにする。
default hud_visible = False

init python:

    ## スキルラインの内部名 → (表示名, ストア変数名)
    SKILL_LINES = {
        "knowledge":     ("知識・オカルト", "skill_knowledge"),
        "investigation": ("探索",           "skill_investigation"),
        "negotiation":   ("交渉",           "skill_negotiation"),
        "combat":        ("戦闘",           "skill_combat"),
    }

    SAN_MAX = 99

    def get_skill(line):
        """スキルラインの現在値を返す。line は SKILL_LINES のキー。"""
        return getattr(store, SKILL_LINES[line][1])

    def skill_name(line):
        return SKILL_LINES[line][0]

    def skill_check(line, threshold):
        """技能値が閾値以上なら True。「高いほど有利な選択肢が増える」判定の共通窓口。"""
        return get_skill(line) >= threshold

    def gain_skill(line, amount=1):
        """スキルラインを成長させ、画面右下に通知を出す。"""
        var = SKILL_LINES[line][1]
        setattr(store, var, getattr(store, var) + amount)
        renpy.notify("%s +%d" % (skill_name(line), amount))

    def change_san(delta):
        """SANを増減する(0〜SAN_MAXでクランプ)。0到達の分岐は calendar_hub 側で判定する。"""
        store.san = max(0, min(SAN_MAX, store.san + delta))
        if delta < 0:
            renpy.notify("SAN %d" % delta)
        elif delta > 0:
            renpy.notify("SAN +%d" % delta)

    def change_relationship(who, delta):
        """NPC関係値を増減する。who は 'yuki' / 'rikuhisa' / 'mizuna'。"""
        var = "relationship_" + who
        setattr(store, var, getattr(store, var) + delta)

    def set_flag(flag_var, note=None):
        """エンディング分岐フラグを立て、通知を出す。flag_var はストア変数名の文字列。"""
        setattr(store, flag_var, True)
        if note:
            renpy.notify("【" + note + "】")

    def advance_time(date, time):
        """カレンダー表示を更新する(チャプター1の一本道区間で使用)"""
        store.game_date = date
        store.game_time = time
