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
            ["pint_pandas<=0.7", "typing_extensions>=4.15.0", "poincare>=1.1.2", "matplotlib"], verbose = False
        )


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Poincare introduction

    Poincare is dyscolabs's general dynamical systems simulation library, on which SimBio is based. It will be useful to learn Poincare's basic first.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## A simple example
    Models are represented as classes which inherit for `System`.
    """)
    return


@app.cell
def _():
    import numpy as np
    from poincare import System, Variable, initial

    class Model(System):
        # Define a variable with name `x` with an initial value (t=0) of `1``.
        x: Variable = initial(default=1)
        # The derivative of `x` is assigned (<<) to `-x`.
        # This relation is assigned to a Python variable (`eq`)
        eq = x.derive() << -x

    return Model, System, Variable, initial, np


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    This represents the equation
    $$\frac{dx}{dt} = -x $$
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Simulation is as simple as creating a `Simulator` for our System and calling the `solve` method.
    """)
    return


@app.cell
def _(Model, np):
    from poincare import Simulator

    sim_1 = Simulator(Model)
    result_1 = sim_1.solve(save_at=np.linspace(0,5,50))
    result_1
    return Simulator, result_1


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The output is an [xarray](https://docs.xarray.dev/en/stable/) `Dataset`, which can be plotted via conversion to a more familiar pandas `DataFrame`.
    """)
    return


@app.cell
def _(result_1):
    result_1.to_dataframe().plot()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    As is usual with igher order systems require explicit declaration of derivatives. To declare a harmonic oscillator
    $$ \frac{d^2 x}{dt^2} = -k\cdot x $$
    we can write:
    """)
    return


@app.cell
def _(System, Variable, initial):
    from poincare import Derivative, Parameter, assign

    class Oscillator(System):
        x: Variable = initial(default=1)
        # Declare derivative for x with default value 0
        v: Derivative = x.derive(initial=0)

        # Declare parameter k
        k: Parameter = assign(default=1)

        eq = v.derive() << -k*x

    return Oscillator, Parameter, assign


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The initial values in a `System`'s declaration are only defaults: they can be changed by calling `with_values` on a simulator.
    """)
    return


@app.cell
def _(Oscillator, Simulator, np):
    sim_2 = Simulator(Oscillator)
    result_2 = sim_2.with_values({Oscillator.v :2}).solve(save_at=np.linspace(0,10,100))
    result_2.to_dataframe().plot()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Model composition
    One of poincare's big features is that models are composable: smaller parts can be combined to make a lager model. We can use this to add damping to the oscillator without starting again from scratch.
    """)
    return


@app.cell
def _(Oscillator, Parameter, System, assign):
    class DampedOscillator(System):
        # Create Oscillator, adds all variables, parameters and equations
        # v = 0 changes defualt initial condition for v
        osc = Oscillator(v = 0.5) 

        # Damping constant
        gamma: Parameter = assign(default = 0.5)

        # Acces the oscillators variables with osc.(variable)
        eq = osc.v.derive() << -gamma *osc.v

    return (DampedOscillator,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Instancing `Oscillator` adds all variables, parameters and equations to the outer system; passing `v = 0` when instancing changes the default initial conditon for `osc.v`. Inner variables or parameters can be accesed as attributes with osc.(variable) syntax. The new equation we declare will be added to the one we already declared inside of `Oscillator`, so the total equation woud be

    $$ \frac{d^2 x}{dt^2} = -k\cdot x - \gamma \cdot v. $$



    Simulation works as normal, and internal parametrs' value can be changed with the same `Parent.nested.paramter` syntax:
    """)
    return


@app.cell
def _(DampedOscillator, Simulator, np):
    # Initial values can also be changed at simulator creation
    sim_3 = Simulator(DampedOscillator).with_values({DampedOscillator.osc.k: 2})
    result_3 = sim_3.solve(save_at = np.linspace(0,20,200))
    result_3.to_dataframe().plot()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Excercises
    **1)** Lets bring this a little closer to biology. Declare and simulate the classic LoktaVolterra predator-prey model:

    $$ \begin{align}
    \frac{d\,\text{prey}}{dt} &= \text{prey} \cdot (\alpha - \beta \cdot  \text{predator}),\\
    \frac{d\,\text{predator}}{dt} &= \text{predator} \cdot (\delta \cdot \text{prey} - \gamma).
    \end{align} $$

    Use values $\alpha = 1,\ \beta = 0.1,\ \gamma = 1.5,\ \delta = 0.075$ and simulate it first with $\text{prey}(0) = 50$, $\text{predator}(0) = 10$ and then with $\text{prey}(0) = 10$, $\text{predator}(0) = 50$.

    **2)** Use the `Oscillator` class from above to declare coupled oscillators by instancing it twice in a larger `System` and adding the equations

    $$ \begin{align}
    \frac{d^2x_1}{dt^2} &= k_c\cdot x_2, \\
    \frac{d^2x_2}{dt^2} &= k_c\cdot x_1.
    \end{align} $$

    When creatieng it pass arguments to the instantced systmes to give them initial conditions $x_1(0) = 1, \ x_2(0) = 0$. Then simulate it with no coupling ($k_c = 0$), weak coupling ($k_c = 0.1$) and strong coupling ($k_c=1$).
    """)
    return


if __name__ == "__main__":
    app.run()
