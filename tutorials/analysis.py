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
    # Larger systems and analysis tools
    Poincare and SimBio contain a series of analysis, including parameter sweeps searching for steady states and oscillations. Before anything we need a more instersting example, so we will implement the the [repressilator](https://en.wikipedia.org/wiki/Repressilator).
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## A more interesting example: the repressilator
    The repressilator is a genetic regulatory network where 3 mRNA species $m_1$, $m_2$, $m_3$ interact with 3 proteins $p_1$, $p_2$, $p_3$. We can model it using the equations:

    \begin{aligned}
    \frac{dm_1}{dt} &=  -m_1 + \frac{\alpha}{1+p_3^n} + \alpha_0 \quad \frac{dp_1}{dt} &= - \beta (p_1-m_1)  \\
    \frac{dm_2}{dt} &=  -m_2 + \frac{\alpha}{1+p_1^n} + \alpha_0 \quad \frac{dp_2}{dt} &= - \beta (p_2-m_2) \\
    \frac{dm_3}{dt} &=  -m_3 + \frac{\alpha}{1+p_2^n} + \alpha_0 \quad \frac{dp_2}{dt} &= - \beta (p_3-m_3)
    \end{aligned}
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Simbio is desinged with composability in mind, so we can break this down into parts and combine them later:
    - Each $m_i$ is destroyed at a rate equal it itself.
    - Each $m_i$ is sinthesysed at a rate $\frac{\alpha}{1+p_{i+1}^n} + \alpha_0$.
    - Each $p_i$ is created at a rate equal $-\beta (p_i-m_i)$.

    We can first implement the equation for each $m_i$
    """)
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    from simbio import (
        System,
        Parameter,
        RateLaw,
        Simulator,
        Variable,
        assign,
        initial,
    )
    from simbio.reactions.single import Destruction

    class mRNA(System):
        # Create the species
        m: Variable = initial(default=1)
        p: Variable = initial(default=1)

        # Create parameters
        alpha: Parameter = assign(default=1)
        alpha_0: Parameter = assign(default=1)
        n: Parameter = assign(default=1)
        creation_rate: Parameter = assign(default=alpha / (1 + p**n) + alpha_0)

        # Declare creation and destruction reactions for m
        destroy = Destruction(A=m, rate=1)

        create = RateLaw(reactants=[], products=[m], rate_law=creation_rate)

    sim = Simulator(mRNA)
    result = sim.solve(save_at=np.linspace(0, 10, 1000))
    result.to_dataframe().plot() 
    return (
        Parameter,
        RateLaw,
        Simulator,
        System,
        Variable,
        assign,
        initial,
        mRNA,
        np,
    )


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Since the `Destruction` class creates a `MassAction` the reaction will already be proportional to the concentration of $m_i$, so we can set rate = 1.

    We do the same for the proteins:
    """)
    return


@app.cell
def _(Parameter, RateLaw, Simulator, System, Variable, assign, initial, np):
    class Protein(System):
        m: Variable = initial(default=1)  # Create species
        p: Variable = initial(default=0)
        beta: Parameter = assign(default=1)

        create = RateLaw(
            reactants=[p, m], products=[2 * p, m], rate_law=-beta * (p - m)
        )

    sim_1 = Simulator(Protein)  # Create parameter beta
    result_1 = sim_1.solve(save_at=np.linspace(0, 10, 1000))
    result_1.to_dataframe().plot()  # create_rate: Parameter =  #
    return (Protein,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Now we can combine everything into the single Represillator:
    """)
    return


@app.cell
def _(Parameter, Protein, System, Variable, assign, initial, mRNA):
    class Repressilator(System):
        # Create all the species
        m1: Variable = initial(default=1)
        m2: Variable = initial(default=1)
        m3: Variable = initial(default=1)
        p1: Variable = initial(default=1)
        p2: Variable = initial(default=1)
        p3: Variable = initial(default=1)

        # Create all the parameters
        alpha: Parameter = assign(default=150)
        alpha_0: Parameter = assign(default=0.5)
        n: Parameter = assign(default=2)
        beta: Parameter = assign(default=8)

        # Apply the creation and destruction laws to each species, in
        react_1 = mRNA(m=m1, p=p3, alpha=alpha, alpha_0=alpha_0, n=n)
        react_2 = mRNA(m=m2, p=p1, alpha=alpha, alpha_0=alpha_0, n=n)
        react_3 = mRNA(m=m3, p=p2, alpha=alpha, alpha_0=alpha_0, n=n)
        react_4 = Protein(p=p1, m=m1, beta=beta)
        react_5 = Protein(p=p2, m=m2, beta=beta)
        react_6 = Protein(p=p3, m=m3, beta=beta)

    return (Repressilator,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    We can simulate them by creating an instance of `Simulator`:
    """)
    return


@app.cell
def _(Repressilator, Simulator, np):
    sim_2 = Simulator(Repressilator)
    sim_2.solve(save_at=np.linspace(0, 10, 100)).to_dataframe().plot()
    return (sim_2,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Kind of dissapointgly we don't get oscillations since all initial conditions are equal. To see them we must change the intial conditions.
    """)
    return


@app.cell
def _(Repressilator, np, sim_2):
    sim_2.with_values({
            Repressilator.m1: 1,
            Repressilator.m2: 2,
            Repressilator.m3: 3,
            Repressilator.p1: 4,
            Repressilator.p2: 5,
            Repressilator.p3: 6,
            Repressilator.alpha: 200,
            Repressilator.beta: 5,
        }).solve(
        save_at=np.linspace(0, 100, 1000)).to_dataframe().plot()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Steady state detection
    We can use `poincare.SteadyState` to do a paramter sweep to find the steady state in the non-oscillating case: SimBio will automatically simulate the system until it finds a SteadyState and store the laste result.
    As an example, we could sweep for different $\alpha$ values between 1 and 10
    """)
    return


@app.cell
def _(Repressilator, np, sim_2):
    from poincare import SteadyState

    steady_sim = sim_2.with_values({
            Repressilator.m1: 1,
            Repressilator.m2: 2,
            Repressilator.m3: 3,
            Repressilator.p1: 4,
            Repressilator.p2: 5,
            Repressilator.p3: 6}) # Simulator with initaial conditons for sweep
    steady = SteadyState() # Create steady state finder
    sweep_values = np.linspace(10,20, 50) 
    steady_sweep = steady.sweep(steady_sim, variable=Repressilator.alpha, values= sweep_values)
    steady_sweep
    return (steady_sweep,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Output includes the steady state for all variables as well as the time at which it stopped simulating. We can drop them to plot only the variables.
    """)
    return


@app.cell
def _(steady_sweep):
    steady_sweep.drop_vars(["time", "event"]).to_dataframe().plot()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Oscillations detection
    For ranges where it oscillates we can use `Oscillations` to do a parameter sweep to detect the periofd of oscilllations.  Aside from the parameter and values to sweep we must tell it what variable to look in oscilation for, an estimated upper bound on the systems releaxation time and the maximum and minimum period excpected.
    """)
    return


@app.cell
def _(Repressilator, np, sim_2):
    from poincare import Oscillations

    osc_sim = sim_2.with_values({
            Repressilator.m1: 1,
            Repressilator.m2: 2,
            Repressilator.m3: 3,
            Repressilator.p1: 4,
            Repressilator.p2: 5,
            Repressilator.p3: 6,
            Repressilator.alpha: 200,
            Repressilator.beta: 5,
        }) # Simulator with inital conditions for parameter sweep
    osc = Oscillations()
    osc_sweep_values = np.linspace(5, 20, 15)
    result_2 = osc.sweep(
        osc_sim,
        rel_time=60,  # Estimated upper bound on relaxation time
        T_min=1,  # Minimum period expected
        T_max=20,  # Maximum period expected
        variables=Repressilator.m1,  # Variable to look at, can be an iterable with multiple variables
        parameter=Repressilator.beta,
        values=osc_sweep_values,
    )

    result_2.sel(quantity="period").to_dataframe().plot(
        style="--."
    )  # Parameter to sweep  # Values taken on by parameter
    return (result_2,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    We get a warning for a parameter value for which it couldn't be verified. The result also see includes the amplitude of the oscillation and the mean quadratic difference between periods to get another check on if the the system is actually oscillating.
    """)
    return


@app.cell
def _(result_2):
    result_2.sel(quantity=["amplitude"]).to_dataarray().plot(marker=".")
    result_2.sel(quantity=["difference_rms"]).to_dataarray().plot(marker=".")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Poincare also includes a number of other analysis tools, sucha as searching for bistablity or fits. For mode information see the [full explainer on analysis](https://marimo.app/github.com/dyscolab/dyscolab-tutorials/blob/main/poincare/asymptotic_behaviour.py).
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(rf"""
    # Excercises

    **1)** The `Repressilator` class defines all variables externally and passes them to the subsystems. Since a instanced subclass createa their own variables and parameters if not passed externally this isn't necessary, although must be carefull to not create our variables twice. Make a more character efficient implementation of the repressilator by creating the proteins without external variables and then passing the internal variables created there to the mRNAs.

    **2)** Run another parameter sweep for oscillatios but this time in $\alpha$ between 50 and 200. If we don't know in what range the periods and relaxaton times will be it is generally a reasonable first guess to assume it is monotonous in our parameter, so get an estimate by simulating at the maximum and minimum $\alpha$ and eyeballing a period and relaxation time.
    """)
    return


if __name__ == "__main__":
    app.run()
