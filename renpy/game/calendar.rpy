## カレンダー行動選択ループ(要件定義書 6.3章 / docs/scenario-structure.md 2〜4章)
##
## 12/23〜12/29 を「日×時間帯」の行動枠として扱い、
## 行動選択画面 → 選んだ調査イベントのラベルへ call → 終了後この画面に戻る、
## というハブ&スポーク構造で進行する。12/29の行動枠を使い切ると
## クライマックス(哲学堂公園の儀式 / endings.rpy)へ合流する。
##
## イベント本文はチェーンごとに chapter2_yuki.rpy / chapter2_lens.rpy /
## chapter2_riku.rpy / chapter2_sign.rpy / chapter2_endo.rpy、
## 育成コマンドと暗殺襲撃は chapter2_events.rpy にある。
## イベントを追加するときは、本文のラベルを書き、下の EVENTS に1件追加する。

## 進行状態(セーブ対象)
default day_index = 0        # CALENDAR のインデックス
default slot_index = 0       # その日の時間帯インデックス
default events_done = set()  # 消化済みイベントID
default picked_event = None  # 直前に選択したイベントID
default briefed_days = set() # 朝のニュースを表示済みの日

init python:

    ## 行動可能期間。12/29の夜(21:00)は儀式のため行動枠に含めない。
    CALENDAR = [
        ("12月23日(金)", ["昼", "夕方", "夜"]),   # day 0
        ("12月24日(土)", ["昼", "夕方", "夜"]),   # day 1
        ("12月25日(日)", ["昼", "夕方", "夜"]),   # day 2
        ("12月26日(月)", ["昼", "夕方", "夜"]),   # day 3
        ("12月27日(火)", ["昼", "夕方", "夜"]),   # day 4
        ("12月28日(水)", ["昼", "夕方", "夜"]),   # day 5
        ("12月29日(木)", ["昼", "夕方"]),         # day 6
    ]

    class InvestigationEvent(object):
        """行動選択画面に並ぶ調査イベント1件分の定義。

        id         : イベントID(events_done への記録・ラベル解決に使う)
        name       : 行動選択画面に表示する行動名
        label      : call されるラベル名
        min_day    : 出現開始日(CALENDARのインデックス)。None なら初日から
        max_day    : 出現最終日(同上)。None なら最終日まで。タイムリミット表現に使う
        slots      : 出現する時間帯のタプル。None なら全時間帯
        dates      : 出現する日付文字列のタプル(特定日限定の「窓」イベント用)
        requires   : 前提イベントIDのタプル(すべて消化済みで出現)
        visible_if : 追加の出現条件(引数なしの callable)。OR条件や変数条件に使う
        req        : 解放条件(引数なしの callable)。None なら常時解放。未達なら灰色表示
        req_text   : 条件未達のときにボタンへ添える説明
        repeatable : True なら何度でも選べる(育成コマンド用)
        """

        def __init__(self, id, name, label, min_day=None, max_day=None,
                     slots=None, dates=None, requires=None, visible_if=None,
                     req=None, req_text="", repeatable=False):
            self.id = id
            self.name = name
            self.label = label
            self.min_day = min_day
            self.max_day = max_day
            self.slots = slots
            self.dates = dates
            self.requires = requires
            self.visible_if = visible_if
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
            if self.dates is not None and current_date() not in self.dates:
                return False
            if self.requires is not None:
                for rid in self.requires:
                    if rid not in store.events_done:
                        return False
            if self.visible_if is not None and not self.visible_if():
                return False
            return True

        def unlocked(self):
            """技能値などの解放条件を満たしているか(未達なら灰色表示)。"""
            if self.req is None:
                return True
            return self.req()

    def _done(eid):
        return eid in store.events_done

    ## 調査イベント定義(docs/scenario-structure.md 3章の表に対応)。
    ## 上に並べたものほど行動選択画面の上に表示される。
    EVENTS = [

        ## ---- YUKIチェーン(雪の記憶と保護 / F2) ----
        InvestigationEvent(
            "ev_yuki1", "雪の身元と足取りを調べる", "ev_yuki1",
            req=lambda: skill_check("investigation", 2),
            req_text="探索2で解放"),
        InvestigationEvent(
            "ev_yuki2", "東風谷家を訪ねる(雪と共に)", "ev_yuki2",
            requires=("ev_yuki1",), max_day=0),  # 12/23のみ。12/24朝に全焼する
        InvestigationEvent(
            "ev_yuki2b", "東風谷家の焼け跡を調べる", "ev_yuki2b",
            requires=("ev_yuki1",), min_day=1,
            visible_if=lambda: not _done("ev_yuki2"),
            req=lambda: skill_check("investigation", 4),
            req_text="探索4で解放"),
        InvestigationEvent(
            "ev_yuki3", "Bar「雪国」のエミリアを訪ねる", "ev_yuki3",
            visible_if=lambda: _done("ev_yuki2") or _done("ev_yuki2b")),
        InvestigationEvent(
            "ev_yuki4", "久美啓太の隠れ家を訪ねる", "ev_yuki4",
            visible_if=lambda: _done("ev_yuki2") or _done("ev_yuki2b"),
            req=lambda: _done("ev_yuki3") or skill_check("negotiation", 3),
            req_text="エミリアの紹介 または 交渉3で解放"),
        InvestigationEvent(
            "ev_yuki5", "長江ビルに潜入する", "ev_yuki5",
            requires=("ev_yuki4",),
            req=lambda: skill_check("investigation", 4),
            req_text="探索4で解放"),
        InvestigationEvent(
            "ev_yuki6", "雪を久美の隠れ家に匿う", "ev_yuki6",
            requires=("ev_yuki4",),
            visible_if=lambda: not store.yuki_protected),

        ## ---- LENSチェーン(ムーンレンズ / F1精算の材料) ----
        InvestigationEvent(
            "ev_lens1", "集めた情報からレンズの在処を割り出す", "ev_lens1",
            requires=("ev_yuki5",),
            req=lambda: skill_check("knowledge", 4),
            req_text="知識・オカルト4で解放"),
        InvestigationEvent(
            "ev_lens2", "哲学堂公園を偵察する", "ev_lens2",
            requires=("ev_lens1",),
            req=lambda: skill_check("investigation", 5),
            req_text="探索5で解放"),

        ## ---- RIKUチェーン(間宮凛久 / F3。12/28 21時まで) ----
        InvestigationEvent(
            "ev_riku1", "凛久の監禁場所を突き止める", "ev_riku1",
            max_day=5,
            visible_if=lambda: _done("ev_yuki5") or skill_check("knowledge", 5),
            req=lambda: skill_check("investigation", 3),
            req_text="探索3で解放"),
        InvestigationEvent(
            "ev_riku2", "中西アパートを見張る", "ev_riku2",
            requires=("ev_riku1",), max_day=5,
            req=lambda: skill_check("investigation", 4),
            req_text="探索4で解放"),
        InvestigationEvent(
            "ev_riku3a", "咲耶の不在を突いて凛久を救出する", "ev_riku3a",
            requires=("ev_riku2",), max_day=5,
            visible_if=lambda: not store.riku_rescued,
            req=lambda: skill_check("investigation", 5),
            req_text="探索5で解放"),
        InvestigationEvent(
            "ev_riku3b", "星の知恵派の職員になりすます", "ev_riku3b",
            requires=("ev_riku1",), max_day=5,
            visible_if=lambda: not store.riku_rescued,
            req=lambda: skill_check("negotiation", 5),
            req_text="交渉5で解放"),
        InvestigationEvent(
            "ev_riku3c", "中西アパートへ強行突入する", "ev_riku3c",
            requires=("ev_riku1",), max_day=5,
            visible_if=lambda: not store.riku_rescued,
            req=lambda: skill_check("combat", 6),
            req_text="戦闘6で解放"),
        InvestigationEvent(
            "ev_riku4", "凛久の洗脳を解く", "ev_riku4",
            max_day=5,
            visible_if=lambda: store.riku_rescued and not store.flag_f3_rikuhisa_saved,
            req=lambda: skill_check("knowledge", 5) or (skill_check("knowledge", 3) and store.yuki_memory >= 3),
            req_text="知識・オカルト5 (雪の記憶が完全なら3)で解放"),

        ## ---- SIGNチェーン(死へと誘う印 / F4) ----
        InvestigationEvent(
            "ev_sign1", "古崎堂で「印」の正体を追う", "ev_sign1",
            req=lambda: skill_check("knowledge", 4),
            req_text="知識・オカルト4で解放"),
        InvestigationEvent(
            "ev_sign2", "星の知恵派東京教会に潜入する", "ev_sign2",
            requires=("ev_sign1",),
            visible_if=lambda: not store.sign_data_1,
            req=lambda: skill_check("investigation", 5),
            req_text="探索5で解放"),
        InvestigationEvent(
            "ev_sign3", "解呪資料の残り半分を探す", "ev_sign3",
            visible_if=lambda: store.sign_data_1 and not store.sign_data_2,
            req=lambda: (skill_check("investigation", 5) or skill_check("knowledge", 5)
                         or (_done("ev_endo2") and skill_check("investigation", 4))),
            req_text="探索5 か 知識5 (遠藤家調査済なら探索4)で解放"),
        InvestigationEvent(
            "ev_sign4", "解呪の手順を研究する(半日)", "ev_sign4",
            visible_if=lambda: (store.sign_known and store.sign_data_1
                                and store.sign_data_2 and not store.sign_research_done),
            req=lambda: skill_check("knowledge", 6),
            req_text="知識・オカルト6で解放"),
        InvestigationEvent(
            "ev_sign5", "東京タワーで解呪の儀式を行う", "ev_sign5",
            visible_if=lambda: store.sign_research_done and not store.flag_f4_sign_removed,
            req=lambda: store.yuki_memory >= 3 or store.flag_f3_rikuhisa_saved,
            req_text="「神に近い詠唱者」(記憶の戻った雪 か 凛久)が必要"),

        ## ---- ENDOチェーン(遠藤啓介 / F5・END⑥) ----
        InvestigationEvent(
            "ev_endo1", "「森本蓮司」の経歴を洗う", "ev_endo1",
            req=lambda: skill_check("investigation", 3),
            req_text="探索3で解放"),
        InvestigationEvent(
            "ev_endo2", "遠藤家を調べる", "ev_endo2",
            requires=("ev_endo1",),
            req=lambda: skill_check("investigation", 4),
            req_text="探索4で解放"),
        InvestigationEvent(
            "ev_endo2b", "遠藤菫に会いに行く", "ev_endo2b",
            requires=("ev_endo1",),
            dates=("12月25日(日)", "12月26日(月)"), slots=("昼",),
            req=lambda: skill_check("negotiation", 3),
            req_text="交渉3で解放"),
        InvestigationEvent(
            "ev_endo3", "遠藤研究所の最深部へ", "ev_endo3",
            requires=("ev_endo2",),
            req=lambda: skill_check("investigation", 4),
            req_text="探索4で解放"),
        InvestigationEvent(
            "ev_endo4", "墓地で「森本蓮司」を張り込む", "ev_endo4",
            requires=("ev_endo1",), slots=("夜",),
            visible_if=lambda: not store.endo_identified,
            req=lambda: skill_check("investigation", 4),
            req_text="探索4で解放"),
        InvestigationEvent(
            "ev_endo5", "奥多摩の別荘で遠藤啓介と対峙する", "ev_endo5",
            requires=("ev_endo2",), min_day=4,
            visible_if=lambda: not (store.flag_f5_endo_stopped or store.flag_endo_route),
            req=lambda: (skill_check("negotiation", 5) or skill_check("combat", 6)
                         or (store.sumire_trust and skill_check("negotiation", 4))),
            req_text="交渉5 か 戦闘6 (菫の信頼があれば交渉4)で解放"),

        ## ---- 育成コマンド(繰り返し可) ----
        InvestigationEvent(
            "ev_library", "図書館・古書店で資料を漁る(知識+1)", "ev_library",
            slots=("昼",), repeatable=True),
        InvestigationEvent(
            "ev_kikikomi", "繁華街で聞き込みをする(探索+1)", "ev_kikikomi",
            repeatable=True),
        InvestigationEvent(
            "ev_office", "瑞名の事務所で情報を整理する(交渉+1)", "ev_office",
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
        ypadding 24

        vbox:
            spacing 8

            label "[game_date]　[game_time]"

            $ slots_left = remaining_slots()
            text "儀式(12/29 夜)まで、残り行動枠 [slots_left]" size 22

            null height 6

            text "この時間、どう動く？"

            null height 4

            ## GUIテンプレート未導入のフォールバックでは scrollbars 付き viewport が
            ## 描画されないため、素の viewport(ホイール/ドラッグスクロール)を使う
            viewport:
                xsize 1000
                ysize 430
                mousewheel True
                draggable True

                vbox:
                    spacing 2
                    for ev in visible_events():
                        if ev.unlocked():
                            textbutton ev.name action Return(ev.id) text_size 24
                        else:
                            textbutton "[ev.name]　※[ev.req_text]" sensitive False text_size 24


label calendar_start:

    $ sync_calendar_time()

    scene bg black
    with dissolve

    "――ここから12月29日の夜までは、日々の行動を自分で選んで過ごすことになる。"

    "限られた行動枠の中で、どの技能を伸ばし、どの手がかりを追うか。その積み重ねが、結末を決める。"

    jump calendar_hub


label calendar_hub:

    ## SAN枯渇は即、早期離脱エンド(⑦)
    if san <= 0:
        jump ending_07_early_exit

    ## 暗殺カウンタが閾値を超えていれば襲撃イベント(END⑦の追加トリガー)
    if assassination_pending:
        $ assassination_pending = False
        call ev_assassination from _call_assassination

    ## 行動枠を使い切ったらクライマックスへ
    if calendar_finished():
        jump climax_ritual

    $ sync_calendar_time()

    ## その日最初の行動枠では、朝のニュース(世界の進行・締切警告)を挟む
    if slot_index == 0 and day_index not in briefed_days:
        $ briefed_days.add(day_index)
        call calendar_day_brief from _call_day_brief

    call screen action_select

    $ picked_event = _return

    call expression event_label(picked_event) from _call_investigation_event

    $ finish_event(picked_event)

    jump calendar_hub


## 朝のニュース。世界はプレイヤーと無関係に進行する(scenario-structure.md 2章)。
label calendar_day_brief:

    scene bg street_night
    with dissolve

    if day_index == 0:

        "◆ 12月23日(金) 朝のニュース"

        "「――昨日中野区で発生したガス爆発は、死者9名、負傷者多数。警察は事故と事件の両面で捜査を……」"

        "そして、瑞名慧と連絡が取れない。昨日「警視庁で面談がある」と言っていたきり、電話は留守電に繋がるだけだ。"

        "（……嫌な予感がする。だが今は、[first_person]にできることをやるしかない）"

    elif day_index == 1:

        "◆ 12月24日(土) 朝のニュース"

        "「――昨日15時30分頃、警視庁で爆発が発生。テロの可能性が高いと見られています。また、今朝未明には渋谷区の住宅街で火災があり、住宅1棟が全焼……」"

        if "ev_yuki2" in events_done:
            "映像に映る焼け跡は――東風谷家だ。昨日のうちに調べておいて、本当に良かった。"
            "隣で画面を見つめる雪の肩が、小さく震えていた。"
        else:
            "映像に映る焼け跡の住所に、[first_person]は青ざめた。――東風谷家だ。"
            "調べる前に、家が失われてしまった。雪はただ黙って、画面を見つめていた。"

    elif day_index == 2:

        "◆ 12月25日(日) クリスマス"

        "「――本日、光山大学では創立60周年の一般記念公開が行われます。また品川の大聖堂では、大規模な礼拝が予定されており……」"

        "浮かれた街の空気の下で、何かが静かに進行している。"

    elif day_index == 3:

        "◆ 12月26日(月) 朝のニュース"

        "「――昨日、光山大学の記念公開で殺傷事件が発生し、イベントは中止。また政府は、米国からの最新鋭装備の受け入れを本日行うと発表……」"

        "国までもが、何かに備えて動き始めている。"

    elif day_index == 4:

        "◆ 12月27日(火) 朝のニュース"

        "「――横須賀の米軍基地に、2つの空母打撃群が入港しました。防衛省は日米安保条約に基づく通常の運用と説明していますが……」"

        "残された時間は、あと2日。"

    elif day_index == 5:

        "◆ 12月28日(水) 朝のニュース"

        "「――都内で続発している連続通り魔事件、昨夜も代々木で新たな被害者が……」"

        if riku_located and not riku_rescued:
            "（今日の21時。それが、間宮凛久を取り戻せる最後の刻限だ）"
        elif riku_rescued and not flag_f3_rikuhisa_saved:
            "（凛久の洗脳を解けるのは、今日の21時まで。急がなければ）"

    elif day_index == 6:

        "◆ 12月29日(木) 決戦の日"

        "「――お台場の大規模イベントの影響で、交通機関に乱れが……」"

        "街はいつも通りの顔をしている。だが今夜21時、哲学堂公園で全てが決まる。"

        "（使える時間は、あと昼と夕方の2枠だけだ）"

    return
