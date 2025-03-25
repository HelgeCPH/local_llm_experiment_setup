import pandas as pd
import numpy as np


df = pd.read_csv("data.csv", delimiter=';')
cols = [
    "Exam Set", "With AI", "Participant", "Unit Test", "Grade", "Task 1",
    "Task 2", "Task 3", "Task 4", "Task 5", "Task 6", "Task 7", "Task 8",
    "Task 9", "Task 1 points", "Task 2 points", "Task 3 points",
    "Task 4 points", "Task 5 points", "Task 6 points", "Task 7 points",
    "Task 8 points", "Task 9 points"
]


def split_time_and_number_of_prompts_stats(value):
    if pd.isna(value):
        return np.nan, np.nan
    parts = value.split()
    if len(parts) == 2:
        t, no_prompts = int(parts[0]), int(parts[1])
    elif len(parts) == 1:
        t = int(parts[0])
        no_prompts = np.nan
    else:
        pass  # That case does not exist in our dataset
    return t, no_prompts


def create_time_df():
    new_rows = []
    for _, row in df[cols].iterrows():
        row_vals_pre = []
        for col_name in cols:
            row_vals = []
            el = row[col_name]
            if col_name == "Exam Set":
                row_vals_pre.append(int(el.replace("Exam set ", "")))
            elif col_name == "With AI":
                row_vals_pre.append(
                    True) if el == "Yes" else row_vals_pre.append(False)
            elif col_name == "Participant":
                row_vals_pre.append(int(el))
            elif col_name == "Unit Test":
                row_vals_pre.append(int(el))
            elif col_name == "Grade":
                row_vals_pre.append(int(el))
            elif col_name.startswith("Task") and not col_name.endswith("points"):
                # if pd.isna(el):
                #     continue
                task_nr = int(col_name.split()[1])
                time_in_s, no_prompts = split_time_and_number_of_prompts_stats(
                    el)
                row_vals = row_vals_pre.copy(
                ) + [task_nr, time_in_s, no_prompts]
                new_rows.append(row_vals)
    new_cols = [
        "exam_set", "llm_support", "experiment_subject", "test_ratio",
        "grade", "task_no", "time", "no_prompts",  # "points"
    ]
    return pd.DataFrame(new_rows, columns=new_cols)


def create_points_df():
    new_rows = []
    for _, row in df[cols].iterrows():
        row_vals_pre = []
        for col_name in cols:
            row_vals = []
            el = row[col_name]
            if col_name == "Exam Set":
                row_vals_pre.append(int(el.replace("Exam set ", "")))
            elif col_name == "With AI":
                row_vals_pre.append(
                    True) if el == "Yes" else row_vals_pre.append(False)
            elif col_name == "Participant":
                row_vals_pre.append(int(el))
            elif col_name == "Unit Test":
                row_vals_pre.append(int(el))
            elif col_name == "Grade":
                row_vals_pre.append(int(el))
            elif col_name.startswith("Task") and col_name.endswith("points"):
                # if pd.isna(el):
                #     continue
                task_nr = int(col_name.split()[1])
                row_vals = row_vals_pre.copy() + [task_nr, el, ]
                new_rows.append(row_vals)

    new_cols = [
        "exam_set", "llm_support", "experiment_subject", "test_ratio",
        "grade", "task_no", "points"
    ]
    return pd.DataFrame(new_rows, columns=new_cols)


def main():
    df = create_time_df()
    df2 = create_points_df()
    df["points"] = df2["points"]

    # remove rows for tasks that do not exist in the exam set
    mask = (df.exam_set == 2) & (df.task_no > 7)
    df.drop(df[mask].index, inplace=True)

    df.to_csv("dataclean.csv", index=False)


if __name__ == '__main__':
    main()
