# アセット仕様書・生成プロンプト集（フェーズ4）

ゲーム側の受け入れ口は実装済み。**下記の規約どおりのファイル名で
`renpy/game/images/`・`renpy/game/audio/` に置くだけで、次回起動時から自動で反映される**
（無い間は背景=単色、立ち絵=非表示、BGM=無音で動作する）。

- 画像生成: ChatGPT(DALL-E)/Midjourney/Stable Diffusion 等
- 音楽生成: Suno/Udio 等
- 権利: 非公開・身内配布前提だが、各サービスの利用規約(生成物の利用条件)は要確認(要件定義9章)

---

## 1. スタイル統一(最重要)

絵柄ブレを防ぐため、**すべての画像プロンプトに共通の接頭辞を付ける**こと。

### 共通スタイル接頭辞(コピペ用)

```
anime visual novel background art, 2016 Tokyo in winter, night scenes,
muted desaturated color palette with deep blue and purple moonlight tones,
subtle cosmic horror atmosphere, quiet and eerie mood, no people,
high detail, 16:9 aspect ratio
```

立ち絵用:

```
anime style character sprite for a visual novel, full body, standing pose,
facing viewer, transparent background, soft muted colors, subtle rim light
as if lit by moonlight, Japanese modern winter clothing, high detail
```

### キャラの絵柄ブレ対策(要件定義9章)

1. まず各キャラの「基準画像」を1枚生成して確定する
2. 表情差分は基準画像を **img2img / 参照画像機能** に入れて表情だけ変える
   (プロンプト全文を書き直さない。「same character, same outfit, same art style,
   only change the facial expression to ...」と指示する)
3. 全キャラで同じスタイル接頭辞・同じ生成サービス・同じモデルを使う

---

## 2. 背景(19点 + タイトル)

- 置き場所: `renpy/game/images/bg/<name>.png`
- サイズ: **1280x720** (大きい場合は縮小トリミングして合わせる)

| ファイル名 | 場所 | プロンプト案(共通接頭辞のあとに追加) |
|---|---|---|
| `title.png` | タイトル画面 | full moon over Tokyo skyline at night, a lone philosophical park with bare winter trees in silhouette, ominous purple clouds, cinematic wide shot |
| `izakaya.png` | 居酒屋「夜叉」 | cozy but dim traditional Japanese izakaya interior, wooden tables, paper lanterns, private booth |
| `street_night.png` | 夜の繁華街 | Tokyo Shimbashi back street at night, neon signs reflecting on wet asphalt, narrow street |
| `alley.png` | 裏路地 | very narrow dark alley between buildings, single flickering street lamp, steam from vents |
| `campus.png` | 光山大学 | modern Japanese university campus in winter, bare ginkgo trees, glass and concrete buildings |
| `office.png` | 玲紀探偵事務所 | small cluttered private detective office, desk with papers, whiteboard with photos and strings, venetian blinds |
| `library.png` | 図書館・古崎堂 | cramped old second-hand bookstore interior at night, towering stacks of old books, warm single lamp |
| `house.png` | 東風谷家 | upscale Japanese suburban house interior, clean but unlived-in, curtains drawn, dim |
| `house_burnt.png` | 東風谷家(焼け跡) | burned ruins of a Japanese suburban house, police tape, morning after fire, ash and charred beams |
| `bar.png` | Bar「雪国」 | tiny hidden luxury bar interior, dark wood counter, backlit bottles, moody lighting |
| `basement.png` | 久美の地下室 | secret basement study filled with occult books and research papers, warm lamp, monitors |
| `nagae.png` | 長江ビル | abandoned building interior turned occult laboratory, palace-like hall underground, disturbing murals, prison cells |
| `apartment.png` | 中西アパート | old five-story Japanese apartment building exterior at dusk, seemingly abandoned, ominous |
| `church.png` | 星の知恵派の教会 | dark church interior with black curtains, altar with strange ancient icon, candle light |
| `lab.png` | 遠藤研究所 | abandoned high-tech research facility corridor, long descending hallway, heavy steel door |
| `grave.png` | 遠藤楓の墓 | small Japanese cemetery at night in a forest edge, one well-kept gravestone among neglected ones, moonlight |
| `villa.png` | 奥多摩の別荘 | log house interior in snowy mountain forest, fireplace burning, books and research equipment |
| `tower.png` | 東京タワー | Tokyo Tower at night seen from its base, dramatic upward angle, winter night sky |
| `park_night.png` | 哲学堂公園(夜) | Japanese park at night with bare winter trees, ominous atmosphere, faint lights between trees |
| `ritual.png` | 儀式場・異空間 | otherworldly alien space in green and purple, distorted geometry, giant tower with 13 lenses like flower petals, cosmic horror |

## 3. 立ち絵(6キャラ・計13枚)

- 置き場所: `renpy/game/images/char/<キャラ>_<表情>.png`
- サイズ: 高さ **約650px**(720pの画面で膝上〜全身が収まる程度)、背景透過PNG
- ゲーム側は `show yuki fear` 等で表示する(配置済み)。差分を後から増やす場合は
  `script.rpy` の `CHAR_SPRITES` に表情名を追加する

| キャラ | 基準デザイン | 必要な差分 |
|---|---|---|
| `yuki` 東風谷雪(17) | 小柄、黒のセミロング、おとなしい印象。フード付きの防寒コート(序盤)。どこか浮世離れした雰囲気 | `normal` `smile` `fear` `sad` |
| `riku` 間宮凛久(17) | 雪と同年代、ややボーイッシュなショートヘア。無地の白い服(監禁中)。虚ろ⇔快活 | `blank`(虚ろ) `normal` `smile` |
| `mizuna` 瑞名慧(29) | 私立探偵。無精髭、着崩したスーツにコート。軽薄そうで目つきは鋭い | `normal` `serious` |
| `kumi` 久美啓太(初老) | 白髪混じり、丸眼鏡、カーディガン。学者風の穏やかな老人 | `normal` |
| `endo` 遠藤啓介(森本蓮司の姿) | 40代の大学教授。整った身なり、しかし深い疲労を湛えた目 | `normal` `tired` |
| `sumire` 遠藤菫(大学1年) | 生真面目な理系女子。ロングヘア、大学の冬服 | `normal` |

プロンプト例(雪・基準画像):

```
(共通立ち絵接頭辞), 17 year old Japanese girl, petite, shoulder-length
black hair, quiet and fragile impression, wearing an oversized hooded
winter coat, slightly anxious neutral expression
```

差分生成(例: fear): 基準画像を参照に
`same character, same outfit, same art style, only change expression to frightened, trembling`

## 4. BGM(8曲)

- 置き場所: `renpy/game/audio/bgm/<name>.ogg` (mp3しか出せない場合は変換する)
- ループ再生される。2〜3分でループの継ぎ目が自然な曲が望ましい
- 生成サービス(Suno等)には「instrumental, loopable, no vocals」を必ず指定

| ファイル名 | 使用場面 | 曲調の指定案 |
|---|---|---|
| `main_theme.ogg` | タイトル画面 | 静かで神秘的なピアノ+ストリングス。月夜、物悲しさ、微かな不穏。dark ambient piano, mysterious, melancholic |
| `daily.ogg` | 日常(夜叉など) | 落ち着いたジャズ風。ローファイ気味。calm jazz lounge, night city, relaxed but slightly lonely |
| `investigation.ogg` | 調査パート | 淡々と刻むミニマルな曲。detective ambient, ticking rhythm, thoughtful, urban night |
| `tension.ogg` | 緊迫(遭遇・潜入・対峙) | 低音ドローン+心拍のようなパーカッション。suspense drone, heartbeat percussion, creeping dread |
| `ritual.ogg` | クライマックス儀式 | 不協和音の聖歌+重いドラム。dissonant choir, ritualistic drums, cosmic horror, overwhelming |
| `ending_good.ogg` | END①②③⑥ | 夜明けを思わせる温かいピアノ。hopeful piano ballad, dawn after long night, bittersweet |
| `ending_bad.ogg` | END④⑤⑦ | 静かな絶望。単音ピアノ+ノイズ。desolate sparse piano, cold ambient noise, tragic |
| (予備) `heartbeat.ogg` | SAN低下演出(将来) | 心音のみ。単純な heartbeat loop |

## 5. SE(任意・後回しでよい)

`renpy/game/audio/se/` に配置(再生コードは導入時に追加する)。
候補: ドアの開閉、足音(アスファルト/廊下)、爆発、群衆のざわめき、教会の鐘、
ページをめくる音、電子ロック、遠雷。フリー素材(効果音ラボ等)でも可。

---

## 6. 導入手順まとめ

1. このリストの順(推奨: タイトル→主要背景5点→雪の立ち絵→BGM4曲)に生成する
2. 規約どおりのファイル名にリネームして `renpy/game/images/` `renpy/game/audio/` に置く
3. ゲームを起動して確認(差し替えに再ビルドは不要)
4. 立ち絵のサイズ・位置が合わない場合は画像側の余白で調整する
   (それでも合わなければ `script.rpy` の登録部で調整するので相談してください)
