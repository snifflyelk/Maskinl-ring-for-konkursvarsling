import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


VEDLEGG_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = VEDLEGG_DIR.parent
SCRIPTS_DIR = VEDLEGG_DIR / "scripts"
OUTPUT_DIR = VEDLEGG_DIR / "output"
METADATA_FILE = VEDLEGG_DIR / "metadata_datafreeze.json"


SNAPSHOT_PIPELINE = [
    "konverter_json_til_csv_kun_AS_ASA.py",
    "lag_analysefil.py",
    "feature_engineered_enheter.py",
    "model_logistisk.py",
    "model_1.py",
    "robusthet_lekkasje.py",
]

API_PIPELINE = [
    "hent_as_asa.py",
    "lag_analysefil.py",
    "feature_engineered_enheter.py",
    "model_logistisk.py",
    "model_1.py",
    "robusthet_lekkasje.py",
]

ROOT_OUTPUT_FILES = [
    "organisasjonsnumre_as_asa.csv",
    "alle_enheter_AS_ASA.csv",
    "analyseklare_enheter.csv",
    "feature_engineered_enheter.csv",
    "robusthet_lekkasje_resultater.csv",
    "modellresultater_terskler.csv",
    "modellresultater_terskler_med_f1.csv",
]

OUTPUT_FOLDERS = [
    "figurer_modell",
    "figurer XGBoost modell",
    "figurer XGBoost med justerbar terskel",
]


def load_metadata():
    if not METADATA_FILE.exists():
        return {}
    with METADATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def run_script(script_name, env):
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        raise FileNotFoundError(f"Fant ikke skript: {script_path}")

    print(f"\n[RUN] {script_name}")
    subprocess.run([sys.executable, str(script_path)], cwd=str(PROJECT_ROOT), check=True, env=env)


def collect_outputs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    copied = []
    for file_name in ROOT_OUTPUT_FILES:
        src = PROJECT_ROOT / file_name
        if src.exists():
            dst = OUTPUT_DIR / file_name
            shutil.copy2(src, dst)
            copied.append(str(dst))

    for folder_name in OUTPUT_FOLDERS:
        src_dir = PROJECT_ROOT / folder_name
        if src_dir.exists() and src_dir.is_dir():
            dst_dir = OUTPUT_DIR / folder_name
            if dst_dir.exists():
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            copied.append(str(dst_dir))

    return copied


def write_run_log(mode, copied_files):
    log_file = OUTPUT_DIR / "reproduksjon_logg.txt"
    now = datetime.now().isoformat(timespec="seconds")

    lines = [
        f"Kjort: {now}",
        f"Modus: {mode}",
        "Kopierte artefakter:",
    ]
    if copied_files:
        lines.extend([f"- {p}" for p in copied_files])
    else:
        lines.append("- Ingen artefakter funnet")

    log_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Kjor full reproduksjonspipeline for masteroppgaven")
    parser.add_argument(
        "--mode",
        choices=["snapshot", "api"],
        default="snapshot",
        help="snapshot = reproduksjon fra lagret alle_enheter.json, api = ny uthenting",
    )
    parser.add_argument(
        "--skip-models",
        action="store_true",
        help="Kjor kun datadel (ingen modellering)",
    )
    args = parser.parse_args()

    metadata = load_metadata()

    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"

    freeze_date = metadata.get("feature_reference_date")
    if freeze_date:
        env["MASTER_FREEZE_DATE"] = freeze_date

    pipeline = SNAPSHOT_PIPELINE if args.mode == "snapshot" else API_PIPELINE
    if args.skip_models:
        pipeline = [s for s in pipeline if not s.startswith("model") and not s.startswith("robusthet")]

    print("Starter reproduksjonspipeline...")
    print(f"Prosjektrot: {PROJECT_ROOT}")
    print(f"Vedleggmappe: {VEDLEGG_DIR}")

    for script in pipeline:
        run_script(script, env)

    copied = collect_outputs()
    write_run_log(args.mode, copied)

    print("\nFerdig.")
    print(f"Artefakter kopiert til: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
