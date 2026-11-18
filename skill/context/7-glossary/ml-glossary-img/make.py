#!/usr/bin/env python3
"""Builds the figures of ml-glossary.md as SVG files beside this script.

Every number drawn is either measured (measured.json, from measure.mjs, using csearch's local bge-base-en-v1.5),
computed here (gradient descent, the line and curve through the points, softmax), or taken from the glossary's own
text (rai's 64 of 96 and 0 of 72, RAM's 178 against the parser's 162). Two figures are drawn by hand to show an idea,
attention and calibration, and their captions in the glossary say so.
Run: python3 make.py
"""
import html, json, math, os, random

OUT = os.path.dirname(os.path.abspath(__file__))
PAPER, INK, GREY, LINE, MASS = '#F7F3ED', '#2D3436', '#6B6560', '#D9D0C3', '#ECE4D8'
RED, BLUE, AMBER, GREEN = '#C75B39', '#1F6FB2', '#B07D12', '#2E8A57'   # validated as a set, light mode
FONT = 'Inter, Helvetica, Arial, sans-serif'
W = 1000
esc = html.escape


def svg(name, h, body, title):
    defs = ''.join(f'<marker id="a{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                   f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for c in (INK, RED, GREY, BLUE))
    open(os.path.join(OUT, name), 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" font-family="{FONT}" '
        f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title><defs>{defs}</defs>'
        f'<rect width="{W}" height="{h}" fill="{PAPER}"/>{body}</svg>\n')


def t(x, y, s, size=18, fill=INK, weight=400, anchor='start', italic=False):
    st = ' font-style="italic"' if italic else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{st}>{esc(str(s))}</text>')


def tl(x, y, rows, size=18, gap=None, **k):
    gap = gap or size * 1.35
    return ''.join(t(x, y + i * gap, r, size, **k) for i, r in enumerate(rows))


def box(x, y, w, h, fill=MASS, stroke=None, rx=8, dash=False):
    s = f' stroke="{stroke}" stroke-width="2"' if stroke else ''
    d = ' stroke-dasharray="7 5"' if dash else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{s}{d}/>'


def arrow(x1, y1, x2, y2, c=INK, w=2.5):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" marker-end="url(#a{c[1:]})"/>'


def line(x1, y1, x2, y2, c=LINE, w=1.5):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"/>'


def path(pts, c, w=3, dash=False):
    d = ' stroke-dasharray="8 6"' if dash else ''
    return (f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{c}" '
            f'stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{d}/>')


def card(x, y, w, h, head, rows, fill=MASS, headfill=INK, size=17):
    return (box(x, y, w, h, fill) + box(x, y, w, 40, headfill, rx=8) + box(x, y + 30, w, 10, headfill, rx=0)
            + t(x + 16, y + 27, head, 17, PAPER, 600) + tl(x + 16, y + 70, rows, size))


M = json.load(open(os.path.join(OUT, 'measured.json')))

# 1 · Machine learning: rules written by hand, or a pattern found from examples ---------------------------------
b = t(40, 50, 'Two ways to make a program', 26, weight=700)
b += t(40, 100, 'Written by hand', 19, GREY, 600)
b += card(40, 120, 250, 110, 'A person writes', ['the rules, one by one'], headfill=GREY)
b += arrow(298, 175, 352, 175) + card(360, 120, 250, 110, 'Input', ['a new case'], headfill=GREY)
b += arrow(618, 175, 672, 175) + card(680, 120, 280, 110, 'Output', ['what the rules say'], headfill=GREY)
b += t(40, 290, 'Machine learning', 19, RED, 600)
b += card(40, 310, 250, 130, 'Many examples', ['each with its answer,', 'e.g. thousands of', 'handwritten 7s'], headfill=RED)
b += arrow(298, 375, 352, 375, RED) + card(360, 310, 250, 130, 'Training', ['finds the pattern', 'by itself'], headfill=RED)
b += arrow(618, 375, 672, 375, RED) + card(680, 310, 280, 130, 'A model', ['given a new case,', 'gives a prediction'], headfill=RED)
svg('rules-or-learning.svg', 470, b, 'Two ways to make a program: rules written by hand, or a model trained on examples')

# 2 · A neural network ---------------------------------------------------------------------------------------------
cols = [(160, 4, 'input'), (380, 6, 'layer 1'), (560, 6, 'layer 2'), (740, 6, 'layer 3'), (900, 2, 'output')]
pos = [[(x, 110 + (300 / (n + 1)) * (i + 1)) for i in range(n)] for x, n, _ in cols]
b = t(40, 50, 'A neural network: small parts joined in layers', 26, weight=700)
for a, c in zip(pos, pos[1:]):
    b += ''.join(line(x1, y1, x2, y2, LINE, 1.2) for x1, y1 in a for x2, y2 in c)
for k, ((x, n, lab), ps) in enumerate(zip(cols, pos)):
    col = BLUE if k == 0 else RED if k == len(cols) - 1 else INK
    b += ''.join(f'<circle cx="{px}" cy="{py:.1f}" r="15" fill="{col}"/>' for px, py in ps)
    b += t(x, 440, lab, 17, GREY, 600, 'middle')
b += box(330, 455, 460, 4, AMBER, rx=2) + t(560, 488, 'the hidden layers: “deep” means there are many', 17, INK, 600, 'middle')
svg('network.svg', 510, b, 'A neural network: an input, three hidden layers and an output, each part joined to the next layer')

# 3 · The training loop --------------------------------------------------------------------------------------------
b = t(40, 50, 'One turn of training, repeated many times', 26, weight=700)
steps = [(40, 'An example', ['a photo marked', '“mango”']), (270, 'The model guesses', ['“banana”']),
         (500, 'Loss', ['how wrong the', 'guess was']), (730, 'Turn the dials', ['a little, so the next', 'guess is less wrong'])]
for i, (x, h, rows) in enumerate(steps):
    b += card(x, 90, 210, 130, h, rows, headfill=RED if i == 2 else INK)
    if i < 3:
        b += arrow(x + 214, 155, x + 226, 155)
b += f'<path d="M835,226 C835,300 145,300 145,232" fill="none" stroke="{RED}" stroke-width="2.5" marker-end="url(#a{RED[1:]})"/>'
b += t(490, 318, 'next example', 17, RED, 600, 'middle')
svg('training-loop.svg', 340, b, 'One turn of training: an example, the model’s guess, the loss, a small turn of the dials, then the next example')

# 4 · Gradient descent and the learning rate (computed on the curve y = x²) -------------------------------------
def descend(rate, n=8, x=-3.0):
    out = [x]
    for _ in range(n):
        x = x - rate * 2 * x
        out.append(x)
    return out


b = t(40, 50, 'Walking downhill in fog: three sizes of step', 26, weight=700)
b += t(40, 80, 'Eight steps of gradient descent on the same valley, starting from the same place', 17, GREY)
for k, (rate, head, col) in enumerate([(0.1, 'About right: reaches the bottom', BLUE),
                                       (1.04, 'Too big: jumps across, further out each time', RED),
                                       (0.01, 'Too small: barely moves', AMBER)]):
    ox, ow, oy, oh = 40 + k * 320, 290, 120, 250
    sx = lambda x: ox + ow / 2 + x * ow / 2 / 6.5
    sy = lambda y: oy + oh - y * oh / 46
    b += box(ox, oy - 10, ow, oh + 60, MASS) + f'<clipPath id="d{k}"><rect x="{ox}" y="{oy - 10}" width="{ow}" height="{oh + 10}"/></clipPath><g clip-path="url(#d{k})">'
    b += path([(sx(x / 10), sy((x / 10) ** 2)) for x in range(-65, 66)], LINE, 3)
    xs = descend(rate)
    pts = [(sx(x), sy(x * x)) for x in xs]
    b += path(pts, col, 2)
    b += ''.join(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="{col}"/>' for px, py in pts)
    b += f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="9" fill="none" stroke="{INK}" stroke-width="2"/></g>'
    b += tl(ox + 14, oy + oh + 24, [head.split(':')[0] + ':', head.split(': ')[1]], 16, fill=INK, weight=600)
b += t(40, 445, 'The height is the loss. The circled dot is where training starts; the bottom is the least wrong the model can be.', 16, GREY)
svg('descent.svg', 465, b, 'Gradient descent with a step that is about right, too big and too small')

# 5 · Training, validation and test sets -------------------------------------------------------------------------
b = t(40, 50, 'One pile of examples, split three ways', 26, weight=700)
parts = [(0.7, 'Training set', 'the model learns from these', BLUE), (0.15, 'Validation', 'for choices while building', AMBER),
         (0.15, 'Test set', 'kept back until the end', RED)]
x = 40
for share, name, what, col in parts:
    w = 920 * share
    b += box(x, 90, w - 6, 70, col, rx=6) + t(x + 14, 133, name, 19, PAPER, 700)
    x += w
for i, (_, name, what, col) in enumerate(parts):
    b += box(40, 186 + i * 30, 16, 16, col, rx=3) + t(66, 200 + i * 30, f'{name}: {what}', 16)
b += t(40, 300, 'ungli calls the kept-back examples held-out cases. The shares shown are only an example.', 16, GREY)
svg('split.svg', 320, b, 'Examples split into a training set, a validation set and a test set kept back until the end')

# 6 · Overfitting: a straight line and a curve through every point ----------------------------------------------
rng = random.Random(7)
px = [i / 9 for i in range(10)]
py = [0.25 + 0.5 * x + rng.gauss(0, 0.08) for x in px]
mx, my = sum(px) / 10, sum(py) / 10
slope = sum((a - mx) * (c - my) for a, c in zip(px, py)) / sum((a - mx) ** 2 for a in px)
icept = my - slope * mx


def lagrange(x):
    return sum(yj * math.prod((x - xm) / (xj - xm) for m, xm in enumerate(px) if m != j) for j, (xj, yj) in enumerate(zip(px, py)))


new = (0.97, 0.25 + 0.5 * 0.97 + 0.02)
b = t(40, 50, 'Learning the examples, or learning the pattern', 26, weight=700)
for k, (head, f, col) in enumerate([('A simple line: misses each point a little', lambda x: icept + slope * x, BLUE),
                                     ('A curve through every point: odd details and all', lagrange, RED)]):
    ox, oy, ow, oh = 40 + k * 470, 120, 440, 300
    sx = lambda x: ox + 20 + x * (ow - 40)
    sy = lambda y: oy + oh - 20 - (y + 0.1) * (oh - 40) / 1.1
    clip = f'clip{k}'
    b += f'<clipPath id="{clip}"><rect x="{ox}" y="{oy}" width="{ow}" height="{oh}"/></clipPath>' + box(ox, oy, ow, oh, MASS)
    b += f'<g clip-path="url(#{clip})">' + path([(sx(i / 400), sy(f(i / 400))) for i in range(401)], col, 3) + '</g>'
    b += ''.join(f'<circle cx="{sx(a):.1f}" cy="{sy(c):.1f}" r="7" fill="{INK}"/>' for a, c in zip(px, py))
    nxp, nyp = sx(new[0]), sy(new[1])
    b += f'<circle cx="{nxp:.1f}" cy="{nyp:.1f}" r="9" fill="{PAPER}" stroke="{AMBER}" stroke-width="4"/>'
    miss = abs(f(new[0]) - new[1])
    b += tl(ox, oy - 30, [head], 16, fill=INK, weight=600)
    b += t(ox, oy + oh + 30, f'Off from the new example by {miss:.2f}', 16, AMBER if k else BLUE, 700)
b += t(40, 495, 'Black dots: training examples. Ringed dot: a new example the model never saw. Same ten points in both.', 16, GREY)
svg('overfit.svg', 515, b, 'Overfitting: a simple line misses the new example by a little; a curve through every training point misses it by more')

# 7 · Tokens (measured: the tokenizer of bge-base-en-v1.5, a BERT-family encoder) --------------------------------
b = t(40, 50, 'How one encoder splits text into tokens', 26, weight=700)
y = 100
for row in M['tokens']:
    b += t(40, y, row['sentence'], 19, GREY, italic=True)
    x = 40
    for tok in row['tokens']:
        cont = tok.startswith('##')
        w = 26 + len(tok) * 11.5
        b += box(x, y + 20, w, 46, AMBER if cont else BLUE, rx=6) + t(x + w / 2, y + 50, tok, 19, PAPER, 600, 'middle')
        x += w + 8
    b += t(x + 12, y + 50, f'{len(row["tokens"])} tokens', 17, INK, 600)
    y += 120
b += t(40, y + 4, 'A blue token starts a word; an amber token (marked ##) continues the word before it.', 16, GREY)
svg('tokens.svg', y + 26, b, 'Two sentences split into tokens; unquestionable becomes un, quest, ion and able')

# 8 · Attention (drawn by hand to show the idea) -----------------------------------------------------------------
words = ['the', 'bat', 'flew', 'out', 'of', 'the', 'cave']
weights = [0.05, None, 0.25, 0.08, 0.04, 0.05, 0.53]
b = t(40, 50, 'Which other words matter for understanding “bat”?', 26, weight=700)
xs = [90 + i * 135 for i in range(len(words))]
for i, (x, wd, wt) in enumerate(zip(xs, words, weights)):
    if wt is not None:
        h = 40 + abs(i - 1) * 32
        b += (f'<path d="M{xs[1]},250 C{xs[1]},{250 - h} {x},{250 - h} {x},250" fill="none" stroke="{RED}" '
              f'stroke-width="{2 + wt * 22:.1f}" stroke-linecap="round" opacity="0.85"/>')
for i, (x, wd) in enumerate(zip(xs, words)):
    b += box(x - 55, 262, 110, 50, INK if i == 1 else MASS, rx=6) + t(x, 295, wd, 21, PAPER if i == 1 else INK, 600, 'middle')
b += tl(40, 360, ['A thicker line means the word counts for more. Here “cave” counts most, so this bat is an animal,',
                  'not a cricket bat. The thicknesses are drawn by hand to show the idea; they are not measured.'], 16, fill=GREY)
svg('attention.svg', 400, b, 'Attention: lines from the word bat to the other words, thickest to cave')

# 9 · Temperature (made-up scores; the arithmetic is the one models use) ---------------------------------------
cands, scores = ['late', 'on time', 'slow', 'full'], [2.0, 1.2, 0.6, 0.1]
b = t(40, 50, 'The train is running ___', 26, weight=700, italic=True)
b += t(40, 80, 'How likely each next word is at three temperatures', 17, GREY)
for k, temp in enumerate([0.3, 1.0, 2.0]):
    e = [math.exp(s / temp) for s in scores]
    p = [v / sum(e) for v in e]
    ox = 40 + k * 320
    b += box(ox, 105, 300, 300, MASS) + t(ox + 16, 135, f'temperature {temp:g}', 18, INK, 700)
    for i, (c, v) in enumerate(zip(cands, p)):
        y = 160 + i * 58
        b += t(ox + 16, y + 22, c, 17) + box(ox + 100, y + 4, max(3, 150 * v), 26, BLUE, rx=3)
        b += t(ox + 108 + max(3, 150 * v), y + 24, f'{round(100 * v)}%', 16, INK, 600)
b += tl(40, 440, ['Low temperature: the likeliest word nearly always wins, so the same question gets the same answer more often.',
                  'High temperature: other words get a real chance. The four scores are made up; the arithmetic is the real one.'], 16, fill=GREY)
svg('temperature.svg', 480, b, 'Temperature: at 0.3 the word late gets almost all the chance; at 2 the four words are closer')

# 10 · The context window --------------------------------------------------------------------------------------
b = t(40, 50, 'What the pointer can see in a long text', 26, weight=700)
n = 60
for i in range(n):
    seen = i < 19
    b += box(40 + i * 15.3, 90, 12, 60, BLUE if seen else LINE, rx=2)
b += line(40, 170, 40 + 19 * 15.3 - 3, 170, BLUE, 3) + t(40, 198, 'about the first 380 tokens: read', 17, BLUE, 700)
b += t(40 + 19 * 15.3 + 10, 198, 'everything after: not seen at all', 17, GREY, 700)
b += t(40, 250, 'So in ungli a long text goes to the finder first, which picks the passage to give the pointer.', 16, GREY)
svg('context-window.svg', 270, b, 'A context window: the pointer reads about the first 380 tokens of a long text and sees nothing after')

# 11 · Embedding map (measured; 768 numbers flattened to 2) -----------------------------------------------------
pts = M['map']['points']
gcol = {'printer': RED, 'rain': BLUE, 'cricket': AMBER, 'crops': GREEN}
gname = {'printer': 'printers', 'rain': 'rain', 'cricket': 'cricket', 'crops': 'crops'}
X = [p['x'] for p in pts]; Y = [p['y'] for p in pts]
sx = lambda x: 300 + (x - min(X)) / (max(X) - min(X)) * 400
sy = lambda y: 140 + (max(Y) - y) / (max(Y) - min(Y)) * 400
b = t(40, 50, 'Twelve sentences placed by meaning', 26, weight=700)
b += t(40, 80, 'Each dot is one sentence, placed by an encoder. Sentences on one topic land near each other.', 17, GREY)
b += box(40, 110, 920, 460, MASS)
for g in gcol:
    gp = [p for p in pts if p['group'] == g]
    cx, cy = sum(sx(p['x']) for p in gp) / 3, sum(sy(p['y']) for p in gp) / 3
    b += ''.join(f'<circle cx="{sx(p["x"]):.1f}" cy="{sy(p["y"]):.1f}" r="9" fill="{gcol[g]}"/>' for p in gp)
    left = cx < 500
    ex_ = min(sx(p['x']) for p in gp) - 20 if left else max(sx(p['x']) for p in gp) + 20
    b += t(ex_, cy + 7, gname[g], 20, gcol[g], 700, 'end' if left else 'start')
for i, g in enumerate(gcol):
    ex = min((p for p in pts if p['group'] == g), key=lambda p: len(p['sentence']))['sentence']
    b += box(40, 590 + i * 28, 14, 14, gcol[g], rx=3) + t(64, 602 + i * 28, f'{gname[g]}, e.g. “{ex}”', 15, INK)
b += tl(40, 728, [f'Measured with bge-base-en-v1.5, which gives each sentence 768 numbers. Flattening 768 numbers to two keeps',
                  f'{round(100 * M["map"]["varianceShown"])}% of the differences between these sentences, so distances on the page are only roughly true.'], 15, fill=GREY)
svg('embedding-map.svg', 770, b, 'Twelve sentences on four topics, placed by an encoder: printers, rain, cricket and crops each form a group')

# 12 · Semantic search (measured) ------------------------------------------------------------------------------------
res = sorted(M['search']['results'], key=lambda r: -r['similarity'])
b = t(40, 50, f'Searching for “{M["search"]["query"]}”', 26, weight=700)
b += t(40, 80, 'How close in meaning each sentence is to the question, from 0 to 1', 17, GREY)
for i, r in enumerate(res):
    y = 110 + i * 56
    has_ink = 'ink' in r['passage'].lower().replace('.', ' ').split()
    b += t(40, y + 26, r['passage'], 17, INK, 600 if i == 0 else 400)
    b += box(500, y + 6, 360 * r['similarity'], 30, RED if i == 0 else BLUE, rx=3)
    b += t(510 + 360 * r['similarity'], y + 28, f'{r["similarity"]:.2f}', 16, INK, 600)
    if has_ink:
        b += t(930, y + 28, 'has “ink”', 14, AMBER, 700, 'end')
y = 110 + len(res) * 56 + 20
b += tl(40, y, ['The closest sentence never says “ink”. A search that matched words would have found only the form sentence.',
                'Measured with bge-base-en-v1.5, the encoder of csearch.'], 16, fill=GREY)
svg('semantic-search.svg', y + 40, b, 'Semantic search: the printer cartridges sentence is closest to ink for the printer, though it never says ink')

# 13 · An exam with and without minus marks --------------------------------------------------------------------
b = t(40, 50, 'What each answer can earn', 26, weight=700)
for k, (head, marks) in enumerate([('A test with no minus marks', [1, 0, 0]), ('JEE Main', [4, -1, 0])]):
    ox = 40 + k * 470
    b += box(ox, 80, 440, 300, MASS) + t(ox + 16, 112, head, 19, INK, 700)
    zero = 260
    b += line(ox + 20, zero, ox + 420, zero, GREY, 1.5)
    for i, (lab, v) in enumerate(zip(['guess, right', 'guess, wrong', '“I don’t know”'], marks)):
        x = ox + 40 + i * 130
        h = v * (100 if k == 0 else 25)
        col = GREEN if v > 0 else RED if v < 0 else GREY
        b += box(x, zero - max(h, 0), 90, max(abs(h), 3), col, rx=3)
        b += t(x + 45, zero - max(h, 0) - 10 if v >= 0 else zero - h + 24, f'{v:+d}' if v else '0', 18, INK, 700, 'middle')
        b += t(x + 45, 365, lab, 15, INK, 400, 'middle')
b += tl(40, 415, ['With no minus marks a guess can only gain, and “I don’t know” never scores, so guessing pays.',
                  'Kalai and colleagues (2025): nine of the ten most influential benchmarks they looked at are marked the first way.'], 16, fill=GREY)
svg('minus-marks.svg', 455, b, 'Marks for a right guess, a wrong guess and I don’t know, with and without minus marks')

# 14 · rai: what it found and what it let through (from the glossary: 64 of 96, 0 of 72) -------------------------
b = t(40, 50, 'rai, measured: 96 real answers and 72 non-answers', 26, weight=700)
cells = [(0, 0, 64, 'real answers it found', GREEN), (1, 0, 32, 'real answers it missed (false negatives)', AMBER),
         (0, 1, 0, 'non-answers it let through (false positives)', RED), (1, 1, 72, 'non-answers it turned away', BLUE)]
b += t(350, 100, 'rai said: an answer', 17, INK, 700, 'middle') + t(740, 100, 'rai said: not an answer', 17, INK, 700, 'middle')
b += tl(40, 175, ['real', 'answers'], 17, fill=INK, weight=700) + tl(40, 325, ['non-', 'answers'], 17, fill=INK, weight=700)
for c, r, v, lab, col in cells:
    x, y = 160 + c * 390, 115 + r * 150
    b += box(x, y, 370, 135, col if v else MASS, stroke=None if v else RED)
    fg = PAPER if v else RED
    b += t(x + 24, y + 70, str(v), 46, fg, 700) + t(x + 24, y + 108, lab, 16, fg, 600)
b += tl(40, 450, ['Recall: it found 64 of the 96 real answers, about two in three.',
                  'Precision: of the 64 it called answers, all 64 were right, because it let no non-answer through.',
                  'ungli would rather miss a real answer than accept a non-answer.'], 16, fill=GREY)
svg('rai-results.svg', 530, b, 'rai found 64 of 96 real answers, missed 32, let none of 72 non-answers through and turned away all 72')

# 15 · A baseline (from the glossary: 162 and 178 of 178) --------------------------------------------------------
b = t(40, 50, 'Does the model add anything? Compare it with something simple', 26, weight=700)
for i, (lab, v, col) in enumerate([('a plain parser on its own (the baseline)', 162, GREY), ('RAM', 178, RED)]):
    y = 100 + i * 80
    b += t(40, y + 32, lab, 18, INK, 600) + box(420, y + 8, 500 * v / 178, 38, col, rx=4)
    b += t(430 + 500 * v / 178 - 20, y + 34, f'{v} of 178', 17, PAPER, 700, 'end')
b += t(40, 290, 'Acts in office notes given the right doer (or nobody, where the note named nobody), on five test sets written', 16, GREY)
b += t(40, 314, 'by models and marked by hand. Notes written by office staff have not been measured yet.', 16, GREY)
svg('baseline.svg', 335, b, 'A plain parser got 162 of 178 acts right; RAM got all 178')

# 16 · Calibration (drawn by hand to show the idea) --------------------------------------------------------------
ox, oy, ow, oh = 140, 90, 420, 420
sx = lambda v: ox + v * ow
sy = lambda v: oy + oh - v * oh
b = t(40, 50, 'Is the model right as often as it says?', 26, weight=700) + box(ox, oy, ow, oh, MASS)
for v in (0, .2, .4, .6, .8, 1):
    b += line(sx(v), oy, sx(v), oy + oh) + line(ox, sy(v), ox + ow, sy(v))
    b += t(sx(v), oy + oh + 26, f'{round(v * 100)}%', 14, GREY, 400, 'middle') + t(ox - 10, sy(v) + 5, f'{round(v * 100)}%', 14, GREY, 400, 'end')
b += path([(sx(0), sy(0)), (sx(1), sy(1))], BLUE, 3)
b += path([(sx(v / 20), sy((v / 20) ** 1.8)) for v in range(21)], RED, 3, dash=True)
b += f'<circle cx="{sx(.7):.1f}" cy="{sy(.7):.1f}" r="9" fill="{BLUE}"/>'
b += t(ox + ow / 2, oy + oh + 56, 'how sure the model says it is', 16, INK, 600, 'middle')
b += f'<text transform="translate(70,{oy + oh / 2}) rotate(-90)" font-size="16" font-weight="600" fill="{INK}" text-anchor="middle">how often it is right</text>'
b += t(600, 140, 'Well calibrated', 19, BLUE, 700) + tl(600, 168, ['of the answers it gives 70%,', 'about seven in ten are right'], 16)
b += t(600, 290, 'Overconfident', 19, RED, 700) + tl(600, 318, ['it says 70%, but is right', 'less often than that'], 16)
b += tl(600, 440, ['Both lines are drawn by hand', 'to show the idea; they are', 'not measured from a model.'], 15, fill=GREY)
svg('calibration.svg', 590, b, 'Calibration: a well calibrated model lies on the diagonal; an overconfident one falls below it')

# 17 · The collapse, and the split -------------------------------------------------------------------------------
b = t(40, 50, 'One channel, or two', 26, weight=700)
b += t(40, 98, 'The collapse', 19, RED, 700)
b += card(40, 115, 200, 100, 'An essay', ['in'], headfill=GREY) + arrow(246, 165, 300, 165, RED)
b += card(306, 115, 330, 100, 'A chat model', ['reads it and judges it', 'in one step'], headfill=RED) + arrow(642, 165, 696, 165, RED)
b += card(702, 115, 258, 100, 'Verdict: “good”', ['nobody can see why'], headfill=RED)
b += t(40, 270, 'Kept apart', 19, BLUE, 700)
b += card(40, 287, 200, 120, 'Language work', ['a model or a person', 'reads and describes'], headfill=BLUE) + arrow(246, 347, 300, 347, BLUE)
b += card(306, 287, 200, 120, 'Signals', ['a category, a score,', 'an embedding'], headfill=BLUE) + arrow(512, 347, 566, 347, BLUE)
b += card(572, 287, 180, 120, 'Judgement work', ['rules people wrote,', 'or a person'], headfill=INK) + arrow(758, 347, 812, 347, INK)
b += card(818, 287, 142, 120, 'Verdict', ['its reasons', 'can be read'], headfill=INK)
svg('collapse.svg', 430, b, 'The collapse: one model reads and judges in one step; kept apart: signals go to rules people wrote, which give the verdict')

# 18 · Koher's older tools: three layers ---------------------------------------------------------------------------
b = t(40, 50, 'The three layers of Koher’s older tools', 26, weight=700)
lay = [('1 · Qualification', ['a model or a person', 'reads the input and', 'picks out signals'], BLUE),
       ('2 · Rules', ['deterministic code', 'people wrote; the', 'decision is made here'], INK),
       ('3 · Language layer', ['a model narrates the', 'decision; a list of', 'forbidden strings checks it'], AMBER)]
for i, (h, rows, col) in enumerate(lay):
    x = 40 + i * 320
    b += card(x, 80, 290, 160, h, rows, headfill=col)
    if i < 2:
        b += arrow(x + 294, 160, x + 316, 160)
b += t(40, 280, 'In Koher’s new work, no model writes at all.', 16, GREY)
svg('three-layers.svg', 300, b, 'Koher’s older tools: qualification, then rules, then a language layer that narrates the decision')

# 19 · A pointer --------------------------------------------------------------------------------------------------
sent = ['The file was received on Monday.', 'The matter will be examined.', 'A reply will be sent in due course.']
b = t(40, 50, 'A pointer answers with a number, or with nothing', 26, weight=700)
b += box(40, 80, 520, 190, MASS)
for i, s in enumerate(sent):
    b += box(56, 98 + i * 56, 40, 40, INK, rx=6) + t(76, 125 + i * 56, str(i + 1), 19, PAPER, 700, 'middle') + t(110, 125 + i * 56, s, 18)
for k, (q, a, col) in enumerate([('When was the file received?', '1', BLUE), ('Who will examine the matter?', 'nothing', RED)]):
    y = 96 + k * 100
    b += t(600, y + 10, q, 18, INK, 600) + arrow(600, y + 34, 660, y + 34, col)
    b += box(668, y + 14, 150 if a == 'nothing' else 60, 40, col, rx=6) + t(678, y + 41, a, 18, PAPER, 700)
b += t(40, 310, 'The note names nobody, so the pointer points at nothing. It cannot write a word of its own.', 16, GREY)
svg('pointer.svg', 330, b, 'A pointer answers when was the file received with sentence 1, and who will examine the matter with nothing')

# 20 · ungli: layers, the window, don't know, the top call --------------------------------------------------
b = t(40, 50, 'ungli: small models in layers', 26, weight=700)
b += box(40, 80, 920, 50, INK, rx=8) + t(60, 112, 'The router: a table people wrote sends each kind of case through its layers, in order', 17, PAPER, 600)
lay = [('Finder', 'number of the closest passage'), ('Pointer or reader', 'number of a sentence, or words'), ('Chooser', 'number of an item on a list')]
for i, (h, what) in enumerate(lay):
    x = 40 + i * 250
    b += box(x, 160, 220, 150, MASS) + t(x + 16, 192, h, 19, INK, 700) + tl(x + 16, 222, [what, 'or nothing'], 15, fill=GREY)
    b += box(x + 16, 262, 188, 34, BLUE, rx=6) + t(x + 110, 285, 'code checks the answer', 15, PAPER, 600, 'middle')
    b += arrow(x + 224, 235, x + 246, 235) if i < 2 else ''
b += arrow(780, 235, 800, 235)
b += card(806, 160, 154, 150, 'Top call', ['from a list', 'written in', 'advance'], headfill=GREEN, size=16)
b += arrow(400, 312, 400, 358, RED)
b += box(140, 362, 520, 76, PAPER, stroke=RED) + t(160, 394, 'Anything else, or an answer scored too low: don’t know', 17, RED, 700)
b += t(160, 420, 'the case goes to a person, or to rules people wrote in advance', 16, INK)
b += t(40, 478, 'No model writes a word. Each answers through the window: a number, or nothing. One route is shown.', 16, GREY)
svg('synapse.svg', 500, b, 'ungli: a router sends a case through a finder, a pointer and a chooser; code checks each answer; anything else is don’t know')


# ===================== second batch: every remaining hard idea =====================

# 21 · Score and probability -------------------------------------------------------------------------------------
b = t(40, 50, 'A score of 0.9', 26, weight=700)
b += t(40, 80, 'The model rates this answer at nine in ten. It is still a prediction, not a known fact.', 17, GREY)
for i in range(10):
    b += box(40 + i * 92, 110, 80, 80, BLUE if i < 9 else MASS, stroke=None if i < 9 else BLUE, rx=6)
b += line(40, 230, 960, 230, GREY, 2)
for v in (0, 0.5, 0.9, 1):
    x = 40 + v * 920
    b += line(x, 222, x, 238, INK, 2) + t(x, 262, f'{v:g}', 17, INK, 700 if v == 0.9 else 400, 'middle')
b += t(40, 300, '0: does not fit at all', 16, GREY) + t(960, 300, '1: fits completely', 16, GREY, anchor='end')
svg('score.svg', 320, b, 'A score of 0.9 shown as nine of ten squares filled, on a scale from 0 to 1')

# 22 · Chatbot and agent ------------------------------------------------------------------------------------------
b = t(40, 50, 'A chatbot answers; an agent goes on by itself', 26, weight=700)
b += card(40, 90, 200, 100, 'You type', ['a question'], headfill=GREY) + arrow(246, 140, 296, 140)
b += card(302, 90, 220, 100, 'The model', ['writes a reply'], headfill=INK)
b += t(560, 145, 'A chatbot stops here.', 18, GREY, 600)
b += card(40, 240, 200, 100, 'You type', ['a task'], headfill=GREY) + arrow(246, 290, 296, 290, RED)
b += card(302, 240, 220, 100, 'The model', ['answers, then', 'picks a next step'], headfill=RED) + arrow(528, 290, 578, 290, RED)
b += card(584, 240, 376, 100, 'Steps it takes on its own', ['search the web, run code,', 'call other programs, and again'], headfill=RED)
b += f'<path d="M772,346 C772,410 412,410 412,350" fill="none" stroke="{RED}" stroke-width="2.5" marker-end="url(#a{RED[1:]})"/>'
b += t(40, 450, 'In ungli, a model that plans the order of steps, or writes a step for another model, is outside the method.', 16, GREY)
svg('agent.svg', 470, b, 'A chatbot writes one reply; an agent answers and then takes further steps on its own, again and again')

# 23 · Parameters: 33 million against 175 billion (numbers from the glossary) -----------------------------------
n = round(175e9 / 33e6)
b = t(40, 50, 'How many dials? One square is 33 million parameters', 26, weight=700)
b += box(40, 90, 14, 14, RED, rx=2) + t(66, 103, 'the reader inside rai: about 33 million, one square', 17, INK, 600)
b += t(40, 140, f'GPT-3, an early large model: 175 billion, about {n:,} squares', 17, INK, 600)
cols_, sz = 120, 7.6
for i in range(n):
    r, c = divmod(i, cols_)
    b += f'<rect x="{40 + c * sz:.1f}" y="{160 + r * sz:.1f}" width="{sz - 1.6:.1f}" height="{sz - 1.6:.1f}" fill="{RED if i == 0 else BLUE}"/>'
h = 160 + (n // cols_ + 1) * sz
b += t(40, h + 34, 'Every square is as big as the whole of rai’s reader, which is the red one at the top left.', 16, GREY)
svg('parameters.svg', h + 56, b, 'Parameters: rai’s reader is one square of 33 million; GPT-3 is about 5,300 such squares')

# 24 · Base model and checkpoint -----------------------------------------------------------------------------------
b = t(40, 50, 'One base model, two readers', 26, weight=700)
b += t(40, 98, 'checkpoints: copies saved during training', 16, GREY)
b += line(40, 130, 420, 130, INK, 3)
for i in range(5):
    b += f'<circle cx="{60 + i * 85}" cy="130" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
b += arrow(424, 130, 470, 130) + card(476, 90, 200, 80, 'Base model', ['someone else trained'], headfill=INK)
b += arrow(680, 120, 740, 85, BLUE) + arrow(680, 140, 740, 185, RED)
b += card(746, 50, 214, 80, 'rai’s reader', ['fine-tuned from it'], headfill=BLUE)
b += card(746, 150, 214, 80, 'RAM’s reader', ['fine-tuned from it'], headfill=RED)
b += t(40, 270, 'Starting from a base model saves training from nothing; the readers in rai and RAM share the same base.', 16, GREY)
svg('base-model.svg', 290, b, 'A base model, saved at checkpoints during its training, from which rai’s and RAM’s readers are both fine-tuned')

# 25 · Three ways to learn ----------------------------------------------------------------------------------------
b = t(40, 50, 'Three ways a model can learn', 26, weight=700)
kinds = [('Supervised', BLUE, ['each example comes', 'with its answer:'], ['an email', '→ “spam”']),
         ('Self-supervised', AMBER, ['the data supplies', 'its own answer:'], ['the ___ flew out', 'of the cave → bat']),
         ('Reinforcement', RED, ['a try gets a score,', 'and good tries win:'], ['try → score 7/10', '→ nudge towards it'])]
for i, (h, col, rows, ex) in enumerate(kinds):
    x = 40 + i * 315
    b += card(x, 80, 295, 210, h, rows, headfill=col)
    b += box(x + 16, 180, 263, 90, PAPER, rx=6) + tl(x + 30, 214, ex, 18, fill=INK, weight=600)
svg('three-ways.svg', 310, b, 'Supervised learning uses labelled examples; self-supervised hides a word; reinforcement learning rewards good tries')

# 26 · Epoch and batch --------------------------------------------------------------------------------------------
b = t(40, 50, 'Batches and epochs', 26, weight=700)
b += t(40, 80, '24 examples in six batches of four. The dials are nudged after each batch.', 17, GREY)
for e in range(2):
    y = 110 + e * 120
    b += t(40, y + 42, f'epoch {e + 1}', 18, INK, 700)
    for bt in range(6):
        x = 150 + bt * 135
        b += box(x, y, 120, 70, MASS, rx=6)
        b += ''.join(box(x + 10 + k * 26, y + 12, 20, 30, BLUE if e == 0 else AMBER, rx=3) for k in range(4))
        b += t(x + 60, y + 62, f'batch {bt + 1}', 13, GREY, 400, 'middle')
        b += t(x + 128, y + 40, '▸', 14, RED, 700, 'middle') if bt < 5 else ''
b += t(40, 370, 'One epoch is one full pass through all 24. Training usually runs several epochs.', 16, GREY)
b += t(40, 394, 'Each small ▸ is a nudge of the dials.', 16, RED)
svg('epochs.svg', 415, b, 'Two epochs, each a pass through six batches of four examples, with a nudge after each batch')

# 27 · Parameters and hyperparameters -------------------------------------------------------------------------------
b = t(40, 50, 'Who sets which numbers', 26, weight=700)
b += card(40, 90, 280, 150, 'People choose, before', ['hyperparameters:', 'the learning rate,', 'the number of epochs'], headfill=GREY)
b += arrow(326, 165, 376, 165) + card(382, 90, 200, 150, 'Training', ['runs with those', 'settings'], headfill=INK)
b += arrow(588, 165, 638, 165, BLUE) + card(644, 90, 316, 150, 'The model learns', ['parameters: the millions', 'of dials inside it'], headfill=BLUE)
svg('hyperparameters.svg', 270, b, 'People choose hyperparameters before training; training then sets the model’s parameters')

# 28 · Random seed (drawn to show the idea) --------------------------------------------------------------------
b = t(40, 50, 'The same seed, or different seeds', 26, weight=700)
b += t(40, 98, 'seed 42, twice', 18, INK, 700) + box(220, 78, 300, 30, LINE, rx=4)
b += f'<circle cx="400" cy="93" r="10" fill="{BLUE}"/><circle cx="400" cy="93" r="5" fill="{PAPER}"/>'
b += t(540, 99, 'the same model, the same result (usually)', 16, INK)
b += t(40, 168, 'five seeds', 18, INK, 700) + box(220, 148, 300, 30, LINE, rx=4)
b += ''.join(f'<circle cx="{x}" cy="163" r="10" fill="{RED}" opacity="0.85"/>' for x in (372, 386, 401, 412, 428))
b += t(540, 169, 'slightly different models, close results', 16, INK)
b += t(40, 230, 'A result that holds over several seeds is less likely to be luck. Positions drawn to show the idea, not measured.', 16, GREY)
svg('seed.svg', 250, b, 'One seed run twice gives the same result; five seeds give results close to each other')

# 29 · Quantisation ------------------------------------------------------------------------------------------------
b = t(40, 50, 'Quantisation: the same numbers, kept with fewer digits', 26, weight=700)
for i, (lab, num, w, col) in enumerate([('full precision', '3.14159265', 640, BLUE), ('quantised', '3.14', 160, AMBER)]):
    y = 100 + i * 90
    b += t(40, y + 34, lab, 18, INK, 700) + box(240, y, w, 52, col, rx=6) + t(256, y + 35, num, 22, PAPER, 700)
b += t(40, 290, 'Every one of the millions of dials is rounded like this. The model takes less memory and runs faster,', 16, GREY)
b += t(40, 314, 'but may answer a little less well, so how much accuracy is lost has to be measured.', 16, GREY)
svg('quantisation.svg', 335, b, 'Quantisation: 3.14159265 stored as 3.14, taking less room')

# 30 · One token after another --------------------------------------------------------------------------------
b = t(40, 50, 'A large language model writes one token at a time', 26, weight=700)
seq = ['The train is running', 'late', 'again', 'today', '.']
for step in range(1, 5):
    y = 80 + (step - 1) * 66
    x = 40
    for k, w_ in enumerate(seq[:step + 1]):
        new_ = k == step
        wd = 26 + len(w_) * 11
        b += box(x, y, wd, 44, RED if new_ else MASS, rx=6) + t(x + wd / 2, y + 29, w_, 18, PAPER if new_ else INK, 600, 'middle')
        x += wd + 8
    b += t(x + 10, y + 29, f'step {step}: add the likeliest next token', 15, GREY)
b += t(40, 370, 'Each new token is chosen from what came before, then becomes part of what the next one is chosen from.', 16, GREY)
svg('next-token.svg', 390, b, 'A language model writing one token at a time: late, again, today, and a full stop')

# 31 · Reading both ways, or only backwards ---------------------------------------------------------------------
words = ['the', 'bat', 'flew', 'out', 'of', 'the', 'cave']
b = t(40, 50, 'Which words can “out” look at?', 26, weight=700)
for k, (h, both) in enumerate([('An encoder such as BERT: both directions', True), ('A model that writes: only the words before', False)]):
    y = 100 + k * 150
    b += t(40, y, h, 18, INK, 700)
    for i, w_ in enumerate(words):
        x = 40 + i * 132
        seen = i != 3 and (both or i < 3)
        col = INK if i == 3 else (BLUE if seen else MASS)
        b += box(x, y + 20, 116, 50, col, rx=6) + t(x + 58, y + 52, w_, 19, PAPER if col != MASS else GREY, 600, 'middle')
b += t(40, 410, 'Blue: words “out” can use. Grey: words it cannot see yet, because a writing model has not written them.', 16, GREY)
svg('directions.svg', 430, b, 'An encoder lets a word look at every other word; a writing model lets it look only at the words before')

# 32 · Encoder or writer ------------------------------------------------------------------------------------------
b = t(40, 50, 'Two kinds of language model', 26, weight=700)
b += card(40, 90, 260, 110, 'Text', ['“the printer', 'cartridges are over”'], headfill=GREY) + arrow(306, 145, 356, 145, BLUE)
b += card(362, 90, 200, 110, 'An encoder', ['reads'], headfill=BLUE) + arrow(568, 145, 618, 145, BLUE)
b += card(624, 90, 336, 110, 'Numbers', ['0.12, −0.40, 0.07 … (768 of them)', 'no words written'], headfill=BLUE)
b += card(40, 240, 260, 110, 'Text', ['“the printer', 'cartridges are over”'], headfill=GREY) + arrow(306, 295, 356, 295, RED)
b += card(362, 240, 200, 110, 'A writing model', ['reads, then writes'], headfill=RED) + arrow(568, 295, 618, 295, RED)
b += card(624, 240, 336, 110, 'More text', ['“so please order new', 'ones by Friday”'], headfill=RED)
b += t(40, 390, 'In ungli none of the models writes. Each answers with a number, or with nothing.', 16, GREY)
svg('encoder-writer.svg', 410, b, 'An encoder turns text into numbers; a writing model turns text into more text')

# 33 · Distillation (from the glossary: half the size, over 99% on some tests) ----------------------------------
b = t(40, 50, 'Distillation: a small student copies a big teacher', 26, weight=700)
b += box(40, 90, 360, 220, BLUE, rx=10) + t(220, 190, 'teacher', 28, PAPER, 700, 'middle') + t(220, 225, 'the bigger model', 17, PAPER, 400, 'middle')
b += arrow(410, 200, 520, 200, INK) + t(465, 185, 'copies how it', 14, INK, 600, 'middle') + t(465, 230, 'pays attention', 14, INK, 600, 'middle')
b += box(530, 122, 255, 156, RED, rx=10) + t(657, 198, 'student', 24, PAPER, 700, 'middle') + t(657, 226, 'half the size', 15, PAPER, 400, 'middle')
b += tl(805, 175, ['kept over 99%', 'of the teacher’s', 'accuracy on', 'some tests'], 17, fill=INK, weight=600)
b += t(40, 350, 'MiniLM, from Wang and colleagues (2020). Boxes drawn to the ratio of size: the student has half the parameters.', 16, GREY)
svg('distillation.svg', 370, b, 'Distillation: a student model half the size of its teacher kept over 99% of its accuracy on some tests')

# 34 · The window, not the door ----------------------------------------------------------------------------------
b = t(40, 50, 'The size of the window, not the door', 26, weight=700)
b += box(60, 90, 520, 330, MASS, stroke=INK, rx=4)
b += box(110, 190, 160, 230, INK, rx=4) + t(190, 300, 'the door', 18, PAPER, 700, 'middle') + tl(130, 335, ['the model’s', 'own size: any'], 14, fill=PAPER)
b += box(400, 150, 90, 70, PAPER, stroke=RED, rx=4) + t(445, 195, '3', 30, RED, 700, 'middle')
b += arrow(492, 185, 620, 185, RED)
b += t(630, 175, 'the window', 20, RED, 700) + tl(630, 205, ['what comes out of the model:', 'a few tokens, all of them', 'a number from a list,', 'or nothing'], 17, fill=INK)
b += tl(630, 345, ['Code holds the window small', 'when the model is called,', 'and checks what comes out.'], 16, fill=GREY)
svg('window-door.svg', 450, b, 'A house with a big door, the model’s size, and a small window, its output: a number or nothing')

# 35 · Hosted or on your own machine -------------------------------------------------------------------------------
b = t(40, 50, 'Where the model runs', 26, weight=700)
b += card(40, 90, 420, 150, 'On your own computer', ['the model runs here', 'no answer carries a fee', 'what you send stays here'], headfill=GREEN)
b += card(540, 90, 420, 150, 'Hosted', ['the model runs on somebody else’s', 'computers, reached over the internet', 'through an API; usually paid per answer'], headfill=AMBER)
b += t(40, 280, 'ungli prefers models that run on your own machine.', 16, GREY)
svg('hosted-local.svg', 300, b, 'A model on your own computer, with no fee per answer, or a hosted model reached through an API and paid per answer')

# 36 · CPU and GPU -------------------------------------------------------------------------------------------------
b = t(40, 50, 'A few strong workers, or thousands of small ones', 26, weight=700)
b += box(40, 90, 420, 260, MASS) + t(60, 122, 'CPU', 20, INK, 700) + t(60, 146, 'a few cores, each does anything', 15, GREY)
b += ''.join(box(80 + (i % 4) * 92, 170 + (i // 4) * 88, 76, 72, BLUE, rx=6) for i in range(8))
b += box(540, 90, 420, 260, MASS) + t(560, 122, 'GPU', 20, INK, 700) + t(560, 146, 'many cores, each does small sums', 15, GREY)
b += ''.join(box(560 + (i % 32) * 12, 166 + (i // 32) * 12, 9, 9, RED, rx=1) for i in range(32 * 14))
b += t(40, 385, 'Training needs huge numbers of small sums at once, which is what a GPU is for. A CPU is enough to run rai’s and RAM’s readers.', 15, GREY)
svg('cpu-gpu.svg', 405, b, 'A CPU with a few large cores and a GPU with hundreds of small ones')

# 37 · Vector --------------------------------------------------------------------------------------------------------
b = t(40, 50, 'A vector is a list of numbers in a fixed order', 26, weight=700)
b += box(40, 90, 330, 250, MASS)
b += line(70, 310, 340, 310, INK, 2) + line(70, 310, 70, 110, INK, 2)
b += t(340, 332, 'east', 14, GREY, 400, 'end') + t(78, 120, 'north', 14, GREY)
b += f'<circle cx="{70 + 3 * 60}" cy="{310 - 2 * 60}" r="10" fill="{RED}"/>' + t(70 + 3 * 60 + 16, 310 - 2 * 60 - 12, '[3, 2]', 18, INK, 700)
b += t(410, 140, 'A point on a map: two numbers', 19, INK, 700) + t(410, 170, '3 east, 2 north', 17)
b += t(410, 240, 'An embedding: hundreds of numbers', 19, INK, 700)
b += box(410, 258, 550, 44, PAPER, stroke=LINE, rx=6) + t(424, 287, '[0.12, −0.40, 0.07, 0.31, … 768 numbers]', 18, BLUE, 600)
svg('vector.svg', 360, b, 'A vector: a point on a map is two numbers; an embedding is hundreds')

# 38 · Three ways to search by meaning ----------------------------------------------------------------------------
b = t(40, 50, 'Three ways to match a question with passages', 26, weight=700)
rows3 = [('Encoder (as in the finder)', BLUE, ['each passage is turned into numbers once, ahead of time;', 'the question’s numbers are compared with them: fast']),
         ('Late interaction (ColBERT)', AMBER, ['numbers kept for every word of a passage,', 'so finer details can match']),
         ('Cross-encoder (re-ranker)', RED, ['reads the question and one passage together;', 'nothing can be worked out in advance: slower'])]
for i, (h, col, rows) in enumerate(rows3):
    y = 80 + i * 110
    b += box(40, y, 300, 90, col, rx=8) + t(56, y + 52, h, 18, PAPER, 700) + tl(370, y + 38, rows, 17)
b += t(40, 425, 'In ungli the last two are used only where a measurement shows they help.', 16, GREY)
svg('search-kinds.svg', 445, b, 'Three ways to search by meaning: an encoder, late interaction and a cross-encoder')

# 39 · RAG, and what ungli keeps -----------------------------------------------------------------------------
b = t(40, 50, 'Retrieval-augmented generation, and what ungli keeps', 26, weight=700)
b += t(40, 98, 'RAG', 19, AMBER, 700)
for i, (h, col) in enumerate([('Question', GREY), ('Search finds passages', BLUE), ('A writing model', AMBER), ('A written answer', AMBER)]):
    x = 40 + i * 235
    b += box(x, 110, 215, 70, col, rx=8) + tl(x + 14, 140, [h], 16, fill=PAPER, weight=600)
    b += arrow(x + 217, 145, x + 233, 145) if i < 3 else ''
b += t(40, 238, 'ungli', 19, BLUE, 700)
for i, (h, col) in enumerate([('Question', GREY), ('Search finds passages', BLUE), ('The number of a passage, or nothing', BLUE)]):
    x = 40 + i * 235
    w_ = 215 if i < 2 else 450
    b += box(x, 250, w_, 70, col, rx=8) + t(x + 14, 291, h, 16, PAPER, 600)
    b += arrow(x + 217, 285, x + 233, 285) if i < 2 else ''
b += t(40, 360, 'ungli keeps the search and leaves out the writing.', 16, GREY)
svg('rag.svg', 380, b, 'RAG: a search finds passages and a writing model answers from them; ungli keeps the search and drops the writing')

# 40 · A classifier ------------------------------------------------------------------------------------------------
b = t(40, 50, 'A classifier sorts into groups chosen in advance', 26, weight=700)
b += card(40, 90, 230, 100, 'An email', ['“You have won …”'], headfill=GREY) + arrow(276, 140, 326, 140)
b += card(332, 90, 220, 100, 'A classifier', ['a model'], headfill=INK)
b += arrow(558, 125, 620, 105, RED) + arrow(558, 155, 620, 175, BLUE)
b += box(626, 80, 200, 50, RED, rx=6) + t(642, 112, 'spam', 18, PAPER, 700)
b += box(626, 150, 200, 50, MASS, stroke=BLUE, rx=6) + t(642, 182, 'not spam', 18, BLUE, 700)
b += t(40, 250, 'The groups exist before the model sees anything. It cannot invent a new one.', 16, GREY)
svg('classifier.svg', 270, b, 'A classifier sorting an email into spam or not spam')

# 41 · Zero-shot, few-shot, training ----------------------------------------------------------------------------
b = t(40, 50, 'How many worked examples the model gets', 26, weight=700)
for i, (h, k, note, col) in enumerate([('Zero-shot', 0, 'just the job, in words', BLUE), ('Few-shot', 3, 'a handful in the prompt', AMBER),
                                       ('Training', 40, 'many, to learn from', RED)]):
    x = 40 + i * 315
    b += box(x, 80, 295, 200, MASS) + t(x + 16, 112, h, 20, col, 700) + t(x + 16, 138, note, 15, GREY)
    b += ''.join(box(x + 16 + (j % 10) * 26, 156 + (j // 10) * 26, 20, 20, col, rx=3) for j in range(k))
    b += t(x + 16, 262, 'no examples', 15, INK, 600) if k == 0 else ''
svg('shots.svg', 300, b, 'Zero-shot gets no worked examples, few-shot a handful, training many')

# 42 · Human feedback and sycophancy ---------------------------------------------------------------------------
b = t(40, 50, 'Training on people’s ratings, and how it can teach flattery', 26, weight=700)
b += card(40, 90, 260, 140, 'The model answers twice', ['A: agrees with you', 'B: disagrees, with reasons'], headfill=INK)
b += arrow(306, 160, 356, 160) + card(362, 90, 260, 140, 'A person picks one', ['often the answer that', 'agreed with them'], headfill=AMBER)
b += arrow(628, 160, 678, 160) + card(684, 90, 276, 140, 'The model is nudged', ['towards the picked answer'], headfill=RED)
b += f'<path d="M822,236 C822,300 170,300 170,236" fill="none" stroke="{RED}" stroke-width="2.5" marker-end="url(#a{RED[1:]})"/>'
b += tl(40, 335, ['Repeated many times, the model learns what people prefer, including agreement over truth.',
                  'Sharma and colleagues (2024) found signs that part of sycophancy comes from this.'], 16, fill=GREY)
svg('human-feedback.svg', 375, b, 'Human feedback: people pick between two answers, the model is nudged towards their choice, and can learn to agree')

# 43 · Black box, or rules anyone can read -------------------------------------------------------------------------
b = t(40, 50, 'Can the person affected read the reasons?', 26, weight=700)
b += t(40, 98, 'A black box', 19, RED, 700)
b += card(40, 110, 200, 90, 'Input', ['an application'], headfill=GREY) + arrow(246, 155, 296, 155)
b += box(302, 110, 220, 90, INK, rx=8) + t(412, 162, '? ? ?', 26, PAPER, 700, 'middle') + arrow(528, 155, 578, 155)
b += card(584, 110, 200, 90, 'Answer', ['“rejected”'], headfill=RED)
b += t(40, 258, 'Readable rules', 19, BLUE, 700)
b += card(40, 270, 200, 120, 'Input', ['an application'], headfill=GREY) + arrow(246, 330, 296, 330)
b += box(302, 270, 300, 120, PAPER, stroke=BLUE, rx=8) + tl(318, 300, ['if the income certificate', 'is missing:', '  ask for it, do not reject'], 16, fill=INK)
b += arrow(608, 330, 658, 330) + card(664, 270, 200, 120, 'Answer', ['with its rule'], headfill=BLUE)
svg('black-box.svg', 410, b, 'A black box gives an answer with no visible reasons; readable rules show the rule behind the answer')

# 44 · Drift (drawn to show the idea) ------------------------------------------------------------------------
b = t(40, 50, 'Drift: the world moves, the model stays', 26, weight=700)
ox, oy, ow, oh = 100, 90, 820, 260
b += box(ox, oy, ow, oh, MASS)
b += path([(ox + 20, oy + 40), (ox + 200, oy + 42), (ox + 400, oy + 70), (ox + 600, oy + 130), (ox + 800, oy + 200)], RED, 3)
b += line(ox + 200, oy, ox + 200, oy + oh, INK, 2) + t(ox + 208, oy + 22, 'model trained', 15, INK, 600)
b += t(ox + 250, oy + 175, 'its answers get slowly worse', 16, RED, 600)
b += t(ox + ow / 2, oy + oh + 30, 'time', 16, GREY, 600, 'middle')
b += f'<text transform="translate(70,{oy + oh / 2}) rotate(-90)" font-size="16" fill="{GREY}" font-weight="600" text-anchor="middle">how well it works</text>'
b += t(40, 410, 'Drawn to show the idea, not measured. In SDC, “drift under pressure” is a person’s standard shifting instead.', 16, GREY)
svg('drift.svg', 430, b, 'Drift: after a model is trained, its answers get slowly worse as the world changes')

# 45 · One accuracy, two kinds of mistake (illustrative) --------------------------------------------------------
b = t(40, 50, 'Both are 90% accurate. Their mistakes differ.', 26, weight=700)
for k, (h, miss, wrong) in enumerate([('Model A', 10, 0), ('Model B', 0, 10)]):
    ox = 40 + k * 470
    b += t(ox, 100, h, 20, INK, 700)
    for i in range(100):
        r, c = divmod(i, 20)
        col = GREEN if i < 90 else (AMBER if miss else RED)
        b += box(ox + c * 21, 118 + r * 21, 17, 17, col, rx=2)
    b += t(ox, 250, f'{miss} real things missed' if miss else f'{wrong} wrong things let through', 17, AMBER if miss else RED, 700)
b += t(40, 300, 'Green: right. Amber: a false negative. Red: a false positive. An example, not a measurement.', 16, GREY)
svg('accuracy.svg', 320, b, 'Two models, each right 90 times in 100: one misses ten real things, the other lets ten wrong things through')

# 46 · False positive and false negative: the plagiarism checker -----------------------------------------------
b = t(40, 50, 'A plagiarism checker’s two mistakes', 26, weight=700)
for k, (h, case, col) in enumerate([('False positive: a wrong “yes”', ['flags an essay the student', 'wrote herself'], RED),
                                     ('False negative: a wrong “no”', ['misses an essay that', 'was copied'], AMBER)]):
    x = 40 + k * 470
    b += card(x, 80, 440, 130, h, case, headfill=col)
svg('false-yes-no.svg', 230, b, 'A false positive flags an essay the student wrote; a false negative misses a copied one')

# 47 · Reproducibility (drawn to show the idea) ---------------------------------------------------------------
b = t(40, 50, 'Run it three times', 26, weight=700)
for k, (h, outs, col) in enumerate([('Rules in code', ['complete', 'complete', 'complete'], BLUE),
                                     ('A chat model', ['complete', 'mostly complete', 'needs more detail'], RED)]):
    y = 90 + k * 160
    b += box(40, y, 220, 120, col, rx=8) + t(56, y + 66, h, 19, PAPER, 700)
    for i, o in enumerate(outs):
        b += arrow(266, y + 60, 340, y + 20 + i * 40, col, 2) + box(346, y + 4 + i * 40, 280, 32, MASS, rx=5) + t(360, y + 26 + i * 40, o, 16)
b += t(40, 430, 'The same description, checked three times. Example answers, drawn to show the idea.', 16, GREY)
svg('reproducibility.svg', 450, b, 'Rules in code give the same answer three times; a chat model may give three different answers')

# 48 · Language work and judgement work: the umpire and the commentator ----------------------------------------
b = t(40, 50, 'At the cricket', 26, weight=700)
b += card(40, 80, 440, 170, 'The commentator: language work', ['“Full and wide, and he drives', 'it through the covers.”', '', 'describes the ball'], headfill=BLUE)
b += card(520, 80, 440, 170, 'The umpire: judgement work', ['raises a finger: out', '', '', 'decides'], headfill=INK)
b += box(40, 280, 920, 70, PAPER, stroke=RED, rx=8)
b += t(60, 322, 'When the commentator says “a poor shot”, the two kinds of work are mixed: SDC writes about this.', 16, RED, 600)
svg('umpire.svg', 370, b, 'The commentator describes the ball, which is language work; the umpire gives the batter out, which is judgement work')

# 49 · A threshold -------------------------------------------------------------------------------------------------
b = t(40, 50, 'A threshold: a cut-off in the rules', 26, weight=700)
b += box(40, 110, 920 * 0.62, 50, MASS, rx=6) + box(40 + 920 * 0.62, 110, 920 * 0.38, 50, BLUE, rx=6)
b += line(40 + 920 * 0.62, 90, 40 + 920 * 0.62, 180, RED, 4) + t(40 + 920 * 0.62, 82, 'cut-off', 16, RED, 700, 'middle')
b += t(60, 142, 'below: don’t know', 17, INK, 600) + t(60 + 920 * 0.62, 142, 'above: accepted', 17, PAPER, 600)
b += t(40, 200, '0', 15, GREY) + t(960, 200, '1', 15, GREY, 400, 'end')
b += tl(40, 240, ['In ungli the cut-off is set on examples people answered by hand,', 'then checked on examples the model never saw. The position shown is only an example.'], 16, fill=GREY)
svg('threshold.svg', 290, b, 'A threshold on a score from 0 to 1: below the cut-off the case is don’t know, above it the answer is accepted')

# 50 · A chooser ---------------------------------------------------------------------------------------------------
b = t(40, 50, 'A chooser picks from a list written in advance', 26, weight=700)
b += box(40, 80, 400, 160, MASS) + t(56, 110, 'the list, written by people', 16, GREY, 600)
for i, it in enumerate(['complete', 'not complete']):
    b += box(56, 126 + i * 52, 36, 36, INK, rx=6) + t(74, 150 + i * 52, str(i + 1), 18, PAPER, 700, 'middle') + t(106, 150 + i * 52, it, 18)
b += arrow(450, 140, 520, 140, BLUE) + box(528, 118, 60, 44, BLUE, rx=6) + t(558, 148, '2', 20, PAPER, 700, 'middle')
b += t(604, 148, 'an item’s number', 16, INK)
b += arrow(450, 200, 520, 200, RED) + box(528, 178, 130, 44, RED, rx=6) + t(542, 208, 'nothing', 18, PAPER, 700)
b += t(674, 208, 'when none fits', 16, INK)
svg('chooser.svg', 260, b, 'A chooser answers with the number of an item on a list written in advance, or with nothing')

# 51 · A domain guide (described in ungli; not yet trained) ----------------------------------------------------
b = t(40, 50, 'Close in meaning is not always the right answer', 26, weight=700)
b += box(40, 80, 920, 64, PAPER, stroke=LINE, rx=8) + t(60, 120, 'Groundnut, on chalky soil: new leaves are yellow between the veins. Why?', 18, INK, 600)
b += t(40, 186, 'A general encoder', 19, BLUE, 700) + t(40, 210, 'sees both as “yellow leaves”', 15, GREY)
b += box(280, 166, 300, 50, BLUE, rx=6) + t(296, 197, 'nitrogen shortage', 17, PAPER, 600)
b += box(600, 166, 300, 50, BLUE, rx=6) + t(616, 197, 'iron shortage', 17, PAPER, 600)
b += t(40, 276, 'A person who knows', 19, GREEN, 700) + t(40, 300, 'groundnut picks iron first', 15, GREY)
b += box(280, 256, 300, 50, MASS, rx=6) + t(296, 287, 'nitrogen shortage', 17, GREY, 600)
b += box(600, 256, 300, 50, GREEN, rx=6) + t(616, 287, 'iron shortage', 17, PAPER, 700)
b += t(40, 350, 'A domain guide would learn this from labels such people write. No domain guide has been trained yet.', 16, GREY)
svg('domain-guide.svg', 370, b, 'A general encoder finds nitrogen and iron shortage equally close; a person who knows groundnut picks iron')

print('written:', len([f for f in os.listdir(OUT) if f.endswith('.svg')]), 'figures')
