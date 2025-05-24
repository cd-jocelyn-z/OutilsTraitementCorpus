import ollama
from pathlib import Path
from textwrap import dedent
from corpus_utils import load_json, save_json
from datastructures import GeneratedDesc

def create_prompt(program_name: str, ep_title: str, desc: str, schedule_time: str, tracks: str):
    return [
        {
            "role": "system",
            "content": dedent("""
                You are an expert radio curator working for an international cultural archive.
                You specialize in crafting engaging, listener-friendly episode summaries using sparse metadata.
                
                Your task is to generate a clear and compelling summary of each episode for a global audience.

                Always return your response as a single JSON object with the following structure:
                {
                  "generated_desc": "<an engaging episode summary in English, around 10 sentences>"
                }
            """)
        },
        {
            "role": "assistant",
            "content": "Understood. I will provide a clear, engaging summary of the episode based solely on the provided metadata. The response will be formatted as a single JSON object with a 'generated_desc' field."
        },
        {
            "role": "user",
            "content": dedent(f"""
                This information comes from WFMU, a freeform, listener-supported radio station based in the United States.

                Below is a summary of a past broadcast:

                Programme: {program_name}
                Episode Title: {ep_title}
                Description: {desc}
                Hour: {schedule_time}
                Tracks: {tracks}

                This episode currently lacks a clear, engaging description to help listeners.
                Please place special emphasis on the musical tracks featured in the program. Highlight the mood, variety, or notable artists where possible, and suggest what a listener might take away from the listening experience.

                Based on this metadata, generate a new, engaging summary of the episode for a diverse, global audience.
            """)
        }
    ]



def run_llm_synthetic_desc(ep, messages, model_name: str = "gemma3:4b", verbose: bool = True):
    try:
        response = ollama.chat(
            model=model_name,
            messages=messages,
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 300
            },
            format=GeneratedDesc.model_json_schema(),
        )

        llm_gen_description = response.message.content
        try:
            validated = GeneratedDesc.model_validate_json(llm_gen_description)
            ep.synthetic_description = validated.generated_desc
        except Exception as e:
            print(f"Validation error for episode: {ep.episode_title}")
            print("LLM Generated Description:\n", llm_gen_description)
            print("Error:\n", e)
            ep.synthetic_description = None

        original_length = len(ep.short_description) if ep.short_description else 0
        synthetic_length = len(ep.synthetic_description or "")
        print(f"\nProgram: {ep.program_name}")
        print(f"Episode: {ep.episode_title}")
        print(f"Synthetic Description:\n{ep.synthetic_description}")
        print(f"Original desc length: {original_length}")
        print(f"Synthetic desc length: {synthetic_length}")
        print("-" * 60)

    except Exception as e:
        print(f"Ollama generation failed for episode: {ep.episode_title}, model={model_name}")
        print(e)
        ep.synthetic_description = None


def generate_and_save_augmented_json(input_path: Path, output_path: Path):
    corpus = load_json(input_path)
    episodes = corpus.episodes[:5] 

    for ep in episodes:
        tracks = " ".join(t.track for t in ep.tracks if t.track)
        prompt = create_prompt(
        ep.program_name,
        ep.episode_title,
        ep.short_description,
        ep.schedule_time,
        tracks
    )
        run_llm_synthetic_desc(ep, prompt)

    save_json(corpus, output_path)
    print(f"\nSaved augmented corpus → {output_path}")

    success_count = sum(1 for ep in episodes if ep.synthetic_description)
    print(f"Total augmented: {success_count} / {len(episodes)}")

if __name__ == "__main__":
    input_path = Path("data/clean/full_corpus.json")
    output_path = Path("data/clean/full_corpus_augmented_ollama.json")

    generate_and_save_augmented_json(input_path, output_path)