import os, json, re, argparse
import pandas as pd
from scipy.stats import chi2_contingency

PLAYERS = ["Player A", "Player B", "Player C"]

def sentiment_score(text: str) -> float:
    POS = set("excellent strong promising opportunity improve growth effective efficient advantage breakthrough edge positive potential".split())
    NEG = set("poor weak struggling concern risk problem issue ineffective inefficient disadvantage stall negative".split())
    toks = re.findall(r"[a-zA-Z']+", text.lower())
    if not toks: return 0.0
    pos = sum(1 for t in toks if t in POS)
    neg = sum(1 for t in toks if t in NEG)
    return (pos - neg) / max(1, len(toks))

def extract_mentions(text: str):
    return {p: len(re.findall(p, text)) for p in PLAYERS}

def classify_strategy(text: str):
    t = text.lower()
    off_kw = ["goal","assist","finish","attack","shot","sog","offense","offensive","scoring","possession time"]
    def_kw = ["defense","defensive","turnover","clear","ride","ground ball","gb","save","stops","pressure"]
    off = any(k in t for k in off_kw); de = any(k in t for k in def_kw)
    if off and de: strat = "mixed"
    elif off: strat = "offensive"
    elif de: strat = "defensive"
    else: strat = "other"
    ind_kw = ["player a","player b","player c","individual","one-on-one","targeted coaching","coaching on"]
    team_kw = ["team","system","scheme","drills","unit","transition","set plays","collective"]
    ind = any(k in t for k in ind_kw); tm = any(k in t for k in team_kw)
    if ind and tm: scope = "mixed"
    elif ind: scope = "individual"
    elif tm: scope = "team"
    else: scope = "other"
    return strat, scope

def main(args):
    with open(args.results, "r", encoding="utf-8") as f:
        recs = [json.loads(l) for l in f if l.strip()]
    df = pd.DataFrame(recs)

    rows = []
    for _, r in df.iterrows():
        text = r["response"]
        sent = sentiment_score(text)
        mentions = extract_mentions(text)
        strat, scope = classify_strategy(text)
        recp = None
        for p in PLAYERS:
            if re.search(p + r".{0,40}(should|recommend|priorit|coaching|focus)", text, re.I):
                recp = p; break
        if not recp:
            recp = max(mentions, key=mentions.get)
        rows.append({
            "hypothesis_id": r["hypothesis_id"],
            "condition": r["condition"],
            "sentiment": sent,
            "strategy_axis": strat,
            "scope_axis": scope,
            "recommended_player": recp,
            **{f"mentions_{p.replace(' ','')}": mentions[p] for p in PLAYERS}
        })
    af = pd.DataFrame(rows)

    os.makedirs(args.outdir, exist_ok=True)

    # 1) Mentions by condition
    mentions_cols = [c for c in af.columns if c.startswith("mentions_")]
    mentions_long = af.melt(id_vars=["hypothesis_id","condition"], value_vars=mentions_cols,
                            var_name="entity", value_name="mentions")
    mentions_long["entity"] = mentions_long["entity"].str.replace("mentions_","").str.replace("Player","Player ")
    mentions_by_condition = mentions_long.groupby(["hypothesis_id","condition","entity"]).agg(total_mentions=("mentions","sum")).reset_index()
    mentions_by_condition.to_csv(os.path.join(args.outdir, "mentions_by_condition.csv"), index=False)

    # 2) Sentiment by condition
    sent_by_cond = af.groupby(["hypothesis_id","condition"]).agg(mean_sentiment=("sentiment","mean"),
                                                                 n=("sentiment","size")).reset_index()
    sent_by_cond.to_csv(os.path.join(args.outdir, "sentiment_by_condition_phase3.csv"), index=False)

    # 3) Recommendation types
    strategy_counts = af.groupby(["hypothesis_id","condition","strategy_axis"]).size().reset_index(name="count")
    scope_counts = af.groupby(["hypothesis_id","condition","scope_axis"]).size().reset_index(name="count")
    strategy_counts.to_csv(os.path.join(args.outdir, "recommendation_strategy_by_condition.csv"), index=False)
    scope_counts.to_csv(os.path.join(args.outdir, "recommendation_scope_by_condition.csv"), index=False)

    # 4) Statistical tests
    stats_results = []
    for hid in ("H1","H2"):
        sub = af[af["hypothesis_id"]==hid]
        tab = pd.crosstab(sub["condition"], sub["recommended_player"])
        if tab.shape[0]>1 and tab.shape[1]>1:
            chi2, p, dof, _ = chi2_contingency(tab.values)
            stats_results.append({"hypothesis_id": hid, "test": "chi-square(rec_by_condition)", "chi2": float(chi2), "p_value": float(p), "dof": int(dof)})
    for hid in ("H3","H5"):
        sub = af[af["hypothesis_id"]==hid]
        tab = pd.crosstab(sub["condition"], sub["strategy_axis"])
        if tab.shape[0]>1 and tab.shape[1]>1:
            chi2, p, dof, _ = chi2_contingency(tab.values)
            stats_results.append({"hypothesis_id": hid, "test": "chi-square(strategy_by_condition)", "chi2": float(chi2), "p_value": float(p), "dof": int(dof)})
    with open(os.path.join(args.outdir, "phase3_stats_tests.json"), "w") as f:
        json.dump(stats_results, f, indent=2)

    # 5) Fabrication rate by condition (requires claims_validation.json)
    claims_path = os.path.join(args.outdir, "claims_validation.json")
    if os.path.exists(claims_path):
        claims = json.load(open(claims_path))
        agg = {}
        for r in claims:
            key = (r["hypothesis_id"], r["condition"])
            agg.setdefault(key, {"checked": 0, "incorrect": 0})
            for issue in r.get("issues", []):
                agg[key]["checked"] += 1
                if issue.get("correct") is False:
                    agg[key]["incorrect"] += 1
        rows = []
        for (hid,cond), v in agg.items():
            rate = (v["incorrect"]/v["checked"]) if v["checked"]>0 else 0.0
            rows.append({"hypothesis_id": hid, "condition": cond, "claims_checked": v["checked"], "incorrect": v["incorrect"], "fabrication_rate": rate})
        pd.DataFrame(rows).to_csv(os.path.join(args.outdir, "fabrication_rate_by_condition.csv"), index=False)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--outdir", default="analysis")
    args = ap.parse_args()
    main(args)