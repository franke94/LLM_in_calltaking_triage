
from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

client = OpenAI()


CALLER_SYSTEM = """\
Du bist der ANRUFER (caller) in einem 112-Notruftraining in Deutschland.
Du sprichst kurz, emotional realistisch, mit typischen Unsicherheiten/Alltagssprache.
Du bist Laie, kannst also keine medizinischen Fachbegriffe nenne und nur beschreiben was du siehst.
WICHTIG:
- Antworte IMMER nur als caller. Keine Meta-Erklärungen, keine Rollenwechsel.
- Wenn der calltaker nach Details fragt, gib sie nur, wenn sie aus dem Szenario ableitbar sind.
- Halte Antworten meist 1–3 Sätze, außer bei kritischen Details (Atmung, Bewusstsein, Blutung).
- Du bist aufgeregt, vielleicht auch panisch, aber versuchst trotzdem zu antworten. Das kann zu unvollständigen Sätzen, Wiederholungen oder Abschweifungen führen.
"""

def run_emergency_call(
    call: str,
    scenario_text: str,
    model: str = "gpt-5.2",
    temperature: float = 0.6,
    out_dir: str = "notruf_transcripts",
):
    """
    scenario_text: dein bereits generierter Szenariotext (Aktuelles Ereignis / Situation vor Ort / Vorgeschichte)
    Du tippst als calltaker; Modell antwortet als caller.
    Transcript wird als Markdown gespeichert.
    """
    Path(out_dir).mkdir(exist_ok=True)

    # Wir geben dem Modell das Szenario als "versteckten Kontext" (system-level + additional system message)
    messages = [
        {"role": "system", "content": CALLER_SYSTEM},
        {"role": "system", "content": f"SCENARIO (nur für dich als caller, nicht vorlesen):\n{scenario_text}"},
    ]

    transcript_lines = []
    print("\n--- Notruftraining gestartet ---")
    print("Tippe deine calltaker-Fragen. Befehle: /end beendet, /save speichert sofort.\n")

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
            print("--- beendet ---")
            break

        if user_in.lower() == "/save":
            save_transcript()
            continue

        # calltaker (user role)
        transcript_lines.append(f"**calltaker**: {user_in}")
        messages.append({"role": "user", "content": user_in})

        # Modell antwortet als caller
        resp = client.responses.create(
            model=model,
            input=messages,
            temperature=temperature,
        )

        caller_text = (resp.output_text or "").strip()
        # Fallback, falls leer:
        if not caller_text:
            caller_text = "[Keine Antwort erhalten]"

        print(f"caller> {caller_text}\n")

        transcript_lines.append(f"**caller**: {caller_text}")
        messages.append({"role": "assistant", "content": caller_text})


import sys
if __name__ == "__main__":
    # Standardwert falls keine Zahl übergeben wird
    case_number = 0


    # prüfen ob Argument übergeben wurde
    if len(sys.argv) > 1:
        case_number = int(sys.argv[1])

    call = f"case_{case_number}.txt"
    scenario_path = Path("../emergency_calls/cases") / call

    if not scenario_path.exists():
        print(f" Datei nicht gefunden: {scenario_path}")
        sys.exit(1)

    scenario_text = scenario_path.read_text(encoding="utf-8")

    run_emergency_call(
        call=call,
        scenario_text=scenario_text,
        model="gpt-5.2",
        temperature=0.6,
        out_dir="notruf_transcripts"
    )