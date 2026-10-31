"""Draws brand-coloured side-view illustrations for vehicles without photos -> site/img/van-*.svg"""
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'site', 'img')

def van(L, nwin, label, accent, urbania=False):
    F = 372                      # front x
    R = F - L                    # rear x
    roof, bot = (84, 214) if not urbania else (88, 214)
    ws = F - 62                  # windshield top start
    nose = 'L{a} 140 L{b} 147 Q{c} 150 {c} 159'.format(a=F - 24, b=F - 6, c=F) if not urbania else \
           'L{a} 128 Q{b} 142 {c} 156'.format(a=F - 18, b=F - 4, c=F)
    body = f'M{R} {bot} L{R} {roof+12} Q{R} {roof} {R+12} {roof} L{ws} {roof} Q{ws+14} {roof} {ws+22} {roof+10} {nose} L{F} {bot-10} Q{F} {bot} {F-10} {bot} Z'
    # windows
    x0, x1, gap = R + 14, ws - 4, 6
    w = (x1 - x0 - gap * (nwin - 1)) / nwin
    wins = ''.join(f'<rect x="{x0 + i * (w + gap):.1f}" y="{roof+12}" width="{w:.1f}" height="36" rx="5" fill="url(#gl)"/>' for i in range(nwin))
    shield = f'<path d="M{ws+4} {roof+12} L{ws+16} {roof+12} Q{ws+22} {roof+12} {ws+26} {roof+18} L{F-26 if not urbania else F-20} {roof+48} L{ws+4} {roof+48} Z" fill="url(#gl)"/>'
    w1, w2 = R + 62, F - 64
    wheel = lambda x: f'<circle cx="{x}" cy="{bot}" r="27" fill="#2a3150"/><circle cx="{x}" cy="{bot}" r="21" fill="#1a1f36"/><circle cx="{x}" cy="{bot}" r="9" fill="#cfd3dd"/><circle cx="{x}" cy="{bot}" r="3" fill="#1a1f36"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img" aria-label="{label}">
<defs>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbe9d7"/><stop offset=".7" stop-color="#f6efe3"/><stop offset="1" stop-color="#efe5d4"/></linearGradient>
 <linearGradient id="gl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2b3990"/><stop offset="1" stop-color="#121a3d"/></linearGradient>
 <linearGradient id="bd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e9e6f0"/></linearGradient>
</defs>
<rect width="400" height="300" fill="url(#sky)"/>
<circle cx="318" cy="70" r="34" fill="#f4a53c" opacity=".35"/>
<path d="M0 196 Q60 176 120 190 T240 186 T400 192 V300 H0Z" fill="#eadfcb"/>
<rect y="240" width="400" height="60" fill="#e3d7c2"/>
<g opacity=".7"><rect x="20" y="268" width="50" height="5" rx="2" fill="#fff"/><rect x="120" y="268" width="50" height="5" rx="2" fill="#fff"/><rect x="220" y="268" width="50" height="5" rx="2" fill="#fff"/><rect x="320" y="268" width="50" height="5" rx="2" fill="#fff"/></g>
<ellipse cx="{(R+F)/2}" cy="{bot+28}" rx="{L/2+14}" ry="9" fill="#121a3d" opacity=".18"/>
<path d="{body}" fill="url(#bd)" stroke="#c9c6d6" stroke-width="1.5"/>
{wins}{shield}
<rect x="{R}" y="{roof+60}" width="{F-R-(10 if not urbania else 4)}" height="9" fill="{accent}"/>
<rect x="{R}" y="{roof+72}" width="{F-R-(10 if not urbania else 4)}" height="3" fill="#1f2d6e"/>
<text x="{R+18}" y="{roof+102}" font-family="Manrope,Arial,sans-serif" font-weight="800" font-size="15" letter-spacing="3" fill="#1f2d6e">ANNAPURNA</text>
<line x1="{ws-2}" y1="{roof+54}" x2="{ws-2}" y2="{bot-8}" stroke="#cfcbd9" stroke-width="2"/>
<rect x="{F-12}" y="{roof+66}" width="10" height="9" rx="3" fill="#f4a53c"/>
<rect x="{R-2}" y="{bot-22}" width="8" height="12" rx="2" fill="#e8553a"/>
<rect x="{R}" y="{bot-6}" width="{F-R}" height="8" rx="4" fill="#3a3f57"/>
{wheel(w1)}{wheel(w2)}
</svg>'''

for name, args in {
    'van-tempo26': (330, 7, 'Force Tempo Traveller 26 seater illustration', '#e8553a'),
    'van-tempo17': (280, 5, 'Force Tempo Traveller 17 seater illustration', '#e8553a'),
    'van-urbania': (290, 5, 'Force Urbania 17 seater illustration', '#f4a53c', True),
}.items():
    with open(os.path.join(OUT, name + '.svg'), 'w') as f:
        f.write(van(*args))
print('vans ok')
