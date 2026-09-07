# Simbio Tutorial
Simbio Tutorial for COMBINE 2026. To run in a browser following these links to run it on marimo.app:
- https://marimo.app/https://github.com/dyscolab/simbio-tutorial/blob/main/tutorials/poincare_intro.py
- https://marimo.app/https://github.com/dyscolab/simbio-tutorial/blob/main/tutorials/simbio_intro.py
- https://marimo.app/https://github.com/dyscolab/simbio-tutorial/blob/main/tutorials/analysis.py

For running it locally, the dependencies are available via either pixi or uv.

## pixi
It is recommended to use [pixi](https://pixi.prefix.dev/latest/) to manage environments. Run

```pixi run open```

to open landing page with all tutorial notebooks in browser or

```pixi run open [path to notebook]```

to open a specific tutorial.

## uv
The same dependencies are also declared in `pyproject.toml` for [uv](https://docs.astral.sh/uv/). Run

```uv run marimo edit tutorials```

to open the landing page with all tutorial notebooks in browser or

```uv run marimo edit tutorials/poincare_intro.py```
```uv run marimo edit tutorials/simbio_intro.py```
```uv run marimo edit tutorials/io.py```
```uv run marimo edit tutorials/analysis.py```

to open a specific tutorial. Use `uv run marimo run [path to notebook]` instead to open a tutorial as a read-only app with the code hidden.
