# kyoyo 教養図解

ひとつのテーマの全体像を図解した資料集です。GitHub Pagesで公開しています。

公開URL: https://ti0614.github.io/kyoyo/

## 資料一覧

| ジャンル | 資料 | パス |
| --- | --- | --- |
| 歴史 | 日本史の流れ図 | `japanese-history/` |
| 歴史 | 原始・古代の日本史（詳説） | `japanese-history/ancient/` |
| 歴史 | 中世の日本史（詳説） | `japanese-history/medieval/` |
| 歴史 | 近世の日本史（詳説） | `japanese-history/early-modern/` |
| 歴史 | 近代の日本史（詳説） | `japanese-history/modern/` |
| 歴史 | 現代の日本史（詳説） | `japanese-history/contemporary/` |
| 哲学 | 西洋哲学史 ― 問いの系譜 | `western-philosophy/` |
| 数学 | 高校数学 ― 考え方の地図 | `high-school-math/` |
| 雑談 | 人は何で考えているのか | `zatsudan/how-we-think/` |

## 構成

```
index.html              目次ページ
japanese-history/       日本史の流れ図
  index.html
  ancient/              原始・古代の詳説
  medieval/             中世の詳説
  early-modern/         近世の詳説
  modern/               近代の詳説
  contemporary/         現代の詳説
western-philosophy/     西洋哲学史 ― 問いの系譜
high-school-math/       高校数学 ― 考え方の地図
zatsudan/               雑談メモ
  how-we-think/         人は何で考えているのか
tools/                  ふりがなを付けるスクリプトと辞書
.claude/agents/         確認役のサブエージェント（事実確認・内容確認）
CLAUDE.md               資料作成のルール（文体・構成・ふりがな）
```

## 資料の追加方法

1. `テーマ名/index.html` としてフォルダを作る（フォルダ名は英小文字とハイフン）
2. ページ上部に目次へ戻るリンク（`../`）を入れる
3. トップの `index.html` と、この README の資料一覧に追記する

各ページは外部ファイルに依存しない1枚のHTMLで作ります（フォントのみGoogle Fontsを使用）。
