
import os, json, argparse, time, random
from datetime import datetime
from typing import Dict, Any
from tqdm import tqdm
from scripts.utils import ensure_dir, jsonl_write, now_iso

# Lazy imports only if needed
def ask_openai(model: str, prompt: str, temperature: float, seed: int) -> str:
    import openai
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        seed=seed
    )
    return resp.choices[0].message.content

def ask_anthropic(model: str, prompt: str, temperature: float, seed: int) -> str:
    import anthropic
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=800,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text

def ask_gemini(model: str, prompt: str, temperature: float, seed: int) -> str:
    import google.generativeai as genai
    genai.configure()
    m = genai.GenerativeModel(model)
    resp = m.generate_content(prompt, generation_config={"temperature": temperature}, safety_settings=None)
    return resp.text

def ask_mock(model: str, prompt: str, temperature: float, seed: int) -> str:
    random.seed(seed)
    # Minimal variability while still structured
    stances = ["cautiously positive", "balanced", "critical"]
    recs = ["individual coaching", "team drills", "defensive focus", "offensive sets"]
    tone = random.choice(stances)
    rec = ", ".join(random.sample(recs, 2))
    return f"[MOCK:{model}] Tone: {tone}. Recommendations: {rec}. Rationale grounded in provided numbers."

def main(args):
    with open(args.manifest, "r") as f:
        manifest = json.load(f)

    models = manifest["models"]
    temperature = manifest["temperature"]
    n_samples = manifest["n_samples_per_prompt"]
    prompts = manifest["prompts"]

    provider = args.provider.lower()
    if provider == "openai":
        asker = ask_openai
    elif provider == "anthropic":
        asker = ask_anthropic
    elif provider == "gemini":
        asker = ask_gemini
    elif provider == "mock":
        asker = ask_mock
    else:
        raise ValueError("provider must be one of: openai, anthropic, gemini, mock")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outpath = os.path.join(args.outdir, f"{stamp}_{provider}.jsonl")
    ensure_dir(args.outdir)

    records = []
    for model in models:
        if args.only_model and model != args.only_model:
            continue
        for p in tqdm(prompts, desc=f"Provider={provider}, model={model}"):
            for i in range(n_samples):
                seed = int(p["seed"]) + i
                try:
                    text = asker(model, p["prompt"], temperature, seed)
                except Exception as e:
                    text = f"[ERROR] {type(e).__name__}: {e}"
                rec = {
                    "timestamp": now_iso(),
                    "provider": provider,
                    "model": model,
                    "seed": seed,
                    "hypothesis_id": p["hypothesis_id"],
                    "condition": p["condition"],
                    "prompt_hash": hash(p["prompt"]) % (10**10),
                    "prompt": p["prompt"],
                    "response": text
                }
                records.append(rec)

            if len(records) >= 50:
                jsonl_write(outpath, records)
                records = []

    if records:
        jsonl_write(outpath, records)

    print(f"Wrote responses to {outpath}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="prompts/manifest.json")
    ap.add_argument("--outdir", default="results")
    ap.add_argument("--provider", default="mock", help="openai|anthropic|gemini|mock")
    ap.add_argument("--only_model", default="", help="optional filter: only run a single model name")
    args = ap.parse_args()
    main(args)
