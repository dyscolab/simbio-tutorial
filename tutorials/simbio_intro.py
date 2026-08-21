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

    SimBio's main differnece is that a system's dynamics are declared as reaction instead as equations. The simplest one is the `RateLaw`, which we can use to simulate a simple $2A + B \rightarrow C$ synthesis.
    """)
    return


@app.cell
def _():
    import numpy as np
    from simbio import System, RateLaw, Variable, initial

    class SynthesisRL(System):
        # Create species A, B, and C, each with intial value 1
        A: Variable = initial(default=1)
        B: Variable = initial(default=1)
        C: Variable = initial(default=0)

        # Reaction 2A + B -> C at rate 1
        reaction = RateLaw(reactants=[2 * A, B], products=[C], rate_law=1)

    return SynthesisRL, System, Variable, initial, np


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    This represents the equations
    $$
    \begin{aligned}
    \frac{dA}{dt} &= -2, \\
    \frac{dB}{dt} &= -1, \\
    \frac{dC}{dt} &= 1.
    \end{aligned}
    $$
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
def _(Simulator, System, Variable, initial, np):
    from simbio import MassAction

    class SynthesisMA(System):
        A: Variable = initial(default=1)
        B: Variable = initial(default=1)
        C: Variable = initial(default=0)

        # Reaction 2A + B -> C at rate according to the law of mass action
        reaction = MassAction(reactants=[2 * A, B], products=[C], rate=1) # rate instead of rate_law

    sim_2 = Simulator(SynthesisMA)
    result_2 = sim_2.solve(save_at = np.linspace(0,10,100))
    result_2.to_dataframe().plot()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In this case the equations are
    $$
    \begin{aligned}
    \frac{dA}{dt} &= -2A^2, \\
    \frac{dB}{dt} &= -B, \\
    \frac{dC}{dt} &= A^2B.
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Pre-made reacitons
    Poincare contains a number of pre-made reactions which can be used as building blocks for systems. For the reaction above we can use the `Sythesis` reaction.
    """)
    return


@app.cell
def _(Simulator, System, Variable, initial, np):
    from simbio.reactions.single import Synthesis

    class SynthesisPM(System):
        # Create species A, B, and C, each with intial value 1
        A: Variable = initial(default=1)
        B: Variable = initial(default=1)
        C: Variable = initial(default=0)

        # Synthesis 2A + B -> C at rate 1
        reaction = Synthesis(A = 2*A, B = B, AB = C, rate = 1)

    sim_3 = Simulator(SynthesisPM)
    result_3 = sim_3.solve(save_at = np.linspace(0,10,100))
    result_3.to_dataframe().plot()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Pre made reactions use MassAction kinematics, so the result is the same as using MassAction. Simbio also has compound reactions; we can allow `C` to convert back into `A` and `B` by using `ReversibleSynthesis`
    """)
    return


@app.cell
def _(Simulator, System, Variable, initial, np):
    from simbio import Parameter, assign
    from simbio.reactions.compound import ReversibleSynthesis

    class SynthesisRev(System):
        # Create species A, B, and C, each with intial value 1
        A: Variable = initial(default=1)
        B: Variable = initial(default=1)
        C: Variable = initial(default=0)

        k_forward: Parameter = assign(default=1)
        k_reverse: Parameter = assign(default=0.5)

    
        # Synthesis 2A + B <-> C, separate forward and reverse rate
        reaction = ReversibleSynthesis(A = 2*A, B = B, AB = C, forward_rate = k_forward, reverse_rate = k_reverse)

    sim_4 = Simulator(SynthesisRev)
    result_4 = sim_4.solve(save_at = np.linspace(0,10,100))
    result_4.to_dataframe().plot()
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

    Compound reactions from`simbio.reactions.compound`:
    - `ReversibleSynthesis(A: Species, B: Species, AB: Species, forward_rate: Parameter, reverse_rate: Parameter)`: A `Synthesis` and `Dissociation` reactions each with a separate `rate`, A + B <-> AB.
    - `Equilibration(A: Species, B: Species, forward_rate: Parameter, reverse_rate: Parameter)`: A forward and backward `Conversion`, each with a separate `rate`, A <-> B.
    - `CatalyzeConvert(A: Species, B: Species, AB: Species, P: Species, forward_rate: Parameter, reverse_rate: Parameter, conversion_rate: Parameter)`: A `ReversibleSynthesis` between `A`, `B`, and `AB`, and a `Conversion` from `AB` to `P` with `rate = conversion_rate`, A + B <-> A:B -> P.
    """)
    return


if __name__ == "__main__":
    app.run()
