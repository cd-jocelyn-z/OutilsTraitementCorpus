from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from pathlib import Path
from textwrap import dedent
from corpus_utils import save_json, load_json

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def create_prompt(program_name: str, ep_title: str, desc: str, schedule_time: str, tracks: str) -> str:
    return dedent(f"""
        This information comes from WFMU, a freeform, listener-supported radio station based in the United States.

        Below is a summary of a past broadcast:

        Programme: {program_name}
        Episode Title: {ep_title}
        Description: {desc}
        Hour: {schedule_time}
        Tracks: {tracks}

        This episode currently lacks a clear, engaging description to help listeners — especially an international audience — understand whether they’d want to explore it in the station's public archive.

        Based on the information provided above, generate a new, engaging summary of this episode that could appeal to a diverse, global audience.
    """)


def augment_data(input_path: Path, output_path: Path):
    corpus = load_json(input_path)
    episodes = corpus.episodes

    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    augmented_count = 0
    for ep in episodes:
        tracks = " ".join(t.track for t in ep.tracks if t.track)

        prompt = create_prompt(
            ep.program_name,
            ep.episode_title,
            ep.short_description,
            ep.schedule_time,
            tracks
        )

        inputs = tokenizer(prompt, return_tensors="pt").to(device)

        outputs = model.generate(
            **inputs,
            max_new_tokens=80,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id
        )

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        marker = "generate a new, engaging summary of this episode that could appeal to a diverse, global audience."
        if marker.lower() in generated_text.lower():
            split_point = generated_text.lower().find(marker.lower())
            synthetic_description = generated_text[split_point + len(marker):].strip()
        else:
            synthetic_description = generated_text.strip()

        ep.synthetic_description = synthetic_description
        augmented_count += 1

        original_length = len(ep.short_description) if ep.short_description else 0
        synthetic_length = len(synthetic_description)

        print(f"Program: {ep.program_name}")
        print(f"Episode: {ep.episode_title}")
        print(f"Original description length: {original_length}")
        print(f"Synthetic description length: {synthetic_length}")
        print("-" * 60)

    save_json(corpus, output_path)
    print(f"\nCorpus saved with {augmented_count} synthetic descriptions.")

if __name__ == "__main__":
    input_path = Path("data/clean/full_corpus.json")
    output_path = Path("data/clean/full_corpus_augmented-test.json")

    augment_data(input_path, output_path)
