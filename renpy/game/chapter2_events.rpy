## 育成コマンド(繰り返し可)と、暗殺カウンタの襲撃イベント
## メインチェーンの本文は chapter2_yuki / lens / riku / sign / endo .rpy を参照。

label ev_library:

    scene bg library
    with dissolve

    "【図書館・古書店で資料を漁る】"

    "失踪事件の記録、郷土史、そして胡乱なオカルト文献。積み上げた資料の中から、いくつかの符合を拾い上げた。"

    $ gain_skill("knowledge")

    return


label ev_kikikomi:

    scene bg street_night
    with dissolve

    "【繁華街で聞き込みをする】"

    "人混みに紛れ、夜の街を歩き回る。黒いコートの男たちの目撃談、妙な集会の噂――足で稼いだ情報が、少しずつ地図を埋めていく。"

    $ gain_skill("investigation")

    return


label ev_office:

    scene bg office
    with dissolve

    "【瑞名の事務所で情報を整理する】"

    if "ev_yuki4" in events_done:
        "主のいない玲紀探偵事務所で、ホワイトボードに集めた情報を並べていく。瑞名の残したメモの書き方を追ううち、人から話を引き出す組み立てが身についていく。"
    else:
        "玲紀探偵事務所のホワイトボードに、集めた情報を並べていく。……瑞名は、まだ戻らない。彼の残した調査ノートが、無言の師匠だった。"

    $ gain_skill("negotiation")

    return


label ev_training:

    scene bg campus
    with dissolve

    "【護身の心得を仕込んでもらう】"

    "瑞名の伝手で紹介された道場で、身のこなしと護身術の基礎を叩き込まれる。荒事は御免だが、備えは必要だ。"

    $ gain_skill("combat")

    return


label ev_rest:

    scene bg black
    with dissolve

    "【休息をとる】"

    "何もしない時間を、意識的に作る。温かい食事と睡眠が、すり減った心を少しだけ元に戻してくれる。"

    $ change_san(5)

    return


## ---------------------------------------------------------------
## 暗殺襲撃イベント(END⑦の追加トリガー / scenario-structure.md 7章)
## add_heat() で注意度が閾値を超えると、calendar_hub から call される。
## 行動枠は消費しない。敗北すると早期離脱エンドへ直行する。
## ---------------------------------------------------------------

label ev_assassination:

    scene bg alley
    with dissolve

    "【襲撃】"

    "その夜、人気のない路地に入った瞬間——空気が変わった。"

    "前方にひとり。背後にふたり。足音を消した人影が、ゆっくりと距離を詰めてくる。フードの下に覗くのは、聖歌隊の徽章。"

    "（SAN48——踏み込みすぎた代償が、来た）"

    $ change_san(-2)

    menu:

        "迎え撃つ":

            if skill_check("combat", 4):

                "[first_person]は先手を取った。最初のひとりの懐に飛び込み、奪ったナイフで残るふたりを牽制する。"

                "拮抗は数秒。暗殺者たちは深追いを嫌い、闇に溶けるように退いていった。"

                $ assassination_heat = 1

                "（……凌いだ。だが次は、この人数では済まないかもしれない）"

            else:

                "[first_person]は必死に応戦した。だが、相手は殺しの訓練を積んだプロだった。"

                "視界が反転する。冷たいアスファルト。遠のく意識の中、澄んだ歌声のようなものが聞こえた気がした。"

                ## call されたラベル内からエンディングへ抜けるため、戻り先を破棄する
                $ renpy.pop_call()
                $ early_exit_cause = "assassin"

                jump ending_07_early_exit

        "全力で逃げる":

            if skill_check("investigation", 5):

                "頭に叩き込んだ路地の地図が、[first_person]を救った。"

                "フェンスを越え、飲み屋の厨房を突っ切り、人混みの中へ——気配が完全に消えるまで走り続けた。"

                $ assassination_heat = 1

                "（撒いた……。当分は、裏道を変えて動かないと）"

            else:

                "走った。だが、彼らのほうが速かった。"

                "行き止まりの壁。振り返った[first_person]の首筋に、鋭い痛み。クラーレの痺れが広がっていく。"

                ## call されたラベル内からエンディングへ抜けるため、戻り先を破棄する
                $ renpy.pop_call()
                $ early_exit_cause = "assassin"

                jump ending_07_early_exit

    return
