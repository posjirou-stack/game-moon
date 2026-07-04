## 月夜が魅せる物語 -Fated Moonlight- 基本設定
## GUIはRen'Py標準テンプレート+月夜テーマ(gui.rpy/screens.rpy)を使用。

define config.name = _("月夜が魅せる物語 -Fated Moonlight-")
define gui.show_name = True

define config.version = "0.3.0-dev"

define build.name = "tsukiyo_ga_miseru_monogatari"

define config.window_icon = None

## セーブディレクトリ名(他のRen'Pyゲームと衝突しないように専用名にする)
define config.save_directory = "TsukiyoGaMiseruMonogatari-0.1"

define config.has_autosave = True

## 二次創作である旨を明記(非公開・身内配布前提)
define config.window_title = "月夜が魅せる物語 -Fated Moonlight-（プロトタイプ・非公開）"

## 終了確認はGUIテンプレートのconfirm画面に任せる

## タイトル画面のBGM(ファイルが置かれていれば自動で有効になる)
define config.main_menu_music = "audio/bgm/main_theme.ogg" if renpy.loadable("audio/bgm/main_theme.ogg") else None
