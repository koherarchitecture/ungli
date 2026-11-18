# Testing teetar aadhi bater with students

29 October 2026, on Prayas's word: *"gated access for 50 students, limited test routine, full logging everythihng for grounding"*. Shaped on ka fakir's scheme of 28 October (`syntax/archive/lakir-ka-fakir/grounding/SCHEME.md`). The numbers below are settings on the server, taken from ka fakir as a starting point; they are his to set and change without changing code.

## Who

Fifty student logins, `t01` to `t50`, one teacher login (`prayas`) and one demo login, issued by `make-logins.py` (passwords in `[a private file]`, kept out of git, never printed). A login is the student's pseudonym; only the teacher holds the list of which login is whose. The round has fifty people in all, named testers included (his word, 30 October 2026: *"count logins made as a part of original 50 planned. not extra"*): each named login takes the place of the highest-numbered t-login still unused, which `make-logins.py add <name> student` retires by itself, so t39 to t50 were retired for the first twelve and the student logins now run t01 to t38. Twelve testers invited before the students (30 October 2026, his word) have logins made from their own names, as for syntax.workshop: sourav, supriya, anil, ansh, priyanka, simran, parisha, devaki, nikhil, sanjhi, dhyeya and dhruv, issued as student logins, so the same consent and limits apply and their lines can be told from the students' by name. The demo login is a student's in every way, consent and limits included; its lines are marked `demo` in the export.

## The routine

Each person is asked for at least 12 readings, with no most, in all or in a day (`TAB_READINGS`): 12 is a minimum (his words, 30 October 2026: *"12-reading is min limit not max"*, then *"I said min"*, which took away the three-a-day cap as well). The page fills a mark for each reading towards the twelve and shows how many days in a row a person has come back. A reading is one press of Read it, so changing a piece and reading it again counts as another. A reading that fails because aadha cannot be reached is not counted.

After a reading the student can, without using another: change the balance settings and watch the animal answer; say, sentence by sentence, that aadha read it wrongly and what they would call it (story, noise, grammar without sense); and write a note on the reading. The balance settings start from `TAB_HALF`, `TAB_REACH`, `TAB_AT_LEAST` and `TAB_UNDESIRABLE_MAX` (0.15, 0.05, 4, 0.05): the share of the good noise sets the dance, full at 15% and still below 10% and above 20%; more than 5% unwanted noise keeps the animal still whatever else the piece does (his words, 30 October 2026, 12:46: *"the 15 is the desirable noise. undesirable noise can be upto 2% only"*; raised to 5% on 31 October, 08:19: *"make them both 5"*). A slider moves the full-dance point; each number is a box on the page.

## What is kept

Everything a student does in the tool, in one record in order (`/app/data/log.jsonl` on the server), each line with the time, the login and the version: their consent and every change to it; every reading (the piece as written, the sentences code cut it into, aadha's mark for each (story, the good noise, unwanted noise), the settings, the noise share and how much the animal danced); every change of settings after a reading, with the dance it gave; every correction of a mark, with aadha's mark beside it (the latest for a sentence counts; choosing *I agree* again is kept too); every note. Nothing else: no visits, no counters, no clicks, no time on the page; the app's access log is off.

Taking part means agreeing to keep everything; training and quoting are separate choices. Unticking the first box or withdrawing deletes every line under the login and keeps one line saying the login withdrew.

## From the record

`pull.sh` fetches the whole record (teacher login only) into `record.jsonl`, each line carrying its writer's choices on training and quoting as they stand at the pull. Only lines with `train: true` go towards training the next aadha; the teacher reads the corrections and decides which become training rows.
