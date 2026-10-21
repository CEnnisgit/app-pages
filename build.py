"""Static privacy/support/index pages for GitHub Pages. No JS. Run: python3 build.py"""
import json, os, re, shutil, sys, markdown
from PIL import Image
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..', 'design-kit', 'tools'))
from tokens import THEMES, EXTRA
from mock import contrast
CFG = json.load(open(os.path.join(ROOT, 'config.json')))
APPS = {
 'quietwell': dict(name='Quietwell', theme='quietwell', dark_only=True, icon='../sleep/design/icon-1024.png',
   tagline='A sound machine that makes brown noise, fan and rain live on your iPhone.',
   bullets=['White, pink and brown noise, fan and rain, free with a sleep timer', 'Mix up to four sounds with Quietwell Pro', 'No account, no ads, Data Not Collected']),
 'keepwell': dict(name='Keepwell', theme='keepwell', dark_only=False, icon='../keepwell-ready/Keepwell/Resources/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png',
   tagline='Keepwell helps you clean up your camera roll one month at a time. Swipe to keep or delete. Everything stays on your phone.', bullets=[]),
 'glasswell': dict(name='Glasswell', theme='water', dark_only=False, icon='../water/design/icon-1024.png',
   tagline='A simple water tracker. Log a glass in one tap and get reminders that stop at your goal.',
   bullets=['One-tap logging, a daily goal and reminders', 'Saves to Apple Health; your data stays on your iPhone', 'No account, no ads, Data Not Collected']),
}
EULA = 'https://www.apple.com/legal/internet-services/itunes/dev/stdeula/'

def css(app):
    th = THEMES[APPS[app]['theme']]
    def vars_(m): return ';'.join(f'--{k}:{v}' for k, v in th[m].items())
    if APPS[app]['dark_only']:
        root = f':root{{{vars_("dark")};color-scheme:dark}}'
    else:
        root = f':root{{{vars_("light")};color-scheme:light dark}}@media (prefers-color-scheme:dark){{:root{{{vars_("dark")}}}}}'
    return root + '''
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--background);color:var(--textPrimary);font:17px/1.6 -apple-system,BlinkMacSystemFont,"SF Pro Text","Inter","Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accentText);text-underline-offset:2px}a:focus-visible{outline:3px solid var(--accentText);outline-offset:2px;border-radius:4px}
.skip{position:absolute;left:-999px}.skip:focus{left:16px;top:8px;background:var(--surface);padding:8px 12px;z-index:9}
header{border-bottom:1px solid var(--separator);background:var(--surface)}
.bar{max-width:720px;margin:0 auto;padding:12px 24px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--textPrimary);text-decoration:none;margin-right:auto}
.brand img{width:36px;height:36px;border-radius:9px}
nav a{display:inline-block;padding:10px 8px;min-height:44px;font-weight:600;text-decoration:none}nav a[aria-current]{color:var(--textPrimary);text-decoration:underline}
main{max-width:720px;margin:0 auto;padding:32px 24px 48px}
h1{font-size:2rem;line-height:1.2;letter-spacing:-.02em;margin:0 0 16px}h2{font-size:1.3rem;margin:40px 0 8px}h3{font-size:1.06rem;margin:28px 0 4px}
p,li{color:var(--textPrimary)}ul,ol{padding-left:1.3em}li{margin:4px 0}
.card{background:var(--surface);border:1px solid var(--separator);border-radius:16px;padding:20px}
.hero{text-align:center}.hero img{width:128px;height:128px;border-radius:29px;box-shadow:0 8px 24px rgba(0,0,0,.25)}
.hero p.tag{color:var(--textSecondary);font-size:1.1rem;max-width:34em;margin:0 auto 24px}
.links{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin:24px 0}
.btn{display:inline-flex;align-items:center;min-height:48px;padding:0 22px;border-radius:14px;background:var(--accent);color:var(--onAccent);font-weight:700;text-decoration:none}
.btn.alt{background:var(--surface);color:var(--textPrimary);border:1px solid var(--separator)}
.soon{display:inline-block;padding:6px 12px;border-radius:999px;background:var(--accentSoft);color:var(--accentText);font-weight:700;font-size:.9rem}
footer{border-top:1px solid var(--separator);color:var(--textSecondary);font-size:.9rem}footer .bar{display:block;padding:20px 24px 32px}
footer p{color:var(--textSecondary);margin:4px 0}\n.muted{color:var(--textSecondary)}main h1:first-of-type{margin-top:8px}
'''

def shell(app, title, current, body, depth):
    a = APPS[app]; up = '../' * depth
    nav = ''.join(f'<a href="{up}{href}"{" aria-current=\"page\"" if k == current else ""}>{lab}</a>'
                  for k, href, lab in (('home', '', 'Home'), ('privacy', 'privacy/', 'Privacy'), ('support', 'support/', 'Support')))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{a['tagline']}">
<meta name="theme-color" content="{THEMES[a['theme']]['dark' if a['dark_only'] else 'light']['surface']}">
<link rel="icon" href="{up}icon-180.png"><link rel="apple-touch-icon" href="{up}icon-180.png">
<link rel="stylesheet" href="{up}style.css"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header><div class="bar"><a class="brand" href="{up}"><img src="{up}icon-180.png" alt="" width="36" height="36">{a['name']}</a><nav aria-label="Site">{nav}</nav></div></header>
<main id="main">{body}</main>
<footer><div class="bar"><p>{a['name']} is an app by <span class="seller">{CFG['SELLER']}</span>. Contact: <a href="mailto:{CFG['EMAIL']}">{CFG['EMAIL']}</a></p>
<p><a href="{up}privacy/">Privacy Policy</a> · <a href="{up}support/">Support</a> · <a href="{EULA}">Terms of Use (Apple standard EULA)</a></p></div></footer>
</body></html>
'''

def md(path):
    s = open(path).read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S).replace('{{SELLER}}', f'<span class="seller">{CFG["SELLER"]}</span>').replace('{{EMAIL}}', f'<a href="mailto:{CFG["EMAIL"]}">{CFG["EMAIL"]}</a>')
    s = s.replace(f'**<a href="mailto:{CFG["EMAIL"]}">{CFG["EMAIL"]}</a>**', f'<strong><a href="mailto:{CFG["EMAIL"]}">{CFG["EMAIL"]}</a></strong>')
    out, prev = [], ''
    for ln in s.split('\n'):
        is_li = re.match(r'\s*([-*]|\d+\.)\s', ln); prev_li = re.match(r'\s*([-*]|\d+\.)\s', prev)
        if is_li and prev.strip() and not prev_li: out.append('')
        out.append(ln); prev = ln
    return markdown.markdown('\n'.join(out), extensions=['sane_lists'])

def fill(s):
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = s.replace('mailto:{{EMAIL}}', 'mailto:' + CFG['EMAIL']).replace('{{EMAIL}}', CFG['EMAIL'])
    return s.replace('{{SELLER}}', f'<span class="seller">{CFG["SELLER"]}</span>')
def src(app, page):
    h = os.path.join(ROOT, 'src', app, f'{page}.html')
    return fill(open(h).read()) if os.path.exists(h) else md(os.path.join(ROOT, 'src', app, f'{page}.md'))
out = os.path.join(ROOT, 'apps'); shutil.rmtree(out, ignore_errors=True)
for app, a in APPS.items():
    d = os.path.join(out, app); os.makedirs(d)
    open(f'{d}/style.css', 'w').write(css(app))
    Image.open(os.path.join(ROOT, a['icon'])).convert('RGB').resize((180, 180), Image.LANCZOS).save(f'{d}/icon-180.png')
    for page in ('privacy', 'support'):
        os.makedirs(f'{d}/{page}')
        html = src(app, page)
        title = re.search(r'<h1>(.*?)</h1>', html).group(1)
        open(f'{d}/{page}/index.html', 'w').write(shell(app, title, page, html, 1))
    if os.path.exists(os.path.join(ROOT, 'src', app, 'index.html')):
        body = f'<section class="hero"><img src="icon-180.png" alt="{a["name"]} app icon" width="128" height="128"></section>' + src(app, 'index')
        open(f'{d}/index.html', 'w').write(shell(app, f"{a['name']} for iPhone", 'home', body, 0)); continue
    lis = ''.join(f'<li>{b}</li>' for b in a['bullets'])
    body = f'''<section class="hero"><img src="icon-180.png" alt="{a['name']} app icon" width="128" height="128">
<h1>{a['name']}</h1><p class="tag">{a['tagline']}</p><span class="soon">Coming soon to the App Store for iPhone</span>
<div class="links"><a class="btn" href="support/">Get support</a><a class="btn alt" href="privacy/">Privacy Policy</a></div></section>
<div class="card"><ul>{lis}</ul></div>'''
    open(f'{d}/index.html', 'w').write(shell(app, f"{a['name']} for iPhone", 'home', body, 0))
open(os.path.join(ROOT, 'index.html'), 'w').write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Apps</title></head><body style="font-family:-apple-system,Inter,sans-serif;max-width:640px;margin:40px auto;padding:0 24px"><h1>Apps</h1><ul><li><a href="apps/quietwell/">Quietwell</a></li><li><a href="apps/glasswell/">Glasswell</a></li><li><a href="apps/keepwell/">Keepwell</a></li></ul></body></html>\n')
open(os.path.join(ROOT, '.nojekyll'), 'w').write('')
# AA audit of the pairs the CSS uses
for app, a in APPS.items():
    for m in (['dark'] if a['dark_only'] else ['light', 'dark']):
        t = THEMES[a['theme']][m]
        for fg, bg in (('textPrimary','background'),('textPrimary','surface'),('textSecondary','surface'),('textSecondary','background'),('accentText','background'),('accentText','surface'),('onAccent','accent'),('accentText','accentSoft')):
            r = contrast(t[fg], t[bg]); assert r >= 4.5, (app, m, fg, bg, r)
print('built; all text pairs >= 4.5:1')
