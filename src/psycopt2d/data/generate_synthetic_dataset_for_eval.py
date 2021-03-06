import datetime as dt

import numpy as np
import pandas as pd
from wasabi import Printer


def years_to_seconds(years):
    """Calculates number of seconds in a number of years.

    Args:
        years (int): Number of years.

    Returns:
        _type_: _description_
    """
    return years * 365 * 24 * 60 * 60


def return_0_with_prob(prob):
    return 0 if np.random.random() < prob else 1


def null_series_with_prob(
    series: pd.Series,
    prob: float,
    null_value=np.NaN,
) -> pd.Series:
    """Overwrite all values in series with null_value with a given probability.

    Args:
        series (pd.Series): Series.
        prop (float): The probability of overwriting all with null_value.

    Returns:
        pd.Series:
    """

    if return_0_with_prob(prob) == 0:
        # Replace all values in series with null_value
        series.loc[:] = null_value
        return series
    else:
        return series


def overwrite_prop_with_null(
    series: pd.Series,
    prop: float,
    null_value=np.NaN,
) -> pd.Series:
    """Overwrite a proportion of all values in a series with a null value (NaN
    or NaT).

    Args:
        series (pd.Series): The series to overwrite in.
        prop (float): How large a proportion to overwrite.
    """
    series.loc[
        np.random.choice(series.index, int(len(series) * prop), replace=False)
    ] = null_value

    return series


if __name__ == "__main__":
    msg = Printer(timestamp=True)
    base = pd.Timestamp.today()
    n_rows = 100_000

    df = pd.DataFrame()

    df["dw_ek_borger"] = [np.random.randint(0, 100_000) for n in range(n_rows)]

    # Generate timestamps
    df["timestamp"] = [base] * n_rows

    msg.info("Adding differences")
    df["time_differences"] = [
        dt.timedelta(
            seconds=np.random.randint(
                years_to_seconds(years=5),
                years_to_seconds(years=10),
            ),
        )
        for n in range(n_rows)
    ]
    df["timestamp"] = df["timestamp"] + df["time_differences"]
    df.drop("time_differences", axis=1, inplace=True)

    df["pred_prob"] = [(np.random.random() - 0.45) for n in range(n_rows)]
    df["pred_prob"] = df["pred_prob"].clip(0, 1)
    df["pred"] = df["pred_prob"].clip(0, 1).round()

    df["timestamp_first_pred_time"] = df.groupby("dw_ek_borger")["timestamp"].transform(
        "min",
    )

    # Generate t2d timestamps
    msg.info("Generating T2D-timestamps")
    df["timestamp_t2d_diag"] = df.groupby("dw_ek_borger")[
        "timestamp_first_pred_time"
    ].transform("min") + dt.timedelta(
        seconds=np.random.randint(0, years_to_seconds(years=5)),
    )
    df["timestamp_t2d_diag"] = df.groupby("dw_ek_borger")["timestamp_t2d_diag"].apply(
        lambda x: null_series_with_prob(x, prob=0.95),
    )

    # Generate first HbA1c timestmaps
    msg.info("Generating HbA1c timestamps")
    df["timestamp_first_hba1c"] = df.groupby("dw_ek_borger")[
        "timestamp_first_pred_time"
    ].transform("min") + dt.timedelta(
        seconds=np.random.randint(0, years_to_seconds(years=4)),
    )
    df["timestamp_hba1c_copy"] = df["timestamp_first_hba1c"]

    # Replace most with null
    msg.info("Replacing with null")
    df["timestamp_first_hba1c"] = df.groupby("dw_ek_borger")[
        "timestamp_first_hba1c"
    ].apply(lambda x: null_series_with_prob(x, prob=0.95))

    # Put back values if there is a T2D date
    msg.info("Putting back if there is T2D date")
    df["timestamp_first_hba1c"] = df.apply(
        lambda x: x["timestamp_hba1c_copy"]
        if not pd.isnull(x["timestamp_t2d_diag"])
        else x["timestamp_first_hba1c"],
        axis=1,
    )
    df.drop("timestamp_hba1c_copy", axis=1, inplace=True)

    # True label
    df["label"] = df["timestamp_t2d_diag"].notnull().astype(int)

    # Round off datetimes to whole minutes
    for col in df.columns:
        if "timestamp" in col:
            df[col] = df[col].dt.round("min")

    df.to_csv("df_synth_for_eval.csv")
