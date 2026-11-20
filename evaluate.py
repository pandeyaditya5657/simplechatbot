"""Evaluate intent recognition on test_sentences.json (sentences not copied
from intents.json). Run:  python evaluate.py"""
import json
from pathlib import Path

from chatbot import Chatbot, preprocess

BASE = Path(__file__).parent
tests = json.load(open(BASE / "test_sentences.json", encoding="utf-8"))
bot = Chatbot()
known = set(bot.patterns)

cases = [(s, e) for s, e in tests["in_scope"]] + [(s, "fallback") for s in tests["out_of_scope"]]
copied = [s for s, _ in cases if preprocess(s) in known]
if copied:
    print("WARNING: these test sentences duplicate a stored pattern:", copied)


def run(threshold):
    bot.threshold = threshold
    rows = []
    for s, exp in cases:
        r = bot.respond(s)
        rows.append((s, exp, r["intent"], r["confidence"]))
    return rows


def summary(rows):
    n = len(rows)
    ins = [r for r in rows if r[1] != "fallback"]
    oos = [r for r in rows if r[1] == "fallback"]
    return {
        "overall": sum(r[1] == r[2] for r in rows) / n,
        "in_scope": sum(r[1] == r[2] for r in ins) / len(ins),
        "oos_reject": sum(r[2] == "fallback" for r in oos) / len(oos),
        "wrong_intent": sum(r[2] not in (r[1], "fallback") for r in ins),
        "wrongly_rejected": sum(r[2] == "fallback" for r in ins),
    }


if __name__ == "__main__":
    rows = run(bot.threshold)
    s = summary(rows)
    print(f"Sentences: {len(rows)}  (in-scope {len(tests['in_scope'])}, out-of-scope {len(tests['out_of_scope'])})")
    print(f"Overall accuracy       : {s['overall']:.1%}")
    print(f"In-scope accuracy      : {s['in_scope']:.1%}")
    print(f"Out-of-scope rejected  : {s['oos_reject']:.1%}")
    print(f"Wrong intent (in-scope): {s['wrong_intent']}")
    print(f"Wrongly rejected       : {s['wrongly_rejected']}")
    print("\nMistakes:")
    for sent, exp, pred, score in rows:
        if exp != pred:
            print(f"  {sent!r}: expected {exp}, got {pred} ({score})")
    print("\nThreshold sweep:")
    for t in (0.30, 0.40, 0.50, 0.60, 0.65, 0.70, 0.80):
        x = summary(run(t))
        print(f"  {t:.2f}  in-scope {x['in_scope']:.1%}  reject {x['oos_reject']:.1%}  overall {x['overall']:.1%}")
