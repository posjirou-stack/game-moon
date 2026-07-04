## RIKUチェーン — 間宮凛久の救出(F3。タイムリミット 12/28 21:00)
## docs/scenario-structure.md 3.3章に対応。
## 救出手段は3択(3a隠密/3b偽装/3c強行)。いずれかで riku_rescued、ev_riku4でF3成立。

label ev_riku1:

    scene bg street_night
    with dissolve

    "【凛久の監禁場所を突き止める】"

    "「中野ヒカリエビルから、応急的に別の施設へ移送」——資料にあったその“施設”を、[first_person]は追った。"

    "教団のフロント企業の物件記録、深夜の物資搬入の目撃談、そして「行政上は無人のはずのアパート」。"

    "――金町駅から徒歩15分。中西アパート。古びた5階建てのそこだけが、夜も“気配”を消しきれていない。"

    $ riku_located = True
    $ gain_skill("investigation")

    if yuki_memory >= 3:
        "（雪の記憶とも一致する。……凛久はあそこだ。だが焦るな。あの手の施設に、丸腰で踏み込めば終わりだ）"
    else:
        "（状況証拠は揃った。……凛久はあそこにいる。だが、確実にやるなら下調べが要る）"

    "刻限は12月28日の21時。それを過ぎれば、洗脳教育は「完了」する。"

    return


label ev_riku2:

    scene bg apartment
    with dissolve

    "【中西アパートを見張る】"

    "廃墟を装ったアパートを、[first_person]は離れた場所から観察し続けた。"

    "出入りする人影は少ない。だが規則性がある。毎日12時から13時、中肉中背の男——星の知恵派の“秘書”岡本志郎が様子を見に来る。"

    "そして、フードを目深に被った小柄な少女。彼女が出かけるのは決まって“あの予定表”の時刻の前後——連続通り魔事件の、実行時刻だ。"

    $ change_san(-2)

    "（伊東咲耶。SAN48のリーダーにして、凛久の“世話係”……。彼女が暗殺任務で施設を空ける前後2時間、監視は最も薄くなる）"

    if "assassin_list" not in archive_items:
        $ add_archive("assassin_list")
        "張り込みの間に盗み見た搬入伝票と移動記録から、[first_person]は彼女の“予定表”を再構成した。"

    $ riku_scouted = True
    $ gain_skill("investigation")

    "（搬入ルート、監視カメラの配置、咲耶の不在時間。……救い出す道筋が見えた）"

    return


label ev_riku3a:

    scene bg apartment
    with dissolve

    "【咲耶の不在を突いて凛久を救出する】"

    "決行は、伊東咲耶が“任務”で施設を離れる時間帯。"

    "搬入口から地下へ。監視カメラの死角を縫い、息を殺して進む。広大な地下空間——射撃場、訓練場、そして病院を模した一角。"

    $ change_san(-2)

    "洗脳室の奥の小部屋に、その少女はいた。写真の中で雪と笑っていた少女——間宮凛久。"

    show riku blank
    with dissolve

    rikuhisa "……あなた、だれ？　咲耶ちゃんじゃ、ない。"

    "虚ろな瞳。だが押し問答をする時間はない。[first_person]は用意していた強力な睡眠導入剤を使い、眠った彼女を毛布ごと担ぎ上げた。"

    "警報が鳴り響く前に、来た道を戻る。搬入トラックの陰、フェンスの破れ目、そして夜の路地へ――。"

    $ riku_rescued = True
    $ gain_skill("investigation")
    $ change_relationship("rikuhisa", 1)

    "（連れ出した。……だが、これで終わりじゃない。彼女の心は、まだ奴らの檻の中だ）"

    return


label ev_riku3b:

    scene bg apartment
    with dissolve

    "【星の知恵派の職員になりすます】"

    "教団の資料から拾い上げた内部用語、階級、そして“合言葉”。[first_person]はそれらを頭に叩き込み、正面から中西アパートの敷居を跨いだ。"

    "「本部の指示だ。移送計画の前倒しで、対象の状態確認に来た」"

    "監視役の男は疑わしげに[first_person]を睨んだが——淀みなく続く専門用語と、堂々とした態度に、やがて道を開けた。"

    $ change_san(-2)

    "洗脳室の奥。間宮凛久は、抵抗しなかった。"

    show riku blank
    with dissolve

    rikuhisa "……教団の、命令なんですね。わかりました。凛久、ついていきます。"

    "従順に頷くその姿が、かえって胸を抉った。彼女の意思は、命令の前では無いに等しいのだ。"

    "[first_person]は「移送」の名目で、彼女を堂々と連れ出した。"

    $ riku_rescued = True
    $ gain_skill("negotiation")
    $ change_relationship("rikuhisa", 1)

    "（誰も傷つけずに済んだ。……だが本当の勝負は、彼女の洗脳を解くことだ）"

    return


label ev_riku3c:

    scene bg apartment
    with dissolve

    "【中西アパートへ強行突入する】"

    "時間がない。[first_person]は迷いを捨て、正面から扉を蹴破った。"

    "警報。怒号。防護服に身を包んだSAN48の暗殺者たちが、神経ガスの噴射器を手に殺到してくる。"

    $ change_san(-3)

    "鍛え上げた体術で最初の2人を沈め、奪ったガスマスクで毒煙を凌ぎ、地下への階段を駆け下りる。"

    "洗脳室の扉をこじ開けた、その瞬間——"

    rikuhisa "……敵、ですね。"

    "間宮凛久の姿が、部屋の奥の“歪んだ空間”へ吸い込まれかけた。門だ。逃げられる――！"

    if yuki_memory >= 3:
        "咄嗟に、[first_person]は雪から預かっていた言葉を叫んだ。"
        m "――「ゆきりん」！　雪が、そう呼んでいいのは自分だけだって言ってたぞ！"
        rikuhisa "…………ゆき、ちゃん……？"
        "門の縁で、凛久の足が止まった。その一瞬の隙に、[first_person]は彼女の腕を掴んで引き戻した。"
    else:
        "間一髪、[first_person]は閉じかけた門の縁から、力ずくで彼女を引き戻した。腕に、焼けるような痛みが走る。"
        $ change_san(-2)

    "暴れる彼女を抱えたまま、[first_person]は炎と警報の中を突破した。"

    $ riku_rescued = True
    $ gain_skill("combat")
    $ change_relationship("rikuhisa", 1)
    $ add_heat(2)

    "（強引すぎたか……。だが、取り戻した。あとは彼女の心だ）"

    return


label ev_riku4:

    scene bg basement
    with dissolve

    "【凛久の洗脳を解く】"

    "久美の地下室に匿った凛久は、静かだった。静かすぎた。"

    show riku blank
    with dissolve

    rikuhisa "内側に存在するこの世界を外宇宙へ、あるべき場所へ回帰し、この崩壊寸前の世界原理を破壊しないといけないのだよ？　……大丈夫？"

    "口をつくのは、教え込まれた“経典”ばかり。彼女の目は、[first_person]たちの向こう側の何かを見ている。"

    if yuki_memory >= 3:

        "だが——こちらには、切り札がいた。"

        show yuki sad at left
        with dissolve

        yuki "……りくちゃん。わたしだよ。ゆきだよ。"

        "匿われていた雪が、凛久の手を握る。長江ビルの記憶、吹奏楽の記憶、ふたりで交わした他愛ない約束——雪は、ひとつひとつ言葉にして積み上げていく。"

        yuki "一緒に帰ろう。また、一緒に吹こう？　ね、りくちゃん。"

        rikuhisa "…………ゆき……ちゃ……"

        "凛久の瞳から、ぽろぽろと涙がこぼれた。長い長い夜が、明け始めた瞬間だった。"

    else:

        "[first_person]は文献の知識を総動員し、久美の助力を借りて、幾晩分にも思える対話を重ねた。"

        "教団の“経典”の矛盾を突き、彼女自身の記憶——吹奏楽、コンクール、金賞の写真——を、少しずつ呼び覚ましていく。"

        rikuhisa "……わたし……そうだ、わたし、コンクールで……ゆきちゃんと……"

        "虚ろだった瞳に、ゆっくりと光が戻っていく。"

    $ change_san(-3)
    $ set_flag("flag_f3_rikuhisa_saved", "F3: 間宮凛久 救出")
    $ change_relationship("rikuhisa", 2)
    $ change_relationship("yuki", 1)

    "――間に合った。12月28日21時の刻限より、早く。"

    show riku normal

    rikuhisa "……ありがとう、ございます。わたし、覚えてます。ぜんぶ。……あの人たちのことも、“あの場所”のことも。"

    "凛久は涙を拭うと、まっすぐに[first_person]を見た。それは、依代でも人形でもない、ひとりの少女の目だった。"

    return
