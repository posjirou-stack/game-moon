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
## F1・F2はクライマックス(endings.rpy)で下記の進行変数から精算される。
default flag_f1_moonlens = False        # F1: ムーンレンズ奪取
default flag_f2_yuki_saved = False      # F2: 東風谷雪 救出
default flag_f3_rikuhisa_saved = False  # F3: 間宮凛久 救出(12/28 21:00まで)
default flag_f4_sign_removed = False    # F4: 死へと誘う印 解除
default flag_f5_endo_stopped = False    # F5: 遠藤啓介の野望阻止
default flag_endo_route = False         # ⑥特殊エンド: 遠藤啓介ルートに入ったか

## ---- メインチェーン進行変数(docs/scenario-structure.md 3章) ----

## YUKIチェーン
default yuki_memory = 0        # 雪の記憶回復度(0〜3): 1=自宅 2=縁者 3=長江ビル
default yuki_protected = False # 雪を安全な場所に匿ったか(F2の前提)

## LENSチェーン(F1はクライマックスで compute_f1() により精算)
default lens_located = False       # ムーンレンズの所在=哲学堂公園と確定
default lens_route = False         # 防衛体制と地下侵入経路の情報
default arsenal_destroyed = False  # 山野ビル(武器工場)破壊 ※優先度B

## RIKUチェーン
default riku_located = False   # 監禁場所=中西アパートの特定
default riku_scouted = False   # 咲耶の不在時間帯の把握
default riku_rescued = False   # 凛久の身柄確保(洗脳解除=F3はev_riku4)

## SIGNチェーン
default sign_known = False          # 印の正体の知識
default sign_data_1 = False         # 呪文詳細・第1資料(長江ビル/東京教会)
default sign_data_2 = False         # 呪文詳細・第2資料(遠藤研究所など)
default sign_research_done = False  # 12時間の解呪研究完了

## ENDOチェーン
default endo_suspect = False     # 「森本蓮司」への疑い
default endo_identified = False  # 森本蓮司=遠藤啓介の確証
default sumire_trust = False     # 遠藤菫の信頼(F5説得の緩和・END⑥分岐)

## 勢力(協力組織)。"kumi"/"gov"/"gilt"/"yama"/"sangen"/"bab" を格納する
default allies = set()

## 暗殺カウンタ(END⑦の追加トリガー。scenario-structure.md 7章)
default assassination_heat = 0        # 敵組織の注意度
default assassination_pending = False # 閾値超過→次のハブで襲撃イベント発生

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

    ## ---- 暗殺カウンタ(END⑦の追加トリガー) ----

    ASSASSINATION_THRESHOLD = 4

    def add_heat(amount):
        """敵組織の注意度を上げる。閾値を超えると次のハブで襲撃イベントが発生する。

        久美啓太の隠れ家(allies に "kumi")を確保していれば、原作の
        「幾度も暗殺を防いだ実績のある久美啓太の家」に倣い襲撃は発生しない。
        """
        store.assassination_heat += amount
        if store.assassination_heat >= ASSASSINATION_THRESHOLD and "kumi" not in store.allies:
            store.assassination_pending = True
            renpy.notify("……刺すような視線を感じる")
        else:
            renpy.notify("敵組織の注意を引いた(注意度 %d)" % store.assassination_heat)

    def magician_count():
        """解呪儀式(SIGN-5)に動員できる協力魔術師の人数(scenario-structure.md 4章)。"""
        total = 0
        if "kumi" in store.allies:
            total += 20
        if "gov" in store.allies:
            total += 30
        if "yama" in store.allies:
            total += 50
        if "sangen" in store.allies:
            total += 30
        if "gilt" in store.allies:
            total += 150
        return total
