import ollama
from pathlib import Path
from textwrap import dedent
from corpus_utils import load_json, save_json
from datastructures import GeneratedDesc, Corpus
from typing import List, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def create_prompt(program_name: str, ep_title: str, desc: str, schedule_time: str, tracks: str) -> List[Dict]:

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


import json


def run_llm_synthetic_desc(ep, messages, model_name: str = "gemma3:4b", max_retries: int = 3):
    """
    Runs the LLM to generate a response with retry logic.
    """
    for attempt in range(max_retries):
        try:
            response = ollama.chat(
                model=model_name,
                messages=messages,
                options={
                    "temperature": 0.7,
                    "top_p": 0.7,
                },
                format=GeneratedDesc.model_json_schema(),
            )
            llm_gen_description = response.message.content
            try:
                parsed_description = json.loads(llm_gen_description)
                validated = GeneratedDesc.model_validate_json(json.dumps(parsed_description))
                ep.synthetic_desc = validated.generated_desc
                break
            except json.JSONDecodeError as json_error:
                print(f"Attempt {attempt + 1}/{max_retries}: Invalid JSON from LLM response.")
                print("LLM Response:\n", llm_gen_description)
                print("JSON Parsing Error:\n", json_error)
                if attempt == max_retries - 1:
                    ep.synthetic_desc = None
            except Exception as schema_validation_error:
                print(f"Attempt {attempt + 1}/{max_retries}: Schema validation failed for episode.")
                print("LLM Generated Response:\n", llm_gen_description)
                print("Schema Validation Error:\n", schema_validation_error)
                if attempt == max_retries - 1: 
                    ep.synthetic_desc = None

        except Exception as e:
            print(
                f"Attempt {attempt + 1}/{max_retries}: Ollama generation failed for episode: {ep.episode_title}, model={model_name}")
            print(e)
            if attempt == max_retries - 1:
                ep.synthetic_desc = None
            continue


    original_length = len(ep.short_description) if ep.short_description else 0
    synthetic_length = len(ep.synthetic_desc or "")
    print(f"\nProgram: {ep.program_name}")
    print(f"Episode: {ep.episode_title}")
    print(f"Synthetic Description:\n{ep.synthetic_desc}")
    print(f"Original desc length: {original_length}")
    print(f"Synthetic desc length: {synthetic_length}")
    print("-" * 60)


def generate_and_save_augmented_json(input_path: Path, output_path: Path, num_episodes: int =35) -> tuple[Corpus, int]:
    corpus: Corpus = load_json(input_path)
    episodes = corpus.episodes[:num_episodes]

    success_count = 0
    total_count = len(episodes)

    for i, ep in enumerate(episodes, 1):
        print(f"\nProcessing episode {i}/{total_count}: {ep.episode_title}")
        try:

            tracks = " ".join(
                f"{t.artist} - {t.track}" +
                (f" [{t.album}]" if t.album else "") +
                (f" ({t.label})" if t.label else "") +
                (f" ({t.year})" if t.year else "")
                for t in ep.tracks
            )

            prompt = create_prompt(
                ep.program_name,
                ep.episode_title,
                ep.short_description,
                ep.schedule_time,
                tracks
            )

            run_llm_synthetic_desc(ep, prompt)

            if ep.synthetic_desc:
                success_count += 1


        except Exception as e:
            print(f"Error processing episode {i}/{total_count}: {ep.episode_title}")
            print(f"Error details: {str(e)}")
            continue 
    

    save_json(corpus, output_path)
    print(f"\nSaved augmented corpus: {output_path}")
    print(f"Successfully processed: {success_count} / {total_count} episodes")

    return corpus, success_count
if __name__ == "__main__":
    input_path = PROJECT_ROOT / "data" / "clean" / "full_corpus.json"
    output_path = PROJECT_ROOT / "data" / "clean" / "full_corpus_augmented_ollama.json"

    generate_and_save_augmented_json(input_path, output_path)