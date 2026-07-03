## 最小限のフォント設定。
## デフォルトフォント(DejaVu系)は日本語グリフを含まないため、IPAゴシックに差し替える。
## フォントは fonts/ipag.ttf に同梱(IPAフォントライセンスv1.0、再配布可)。

style default:
    font "fonts/ipag.ttf"

style input:
    font "fonts/ipag.ttf"

## HUD・ステータス画面・デバッグメニューのボタン/見出しにも日本語が入るため、
## 派生スタイル側でも明示的に指定しておく(テーマ側の上書き対策)。
style button_text:
    font "fonts/ipag.ttf"

style label_text:
    font "fonts/ipag.ttf"
