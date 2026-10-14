"""Task_4: paired statistical tests and graphs for the saved Task_2/Task_3 results."""

import csv
import os
import re
import tempfile
from itertools import combinations
from pathlib import Path

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "ai4se-task4-matplotlib-config")
)
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binomtest, permutation_test


TASK_DIR = Path(__file__).resolve().parent
METRIC_DIR = TASK_DIR.parent / "Task_3"
MODELS = ["GPT-6 sol (High)", "GPT-5.6 sol (light)"]
PROMPTS = ["APE", "STAR", "ToT"]
ALPHA = 0.05
SEED = 20261014
RESAMPLES = 200_000


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def recorded_times():
    """Read the user's measured times from the two tables in Report.md."""
    report = (TASK_DIR.parent / "Report.md").read_text(encoding="utf-8-sig")
    times = {}
    for section_number, model in enumerate(MODELS, start=1):
        section = report.split(f"### 2.{section_number} {model}", 1)[1]
        section = section.split("###", 1)[0].split("## Task_3", 1)[0]
        pattern = r"\|\s*(APE|STAR|ToT)\s*\|\s*(?:\d+/\d+\s*\|\s*)?[\d.]+\s*\|\s*(\d+)m\s*(\d+)s\s*\|"
        for prompt, minutes, seconds in re.findall(pattern, section):
            times[model, prompt] = 60 * int(minutes) + int(seconds)
    if len(times) != 6:
        raise ValueError("Expected six recorded times in the Task_2 tables")
    return times


def exact_mcnemar(first, second):
    """Two-sided exact test using only questions with different correctness."""
    first_only = int(np.sum((first == 1) & (second == 0)))
    second_only = int(np.sum((first == 0) & (second == 1)))
    discordant = first_only + second_only
    p = binomtest(min(first_only, second_only), discordant, p=0.5).pvalue if discordant else 1.0
    return float(p), discordant


def paired_score_test(first, second):
    """Swap scores within each question; compare the mean score difference."""
    differences = second - first
    # Zero differences do not affect any swap, so omit them from enumeration.
    nonzero = differences[np.abs(differences) > 1e-12]
    if not len(nonzero):
        return 1.0, "identical scores", 0
    exact = len(nonzero) <= 20
    result = permutation_test(
        (nonzero,), np.mean,
        permutation_type="samples", vectorized=True,
        n_resamples=np.inf if exact else RESAMPLES,
        batch=4096, alternative="two-sided",
        rng=np.random.default_rng(SEED),
    )
    method = "exact paired permutation" if exact else f"paired permutation ({RESAMPLES} resamples)"
    return float(result.pvalue), method, len(nonzero)


def holm_adjust(pvalues):
    """Holm correction across all twelve prompt comparisons in this analysis."""
    adjusted = [0.0] * len(pvalues)
    previous = 0.0
    for rank, index in enumerate(sorted(range(len(pvalues)), key=pvalues.__getitem__)):
        previous = max(previous, min(1.0, (len(pvalues) - rank) * pvalues[index]))
        adjusted[index] = previous
    return adjusted


def make_graphs(results):
    colors = ["#2563EB", "#D97706"]
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    x = np.arange(len(PROMPTS))
    width = 0.34
    by_run = {(row["model"], row["prompt"]): row for row in results}

    def draw(ax, field, title, ylabel, percentage=False):
        for index, model in enumerate(MODELS):
            values = [by_run[model, prompt][field] for prompt in PROMPTS]
            bars = ax.bar(x + (index - 0.5) * width, values, width,
                          label=model, color=colors[index])
            ax.bar_label(bars, fmt="%.2f" if percentage else "%d", padding=3, fontsize=8)
        ax.set_xticks(x, PROMPTS)
        ax.set_title(title, pad=12)
        ax.set_ylabel(ylabel)
        ax.set_ylim(0, 106 if percentage else 145)
        if percentage:
            ax.set_yticks(range(0, 101, 20))
        ax.set_axisbelow(True)
        ax.grid(axis="y", alpha=0.2)
        ax.legend(loc="lower left", fontsize=8)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), layout="constrained")
    draw(axes[0], "accuracy_percent", "Presnost uplnych odpovedi", "Accuracy (%)", True)
    draw(axes[1], "result_score_percent", "Zhoda vyslednych riadkov", "Skore zhody (%)", True)
    fig.savefig(TASK_DIR / "metrics_comparison.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5), layout="constrained")
    draw(ax, "time_seconds", "Namerane casy jednotlivych behov", "Cas (s)")
    fig.savefig(TASK_DIR / "times_comparison.png", dpi=180)
    plt.close(fig)


def main():
    csv.field_size_limit(1_000_000_000)
    summaries = read_csv(METRIC_DIR / "metric_results.csv")
    score_rows = read_csv(METRIC_DIR / "metric_scores.csv")
    times = recorded_times()
    groups = {}
    reference_questions = None
    for model in MODELS:
        for prompt in PROMPTS:
            rows = sorted(
                (row for row in score_rows if row["model"] == model and row["prompt"] == prompt),
                key=lambda row: int(row["question_number"]),
            )
            questions = [(int(row["question_number"]), row["question"]) for row in rows]
            if len(rows) != 155 or len(set(number for number, _ in questions)) != 155:
                raise ValueError("Expected 155 unique question numbers for every run")
            if reference_questions is not None and questions != reference_questions:
                raise ValueError("The runs must contain the same questions for paired tests")
            reference_questions = questions
            groups[model, prompt] = {
                field: np.array([float(row[field]) for row in rows])
                for field in ["exact_match", "result_score"]
            }

    results = []
    for row in summaries:
        values = groups[row["model"], row["prompt"]]
        for field, source in [("accuracy_percent", "exact_match"), ("result_score_percent", "result_score")]:
            if not np.isclose(float(row[field]), 100 * np.mean(values[source]), atol=1e-10):
                raise ValueError("Summary and per-question scores disagree")
        results.append({
            "model": row["model"], "prompt": row["prompt"],
            "accuracy_percent": float(row["accuracy_percent"]),
            "result_score_percent": float(row["result_score_percent"]),
            "time_seconds": times[row["model"], row["prompt"]],
            "questions": int(row["questions"]), "correct": int(row["correct"]),
            "sql_errors": int(row["sql_errors"]),
        })

    tests = []
    for model in MODELS:
        for first, second in combinations(PROMPTS, 2):
            for field, metric in [("exact_match", "accuracy"), ("result_score", "result_score")]:
                a, b = groups[model, first][field], groups[model, second][field]
                if field == "exact_match":
                    p, different_questions = exact_mcnemar(a, b)
                    method = "exact McNemar"
                else:
                    p, method, different_questions = paired_score_test(a, b)
                tests.append({
                    "model": model, "first_prompt": first, "second_prompt": second,
                    "metric": metric, "second_minus_first_pp": float(100 * np.mean(b - a)),
                    "different_questions": different_questions, "method": method,
                    "p_raw": p, "p_holm": 0.0, "significant": False,
                })
    for row, adjusted in zip(tests, holm_adjust([row["p_raw"] for row in tests])):
        row["p_holm"] = adjusted
        row["significant"] = adjusted < ALPHA
        print(f"{row['model']}, {row['first_prompt']} vs {row['second_prompt']}, "
              f"{row['metric']}: p={row['p_raw']:.6f}, Holm p={adjusted:.6f}, "
              f"significant={row['significant']}")

    write_csv(TASK_DIR / "comparison_results.csv", results)
    write_csv(TASK_DIR / "statistical_tests.csv", tests)
    make_graphs(results)


if __name__ == "__main__":
    main()
