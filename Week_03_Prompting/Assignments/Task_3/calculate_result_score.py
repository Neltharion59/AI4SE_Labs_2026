"""Task_3: Skore zhody vysledkov so zapocitanim opakovanych riadkov."""

import csv
import json
import runpy
import sqlite3
from collections import Counter, defaultdict, deque
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
DATA_DIR = TASK_DIR.parent / "Task_2" / "data"
RUNS = [
    ("GPT-6 sol (High)", "APE", "APE_predictions.csv"),
    ("GPT-6 sol (High)", "STAR", "STAR_predictions.csv"),
    ("GPT-6 sol (High)", "ToT", "ToT_predictions.csv"),
    ("GPT-5.6 sol (light)", "APE", "APE_predictions_5.6.csv"),
    ("GPT-5.6 sol (light)", "STAR", "STAR_predictions_5.6.csv"),
    ("GPT-5.6 sol (light)", "ToT", "ToT_predictions_5.6.csv"),
]


def result_score(expected_rows, predicted_rows):
    """Skore = 2 * zhodne riadky / (ocakavane riadky + vratene riadky)."""
    total_rows = len(expected_rows) + len(predicted_rows)
    if total_rows == 0:
        return 1.0
    expected = Counter(tuple(row) for row in expected_rows)
    predicted = Counter(tuple(row) for row in predicted_rows)
    matches = sum((expected & predicted).values())
    return 2 * matches / total_rows


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    csv.field_size_limit(1_000_000_000)
    labels = read_csv(DATA_DIR / "restaurants_dataset.csv")
    evaluator = runpy.run_path(str(DATA_DIR / "evaluate_retrieval_predictions.py"))
    summaries = []
    all_scores = []

    for model, prompt, filename in RUNS:
        # Priradime ocakavane vysledky k otazkam, aj ked sa otazka opakuje.
        expected_by_question = defaultdict(deque)
        for number, label in enumerate(labels, start=1):
            expected_by_question[label["question"]].append(
                (number, json.loads(label["result"]))
            )

        scores = []
        connection = evaluator["load_database"]()
        try:
            connection.execute("PRAGMA query_only = ON")
            for prediction in read_csv(DATA_DIR / filename):
                question = prediction["question"]
                if not expected_by_question[question]:
                    raise ValueError(f"Unknown or extra question in {filename}")
                number, expected = expected_by_question[question].popleft()

                # Vykoname SQL a vypocitame skore. Neplatne SQL ma skore 0.
                score, exact, predicted_count, sql_error = 0.0, 0, "", ""
                try:
                    actual = connection.execute(prediction["predicted_sql"]).fetchall()
                    score = result_score(expected, actual)
                    exact = int(score == 1.0)
                    predicted_count = len(actual)
                except sqlite3.Error as error:
                    sql_error = str(error)

                scores.append({
                    "model": model,
                    "prompt": prompt,
                    "question_number": number,
                    "question": question,
                    "result_score": score,
                    "exact_match": exact,
                    "expected_rows": len(expected),
                    "predicted_rows": predicted_count,
                    "sql_error": sql_error,
                })
        finally:
            connection.close()

        if any(expected_by_question.values()) or not scores:
            raise ValueError(f"Missing predictions or empty dataset in {filename}")

        # Kazda otazka ma rovnaku vahu vo vyslednom priemere.
        total = len(scores)
        correct = sum(row["exact_match"] for row in scores)
        summary = {
            "model": model,
            "prompt": prompt,
            "predictions_file": filename,
            "questions": total,
            "correct": correct,
            "accuracy_percent": 100 * correct / total,
            "result_score_percent": 100 * sum(row["result_score"] for row in scores) / total,
            "sql_errors": sum(bool(row["sql_error"]) for row in scores),
        }
        summaries.append(summary)
        all_scores.extend(sorted(scores, key=lambda row: row["question_number"]))
        print(
            f"{model}, {prompt}: Skore zhody vysledkov = {summary['result_score_percent']:.2f}%, "
            f"accuracy = {summary['accuracy_percent']:.2f}% "
            f"({summary['correct']}/{summary['questions']})"
        )

    write_csv(TASK_DIR / "metric_results.csv", summaries)
    write_csv(TASK_DIR / "metric_scores.csv", all_scores)


if __name__ == "__main__":
    main()
