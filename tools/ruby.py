"""ページにふりがな（<ruby>）を付ける。

使い方:
    python3 tools/ruby.py japanese-history/medieval/index.html
    python3 tools/ruby.py western-philosophy/index.html

- 読みは辞書から読む。新しい語はそちらに足す。
  日本史は tools/ruby-dict.txt、西洋哲学史は tools/ruby-dict-western-philosophy.txt
  （ページの最上位フォルダ名に合う ruby-dict-<フォルダ名>.txt があればそれを使う）。
- 実行のたびに既存の <ruby> を外してから付け直すので、何度実行しても結果は同じ。
  本文を書き換えたあとは、そのまま再実行すればよい。
- 次の単位ごとに、辞書の各グループを最初の1回だけ付ける:
    章の本文（section.chapter から補足を除いた部分） / 補足（details.note）1つずつ /
    冒頭の流れ（ol.overview） / なぜ次の時代へ（section.why） /
    西洋哲学史の問いのカード（article.step）1つずつ。カード上の小見出し（.tag）には付けない
- 補足の見出し（summary）には付けない。ただし人物の補足は見出しの名前に付ける。
"""
import pathlib
import re
import sys

TOOLS = pathlib.Path(__file__).parent
reading, group, not_after = {}, {}, {}
pat = None


def load(path):
    """ページの最上位フォルダ名に合う辞書を読み込む"""
    global pat
    top = pathlib.Path(path).resolve().relative_to(TOOLS.parent.resolve()).parts[0]
    d = TOOLS / f'ruby-dict-{top}.txt'
    if not d.exists():
        d = TOOLS / 'ruby-dict.txt'
    reading.clear(); group.clear(); not_after.clear()
    lines = [l for l in d.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')]
    for gi, line in enumerate(lines):
        for item in line.split('|'):
            w, r = item.split(':')
            if '!' in r:  # 「国人:こくじん!外中」= 直前が「外」「中」のとき（外国人・中国人）は付けない
                r, not_after[w] = r.split('!')
            reading[w] = r
            group[w] = gi
    pat = re.compile('|'.join(alt(w) for w in sorted(reading, key=len, reverse=True)))


def alt(w):
    rx = re.escape(w)
    return f'(?<![{re.escape(not_after[w])}]){rx}' if w in not_after else rx


def strip(html):
    while '<ruby>' in html:
        html = re.sub(r'<ruby>([^<]*)<rt>[^<]*</rt></ruby>', r'\1', html)
    return html


def annotate(html):
    used = set()

    def text(t):
        def rep(m):
            w = m.group(0)
            if group[w] in used:
                return w
            used.add(group[w])
            return f'<ruby>{w}<rt>{reading[w]}</rt></ruby>'
        return pat.sub(rep, t)
    # タグの外側（テキスト）だけを置換する
    return re.sub(r'(<[^>]+>)|([^<]+)', lambda m: m.group(1) or text(m.group(2)), html)


def protect(html, rx, store, fn=lambda x: x):
    def keep(m):
        store.append(fn(m.group(0)))
        return f'\x00{len(store) - 1}\x00'
    return re.sub(rx, keep, html, flags=re.S)


def restore(html, store):
    while '\x00' in html:
        html = re.sub(r'\x00(\d+)\x00', lambda m: store[int(m.group(1))], html)
    return html


def note(html):
    store = []
    if not html.startswith('<details class="note person"'):  # 人物は見出しの名前に付ける
        html = protect(html, r'<summary>.*?</summary>', store)
    return restore(annotate(html), store)


def chapter(html):
    store = []
    html = protect(html, r'<details class="note.*?</details>', store, note)
    return restore(annotate(html), store)


def step(html):
    store = []
    html = protect(html, r'<div class="tag">.*?</div>', store)
    return restore(annotate(html), store)


def main(path):
    load(path)
    p = pathlib.Path(path)
    s = strip(p.read_text(encoding='utf-8'))
    s = re.sub(r'<section class="chapter" id="c\d+">.*?</section>', lambda m: chapter(m.group(0)), s, flags=re.S)
    s = re.sub(r'<ol class="overview">.*?</ol>', lambda m: annotate(m.group(0)), s, flags=re.S)
    s = re.sub(r'<section class="why">.*?</section>', lambda m: annotate(m.group(0)), s, flags=re.S)
    s = re.sub(r'<article class="step">.*?</article>', lambda m: step(m.group(0)), s, flags=re.S)
    p.write_text(s, encoding='utf-8')
    print(f'{path}: ruby {s.count("<ruby>")}')


if __name__ == '__main__':
    for a in sys.argv[1:]:
        main(a)
