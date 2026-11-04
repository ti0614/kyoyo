#!/usr/bin/env python3
"""雑談メモをパスワードで暗号化する / 元に戻す。

  python3 tools/lock.py lock   zatsudan/<名前>/index.html   # 暗号化して上書き
  python3 tools/lock.py unlock zatsudan/<名前>/index.html > 出力先.html  # 復号して標準出力へ

パスワードは環境変数 KYOYO_ZATSUDAN_PASS か、実行時の入力で渡す。
暗号化は AES-256-GCM、鍵は PBKDF2-SHA256（60万回）でパスワードから作る。
ブラウザ側は Web Crypto で復号するので、リポジトリには暗号文しか残らない。
"""
import base64, getpass, html, json, os, re, sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITER = 600_000
MARK = '<meta name="kyoyo-lock" content="1">'

PAGE = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
""" + MARK + """
<title>雑談メモ</title>
<style>
:root{--paper:#eef0ee;--surface:#f8f9f7;--ink:#1d2326;--muted:#5d686b;--line:#c9cfcc;--accent:#24476b;--bad:#9b2c2c;
  --body:"Zen Kaku Gothic New","Hiragino Sans","Yu Gothic",system-ui,sans-serif;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#15191b;--surface:#1d2326;--ink:#e4e8e6;--muted:#9aa5a7;--line:#343d40;--accent:#8fb4dc;--bad:#e59a9a;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#15191b;--surface:#1d2326;--ink:#e4e8e6;--muted:#9aa5a7;--line:#343d40;--accent:#8fb4dc;--bad:#e59a9a;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);line-height:1.8}
main{max-width:420px;margin:0 auto;padding:64px 20px;display:flex;flex-direction:column;gap:16px}
a{color:var(--accent);font-size:.85rem;text-decoration:none}
h1{font-size:1.3rem;margin:0}
p{margin:0;color:var(--muted);font-size:.9rem}
form{display:flex;flex-direction:column;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:16px}
input[type=password]{font:inherit;padding:10px 12px;border:1px solid var(--line);border-radius:6px;background:var(--paper);color:var(--ink)}
input:focus-visible,button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
label.keep{display:flex;gap:8px;align-items:center;font-size:.9rem}
button{font:inherit;font-weight:700;padding:10px;border:0;border-radius:6px;background:var(--accent);color:var(--paper);cursor:pointer}
#err{color:var(--bad);min-height:1.5em}
</style>
</head>
<body>
<main>
  <a href="__BACK__">← kyoyo 目次</a>
  <h1>雑談メモ</h1>
  <p>このページはパスワードで保護されている。</p>
  <form id="f">
    <label for="pw">パスワード</label>
    <input type="password" id="pw" autocomplete="current-password" required>
    <label class="keep"><input type="checkbox" id="keep" checked> このブラウザに記憶する</label>
    <button type="submit">開く</button>
    <p id="err" role="alert"></p>
  </form>
</main>
<script type="application/json" id="data">__DATA__</script>
<script>
(function(){
  var KEY="kyoyo-zatsudan-pass";
  var d=JSON.parse(document.getElementById("data").textContent);
  function b(s){return Uint8Array.from(atob(s),function(c){return c.charCodeAt(0)})}
  async function open(pw){
    var base=await crypto.subtle.importKey("raw",new TextEncoder().encode(pw),"PBKDF2",false,["deriveKey"]);
    var k=await crypto.subtle.deriveKey({name:"PBKDF2",salt:b(d.salt),iterations:d.iter,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["decrypt"]);
    var pt=await crypto.subtle.decrypt({name:"AES-GCM",iv:b(d.iv)},k,b(d.ct));
    return new TextDecoder().decode(pt);
  }
  function show(h){document.open();document.write(h);document.close()}
  function get(){try{return localStorage.getItem(KEY)}catch(e){return null}}
  function set(v){try{v?localStorage.setItem(KEY,v):localStorage.removeItem(KEY)}catch(e){}}
  var saved=get();
  if(saved){open(saved).then(show,function(){set(null)})}
  var err=document.getElementById("err");
  document.getElementById("f").addEventListener("submit",function(e){
    e.preventDefault();err.textContent="確認中…";
    var pw=document.getElementById("pw").value;
    open(pw).then(function(h){if(document.getElementById("keep").checked)set(pw);show(h)},
      function(){err.textContent="パスワードが違う。"});
  });
})();
</script>
</body>
</html>
"""


def key(pw, salt):
    return PBKDF2HMAC(hashes.SHA256(), 32, salt, ITER).derive(pw.encode())


def password():
    pw = os.environ.get("KYOYO_ZATSUDAN_PASS") or getpass.getpass("パスワード: ")
    if not pw:
        sys.exit("パスワードが空です")
    return pw


def lock(path):
    src = open(path, encoding="utf-8").read()
    if MARK in src:
        sys.exit(f"{path} はすでに暗号化されています")
    pw = password()
    salt, iv = os.urandom(16), os.urandom(12)
    ct = AESGCM(key(pw, salt)).encrypt(iv, src.encode(), None)
    e = lambda x: base64.b64encode(x).decode()
    data = json.dumps({"iter": ITER, "salt": e(salt), "iv": e(iv), "ct": e(ct)})
    back = "../" if os.path.normpath(path).count(os.sep) == 1 else "../../"
    open(path, "w", encoding="utf-8").write(PAGE.replace("__BACK__", back).replace("__DATA__", data))
    print(f"暗号化しました: {path}", file=sys.stderr)


def unlock(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r'<script type="application/json" id="data">(.*?)</script>', src, re.S)
    if MARK not in src or not m:
        sys.exit(f"{path} は暗号化されていません")
    d = json.loads(m.group(1))
    b = base64.b64decode
    try:
        pt = AESGCM(key(password(), b(d["salt"]))).decrypt(b(d["iv"]), b(d["ct"]), None)
    except Exception:
        sys.exit("パスワードが違います")
    sys.stdout.write(pt.decode())


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("lock", "unlock"):
        sys.exit(__doc__)
    (lock if sys.argv[1] == "lock" else unlock)(sys.argv[2])
