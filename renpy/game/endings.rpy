## クライマックス(12/29 儀式)とエンディング判定・7エンディングの骨格
## (要件定義書 5.2章のエンディング表に対応)
##
## 分岐条件はここで一元管理する。各エンディングの本文はフェーズ3で執筆するため、
## 現在は到達確認用のプレースホルダー(タイトル+概要)のみ。

## エンディング回収状況(周回をまたいで保持される)。タイトル画面の「事件簿」で使う予定。
default persistent.endings_seen = set()

init python:

    ENDING_TITLES = {
        "01": "① 真エンド「大団円」",
        "02": "② グッドエンド「勝利と代償」",
        "03": "③ ノーマルエンド「黒幕を止められず」",
        "04": "④ 限定的破滅エンド",
        "05": "⑤ 真バッドエンド「東京壊滅」",
        "06": "⑥ 特殊エンド「遠藤啓介ルート」",
        "07": "⑦ 早期離脱エンド",
    }

    def determine_ending():
        """フラグF1〜F5から到達エンディングのラベル名を返す(5.2章の表を実装)。

        ⑦早期離脱(SAN枯渇)はここに来る前に calendar_hub が直接分岐する。
        ⑥特殊エンドは対話イベントでの明示的な選択(flag_endo_route)を最優先する。
        """
        if store.flag_endo_route:
            return "ending_06_endo"
        if store.flag_f1_moonlens:
            if store.flag_f5_endo_stopped:
                if store.flag_f2_yuki_saved and store.flag_f3_rikuhisa_saved:
                    return "ending_01_true"
                return "ending_02_good"
            return "ending_03_normal"
        if store.flag_f4_sign_removed:
            return "ending_04_limited"
        return "ending_05_worst"

    def record_ending(code):
        """エンディング到達を周回をまたいで記録する。"""
        if persistent.endings_seen is None:
            persistent.endings_seen = set()
        persistent.endings_seen.add(code)


label climax_ritual:

    $ advance_time("12月29日(木)", "夜")

    scene bg park_night
    with dissolve

    "◆ 12月29日(木) 21:00　哲学堂公園"

    "冬の夜気が張り詰める哲学堂公園に、低い詠唱の声が満ちていく。"

    "――シュブ＝ニグラス降臨の儀式が、始まろうとしていた。"

    scene bg ritual
    with dissolve

    ## ここまでの行動の成果を確認する(フェーズ3で本格的な儀式シーンに差し替える)
    if flag_f1_moonlens:
        "だが、儀式の要「ムーンレンズ」は[first_person]たちの手の中にある。祭壇の中心で、ナイ牧師の表情が初めて歪んだ。"
    else:
        "祭壇の中心には、月光を集めて輝く「ムーンレンズ」。……奪えなかった。儀式は、完成へと向かっていく。"

    if flag_f4_sign_removed:
        "ナイ牧師の切り札「死へと誘う印」は、すでに解呪の手順を踏んである。"

    if flag_f2_yuki_saved:
        "東風谷雪は、安全な場所にいる。少なくとも彼女が祭壇に立たされることはない。"

    if flag_f3_rikuhisa_saved:
        "洗脳を解かれた間宮凛久も、カルティストの列にはいない。"

    "【プレースホルダー】儀式クライマックスの本文はフェーズ3で執筆されます。ここまでの行動の結果から、結末が導かれます――"

    jump expression determine_ending()


## ---------------------------------------------------------------
## 7エンディング(現在は到達確認用プレースホルダー)
## ---------------------------------------------------------------

label ending_01_true:

    $ record_ending("01")

    scene bg black
    with dissolve

    centered "ENDING　① 真エンド「大団円」"

    "（プレースホルダー）儀式は阻止され、雪も凛久も生還した。遠藤啓介の野望は潰え、教団は壊滅。東京に、静かな年の瀬が戻ってくる。"

    jump ending_epilogue


label ending_02_good:

    $ record_ending("02")

    scene bg black
    with dissolve

    centered "ENDING　② グッドエンド「勝利と代償」"

    "（プレースホルダー）儀式は止めた。黒幕の野望も阻んだ。……それでも、救えなかった人がいる。勝利の味は、ひどく苦い。"

    jump ending_epilogue


label ending_03_normal:

    $ record_ending("03")

    scene bg black
    with dissolve

    centered "ENDING　③ ノーマルエンド「黒幕を止められず」"

    "（プレースホルダー）儀式そのものは阻止された。だが遠藤啓介は目的を諦めることなく、静かに日本を去った。「IDE2.0計画」は、まだ終わっていない。"

    jump ending_epilogue


label ending_04_limited:

    $ record_ending("04")

    scene bg black
    with dissolve

    centered "ENDING　④ 限定的破滅エンド"

    "（プレースホルダー）ムーンレンズは奪えず、儀式は決行された。それでも「死へと誘う印」を解除していたことで、最悪の被害だけは免れた。……これは敗北か、それとも。"

    jump ending_epilogue


label ending_05_worst:

    $ record_ending("05")

    scene bg black
    with dissolve

    centered "ENDING　⑤ 真バッドエンド「東京壊滅」"

    "（プレースホルダー）月が、割れるように輝いた。シュブ＝ニグラスは降臨し、関東3000万の魂が贄となる。ナイ牧師の望んだ世界が、ここに始まる。"

    jump ending_epilogue


label ending_06_endo:

    $ record_ending("06")

    scene bg black
    with dissolve

    centered "ENDING　⑥ 特殊エンド「遠藤啓介ルート」"

    "（プレースホルダー）彼の語った未来を、[first_person]は聞き届けてしまった。人類の変容――それを引き留めるのか、見送るのか。答えは、まだ[first_person]の手の中にある。"

    jump ending_epilogue


label ending_07_early_exit:

    $ record_ending("07")

    scene bg black
    with dissolve

    centered "ENDING　⑦ 早期離脱エンド"

    "（プレースホルダー）心が、限界を迎えた。深淵を覗きすぎた者の意識は昏い水底へと沈み、[first_person]の「探索」はここで終わる。"

    jump ending_epilogue


## エンディング共通の締め。周回プレイへの導線。
label ending_epilogue:

    $ hud_visible = False

    $ endings_count = len(persistent.endings_seen)

    "【エンディング到達】この周回はここまでです。"

    "エンディング回収状況: [endings_count] / 7"

    "別の技能を伸ばし、別の選択をすれば、違う結末に辿り着けるかもしれません。"

    return
