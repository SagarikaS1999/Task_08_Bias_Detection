
import argparse, json, os, re
from scripts.utils import read_jsonl

def load_truth(path):
    with open(path, "r") as f:
        return json.load(f)

def extract_numbers(text):
    # returns list of (number, context window)
    nums = []
    for m in re.finditer(r"(-?\d+\.?\d*)", text):
        start = max(0, m.start()-20)
        end = min(len(text), m.end()+20)
        nums.append((float(m.group(1)), text[start:end]))
    return nums

def check_claims(text, truth):
    issues = []
    # Example heuristic: if text says "more turnovers than opponents" verify numbers
    if re.search(r"turnover[s]? .*than opponent", text, re.I):
        ours = truth["turnovers"]
        theirs = truth["opponent_turnovers"]
        cond = ours > theirs
        issues.append({"claim": "more turnovers than opponents", "truth": f"{ours} vs {theirs}", "correct": cond})

    if re.search(r"better free position", text, re.I):
        # compare made/attempt rate
        ours = truth["free_position_made"] / truth["free_position_att"]
        theirs = truth["opponent_free_position_made"] / truth["opponent_free_position_att"]
        cond = ours > theirs
        issues.append({"claim": "better free position rate", "truth": f"{ours:.3f} vs {theirs:.3f}", "correct": cond})

    # Flag naked numeric hallucinations > 400 when talking about shots (since total attempts 716 for team)
    if re.search(r"shot", text, re.I):
        for num, ctx in extract_numbers(text):
            if num > 1000:
                issues.append({"claim": f"suspicious large number {num}", "context": ctx, "correct": False})

    return issues

def main(args):
    truth = load_truth(args.truth_json)
    report = []
    for fn in os.listdir(args.results_dir):
        if not fn.endswith(".jsonl"): 
            continue
        for rec in read_jsonl(os.path.join(args.results_dir, fn)):
            issues = check_claims(rec["response"], truth)
            report.append({
                "provider": rec["provider"],
                "model": rec["model"],
                "hypothesis_id": rec["hypothesis_id"],
                "condition": rec["condition"],
                "issues": issues
            })

    with open(args.out, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Wrote validation report to {args.out}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--truth_json", default="data/su_stats_excerpt.json")
    ap.add_argument("--results_dir", default="results")
    ap.add_argument("--out", default="analysis/claims_validation.json")
    args = ap.parse_args()
    main(args)
