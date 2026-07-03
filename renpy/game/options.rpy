## 月夜が魅せる物語 -Fated Moonlight- 基本設定
## GUIテーマは未導入で、標準スクリーンのまま進める(テーマ導入はフェーズ3)。

define config.name = _("月夜が魅せる物語 -Fated Moonlight-（プロトタイプ）")
define gui.show_name = False

define config.version = "0.2.0-dev"

define build.name = "tsukiyo_ga_miseru_monogatari"

define config.window_icon = None

## セーブディレクトリ名(他のRen'Pyゲームと衝突しないように専用名にする)
define config.save_directory = "TsukiyoGaMiseruMonogatari-0.1"

define config.has_autosave = True

## 二次創作である旨を明記(非公開・身内配布前提)
define config.window_title = "月夜が魅せる物語 -Fated Moonlight-（プロトタイプ・非公開）"

## GUIテンプレート未導入の間は終了確認画面(yesno)が存在せず、ウィンドウを閉じると
## 例外になるため、確認なしで即終了させる。GUIテーマ導入(フェーズ3)時に見直すこと。
define config.quit_action = Quit(confirm=False)
