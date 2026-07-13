## クライマックス(12/29 儀式)とエンディング判定・7エンディング本文
## (要件定義書 5.2章 / docs/scenario-structure.md 5・7章)
##
## 分岐条件はここで一元管理する。F1・F2はクライマックス冒頭で進行変数から精算される。

## エンディング回収状況(周回をまたいで保持される)。タイトル画面の「事件簿」で使う。
default persistent.endings_seen = set()

## END⑦の到達原因("san"=正気度枯渇 / "assassin"=暗殺)
default early_exit_cause = None

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

        ⑦早期離脱(SAN枯渇・暗殺)はここに来る前に直接分岐する。
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

    def compute_f1():
        """F1(ムーンレンズ奪取)の精算(scenario-structure.md 3.2章)。

        「所在の情報」「戦術的な優位」「異空間への鍵(女神個体)」の3点が揃って成立する。
        """
        if not store.lens_located:
            return False
        advantage = (store.lens_route or store.arsenal_destroyed
                     or len(store.allies) >= 2)
        if not advantage:
            return False
        key = (store.yuki_memory >= 3) or store.flag_f3_rikuhisa_saved
        return key


## ===============================================================
## クライマックス: 12月29日夜 哲学堂公園
## ===============================================================

label climax_ritual:

    $ advance_time("12月29日(木)", "夜")
    $ play_bgm("ritual")

    ## ここまでの進行変数からF1・F2を精算する
    $ flag_f1_moonlens = compute_f1()
    $ flag_f2_yuki_saved = yuki_protected

    scene bg street_night
    with dissolve

    "◆ 12月29日(木) 夕刻　東京"

    if flag_f4_sign_removed and not flag_f1_moonlens:

        "その日の正午、東京は悲鳴を上げた。"

        "レインボーブリッジ。首都高。地下鉄。同時多発の爆発が交通網を寸断し、報道はテロ一色に染まった。"

        "——満月と新月の教団の仕業だ。生贄の“標”を失った彼らは、囚人の輸送を隠すために、街そのものを混乱させたのだ。"

        $ change_san(-3)

        "（印を解いたことが、奴らを追い詰めた。……それでも、これ以上は好きにさせない）"

    elif flag_f1_moonlens:

        "街は不気味なほど静かだった。クリスマスの残り香と、年の瀬の浮ついた空気。誰も、今夜この街の運命が決まることを知らない。"

    else:

        "街は静かだった。静かなまま、何も知らずに、その時を待っていた。"

    scene bg park_night
    with dissolve

    "◆ 21:00少し前　哲学堂公園"

    "冬の夜気が張り詰める哲学堂公園に、低い詠唱の声が満ちていく。"

    "——シュブ＝ニグラス降臨の儀式が、始まろうとしていた。"

    if flag_f1_moonlens:

        jump climax_assault

    else:

        jump climax_watch


## ---- 突入(F1成立ルート) ----
label climax_assault:

    $ allies_count = len(allies)

    "だが[first_person]たちは、この夜のために全てを積み上げてきた。"

    if len(bonds) >= 3:

        ## 交流イベントの支援描写差分(企画書: 絆はクライマックスの厚みに反映)
        "積み上げてきたのは、情報と戦力だけではなかった。事務所の一杯。屋上の星。閉店後のカクテル。卓を囲んだ夜——この街で交わした時間の分だけ、背中を預けられる顔がある。"

    if allies_count >= 2:
        "手を結んだ[allies_count]つの勢力が、示し合わせたように公園の各所で陽動を開始する。銃声、閃光、怒号——敵の防衛線が、目に見えて薄くなっていく。"
    elif allies_count == 1:
        "数少ない、しかし信頼できる協力者たちが、公園の正面で陽動を開始した。"
    else:
        "頼れる勢力はない。だが敵の目は、20時に襲来した星の知恵派との抗争に釘付けになっていた。その混乱こそが、[first_person]たちの陽動だった。"

    if arsenal_destroyed:
        "武器工場を失った教団の銃火は、驚くほど疎らだった。"

    if lens_route:
        "偵察で掴んだ地下侵入経路——旧防空壕と下水道が、[first_person]たちを公園の心臓部へ導く。"
    else:
        "防衛計画から割り出した搬入路を辿り、[first_person]たちは公園の地下へと潜り込んだ。"

    scene bg ritual
    with dissolve

    "地下中心部。空間が、そこだけ“歪んで”いた。あらゆる直線が曲がって見え、方向感覚が溶けていく。"

    if sumire_gadget:

        ## 独6の実効果: 菫の検知器が「異空間への接近」を教えてくれる
        "懐で、菫の検知器が細く鳴き続けている。この音が“正常な世界”との距離を教えてくれる——感覚が完全に飲まれる前に、自分を繋ぎ止められた。"

        $ change_san(-2)

    else:

        $ change_san(-3)

    if yuki_memory >= 3 and flag_f3_rikuhisa_saved:
        "異空間の“扉”は、雪と凛久——ふたりの女神個体が手を重ねると、静かに口を開けた。"
        yuki "……行きましょう。ここは、わたしたちの“生まれた場所”だから。"
    elif flag_f3_rikuhisa_saved:
        rikuhisa "扉は、凛久が開けます。……あの人たちの神様の力で、あの人たちの終わりを開けるんです。"
        "間宮凛久が指先で虚空に触れると、空間が裂けた。"
    else:
        yuki "手を、離さないでくださいね。"
        "東風谷雪が一歩を踏み出すと、歪みの中心が[first_person]たちを呑み込んだ。"

    "——緑と紫の空。天も地もその色に染まった、外宇宙そのものの空間。"

    "その最奥に、それはあった。高さ15mの鉄塔。頂に花弁のように広がる、13枚の巨大な凸レンズ——ムーンレンズ。"

    "そして祭壇の前に、ふたりの老人が立ちはだかった。満月と新月の教団幹部——博美政景と、猫田金氣。"

    "「ここまで来るか、人の仔よ。だが渡さん。これは我らが“人間に戻る”ための、最後の鍵なのだ」"

    if flag_f3_rikuhisa_saved or yuki_memory >= 3:
        "答えたのは、[first_person]ではなかった。"
        if flag_f3_rikuhisa_saved:
            rikuhisa "……戻れません。神様を呼んでも、あなたたちは戻れない。わたしたちが、その“実験の答え”です。"
        else:
            yuki "……その鍵は、誰のことも救いません。わたしが、証明です。"
        "女神個体の言葉に、老人たちの詠唱が一瞬、揺らいだ。"

    "その隙を、[first_person]は逃さなかった。"

    if skill_check("combat", 5):
        "打ち合いは短かった。老いた狂信者の術より、[first_person]の拳の方が速かった。"
    else:
        "格闘の心得などなくても、拮抗はできる。時間さえ稼げば——レンズに手が届く。"

    "ロープを引き、金具を外し、一枚、また一枚。13枚目のレンズが腕の中に収まった、その瞬間。"

    "——空間の彼方から、この世のものではない咆哮が轟いた。"

    "何か巨大なものが、地を抉りながらこちらへ這い寄ってくる。無数の目に覆われたゼリー状の頭部。大きな歯の並んだ嘴——ムーンレンズの守護者。"

    $ change_san(-4)

    if skill_check("knowledge", 7):

        "だが[first_person]の頭には、あの膨大な文献の知識があった。"

        "床に描かれた紋様——《旧き印》。指でなぞり、掠れた声で詠唱をなぞる。守護者の巨体が、見えない壁に阻まれて軋んだ。"

        "稼いだ時間で、[first_person]たちは“扉”へと駆け抜けた。"

    else:

        "考えるな。走れ。"

        "背後で空間そのものが悲鳴を上げる中、[first_person]たちは転がるように“扉”へ飛び込んだ。"

        $ change_san(-2)

    scene bg park_night
    with dissolve

    "冷たい夜気。土の匂い。——現実の世界だ。"

    "腕の中には、13枚のレンズ。頭上の夜空に、月はまだ、ただの月として輝いていた。"

    "祭壇の中心で、遅れて異変を悟ったナイ牧師の表情が——初めて、歪んだ。"

    "儀式は、失敗した。"

    jump expression determine_ending()


## ---- 断念/失敗(F1不成立ルート) ----
label climax_watch:

    scene bg ritual
    with dissolve

    "[first_person]に、あの公園の心臓部へ踏み込む力はなかった。情報が、味方が、あるいは“扉を開ける鍵”が——足りなかった。"

    "21時。詠唱が最高潮に達する。"

    "20時に公園へ攻め入った星の知恵派は、瞬く間に教団の防衛を食い破り、祭壇を制圧していた。"

    if not riku_rescued:

        "そして祭壇の中央に——白い衣を着せられた少女が立たされていた。"

        "間宮凛久。守れなかった、もうひとりの女神個体。"

        "彼女の虚ろな瞳が月を映し、その唇が、意思のない詠唱を紡いでいく。"

        $ change_san(-4)

    else:

        "祭壇にはナイ牧師が立ち、漆黒の祭服が月光を吸い込んでいた。彼の詠唱は、歌のように、嘆きのように、夜を満たしていく。"

        $ change_san(-3)

    "ムーンレンズが、月光を集めていく。13枚のレンズが白熱し、上空に“もうひとつの満月”が生まれる——"

    jump expression determine_ending()


## ===============================================================
## 7エンディング
## ===============================================================

label ending_01_true:

    $ record_ending("01")

    scene bg black
    with dissolve

    $ play_bgm("ending_good")

    centered "ENDING　① 真エンド「大団円」"

    scene bg office
    with dissolve

    "◆ 12月31日　玲紀探偵事務所"

    if mizuna_rescued:
        mizuna "——以上で、本件は完了だ。報告書はまとめておく。手当は弾んどいたぜ。まったく、とんでもねえ“人捜し”になったもんだ。"
        "憔悴の抜けきらない顔で、それでも瑞名は笑った。地獄のような監禁生活を経てなお、この男の軽口は健在だった。"
    else:
        mizuna "……悪かったな。肝心なところで、全部お前に背負わせちまった。"
        "教団の崩壊とともに解放された瑞名は、深々と頭を下げた。雇い主のそんな姿を見るのは、初めてだった。"

    "満月と新月の教団は解散した。人に戻れなかった者たちは、それでも人を巻き込むことをやめ、静かに散っていったという。"

    "星の知恵派は東京から撤退した。ナイ牧師の消息は杳として知れない。だが、あの夜以降、都内の“連続通り魔事件”はぴたりと止んだ。"

    "バベッジ・ジャパンでは伊藤茂信が失脚し、「IDE2.0」の計画は本社預かりのまま凍結された。"

    if flag_f5_endo_stopped and sumire_trust:
        "そして年の瀬の墓地で、花を抱えた娘と、疲れた顔の父が、十数年ぶりに並んで手を合わせたという。——それを見た者は、[first_person]たちの他にいない。"
    elif flag_f5_endo_stopped:
        "遠藤啓介は、すべての研究データを自らの手で封印した。「君たちが正しかったのかは、まだ分からない。だが、賭けてみることにするよ」——それが、彼の最後の言葉だった。"

    call ending_recovery from _call_recovery_01

    scene bg street_night
    with dissolve

    "◆ 1月1日　未明"

    "初詣の人波から少し外れた神社の石段に、[first_person]と、雪と、凛久がいた。"

    show riku smile at left
    show yuki smile at right
    with dissolve

    rikuhisa "ゆきちゃん、ほら、甘酒。……[mc_call]さんも。"

    yuki "ふふ。……こういうの、ずっと夢に見てた気がします。牢の中で、ずっと。"

    "ふたりの少女は顔を見合わせ、それから同時に、白い息と一緒に笑った。"

    if relationship_yuki >= 8:

        "帰り道、雪はそっと[first_person]の袖を掴んだ。あの夜の路地と、同じ仕草で。——けれどその顔は、もう怯えてはいなかった。"

        yuki "あの夜、助けてって言った相手があなたで、よかった。……ねえ、[mc_call]さん。“運命”って、信じますか？"

        m "……最近、信じるようになったよ。"

        "月が、笑ったように瞬いた気がした。"

    elif relationship_yuki >= 5:

        "帰り道、雪は少し先を歩きながら振り返った。"

        yuki "来年も……ううん、これからも。たまにで、いいですから。……会いに来てくれますか？"

        "その問いに頷くのは、世界を救うよりずっと簡単だった。"

    else:

        "彼女たちを家まで送り届けて、[first_person]の長い長い“アルバイト”は、ようやく終わった。"

    scene bg black
    with dissolve

    "こうして、月夜の物語は幕を下ろす。"

    "——その日、運命に出会った少年の物語は、大団円をもって。"

    jump ending_epilogue


label ending_02_good:

    $ record_ending("02")

    scene bg black
    with dissolve

    $ play_bgm("ending_good")

    centered "ENDING　② グッドエンド「勝利と代償」"

    "儀式は阻止した。黒幕の野望も断った。教団は散り、街は何も知らないまま年を越していく。"

    "——それでも。"

    if not flag_f3_rikuhisa_saved:

        scene bg park_night
        with dissolve

        "あの夜、星の知恵派は撤退の間際、“回収”していった。祭壇に立たせるはずだった、もうひとりの女神個体を。"

        "間宮凛久。写真の中で雪と笑っていた少女に、[first_person]はついに、間に合わなかった。"

        yuki "……りくちゃんは、生きてます。どこかで、きっと。わたしには、分かるんです。"

        "雪はそう言って、涙も見せずに前を向いた。その横顔の強さが、かえって痛かった。"

        "彼女は今も、親友の帰りを待っている。[first_person]も、あの組織の名を、まだ捨てられずにいる。"

    else:

        scene bg alley
        with dissolve

        "守りきれなかったのは——東風谷雪だった。"

        "安全な場所を用意できないまま連れ歩いた彼女を、教団は儀式の前夜、影のように攫っていった。"

        "凛久は還ってきた。街は救われた。だが、あの路地で[first_person]の袖を掴んだ手の温もりだけが——今も、どこにもない。"

        rikuhisa "……ゆきちゃんを、探しましょう。何年かかっても。わたしと、あなたで。"

        "凛久の目に、涙はなかった。あるのは、かつて[first_person]が彼女を取り戻しに行った時と、同じ色の決意だった。"

    call ending_recovery from _call_recovery_02

    scene bg black
    with dissolve

    "勝利の味は、ひどく苦い。"

    "それでも物語は続いていく。欠けた席を取り戻す、次の物語が。"

    jump ending_epilogue


label ending_03_normal:

    $ record_ending("03")

    scene bg black
    with dissolve

    $ play_bgm("ending_good")

    centered "ENDING　③ ノーマルエンド「黒幕を止められず」"

    "儀式は止めた。ムーンレンズは[first_person]たちの手にあり、シュブ＝ニグラスが東京の空に降りることは、ついになかった。"

    scene bg villa
    with dissolve

    "◆ 12月30日　早朝　奥多摩"

    if endo_identified:

        "夜明けの山道を、[first_person]は登っていた。確信があったわけではない。ただ、あの男が最後に立ち寄る場所は、ここしかない気がした。"

        "山頂の岩場に、森本蓮司の姿があった。彼は朝日に向かって、誰にともなく呟いていた。"

        endo "——楓。計画は失敗だ。……いや、“延期”と言うべきかな。"

        "彼は[first_person]に気づくと、逃げも隠れもせず、ただ小さく会釈をした。"

        endo "君たちの勝ちだ、今回はね。だが「IDE2.0」は私と共にある。人類はいずれ、選ばなくてはならない日が来る。……その時まで、元気で。"

        "深紅の輪が朝焼けに溶け、彼の姿は消えた。追う術は、もうなかった。"

    else:

        "後日、光山大学は「森本蓮司教授の退職」を静かに発表した。海外の研究機関に移った、と。"

        "その名前の裏にいた男の正体を、[first_person]が知ることは、この周回ではなかった。"

        "ただ、バベッジ・インコーポレイテッドの株主向け資料の片隅に、こう記されていたという。——「IDE2.0計画は、然るべき時まで延期する」と。"

    call ending_recovery from _call_recovery_03

    scene bg black
    with dissolve

    "街は救われた。少女たちの運命も、選んだ分だけは。"

    "だが真の黒幕は、まだ世界のどこかで“箱舟”の設計図を抱いている。"

    "——この物語には、まだ続きがある。"

    jump ending_epilogue


label ending_04_limited:

    $ record_ending("04")

    scene bg black
    with dissolve

    $ play_bgm("ending_bad")

    centered "ENDING　④ 限定的破滅エンド"

    scene bg ritual
    with dissolve

    "13枚のレンズが白熱し、上空に偽りの満月が生まれ——シュブ＝ニグラスは、降臨した。"

    "だが。"

    "捧げられるはずだった3000万の魂は、そこになかった。[first_person]たちが東京タワーの夜に解いた“標”は、二度と戻らなかったのだ。"

    "生贄なき降臨は、不完全だった。顕現した“それ”は哲学堂公園とその周辺を一夜にして異界に変えたが、それ以上、広がることはなかった。"

    $ change_san(-4)

    scene bg street_night
    with dissolve

    "政府は「中野区ガス爆発による大規模災害」と発表した。犠牲者、行方不明者、あわせて数千名。中野の一部は今も、立入禁止のまま封鎖されている。"

    "SHIELDと米軍が“災害地域”を囲い込み、封じ込めは続いている。人類は、初めての敗北を——けれど滅亡ではない敗北を、喫した。"

    if flag_f2_yuki_saved and flag_f3_rikuhisa_saved:
        "雪と凛久は生きている。あの夜、久美の隠れ家で身を寄せ合っていたふたりは、いま[first_person]と同じ喪失と、同じ安堵を抱えて生きている。"
    elif flag_f2_yuki_saved:
        "雪は生きている。……ただ、封鎖地域の方角を見つめる時間が、日に日に長くなっていく。"
    else:
        "あの封鎖線の内側に、まだ取り戻せていない名前がある。[first_person]はそれを、一日も忘れたことがない。"

    if personal_sign_removed:
        call ending_personal_sign_note from _call_sign_note_04

    call ending_recovery from _call_recovery_04

    scene bg black
    with dissolve

    "これは敗北か。それとも、ぎりぎりの防衛戦だったのか。"

    "答えの出ないまま、封鎖された街の上に、今夜も月が昇る。"

    jump ending_epilogue


label ending_05_worst:

    $ record_ending("05")

    scene bg black
    with dissolve

    $ play_bgm("ending_bad")

    centered "ENDING　⑤ 真バッドエンド「東京壊滅」"

    scene bg ritual
    with dissolve

    "月が、割れるように輝いた。"

    "その瞬間、関東平野のすべての“右手”が、いっせいに怪しく輝きだした。3000万の標。3000万の生贄。"

    $ change_san(-5)

    if not riku_rescued:

        "祭壇の上で、間宮凛久だった“何か”が両腕を広げる。少女の形をした依代に、外なる神が満ちていく。"

        "彼女は最後の一瞬だけ、少女の目に戻って——泣いたように見えた。"

    "シュブ＝ニグラスは、降臨した。"

    "東京が、悲鳴ごと闇に呑まれていく。ナイ牧師は月下で腕を広げ、彼の望んだ世界の産声を聞いている。"

    if flag_f2_yuki_saved:
        "久美の隠れ家の結界が、最後まで雪を守っていたという。——その“最後”が、どれほどの長さだったのかは、誰も知らない。"

    if personal_sign_removed:
        call ending_personal_sign_note from _call_sign_note_05

        "生贄にならなかった魂は、闇の中を歩き続ける。目撃者として。記録者として。——いつか、反撃の日のために。"

    scene bg black
    with dissolve

    "世界各地で、封印されていた“旧きもの”たちが目を覚まし始める。"

    "人類の時代の終わりが、東京から始まった。"

    jump ending_epilogue


label ending_06_endo:

    $ record_ending("06")

    scene bg black
    with dissolve

    $ play_bgm("ending_good")

    centered "ENDING　⑥ 特殊エンド「遠藤啓介ルート」"

    scene bg villa
    with dissolve

    "◆ 12月30日　早朝　奥多摩"

    "すべてが終わった翌朝、[first_person]の携帯に、非通知の着信があった。"

    endo "——別荘にいる。最後の話をしよう。あの夜の“続き”を聞く権利が、君にはある。"

    show endo tired
    with dissolve

    "暖炉の前で、遠藤啓介は待っていた。旅支度を終えた、ひとりの疲れた男として。"

    endo "私はこの国を去る。シベリアの奥地に、私を匿う“古い血筋”の集落がある。IDE2.0の研究は、そこで続ける。"

    endo "人類は、いずれハスターの前に立つ。その日のための箱舟を、私は造り続ける。……君は、それを聞いた上で、どうする？"

    menu:

        "菫さんの言葉で、彼を引き留める" if sumire_trust:

            m "……行く前に、ひとつだけ。菫さんからの伝言です。"

            "遠藤の手が、止まった。"

            m "「菫は、怒ってないよ」。それから——「今度は、置いていかないで」だそうです。"

            "長い沈黙。薪の爆ぜる音だけが、部屋を満たした。"

            endo "……………………はは。参ったな。1000年後の人類より、明日の娘の方が、ずっと難しい。"

            "遠藤啓介は旅装を解いた。箱舟の設計図は暖炉で灰になり、翌年の春——光山大学に、ひとりの「復職した教授」の姿があったという。"

            "娘とふたり、母の墓に花を供える男の顔は、もう“黄衣の教祖”のものではなかった。"

        "何も言わず、見送る":

            m "……止めません。あなたの祈りは、あなたのものだ。"

            endo "…………そうか。君は最後まで、私を“裁かなかった”な。それがどれほど得難いことか、君はまだ知るまい。"

            "深紅の輪が広がり、彼の姿が向こう側へ滲んでいく。最後に、彼は振り返った。"

            endo "1000年後——君の遠い子孫が、私の箱舟に乗ることになったら。その時は、恨んでくれるな。"

            "輪が閉じた。世界のどこか極北で、今も箱舟は造られ続けている。"

            "それが人類への裏切りなのか、それとも最後の保険なのか。——答え合わせは、1000年後だ。"

        "……共に行く":

            m "……連れて行ってください。あなたの“箱舟”を、最後まで見届けたい。"

            "遠藤は、心底驚いた顔をした。それから、ゆっくりと、愉快そうに笑った。"

            endo "——正気か？　いや……正気でないのは、お互い様か。"

            endo "いいだろう。観測者は必要だ。私の計画を「人間の目」で見張り続ける者が。"

            "深紅の輪をくぐる直前、[first_person]は一度だけ振り返った。東の空、置いていく街の方角を。"

            "（雪さん。凛久さん。瑞名さん。——いつか“答え”を持って帰ります。それまで、どうか元気で）"

            "こうして[mc_name]は、歴史から姿を消した。"

            "数十年後。とある論文誌の片隅に、シベリアの奥地から投稿された正体不明の研究報告が載る。その筆名は——「KARAITO」。"

    call ending_recovery from _call_recovery_06

    scene bg black
    with dissolve

    "月夜の物語は、誰も知らない結末へ。"

    jump ending_epilogue


label ending_07_early_exit:

    $ record_ending("07")

    scene bg black
    with dissolve

    $ play_bgm("ending_bad")

    centered "ENDING　⑦ 早期離脱エンド"

    if early_exit_cause == "assassin":

        "冷たいアスファルトの上で、意識が薄れていく。"

        "最後に見えたのは、フードの下の——歌うように微笑む、少女の顔だった。"

        "翌朝のニュースは、都内で続く連続通り魔事件の、新たな被害者を報じた。名前は、伏せられていた。"

        "久美の隠れ家では、少女がひとり、帰らない足音を待ち続けている。"

        "——探索者の物語は、ここで終わる。だが月夜の物語は、誰も止める者のないまま、12月29日へと進んでいく。"

    else:

        "心が、限界を迎えた。"

        "深淵を覗きすぎた者の意識は昏い水底へと沈み、[first_person]の“探索”はここで終わる。"

        "白い天井。規則正しい点滴の音。窓の外の月を見て、[first_person]は毎晩、誰かの名前を呼ぶという。——それが誰なのか、思い出せないまま。"

        "見舞いに訪れる少女がひとり。彼女は枕元で、思い出話を続けている。いつか、その声が届く日を信じて。"

    scene bg black
    with dissolve

    "——そして12月29日の夜、東京の空に“もうひとつの満月”が昇ったことを、[first_person]が知ることはなかった。"

    jump ending_epilogue


## ===============================================================
## エピローグ共通処理
## ===============================================================

## 生還エンド共通: 心の回復(原作のSAN回復報酬の翻案)
label ending_recovery:

    $ recovery = 3
    if flag_f1_moonlens:
        $ recovery += 3
    if flag_f2_yuki_saved:
        $ recovery += 2
    if flag_f3_rikuhisa_saved:
        $ recovery += 2
    if flag_f4_sign_removed:
        $ recovery += 3
    if flag_f5_endo_stopped:
        $ recovery += 2

    $ change_san(recovery)

    "長い悪夢が終わり、心が少しずつ、元の形を取り戻していく。"

    if len(bonds) >= 3:

        ## 交流イベントの後日談差分(企画書: 絆は「日常回帰」の厚みに反映)
        "回復は、独りの作業ではなかった。事務所には烏龍茶が常備されるようになり、屋上には毛布が二枚になり、閉店後のBarには[first_person]のグラスが増えた。"

        "選んで過ごした時間が、そのまま、帰ってこられる場所になっていた。"

        $ change_san(2)

    return


## END④⑤共通: 個人の印だけを解除していた場合の差分(SIGN-ALT)
label ending_personal_sign_note:

    "……そして[first_person]の右手に、印はない。あの夜、ナイ牧師自身の手で外されたそれが、[first_person]と“それ以外”の運命を分けた。"

    return


## エンディング共通の締め。周回プレイへの導線。
label ending_epilogue:

    $ hud_visible = False
    $ stop_bgm()

    $ endings_count = len(persistent.endings_seen)

    centered "エンディング回収状況　[endings_count] / 7"

    "【エンディング到達】この周回はここまでです。回収状況はタイトル画面の「事件簿」から確認できます。"

    if endings_count < 7:
        "別の技能を伸ばし、別の選択をすれば、違う結末に辿り着けるかもしれません。"
    else:
        "——すべての結末が、事件簿に綴じられました。プレイしていただき、ありがとうございます。"

    return
