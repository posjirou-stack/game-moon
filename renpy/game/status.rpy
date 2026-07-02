## 育成/シミュレーション要素の土台(要件定義書 6.3, 7.1, 12章を参照)
## フェーズ1(MVP)では数値は基本的に動かないが、フェーズ2以降で使う変数の枠を先に用意しておく。

default gender = None          # "male" / "female"
default mc_name = "神来杜湊"    # 苗字:神来杜(からいと) 名:湊(みなと)

## 4方向スキルライン(7.1章)。初期値はハンドアウト4寄り(知識・オカルト)を高めに設定。
default skill_knowledge = 3    # 知識・オカルト(初期タイプ)
default skill_investigation = 1  # 探索(HO1由来)
default skill_negotiation = 1    # 交渉(HO2由来)
default skill_combat = 1         # 戦闘(HO3由来)

## 正気度(SAN)。数値の意味・上限はフェーズ2で精緻化する。
default san = 60

## 主要NPCとの関係値(5章のエンディング分岐で使用する想定)
default relationship_yuki = 0      # 東風谷雪
default relationship_rikuhisa = 0  # 間宮凛久
default relationship_mizuna = 0    # 瑞名慧

## カレンダー進行(12/21始まり)。MVPでは12/22夜まで進む。
default game_date = "12月21日(水)"
default game_time = "夜"

init python:

    def advance_time(date, time):
        """カレンダー表示を更新する(MVPでは演出目的のみ)"""
        store.game_date = date
        store.game_time = time
