import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")

async with app.setup(hide_code=True):
    # Setup cell for marimo notebook, can be ignored
    import marimo as mo
    import sys

    # Import packages if running on marimo playground
    if sys.executable == "/home/pyodide/this.program":
        import micropip

        await micropip.install(
            ["pint_pandas<=0.7", "typing_extensions>=4.15.0", "simbio>=1.2.0", "matplotlib"], verbose = False
        )


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Volume showcase
    By popular demand we included a quick showcase on how systems with volume work on Simbio. The API is similar, but instead of defining a `System` we define a `Compartment` and instead of using a `Variable` we use a `Species`. The only difference between a `Compartment` and a `System` is that a `Compartment` must have a single instance of a `Volume`.
    """)
    return


@app.cell
def _():
    import numpy as np
    import pint
    from simbio import Species, Volume, Parameter, Simulator, Compartment, MassAction, amount, concentration
    u = pint.get_application_registry()

    class Combustion(Compartment):
        V = Volume(initial = 3 * u.L) # Create a Volume for the Compartment
    
        CH4: Species = concentration(default = 1 * u.mol/u.L) # Create CH4 as a concentration
        O2: Species = amount(default = 1 * u.mol) # Create O2 as absolute amount
        CO2: Species = concentration(default = 0 * u.mol/u.L) # Create CO2 as concentration
        H2O: Species = concentration(default = 0 * u.mol/u.L) # Create H2O as concentration

        combustion = MassAction(reactants = [CH4, 2 * O2], products = [CO2, 2* H2O], rate = 1 * u.mol/u.L/u.s * (u.mol/u.L)**-3)

    return Combustion, Simulator, np, u


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    A `Species` is a variable that relates to a `Compartment`'s `Volume`, and they can be created to represent either an amount or a concentration. This is reflected when the reactions are converted into equations.
    """)
    return


@app.cell
def _(Combustion):
    from poincare.printing.latex import latex_equations

    latex_eqs = latex_equations(Combustion, transform={Combustion.combustion.rate: "\\text{rate}"}) # Get Latex equations source
    mo.md(latex_eqs)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Note how since `O2` is an amount it is divided by volume in the equations and multiplied by it when it appears in the left hand side.


    Simulation works as normal.
    """)
    return


@app.cell
def _(Combustion, Simulator, np, u):
    sim = Simulator(Combustion)
    result = sim.solve(save_at=np.linspace(0,10,100)*u.s)
    result
    return (result,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    And we must dequantify it to plot it:
    """)
    return


@app.cell
def _(result):
    result.pint.dequantify().to_dataframe().plot()
    return


if __name__ == "__main__":
    app.run()
