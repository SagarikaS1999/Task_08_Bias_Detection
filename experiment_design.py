
import json, os, argparse, itertools, random
from scripts.utils import ensure_dir, now_iso, hash_text

def main(args):
    with open(args.templates, "r") as f:
        tpl = json.load(f)

    with open(args.instances, "r") as f:
        inst = json.load(f)

    # Build an experiment matrix: for each hypothesis, each variant is a condition
    rows = []
    for hid, variants in inst.items():
        for cond, prompt in variants.items():
            rows.append({
                "hypothesis_id": hid,
                "condition": cond,
                "prompt": prompt,
                "seed": None
            })

    # Optionally expand by seeds to get multiple samples per prompt from each model
    if args.seeds:
        seeds = [int(s) for s in args.seeds.split(",")]
    else:
        seeds = tpl["metadata"]["random_seeds"]

    expanded = []
    for r in rows:
        for s in seeds:
            r2 = dict(r)
            r2["seed"] = s
            expanded.append(r2)

    manifest = {
        "created_at": now_iso(),
        "models": args.models.split(","),
        "temperature": args.temperature,
        "n_samples_per_prompt": args.n_samples,
        "prompts": expanded
    }

    ensure_dir(os.path.dirname(args.out))
    with open(args.out, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wrote experiment manifest with {len(expanded)} prompt-seed combos to {args.out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--templates", default="prompts/prompt_templates.json")
    ap.add_argument("--instances", default="prompts/prompt_instances.json")
    ap.add_argument("--models", default="gpt-4o-mini,claude-3-5-sonnet,gemini-1.5-pro")
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--n_samples", type=int, default=3, help="responses per prompt per model")
    ap.add_argument("--seeds", type=str, default="", help="comma-separated list; empty uses defaults")
    ap.add_argument("--out", default="prompts/manifest.json")
    args = ap.parse_args()
    main(args)
