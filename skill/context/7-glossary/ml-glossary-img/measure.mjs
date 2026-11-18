// Measures the data behind three figures of ml-glossary.md and writes measured.json beside this script.
// Uses csearch's own local model (Xenova/bge-base-en-v1.5, q8) and its transformers.js install; nothing leaves the machine.
// Run: node measure.mjs
import { writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { homedir } from 'node:os';
import { pathToFileURL, fileURLToPath } from 'node:url';

const tf = await import(pathToFileURL(join(homedir(), '.local/share/csearch/node_modules/@huggingface/transformers/dist/transformers.node.mjs')).href);
const MODEL = 'Xenova/bge-base-en-v1.5';
const QUERY_PREFIX = 'Represent this sentence for searching relevant passages: ';   // as csearch uses it

// Token: how a BERT-family tokenizer splits two sentences
const tok = await tf.AutoTokenizer.from_pretrained(MODEL);
const tokens = ['The umpire gave the batter out.', 'The decision was unquestionable.'].map((s) => ({
  sentence: s, tokens: tok.tokenize(s) }));

const embed = await tf.pipeline('feature-extraction', MODEL, { dtype: 'q8' });
const vec = async (texts) => (await embed(texts, { pooling: 'mean', normalize: true })).tolist();
const cos = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);

// Semantic search: one question against a handful of sentences
const query = 'ink for the printer';
const passages = ['The printer cartridges are over.', 'The printer in room 4 is jammed.', 'Heavy rain is expected in Ahmedabad tomorrow.',
  'The umpire gave the batter out.', 'Sign in ink, not pencil, on the form.', 'The new leaves of the groundnut are turning yellow.'];
const [q] = await vec([QUERY_PREFIX + query]);
const pv = await vec(passages);
const search = passages.map((p, i) => ({ passage: p, similarity: +cos(q, pv[i]).toFixed(3),
  sharesAWord: /\bink\b|\bprinter\b/i.test(p) }));

// Embedding map: twelve sentences in four topics, flattened from 768 numbers to 2 by principal components
const groups = {
  printer: ['The printer cartridges are over.', 'The printer in room 4 is jammed.', 'We need toner before the report is printed.'],
  rain: ['Heavy rain is expected in Ahmedabad tomorrow.', 'Carry an umbrella, the monsoon has started.', 'The roads near the river flooded overnight.'],
  cricket: ['The umpire gave the batter out.', 'The bowler took three wickets in the last over.', 'India needs forty runs from five overs.'],
  crops: ['The new leaves of the groundnut are turning yellow.', 'Iron shortage shows between the veins of young leaves.', 'The wheat needs nitrogen before it flowers.'],
};
const items = Object.entries(groups).flatMap(([g, ss]) => ss.map((s) => ({ group: g, sentence: s })));
const V = await vec(items.map((x) => x.sentence));
const mean = V[0].map((_, j) => V.reduce((s, v) => s + v[j], 0) / V.length);
const X = V.map((v) => v.map((x, j) => x - mean[j]));
function component(X, avoid) {               // power iteration on X^T X, orthogonal to `avoid`
  let w = X[0].map((_, j) => Math.sin(j + 1));
  for (let it = 0; it < 200; it++) {
    const s = X.map((x) => cos(x, w));
    w = w.map((_, j) => X.reduce((acc, x, i) => acc + x[j] * s[i], 0));
    if (avoid) { const d = cos(w, avoid); w = w.map((x, j) => x - d * avoid[j]); }
    const n = Math.hypot(...w); w = w.map((x) => x / n);
  }
  return w;
}
const c1 = component(X), c2 = component(X, c1);
const total = X.reduce((s, x) => s + cos(x, x), 0);
const share = (c) => X.reduce((s, x) => s + cos(x, c) ** 2, 0) / total;
const map = items.map((x, i) => ({ ...x, x: +cos(X[i], c1).toFixed(4), y: +cos(X[i], c2).toFixed(4) }));

writeFileSync(join(dirname(fileURLToPath(import.meta.url)), 'measured.json'), JSON.stringify({
  model: MODEL, measured: new Date().toISOString(), tokens, search: { query, results: search },
  map: { points: map, varianceShown: +(share(c1) + share(c2)).toFixed(3) } }, null, 1));
console.log(JSON.stringify({ tokens, search, varianceShown: share(c1) + share(c2) }, null, 1));
