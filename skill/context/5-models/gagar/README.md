# mein sagar

*gagar · mein sagar*: SYNTAX's whole-text reader. A person pastes a text of 100 to 350 words and the page says whether it reads as his kind of story, as plain meaning, or as noise, read by `gagar`, an adapter on aadha's base, through the app `aadha` on blevn; `server.py` holds the logins and keeps each reading, `index.html` is the page. It was live at mein-sagar.syntax.prayasabhinav.net from 4 November 2026 and has been offline since 5 November, 23:06, because the order check passed a text whose halves were swapped.

**Version:** `VERSION` (0.1.0, not deployed); what changed in `CHANGELOG.md`; what comes next in `ROADMAP.md`. The record of how it was built is `HISTORY.md` and `HANDOFF.md`; the reader's tests are `reader.md`; the research lanes of Claude Code and Hermes are `autoresearch/` (contract in `autoresearch/README.md`).

**Git:** history in `[path withheld]` on the Mac, pushed to the private `[private repository]`. The reader's server is a separate history, `aadha-server`, tagged `mein-sagar-v0.1.0` for this version. `deploy.sh` ships only committed `main`, and nothing deploys without his word.
