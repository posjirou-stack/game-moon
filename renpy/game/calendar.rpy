## カレンダー行動選択ループ(要件定義書 6.3章「日付・時間帯システム」)
##
## 12/23〜12/29 を「日×時間帯」の行動枠として扱い、
## 行動選択画面 → 選んだ調査イベントのラベルへ call → 終了後この画面に戻る、
## というハブ&スポーク構造で進行する。12/29の行動枠を使い切ると
## クライマックス(哲学堂公園の儀式 / endings.rpy)へ合流する。
##
## 各イベントの本文は chapter2_events.rpy にある(現状はフェーズ2用のプレースホルダー)。
## イベントを追加するときは、chapter2_events.rpy にラベルを書き、
## 下の EVENTS リストに InvestigationEvent を1件追加するだけでよい。

## 進行状態(セーブ対象)
default day_index = 0        # CALENDAR のインデックス
default slot_index = 0       # その日の時間帯インデックス
default events_done = set()  # 消化済みイベントID
default picked_event = None  # 直前に選択したイベントID

init python:

    ## 行動可能期間。12/29の夜(21:00)は儀式のため行動枠に含めない。
    CALENDAR = [
        ("12月23日(金)", ["昼", "夕方", "夜"]),
        ("12月24日(土)", ["昼", "夕方", "夜"]),
        ("12月25日(日)", ["昼", "夕方", "夜"]),
        ("12月26日(月)", ["昼", "夕方", "夜"]),
        ("12月27日(火)", ["昼", "夕方", "夜"]),
        ("12月28日(水)", ["昼", "夕方", "夜"]),
        ("12月29日(木)", ["昼", "夕方"]),
    ]

    class InvestigationEvent(object):
        """行動選択画面に並ぶ調査イベント1件分の定義。

        id         : イベントID(events_done への記録・ラベル解決に使う)
        name       : 行動選択画面に表示する行動名
        label      : call されるラベル名
        min_day    : 出現開始日(CALENDARのインデックス)。None なら初日から
        max_day    : 出現最終日(同上)。None なら最終日まで。タイムリミット表現に使う
        slots      : 出現する時間帯のタプル。None なら全時間帯
        req        : 解放条件(引数なしの callable)。None なら常時解放
        req_text   : 条件未達のときにボタンへ添える説明
        repeatable : True なら何度でも選べる(育成コマンド用)
        """

        def __init__(self, id, name, label, min_day=None, max_day=None,
                     slots=None, req=None, req_text="", repeatable=False):
            self.id = id
            self.name = name
            self.label = label
            self.min_day = min_day
            self.max_day = max_day
            self.slots = slots
            self.req = req
            self.req_text = req_text
            self.repeatable = repeatable

        def visible(self):
            """現在の日付・時間帯の選択肢一覧に表示されるか。"""
            if (not self.repeatable) and (self.id in store.events_done):
                return False
            if self.min_day is not None and store.day_index < self.min_day:
                return False
            if self.max_day is not None and store.day_index > self.max_day:
                return False
            if self.slots is not None and current_slot() not in self.slots:
                return False
            return True

        def unlocked(self):
            """技能値などの解放条件を満たしているか(未達なら灰色表示)。"""
            if self.req is None:
                return True
            return self.req()

    ## 調査イベント定義。上に並べたものほど行動選択画面の上に表示される。
    ## ここに登録された「フラグ獲得イベント」は、エンディング分岐(endings.rpy)の
    ## 骨格を通しでテストするためのプレースホルダー。本文・条件はフェーズ2で差し替える。
    EVENTS = [
        ## --- フラグ獲得イベント(1回限り) ---
        InvestigationEvent(
            "ev_moonlens", "哲学堂公園で「ムーンレンズ」を探る", "ev_moonlens",
            min_day=3,  # 12/26以降
            req=lambda: skill_check("investigation", 3),
            req_text="探索3以上で解放"),
        InvestigationEvent(
            "ev_yuki_hideout", "雪を安全な場所へ匿う", "ev_yuki_hideout",
            req=lambda: skill_check("investigation", 2),
            req_text="探索2以上で解放"),
        InvestigationEvent(
            "ev_rikuhisa", "間宮凛久を説得する", "ev_rikuhisa",
            max_day=5,  # 12/28まで(F3のタイムリミット)
            req=lambda: skill_check("negotiation", 3),
            req_text="交渉3以上で解放(12/28まで)"),
        InvestigationEvent(
            "ev_sign", "「死へと誘う印」の解呪法を調べる", "ev_sign",
            req=lambda: skill_check("knowledge", 5),
            req_text="知識・オカルト5以上で解放"),
        InvestigationEvent(
            "ev_endo_dialogue", "遠藤啓介と対峙する", "ev_endo_dialogue",
            min_day=4,  # 12/27以降
            req=lambda: skill_check("negotiation", 4) or skill_check("combat", 5),
            req_text="交渉4以上 または 戦闘5以上で解放"),

        ## --- 育成コマンド(繰り返し可) ---
        InvestigationEvent(
            "ev_library", "図書館・古書店で資料を漁る(知識+1)", "ev_library",
            slots=("昼",), repeatable=True),
        InvestigationEvent(
            "ev_kikikomi", "繁華街で聞き込みをする(探索+1)", "ev_kikikomi",
            repeatable=True),
        InvestigationEvent(
            "ev_office", "探偵事務所で瑞名と情報を整理する(交渉+1)", "ev_office",
            repeatable=True),
        InvestigationEvent(
            "ev_training", "護身の心得を仕込んでもらう(戦闘+1)", "ev_training",
            repeatable=True),
        InvestigationEvent(
            "ev_rest", "休息をとる(SAN回復)", "ev_rest",
            repeatable=True),
    ]

    def get_event(event_id):
        for ev in EVENTS:
            if ev.id == event_id:
                return ev
        raise Exception("未定義のイベントID: %r" % (event_id,))

    def event_label(event_id):
        return get_event(event_id).label

    def visible_events():
        return [ev for ev in EVENTS if ev.visible()]

    def current_date():
        return CALENDAR[store.day_index][0]

    def current_slot():
        return CALENDAR[store.day_index][1][store.slot_index]

    def calendar_finished():
        return store.day_index >= len(CALENDAR)

    def remaining_slots():
        """クライマックスまでの残り行動枠数(現在の枠を含む)。"""
        total = 0
        for i in range(store.day_index, len(CALENDAR)):
            slots = len(CALENDAR[i][1])
            if i == store.day_index:
                total += slots - store.slot_index
            else:
                total += slots
        return total

    def sync_calendar_time():
        """HUD・ステータス画面用の日付表示をカレンダー進行に同期する。"""
        if calendar_finished():
            store.game_date = "12月29日(木)"
            store.game_time = "夜"
        else:
            store.game_date = current_date()
            store.game_time = current_slot()

    def advance_slot():
        """時間帯を1つ進める。日の行動枠を使い切ったら翌日へ。"""
        if calendar_finished():
            return
        store.slot_index += 1
        if store.slot_index >= len(CALENDAR[store.day_index][1]):
            store.slot_index = 0
            store.day_index += 1
        sync_calendar_time()

    def finish_event(event_id):
        """イベント消化を記録し、時間を進める。"""
        store.events_done.add(event_id)
        advance_slot()


## 行動選択画面。call screen で呼ばれ、選択されたイベントIDを Return する。
screen action_select():

    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 40
        ypadding 30

        vbox:
            spacing 10

            label "[game_date]　[game_time]"

            $ slots_left = remaining_slots()
            text "儀式(12/29 夜)まで、残り行動枠 [slots_left]" size 22

            null height 10

            text "この時間、どう動く？"

            null height 4

            for ev in visible_events():
                if ev.unlocked():
                    textbutton ev.name action Return(ev.id)
                else:
                    textbutton "[ev.name]　※[ev.req_text]" sensitive False


label calendar_start:

    $ sync_calendar_time()

    scene bg black
    with dissolve

    "――ここから12月29日の夜までは、日々の行動を自分で選んで過ごすことになる。"

    "限られた行動枠の中で、どの技能を伸ばし、どの手がかりを追うか。その積み重ねが、結末を決める。"

    "【システム土台版】各行動の本文はフェーズ2で執筆されます。現在は骨格の動作確認用プレースホルダーです。"

    jump calendar_hub


label calendar_hub:

    ## SAN枯渇は即、早期離脱エンド(⑦)
    if san <= 0:
        jump ending_07_early_exit

    ## 行動枠を使い切ったらクライマックスへ
    if calendar_finished():
        jump climax_ritual

    $ sync_calendar_time()

    call screen action_select

    $ picked_event = _return

    call expression event_label(picked_event) from _call_investigation_event

    $ finish_event(picked_event)

    jump calendar_hub
