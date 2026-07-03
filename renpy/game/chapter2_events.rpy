## 調査イベント本文(フェーズ2用プレースホルダー)
##
## calendar.rpy の EVENTS から call される各イベントのラベル。
## 現在はシステム骨格の動作確認用の仮テキスト。フェーズ2のシナリオ執筆で
## このファイルの各ラベルを本文に差し替える(ラベル名とreturnの構造は維持すること)。

## ---------------------------------------------------------------
## フラグ獲得イベント(1回限り)
## ---------------------------------------------------------------

label ev_moonlens:

    scene bg park_night
    with dissolve

    "【行動: 哲学堂公園で「ムーンレンズ」を探る】"

    "（プレースホルダー）夜の哲学堂公園。磨き上げた探索技能を頼りに、儀式の要となる月長石のレンズ――「ムーンレンズ」の在処を突き止め、奪取に成功した。"

    "これで、12月29日の儀式は本来の形では成立しないはずだ。"

    $ set_flag("flag_f1_moonlens", "F1: ムーンレンズ奪取")

    $ change_san(-3)

    "（……あれを持っているだけで、背筋の奥が冷える）"

    return


label ev_yuki_hideout:

    scene bg alley
    with dissolve

    "【行動: 雪を安全な場所へ匿う】"

    "（プレースホルダー）追手の目をかいくぐり、東風谷雪を信頼できる保護先へ移すことができた。"

    "これで彼女が「儀式」に連れ戻される危険は、ひとまず遠のいた。"

    $ set_flag("flag_f2_yuki_saved", "F2: 東風谷雪 救出")

    $ change_relationship("yuki", 2)

    return


label ev_rikuhisa:

    scene bg street_night
    with dissolve

    "【行動: 間宮凛久を説得する】"

    "（プレースホルダー）雪の親友、間宮凛久。教団に囚われ、洗脳された彼女のもとへたどり着き、粘り強く言葉を重ねた。"

    "虚ろだった瞳に、わずかに光が戻る。……間に合った。"

    $ set_flag("flag_f3_rikuhisa_saved", "F3: 間宮凛久 救出")

    $ change_relationship("rikuhisa", 2)

    $ change_san(-3)

    return


label ev_sign:

    scene bg library
    with dissolve

    "【行動: 「死へと誘う印」の解呪法を調べる】"

    "（プレースホルダー）禁断の文献を読み解き、ナイ牧師の切り札「死へと誘う印」を無効化する手順を突き止めた。"

    "ページをめくるたび、頭の芯が軋むような感覚がした。知るべきでないことを、知ってしまった代償だ。"

    $ change_san(-5)

    $ set_flag("flag_f4_sign_removed", "F4: 死へと誘う印 解除")

    return


label ev_endo_dialogue:

    scene bg office
    with dissolve

    "【行動: 遠藤啓介と対峙する】"

    "（プレースホルダー）すべての糸を引く男、遠藤啓介。彼はこちらを一瞥すると、静かに語り始めた――自らの正体と、「IDE2.0計画」の真意を。"

    endo "……ここまで辿り着いたのは、君たちが初めてだ。それで、どうする？"

    menu:

        "彼の野望を、ここで止める":

            "（プレースホルダー）対話と駆け引きの末、[first_person]は遠藤啓介の計画を放棄させることに成功した。"

            $ set_flag("flag_f5_endo_stopped", "F5: 遠藤啓介の野望阻止")

        "彼の「真意」に、最後まで耳を傾ける":

            "（プレースホルダー）[first_person]は、彼の語る人類の未来図を、否定も肯定もせずに聞き届けた。"

            "――この選択は、誰も知らない結末へと繋がっていく。"

            $ set_flag("flag_endo_route", "特殊ルート: 遠藤啓介との対話")

    $ change_san(-3)

    return


## ---------------------------------------------------------------
## 育成コマンド(繰り返し可)
## ---------------------------------------------------------------

label ev_library:

    scene bg library
    with dissolve

    "【行動: 図書館・古書店で資料を漁る】"

    "（プレースホルダー）失踪事件の記録、郷土史、そして胡乱なオカルト文献。積み上げた資料の中から、いくつかの符合を拾い上げた。"

    $ gain_skill("knowledge")

    return


label ev_kikikomi:

    scene bg street_night
    with dissolve

    "【行動: 繁華街で聞き込みをする】"

    "（プレースホルダー）人混みに紛れ、夜の街を歩き回る。黒いコートの男たちの目撃談、妙な集会の噂――足で稼いだ情報が、少しずつ地図を埋めていく。"

    $ gain_skill("investigation")

    return


label ev_office:

    scene bg office
    with dissolve

    "【行動: 探偵事務所で瑞名と情報を整理する】"

    "（プレースホルダー）玲紀探偵事務所のホワイトボードに、集めた情報を並べていく。瑞名との議論の中で、人から話を引き出すコツも盗んでいく。"

    $ gain_skill("negotiation")

    $ change_relationship("mizuna", 1)

    return


label ev_training:

    scene bg campus
    with dissolve

    "【行動: 護身の心得を仕込んでもらう】"

    "（プレースホルダー）瑞名の伝手で、身のこなしと護身術の基礎を叩き込まれる。荒事は御免だが、備えは必要だ。"

    $ gain_skill("combat")

    return


label ev_rest:

    scene bg black
    with dissolve

    "【行動: 休息をとる】"

    "（プレースホルダー）何もしない時間を、意識的に作る。温かい食事と睡眠が、すり減った心を少しだけ元に戻してくれる。"

    $ change_san(5)

    return
