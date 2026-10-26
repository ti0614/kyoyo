# kyoyo 教養図解

大人の学び直しのための図解資料集です。GitHub Pagesで公開しています。

公開URL: https://ti0614.github.io/kyoyo/

## 資料一覧

| ジャンル | 資料 | パス |
| --- | --- | --- |
| 歴史 | 日本史の流れ図 | `japanese-history/` |
| 歴史 | 中世の日本史（詳説） | `japanese-history/medieval/` |

## 構成

```
index.html              目次ページ
japanese-history/       日本史の流れ図
  index.html
  medieval/             中世の詳説
    index.html
tools/                  ふりがなを付けるスクリプトと辞書
CLAUDE.md               資料作成のルール（文体・構成・ふりがな）
```

## 資料の追加方法

1. `テーマ名/index.html` としてフォルダを作る（フォルダ名は英小文字とハイフン）
2. ページ上部に目次へ戻るリンク（`../`）を入れる
3. トップの `index.html` と、この README の資料一覧に追記する

各ページは外部ファイルに依存しない1枚のHTMLで作ります（フォントのみGoogle Fontsを使用）。
