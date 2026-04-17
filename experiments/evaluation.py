from pathlib import Path
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DOMAINS = ["A", "B", "C", "D", "E"]

# Penalty Matrix penalizes undertriage in particular, i.e. when a particularly critical case has not been recognized.

penalty_matrix = np.array([
    [0, 1, 3, 6],
    [1, 0, 1, 3],
    [4, 2, 0, 1],
    [9, 6, 3, 0]
])


def severity_penalty(gold, pred):
    return int(penalty_matrix[int(gold), int(pred)])


def add_penalty_columns(df: pd.DataFrame):
    """
    Expected gold columns: A,B,C,D,E (int/float)
    Expected run columns:  A_1, A_2, ..., B_1, ... (numeric)
    Adds:            A_1_error, A_2_error, ..., E_n_error
    """

    run_cols = [c for c in df.columns if re.fullmatch(r"[ABCDE]_\d+", str(c))]
    if not run_cols:
        raise ValueError("No run cols found.")

    def calc_row(row, gold_col, pred_col):
        gold = row.get(gold_col, None)
        pred = row.get(pred_col, None)

        if pd.isna(gold) or pd.isna(pred):
            return pd.NA

        return severity_penalty(gold, pred)

    for pred_col in run_cols:
        domain = pred_col.split("_")[0]  # "A"
        err_col = f"{pred_col}_error"  # "A_1_error"

        df[err_col] = df.apply(calc_row, axis=1, args=(domain, pred_col))

    return df


# Calculation of confidence weighted error values

def confidence_error(error, confidence):
    # If the answer is correct (error = 0), then there is a penalty for low confidence; if the answer is incorrect, there is a penalty for high confidence.
    if error == 0:
        return 1 - confidence  # Penalty for low confidence
    else:
        return error * confidence  # Penalty for high confidence



def add_conf_error_columns(df: pd.DataFrame, confidence_error):
    """
    Expected columns:
      - Error:      A_1_error, B_2_error, ...
      - Confidence: A_1_conf,  B_2_conf,  ...
    Adds:
      - A_1_conf_error, B_2_conf_error, ...
    """

    error_cols = [c for c in df.columns if re.fullmatch(r"[ABCDE]_\d+_error", str(c))]
    if not error_cols:
        raise ValueError("No error cols found.")

    def calc_row(row, err_col, conf_col):
        err = row.get(err_col, None)
        conf = row.get(conf_col, None)

        if pd.isna(err) or pd.isna(conf):
            return pd.NA

        return confidence_error(err, conf)

    for err_col in error_cols:
        # err_col: "A_12_error" -> domain="A", run="12"
        m = re.match(r"([ABCDE])_(\d+)_error$", err_col)
        domain, run = m.group(1), m.group(2)

        conf_col = f"{domain}_{run}_conf"
        if conf_col not in df.columns:
            raise ValueError(f"Confidence-Spalte fehlt für {err_col}: erwartet '{conf_col}'")

        out_col = f"{domain}_{run}_conf_error"
        df[out_col] = df.apply(calc_row, axis=1, args=(err_col, conf_col))

    return df


# Sorts the columns, but also takes into account that A_1, A_10, A_11 is an incorrect order.
def natural_sort_key(col):
    return [
        int(text) if text.isdigit() else text
        for text in re.split(r'(\d+)', col)
    ]


# Main function for reading in the runs, loading the gold, joining, and calculating the errors

def build_results(results_folder="results"):
    folder_path = Path(results_folder)
    csv_files = sorted(folder_path.glob("*.csv"))

    df_merged = None

    for run_idx, file_path in enumerate(csv_files, start=1):
        df = pd.read_csv(file_path)

        if "call_nr" not in df.columns:
            raise ValueError(f"'call_nr' fehlt in {file_path.name}")

        df = df.set_index("call_nr")

        rename_dict = {}

        for domain in ["A", "B", "C", "D", "E"]:
            rename_dict[f"severity_{domain}"] = f"{domain}_{run_idx}"
            rename_dict[f"confidence_{domain}"] = f"{domain}_{run_idx}_conf"
            # rename_dict[f"findings_{domain}"] = f"{domain}_{run_idx}_findings"   # If findings should be included
            # rename_dict[f"error_{domain}"] = f"{domain}_{run_idx}_error"

        df = df.rename(columns=rename_dict)
        df = df[list(rename_dict.values())]

        if df_merged is None:
            df_merged = df
        else:
            df_merged = df_merged.join(df, how="outer")

    df_merged = df_merged.sort_index()

    # Gold values
    df_gold = pd.read_csv(PROJECT_ROOT / "emergency_calls" / "abcde_analysis.csv", index_col="call_nr", sep=";")

    df_gold = df_gold.rename(columns={
        "a": "A",
        "b": "B",
        "c": "C",
        "d": "D",
        "e": "E"
    })

    df = df_merged.join(df_gold, how="left")

    # Calculate error
    df = add_penalty_columns(df)

    # Calculate error (weighted error)
    df = add_conf_error_columns(df, confidence_error)

    # natural sort
    df = df[sorted(df.columns, key=natural_sort_key)]

    return df


#only for experiment 1 without confidence or findings
def build_results_short(results_folder="results"):
    folder_path = Path(results_folder)
    csv_files = sorted(folder_path.glob("*.csv"))

    df_merged = None

    for run_idx, file_path in enumerate(csv_files, start=1):
        df = pd.read_csv(file_path)

        if "call_nr" not in df.columns:
            raise ValueError(f"'call_nr' fehlt in {file_path.name}")

        df = df.set_index("call_nr")

        rename_dict = {}

        for domain in ["A", "B", "C", "D", "E"]:
            rename_dict[f"severity_{domain}"] = f"{domain}_{run_idx}"
            #rename_dict[f"confidence_{domain}"] = f"{domain}_{run_idx}_conf"
            # rename_dict[f"findings_{domain}"] = f"{domain}_{run_idx}_findings"   # If findings should be included
            # rename_dict[f"error_{domain}"] = f"{domain}_{run_idx}_error"

        df = df.rename(columns=rename_dict)
        df = df[list(rename_dict.values())]

        if df_merged is None:
            df_merged = df
        else:
            df_merged = df_merged.join(df, how="outer")

    df_merged = df_merged.sort_index()

    # Gold values
    df_gold = pd.read_csv(PROJECT_ROOT / "emergency_calls" / "abcde_analysis.csv", index_col="call_nr", sep=";")

    df_gold = df_gold.rename(columns={
        "a": "A",
        "b": "B",
        "c": "C",
        "d": "D",
        "e": "E"
    })

    df = df_merged.join(df_gold, how="left")

    # Calculate error
    df = add_penalty_columns(df)

    # Calculate error (weighted error)
    #df = add_conf_error_columns(df, confidence_error)

    # natural sort
    df = df[sorted(df.columns, key=natural_sort_key)]

    return df





# Graphical representation

def wide_to_long_runs(df_wide: pd.DataFrame) -> pd.DataFrame:
    """
    Expects a Wide-DF with:
      - call_nr (column or index)
      - Gold columns: A,B,C,D,E
      - Pred columns: A_1, A_2, ..., B_1, ...

    Returns Long-DF:
      call_nr, domain, run, pred, gold
    """
    df = df_wide.copy()

    if "call_nr" in df.columns:
        df = df.set_index("call_nr")
    if df.index.name != "call_nr":
        df.index.name = "call_nr"

    run_ids = sorted({
        int(m.group(1))
        for c in df.columns
        for m in [re.match(r"^[ABCDE]_(\d+)$", str(c))]
        if m
    })
    if not run_ids:
        raise ValueError("No run col found")

    all_long = []
    for r in run_ids:
        for d in DOMAINS:
            pred_col = f"{d}_{r}"
            gold_col = d

            if gold_col not in df.columns:
                raise ValueError(f"Gold-Spalte fehlt: '{gold_col}'")
            if pred_col not in df.columns:
                continue

            tmp = df[[gold_col, pred_col]].copy()
            tmp = tmp.rename(columns={gold_col: "gold", pred_col: "pred"})
            tmp["domain"] = d
            tmp["run"] = f"run{r}"
            tmp["call_nr"] = tmp.index
            all_long.append(tmp[["call_nr", "domain", "run", "pred", "gold"]])

    long_df = pd.concat(all_long, ignore_index=True)

    # Typisieren
    long_df["call_nr"] = pd.to_numeric(long_df["call_nr"], errors="coerce").astype("Int64")
    long_df["pred"] = pd.to_numeric(long_df["pred"], errors="coerce")
    long_df["gold"] = pd.to_numeric(long_df["gold"], errors="coerce")

    return long_df


def plot_runs_vs_gold_big(long_df: pd.DataFrame, title="Gold vs Runs pro Call (A–E)"):
    """
    Large overview plot:
    - 5 lines (A..E)
    - x-axis: call_nr
    - Gold as points
    - One X per run (slightly jittered)
    """
    fig, axes = plt.subplots(5, 1, sharex=True, figsize=(14, 10))

    runs = sorted(long_df["run"].dropna().unique().tolist())
    n_runs = max(len(runs), 1)

    # jitter on the x-axis so that runs are visible separately
    step = 0.8
    offsets = {r: (i - (n_runs - 1) / 2) * (step / max(n_runs - 1, 1)) for i, r in enumerate(runs)}

    for i, d in enumerate(DOMAINS):
        ax = axes[i]
        sub = long_df[long_df["domain"] == d].copy().dropna(subset=["call_nr"])

        gold_per_call = (
            sub.dropna(subset=["gold"])
               .sort_values(["call_nr", "run"])
               .drop_duplicates(subset=["call_nr"])[["call_nr", "gold"]]
        )
        ax.scatter(gold_per_call["call_nr"], gold_per_call["gold"], s=40, label="Gold")

        # Runs als X
        for r in runs:
            rsub = sub[sub["run"] == r].dropna(subset=["pred"])
            if rsub.empty:
                continue
            x = rsub["call_nr"].astype(float) + offsets.get(r, 0.0)
            ax.scatter(x, rsub["pred"], marker="x", s=40, label=r)

        ax.set_ylabel(d)
        ax.set_ylim(-0.2, 3.2)
        ax.grid(True)

        if i == 0:
            ax.legend(ncol=4, fontsize=9)

    axes[-1].set_xlabel("Call (call_nr)")

    plt.suptitle(title)
    plt.tight_layout()

    return fig


## Evaluate Results

# Wide to Long DF
def errors_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expect columns such as:
      A_1_error, A_1_conf_error, B_2_error, ...
    Returns Long-DF:
      call_nr, run, domain, error, conf_error
    """
    dfx = df.copy()
    if "call_nr" in dfx.columns:
        dfx = dfx.set_index("call_nr")
    if dfx.index.name != "call_nr":
        dfx.index.name = "call_nr"

    rows = []
    pat = re.compile(r"^([ABCDE])_(\d+)_(conf_)?error$")

    for col in dfx.columns:
        m = pat.match(str(col))
        if not m:
            continue
        domain, run, is_conf = m.group(1), int(m.group(2)), m.group(3) is not None
        rows.append((col, domain, run, is_conf))

    if not rows:
        raise ValueError("No error cols found.")

    # build Long
    long_parts = []
    for col, domain, run, is_conf in rows:
        tmp = dfx[[col]].copy()
        tmp = tmp.rename(columns={col: "value"})
        tmp["domain"] = domain
        tmp["run"] = run
        tmp["type"] = "conf_error" if is_conf else "error"
        tmp["call_nr"] = tmp.index
        long_parts.append(tmp[["call_nr", "run", "domain", "type", "value"]])

    long_df = pd.concat(long_parts, ignore_index=True)
    long_df["call_nr"] = pd.to_numeric(long_df["call_nr"], errors="coerce").astype("Int64")
    long_df["run"] = pd.to_numeric(long_df["run"], errors="coerce").astype(int)
    long_df["value"] = pd.to_numeric(long_df["value"], errors="coerce")

    return long_df


def summarize_errors(long_df: pd.DataFrame) -> pd.DataFrame:
    """
    Output: pro run × domain × type
      N, mean, median, sum, rmse (auf value)
    """
    def rmse(x):
        x = pd.to_numeric(x, errors="coerce").dropna()
        return float(np.sqrt((x**2).mean())) if len(x) else np.nan

    summary = (
        long_df
        .groupby(["type", "run", "domain"], as_index=False)
        .agg(
            N=("value", "count"),
            mean=("value", "mean"),
            median=("value", "median"),
            sum=("value", "sum"),
            rmse=("value", rmse),
        )
        .sort_values(["type", "run", "domain"])
    )
    return summary


def total_error_per_run(df: pd.DataFrame):
    """
    Expect columns such as:
      A_1_error, A_1_conf_error, B_2_error, ...
    Returns DataFrame with:
      run, sum_error, sum_conf_error
    """

    # identify all error cols
    error_cols = [c for c in df.columns if re.fullmatch(r"[ABCDE]_\d+_error", str(c))]
    conf_error_cols = [c for c in df.columns if re.fullmatch(r"[ABCDE]_\d+_conf_error", str(c))]

    # extract run IDs
    runs = sorted({
        int(re.search(r"_(\d+)_", c).group(1))
        for c in error_cols + conf_error_cols
    })

    rows = []

    for r in runs:
        cols_err = [f"{d}_{r}_error" for d in "ABCDE" if f"{d}_{r}_error" in df.columns]
        cols_conf = [f"{d}_{r}_conf_error" for d in "ABCDE" if f"{d}_{r}_conf_error" in df.columns]

        sum_error = df[cols_err].sum().sum() if cols_err else 0
        sum_conf_error = df[cols_conf].sum().sum() if cols_conf else 0

        rows.append({
            "run": r,
            "sum_error": sum_error,
            "sum_conf_error": sum_conf_error
        })

    result = pd.DataFrame(rows).sort_values("run").reset_index(drop=True)
    return result


def error_summary_per_category(df: pd.DataFrame):
    """
    Calculated per domain (A–E):
    - mean_error
    - sum_error
    - rmse_error
    - mean_conf_error
    - sum_conf_error
    - rmse_conf_error
    across all runs and calls.
    """

    results = []

    for d in DOMAINS:
        err_cols = [c for c in df.columns if re.fullmatch(fr"{d}_\d+_error", str(c))]
        conf_cols = [c for c in df.columns if re.fullmatch(fr"{d}_\d+_conf_error", str(c))]

        err_vals = df[err_cols].values.flatten() if err_cols else np.array([])
        conf_vals = df[conf_cols].values.flatten() if conf_cols else np.array([])

        err_vals = pd.to_numeric(pd.Series(err_vals), errors="coerce").dropna()
        conf_vals = pd.to_numeric(pd.Series(conf_vals), errors="coerce").dropna()

        results.append({
            "domain": d,
            "mean_error": err_vals.mean() if len(err_vals) else np.nan,
            "sum_error": err_vals.sum() if len(err_vals) else np.nan,

            "mean_conf_error": conf_vals.mean() if len(conf_vals) else np.nan,
            "sum_conf_error": conf_vals.sum() if len(conf_vals) else np.nan,

        })

    return pd.DataFrame(results).sort_values("domain")