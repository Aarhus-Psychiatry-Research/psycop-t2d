Current priorities are on the 
[Board 🎬](https://github.com/orgs/Aarhus-Psychiatry-Research/projects/4/views/1).

psycop-t2d
==============================
![python versions](https://img.shields.io/badge/Python-%3E=3.7-blue)
[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)

Prediction of type 2 diabetes among patients with visits to psychiatric hospital departments.

## Installing pre-commit hooks
`pre-commit install`

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------
## Testing configs
To run XGBoost with defaults but a synth dataset:

```
python src/psycopt2d/train_model.py --config-name test_config.yaml +model=xgboost
```

## Train models:
To run XGBoost with defaults:

```
python src/psycopt2d/train_model.py +model=xgboost
```

if you want to change a hyperparameter simply run:

```
python src/psycopt2d/train_model.py  +model=xgboost ++model.args.n_estimators=20
```

to run a sweep with xgboost you will have to add the `--multirun` flag and specify the sweep config.
```
python src/psycopt2d/train_model.py --multirun +model=xgboost
```

## Logging Altair to WandB and saving as png
We use Selenium and chromedriver to save Altair charts as png. This works out-of-the-box on Overtaci, but requires you to download [chromedriver](https://chromedriver.chromium.org) and place it on PATH (e.g. `/usr/local/bin` on OSX) to use locally. Optionally, [see this guide](https://www.swtestacademy.com/install-chrome-driver-on-mac/). If on OSX, you'll probably need to give chromedriver permission to be run. Move to the folder containing the file and run the following line in a terminal:

```
xattr -d com.apple.quarantine chromedriver
```


Minimal example of logging Altair chart to WandB
```py
run = wandb.init()

source = pd.DataFrame(
    {
        "a": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
        "b": [28, 55, 43, 91, 81, 53, 19, 87, 52],
    }
)

chart = alt.Chart(source).mark_bar().encode(x="a", y="b")

tmp_filename = "chart.png"
chart.save(tmp_filename)

run.log({"dummy_chart" : wandb.Image(tmp_filename)})
```




<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
