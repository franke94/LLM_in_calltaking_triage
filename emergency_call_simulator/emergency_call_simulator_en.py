from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

client = OpenAI()


CALLER_SYSTEM = """\
You are the CALLER in a 112 emergency call training scenario.

You speak briefly and with realistic emotion, using everyday language and typical uncertainty.
You are a layperson and cannot use medical terminology; you can only describe what you see.

IMPORTANT:
- Always respond only as the caller. No meta explanations and no role switching.
- If the call taker asks for details, provide them only if they can be inferred from the scenario.
- Keep answers mostly 1–3 sentences, except for critical details (breathing, consciousness, bleeding).
- You are distressed, possibly panicking, but still trying to respond. This may lead to incomplete sentences, repetition, or slight digressions.
"""

def run_emergency_call(
    call: str,
    scenario_text: str,
    model: str = "gpt-5.2",
    temperature: float = 0.6,
    out_dir: str = "notruf_transcripts",
):
    """
    scenario_text: the scenario text you previously generated (current event / on-scene situation / patient history)

    You type as the call taker; the model responds as the caller.

    The transcript is saved as Markdown.
    """
    Path(out_dir).mkdir(exist_ok=True)

    messages = [
        {"role": "system", "content": CALLER_SYSTEM},
        {"role": "system", "content": f"SCENARIO (just for you as a caller, don't hand to the calltaker):\n{scenario_text}"},
    ]

    transcript_lines = []
    print("\n--- Start simulation ---")
    print("Type your call taker questions. Commands: /end ends the call, /save saves immediately.\n")

    def save_transcript():
        fp = Path(out_dir) / f"{Path(call).stem}.md"
        fp.write_text("\n".join(transcript_lines).strip() + "\n", encoding="utf-8")
        print(f"\n[Gespeichert] {fp}\n")
        return fp

    while True:
        user_in = input("calltaker> ").strip()
        if not user_in:
            continue

        if user_in.lower() == "/end":
            save_transcript()
            print("--- end ---")
            break

        if user_in.lower() == "/save":
            save_transcript()
            continue

        transcript_lines.append(f"**calltaker**: {user_in}")
        messages.append({"role": "user", "content": user_in})

        resp = client.responses.create(
            model=model,
            input=messages,
            temperature=temperature,
        )

        caller_text = (resp.output_text or "").strip()
        if not caller_text:
            caller_text = "[Keine Antwort erhalten]"

        print(f"caller> {caller_text}\n")

        transcript_lines.append(f"**caller**: {caller_text}")
        messages.append({"role": "assistant", "content": caller_text})


import sys
if __name__ == "__main__":
    # Standard if no number is passed
    case_number = 0

    if len(sys.argv) > 1:
        case_number = int(sys.argv[1])

    call = f"case_{case_number}.txt"
    scenario_path = Path("../emergency_calls/cases") / call

    if not scenario_path.exists():
        print(f" data not found: {scenario_path}")
        sys.exit(1)

    scenario_text = scenario_path.read_text(encoding="utf-8")

    run_emergency_call(
        call=call,
        scenario_text=scenario_text,
        model="gpt-5.2",
        temperature=0.6,
        out_dir="notruf_transcripts"
    )