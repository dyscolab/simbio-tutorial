import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")

async with app.setup(hide_code=True):
    # Setup cell for marimo notebook, can be ignored
    import marimo as mo
    import sys
    import subprocess
    from pathlib import Path

    # Import packages if running on marimo playground
    if sys.executable == "/home/pyodide/this.program":
        import micropip

        await micropip.install(
            ["pint_pandas<=0.7", "typing_extensions>=4.15.0", "simbio>=1.2.0", "matplotlib"], verbose = False
        )

    def compile_latex(tex_path: str, destination_path: str) -> None:
        tex_path = Path(tex_path).resolve()
        destination_path = Path(destination_path).resolve()

        destination_path.parent.mkdir(parents=True, exist_ok=True)

        subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-output-directory",
                str(destination_path.parent),
                str(tex_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        generated_pdf = destination_path.parent / f"{tex_path.stem}.pdf"

        if not generated_pdf.exists():
            raise RuntimeError("LaTeX compilation failed: no PDF was generated.")

        if generated_pdf != destination_path:
            generated_pdf.replace(destination_path)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # IO in SimBio
    Being meant as a central source of truth for your models, SimBio contains a number of tools to input models from other sources (SBML) and translate it into ohter formats.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Importing models from SBML
    SimBio has the capability to directly import and use models in the [SBML](https://sbml.org/) (Systems Biology Markup Language) format, although it is still an experimantal feature with ongoing work, so importing some models might fail. Aside from opening local files we can also directly download and import import the large amount of existing models from [BioModels](http://biomodels.org/). They can be imported by their BioModels ID using the `load` function:
    """)
    return


@app.cell
def _():
    from simbio.io.biomodels import load

    biomd_id = 35
    model = load(f"BIOMD{biomd_id}")
    model
    return (model,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The imported model works as any `System` in SimBio, so we can simulate it normally.
    """)
    return


@app.cell
def _(model):
    from simbio import Simulator
    import numpy as np

    sim = Simulator(model)
    sim.solve(save_at=np.linspace(0,10,100)).to_dataframe().plot()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Model Reports
    The other half of IO is output. We can use SimBio's `model_report` function to get latex source for a report with all of models equations, variables and parameters. This will also give us a better idea about the model we imported.
    """)
    return


@app.cell
def _(model):
    from simbio.latex import model_report

    model_report(model)
    return (model_report,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    We can also have it write to file if we provide a path
    """)
    return


@app.cell
def _(model, model_report):
    model_report(model, path="./documents/latex_example.tex", replace_algebraics=True)

    compile_latex("./documents/latex_example.tex", "./documents/latex_example.pdf") # function to call pdflatex, defined in setup cell

    mo.pdf(src=Path("./documents/latex_example.pdf"))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Here we use a function defined in the setup cell to complie it in the notebook, but after writing it with `model_report` you can use the latex complier and editor of your choice.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Stohcastic simulation
    As part of SimBio's goal of bieng a central place for all analysis the same models can be simulated stochastically with the [Gillespie algorithm](https://en.wikipedia.org/wiki/Gillespie_algorithm) via an interface with the [rebop](https://rebop.readthedocs.io/en/latest/) library. The interface is similar but we must use a `RebopSiumlator` instad of a regular one. We also pass `solve` an end time `upto_t` and a number of points `n_points` instead of a `save_at`.
    """)
    return


@app.cell
def _(model):
    from simbio.rebop import RebopSimulator

    rsim= RebopSimulator(model)
    rsim.solve(upto_t=10, n_points=100).to_dataframe().plot()
    return


if __name__ == "__main__":
    app.run()
