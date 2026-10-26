"""区分詳説ページにふりがな（<ruby>）を付ける。

使い方:
    python3 tools/ruby.py japanese-history/medieval/index.html

- 読みは tools/ruby-dict.txt から読む。新しい語はそちらに足す。
- 実行のたびに既存の <ruby> を外してから付け直すので、何度実行しても結果は同じ。
  本文を書き換えたあとは、そのまま再実行すればよい。
- 次の単位ごとに、辞書の各グループを最初の1回だけ付ける:
    章の本文（section.chapter から補足を除いた部分） / 補足（details.note）1つずつ /
    冒頭の流れ（ol.overview） / なぜ次の時代へ（section.why）
- 補足の見出し（summary）には付けない。ただし人物の補足は見出しの名前に付ける。
"""
import pathlib
import re
import sys

DICT = pathlib.Path(__file__).with_name('ruby-dict.txt')

reading, group = {}, {}
lines = [l for l in DICT.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')]
for gi, line in enumerate(lines):
    for item in line.split('|'):
        w, r = item.split(':')
        reading[w] = r
        group[w] = gi
pat = re.compile('|'.join(sorted(map(re.escape, reading), key=len, reverse=True)))


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


def main(path):
    p = pathlib.Path(path)
    s = strip(p.read_text(encoding='utf-8'))
    s = re.sub(r'<section class="chapter" id="c\d+">.*?</section>', lambda m: chapter(m.group(0)), s, flags=re.S)
    s = re.sub(r'<ol class="overview">.*?</ol>', lambda m: annotate(m.group(0)), s, flags=re.S)
    s = re.sub(r'<section class="why">.*?</section>', lambda m: annotate(m.group(0)), s, flags=re.S)
    p.write_text(s, encoding='utf-8')
    print(f'{path}: ruby {s.count("<ruby>")}')


if __name__ == '__main__':
    for a in sys.argv[1:]:
        main(a)
