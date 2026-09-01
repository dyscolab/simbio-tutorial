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
            ["pint_pandas<=0.7", "typing_extensions>=4.15.0", "simbio>=1.1.0", "matplotlib"], verbose = False
        )


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # SimBio introduction
    SimBio extends Poincare with bindings created specifically for simulation of Chemical Reaction Networks (CRNs).
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Rate laws and mass action

    SimBio's main differnece is that a system's dynamics are declared as reaction instead as equations. The simplest one is the `RateLaw`, which we can use to simulate a simple $2H + O \rightarrow H_2O$ synthesis.
    """)
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    from simbio import Parameter, assign,System, RateLaw, Variable, initial

    class SynthesisRL(System):
        # Create species H, O, and H2O, each with intial value 1
        H: Variable = initial(default=1)
        O: Variable = initial(default=1)
        H2O: Variable = initial(default=0)

        k: Parameter = assign(default = 1)
    
        # Reaction 2H + O -> H2O at rate 3
        reaction = RateLaw(reactants=[2 * H, O], products=[H2O], rate_law=k)

    return Parameter, SynthesisRL, System, Variable, assign, initial, np


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    This represents the equations
    $$
    \begin{aligned}
    \frac{dH}{dt} &= -2\cdot k, \\
    \frac{dO}{dt} &= -1\cdot k, \\
    \frac{dH2O}{dt} &= +1\cdot k.
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Simulation works the same as in Poincare.
    """)
    return


@app.cell
def _(SynthesisRL, np):
    from simbio import Simulator

    sim_1 = Simulator(SynthesisRL)
    result_1 = sim_1.solve(save_at = np.linspace(0,10,100))
    result_1.to_dataframe().plot()
    return (Simulator,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    To geta more realistic simulation we can use `MassAction`, which assigns rates according to the [law of mass action](https://en.wikipedia.org/wiki/Law_of_mass_action).
    """)
    return


@app.cell
def _(Parameter, Simulator, System, Variable, assign, initial, np):
    from simbio import MassAction

    class SynthesisMA(System):
        H: Variable = initial(default=1)
        O: Variable = initial(default=1)
        H2O: Variable = initial(default=0)

        k: Parameter = assign(default = 1)

        # Reaction 2H + O -> H2O at rate according to the law of mass action
        reaction = MassAction(reactants=[2 * H, O], products=[H2O], rate=k) # rate instead of rate_law

    sim_2 = Simulator(SynthesisMA)
    result_2 = sim_2.solve(save_at = np.linspace(0,10,100))
    result_2.to_dataframe().plot()
    return MassAction, SynthesisMA


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    To get the equations for this model we can use the `latex_equations` function, which gives us Latex source for the models equations.
    """)
    return


@app.cell
def _(SynthesisMA):
    from poincare.printing.latex import latex_equations

    latex_eqs = latex_equations(SynthesisMA) # Get Latex equations source
    mo.md(latex_eqs)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Pre-made reactions
    Poincare contains a number of pre-made reactions which can be used as building blocks for systems. For the reaction above we can use the `Sythesis` reaction.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Pre made reactions use MassAction kinematics, so the result is the same as using MassAction. Simbio also has compound reactions; we can allow $H_2O$ to dissociate back into $H$ and $O$ by using `ReversibleSynthesis`
    """)
    return


@app.cell
def _(Simulator, System, Variable, initial, np):
    from simbio.reactions.single import Synthesis

    class SynthesisPM(System):
        # Create species H, O, and H2O, each with initial value 1
        H: Variable = initial(default=1)
        O: Variable = initial(default=1)
        H2O: Variable = initial(default=0)

        # Synthesis 2H + O -> H2O at rate 1
        reaction = Synthesis(A = 2*H, B = O, AB = H2O, rate = 1)

    sim_3 = Simulator(SynthesisPM)
    result_3 = sim_3.solve(save_at = np.linspace(0,10,100))
    result_3.to_dataframe().plot()
    return


@app.cell
def _(Parameter, Simulator, System, Variable, assign, initial, np):
    from simbio.reactions.compound import ReversibleSynthesis

    class SynthesisRev(System):
        # Create species H, O, and H2O, each with initial value 1
        H: Variable = initial(default=1)
        O: Variable = initial(default=1)
        H2O: Variable = initial(default=0)

        k_forward: Parameter = assign(default=1)
        k_reverse: Parameter = assign(default=0.5)


        # Synthesis 2H + O <-> H2O, separate forward and reverse rate
        reaction = ReversibleSynthesis(A = 2*H, B = O, AB = H2O, forward_rate = k_forward, reverse_rate = k_reverse)

    sim_4 = Simulator(SynthesisRev)
    result_4 = sim_4.solve(save_at = np.linspace(0,10,100))
    result_4.to_dataframe().plot()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    A reference list containing all pre-made reactions can be found at the end of the tutorial.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Units
    SimBio (and also Poincare) allow for the use of units via [pint](https://drive.google.com/drive/u/0/my-drive). To use them we must first create a `UnitsRegistry`
    """)
    return


@app.cell
def _():
    import pint 

    u = pint.get_application_registry() 
    u.m
    return pint, u


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    All variables, parameters, and times can have units. Let's use this to help keep track of quantites in a simple combustion reaction.
    """)
    return


@app.cell
def _(MassAction, System, Variable, initial, u):
    class Combustion(System):
        CH4: Variable = initial(default = 1 * u.mol/u.L)
        O2: Variable = initial(default = 1 * u.mol/u.L)
        CO2: Variable = initial(default = 0 * u.mmol/u.L)
        H2O: Variable = initial(default = 0 * u.mol/u.L)

        combustion = MassAction(reactants = [CH4, 2 * O2], products = [CO2, 2* H2O], rate = 1 * u.mol/u.L/u.s * (u.mol/u.L)**-3)

    return (Combustion,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Units must be defiened consinstently: all our concentration have dimentionality of $\text{substance}/\text{volume}$, and our rates are set accodingly. The rate units might require some explanation. Since MassAction will add $CH_4 \cdot O_2$ to all reactions, giving units of $(\text{mol}/\text{L})^3$. We multiply my its inverse to comensate, and then add the regular rate in $\text{mol}/\text{L}/\text{s}$.

    If we define the units incorrectly we get an error
    """)
    return


@app.cell
def _(MassAction, System, Variable, initial, pint, u):
    try:
        class WrongUnitsCombustion(System):
            CH4: Variable = initial(default = 1 * u.mol/u.L)
            O2: Variable = initial(default = 1 * u.mol)
            CO2: Variable = initial(default = 0 * u.mmol/u.L)
            H2O: Variable = initial(default = 0 * u.mol/u.L)

            combustion = MassAction(reactants = [CH4, 2 * O2], products = [CO2, 2* H2O], rate = 1 * u.mol/u.L/u.s * (u.mol/u.L)**-3)
    except pint.PintError as err:
        print("PintError:", err)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Here `O2` has units of substance. This isn't inherently wrong, buy when we try to make the reaction the doesn't have the left hand side and right hand side of the equation don't have the same dimesnionality. They don't have to be the exact same units as long as they can be converted to each other though; note how in `Combustion` `CO2` has an initial condition in $\text{mmol} / \text{L}$. Simbio does have a way to handle mixing absolute amounts and concentrations via its [voulme interface](https://marimo.app/github.com/dyscolab/dyscolab-tutorials/blob/main/simbio/using_volume.py).

    The same applies for simulation: working out the units in the reaction we are implicity giving our indpendent variable time dimensionality, so our simlation times must be in units of time.
    """)
    return


@app.cell
def _(Combustion, Simulator, np, u):
    sim_5 = Simulator(Combustion)
    result_5 = sim_5.solve(save_at = np.linspace(0,10,100) * u.s)
    result_5
    return result_5, sim_5


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The result is a an `Dataset` with units via [pint-xarray](https://pint-xarray.readthedocs.io/en/stable/). To plot it we can dequantify it first.
    """)
    return


@app.cell
def _(result_5):
    no_units_result_5 = result_5.pint.dequantify()
    no_units_result_5.to_dataframe().plot()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    All amounts are in the unit we set them in, so units `CO2`'s units are in $\text{mmol}/\text{L}$. This can make it kind of hard to make out the rest, so we can convetrt it to $\text{mol}/\text{L}$ first.
    """)
    return


@app.cell
def _(np, sim_5, u):
    result_6 = sim_5.solve(save_at = np.linspace(0,10,100) * u.s)
    result_6["CO2"] = result_6["CO2"].pint.to(u.mol/u.L)
    result_6.pint.dequantify().to_dataframe().plot()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Excercises

    **1)** Rates can depend on other variables and parameters. Make a simple system with variables $A, B, C$ with reactions:

    $$ \begin{align} 2A &\rightarrow B \\
    C &\rightarrow \empty
    \end{align} $$

    where the $2A \rightarrow B$ rate depends on a temperature parameter $T$ and the amount of catalizer $C$.

    **2)** Combustion needs a fuel source. Create a `System` `SustainedCombustion` which includes a `Combustion` subsystem and a constant source of `CH4` and `O2` using the `Creation` inbuilt reaction.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Pre-made ractions reference

    Single reactions from `simbio.reactions.single`:
    - `Creation(A: Species, rate: Parameter)`: A substance `A` is created from nothing at a given rate, ∅ -> A.
    - `AutoCreation(A: Species, rate: Parameter)`: A substance `A` is created at a rate proportional to its abundance, A -> 2A.
    - `Destruction(A: Species, rate: Parameter)`: A substance `A` degrades into nothing, A -> ∅.
    - `Conversion(A: Species, B: Species, rate: Parameter)`: A substance `A` converts into `B`, A -> B.
    - `Synthesis(A: Species, B: Species, AB: Species, rate: Parameter)`:  Two simple substances `A` and `B` combine to form a more complex substance `AB`, A + B -> AB.
    - `Dissociation(AB: Species, A: Species, B: Species, rate: Parameter)`: A more complex substance `AB` breaks down into its more simple parts `A` and `B`, AB -> A + B.

    Compound reactions from `simbio.reactions.compound`:
    - `ReversibleSynthesis(A: Species, B: Species, AB: Species, forward_rate: Parameter, reverse_rate: Parameter)`: A `Synthesis` and `Dissociation` reactions each with a separate `rate`, A + B <-> AB.
    - `Equilibration(A: Species, B: Species, forward_rate: Parameter, reverse_rate: Parameter)`: A forward and backward `Conversion`, each with a separate `rate`, A <-> B.
    - `CatalyzeConvert(A: Species, B: Species, AB: Species, P: Species, forward_rate: Parameter, reverse_rate: Parameter, conversion_rate: Parameter)`: A `ReversibleSynthesis` between `A`, `B`, and `AB`, and a `Conversion` from `AB` to `P` with `rate = conversion_rate`, A + B <-> A:B -> P.
    """)
    return


if __name__ == "__main__":
    app.run()
