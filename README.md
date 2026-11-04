# kyoyo 教養図解

ひとつのテーマの全体像を図解した資料集です。GitHub Pagesで公開しています。

公開URL: https://ti0614.github.io/kyoyo/

## 資料一覧

| ジャンル | 資料 | パス |
| --- | --- | --- |
| 歴史 | 日本史 ― 時代をつなぐ因果 | `japanese-history/` |
| 歴史 | 原始・古代の日本史（詳説） | `japanese-history/ancient/` |
| 歴史 | 中世の日本史（詳説） | `japanese-history/medieval/` |
| 歴史 | 近世の日本史（詳説） | `japanese-history/early-modern/` |
| 歴史 | 近代の日本史（詳説） | `japanese-history/modern/` |
| 歴史 | 現代の日本史（詳説） | `japanese-history/contemporary/` |
| 哲学 | 西洋哲学史 ― 問いの系譜 | `western-philosophy/` |
| 宗教 | 仏教 ― 苦しみをほどく教え（全体像） | `buddhism/` |
| 雑談 | 雑談メモ（パスワードで保護） | `zatsudan/` |

## 構成

```
index.html              目次ページ
japanese-history/       日本史 ― 時代をつなぐ因果
  index.html
  ancient/              原始・古代の詳説
  medieval/             中世の詳説
  early-modern/         近世の詳説
  modern/               近代の詳説
  contemporary/         現代の詳説
western-philosophy/     西洋哲学史 ― 問いの系譜
buddhism/               仏教の全体像（詳しいページは順次追加）
zatsudan/               雑談メモ（パスワードで暗号化。tools/lock.py）
tools/                  ふりがなを付けるスクリプトと辞書、雑談メモの暗号化スクリプト
CLAUDE.md               資料作成のルール（文体・構成・ふりがな）
```

## 資料の追加方法

1. `テーマ名/index.html` としてフォルダを作る（フォルダ名は英小文字とハイフン）
2. ページ上部に目次へ戻るリンク（`../`）を入れる
3. トップの `index.html` と、この README の資料一覧に追記する

各ページは外部ファイルに依存しない1枚のHTMLで作ります（フォントのみGoogle Fontsを使用）。
