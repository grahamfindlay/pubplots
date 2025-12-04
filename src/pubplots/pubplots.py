"""Utilities for creating publication-ready matplotlib figures.

This module provides tools for scaling figures and setting rcParams so that
figures have journal-friendly fonts, font sizes, and DPI, and are imported
correctly by different vector graphics editors (Figma, Adobe, Affinity, etc.).
"""

from contextlib import contextmanager
from contextvars import ContextVar

import matplotlib as mpl

# Module-level context variable for scaling factor
_scaling_ctx: ContextVar[float] = ContextVar("scaling", default=1.0)


def scale(
    *values: int | float | tuple[int | float, ...], scaling_factor: float | None = None
) -> int | float | tuple[int | float, ...]:
    """Scale input value(s) according to the current context, or by `scaling_factor`.

    Preserves the input type: scalar returns scalar, tuple returns tuple.
    Also accepts multiple positional arguments.

    Parameters
    ----------
    *values : int, float, or tuple of int/float
        A single number, tuple of numbers, or multiple numbers to scale.
    scaling_factor : float, optional
        The scaling factor to apply. If None, reads from the current context.
        Defaults to 1.0 if no context is set.

    Returns
    -------
    int, float, or tuple of int/float
        Scaled value(s) in the same type as input.
    """
    if scaling_factor is None:
        scaling_factor = _scaling_ctx.get()

    if len(values) == 1:
        values = values[0]
        if isinstance(values, tuple):
            return tuple(v * scaling_factor for v in values)
        else:
            return values * scaling_factor
    else:
        return tuple(v * scaling_factor for v in values)


def get_rc_params(destination: str) -> tuple[dict, callable]:
    """Get matplotlib rcParams and a scaling factor for publication-ready figures.

    Returns rcParams so that figures have journal-friendly fonts, font sizes, and
    DPI, and are imported correctly by different vector graphics editors.

    Parameters
    ----------
    destination : str
        The vector graphics application into which the figure will be imported.
        "figma" requires special scaling. Anything else ("adobe", "affinity",
        "inkscape") does not.

    Returns
    -------
    rc_params : dict
        A dictionary of rcParams to set for matplotlib.
    scaler : callable
        A function that scales input values according to the selected destination,
        regardless of context.

    Notes
    -----
    **Figma-specific scaling factor explanation**

    *Text scaling:*

    - 1 pt = 1/72 inch virtually everywhere except for Figma,
      where 1pt = 1 CSS pixel = 1/96 inch.
    - Figma attempts to correct for this by scaling up text by 96/72, so an
      SVG with 5pt font will import with 6.66pt font in Figma.
    - The only way to specify a frame size in Figma is in pixels (pts), so if
      you want an 8.5x11" figure at 300ppi, you make a frame that is
      8.5*300 x 11*300 pixels (which is 2550 x 3300 pixels).
    - Thus, assuming a 300ppi frame, font which should print at 5pt needs to
      appear in Figma as 5 * (300 / 72) = 20.833pt, but you must account for
      Figma's (96/72) scaling, so the font must be specified in the SVG as
      5 * (72/96) * (300/72) = 300/96 = 15.625pt.

    *Figure size:*

    - When you write an SVG using matplotlib, the figure size is specified in pts
      (savefig.dpi has no bearing on the SVG created. It is ignored.), using the
      convention that 1pt = 1/72 inch. So if you request a 2"x2" figure, it will
      be saved as 144pt x 144pt.
    - As with text, Figma will scale up these pts by 96/72, so your SVG will get
      imported as 192x192 pixels. If you are using a 300dpi frame, this means
      your figure will actually be 192/300 = 0.64" wide instead of 2" wide.
    - Therefore, to get a figure that is actually 2" wide at 300dpi, you need to
      ask matplotlib to create a figure that is 2 * (300/96) = 6.25" wide, which
      will be saved as 450pt wide, and then imported into Figma as 600 pixels
      wide, which is 600/300 = 2" wide.
    """
    if destination == "figma":
        scaling = 300 / 96
    else:
        scaling = 1.0

    rc_params = {
        "font.family": "sans-serif",  # Essential
        "font.sans-serif": ["Arial"],  # Essential
        "font.size": 6 * scaling,
        "axes.titlesize": 6 * scaling,
        "axes.labelsize": 6 * scaling,
        "xtick.labelsize": 5 * scaling,
        "ytick.labelsize": 5 * scaling,
        "legend.fontsize": 6 * scaling,
        "figure.titlesize": 7 * scaling,
        "figure.labelsize": 7 * scaling,
        "figure.dpi": 150 / scaling,  # Controls display size in notebooks
        "figure.autolayout": True,  # Pre-emptively apply tight_layout
        "savefig.dpi": 300,
        "savefig.format": "svg",
        "svg.fonttype": "none",  # Essential
        "pdf.fonttype": 42,
    }

    def _scale(
        *values: int | float | tuple[int | float, ...],
    ) -> int | float | tuple[int | float, ...]:
        return scale(*values, scaling_factor=scaling)

    return rc_params, _scale


@contextmanager
def destination(destination: str = "default"):
    """Context manager for publication-ready matplotlib figures.

    Sets matplotlib rcParams so that figures have journal-friendly fonts, font
    sizes, DPI, etc., and are imported correctly by different vector graphics
    editors ("destinations"). Also sets an appropriate figure (or text) size
    scaling factor. Within this context, `scale()` will automatically use the
    appropriate scaling factor without needing to pass it explicitly.

    Parameters
    ----------
    destination : str, optional
        The vector graphics application into which the figure will be imported.
        "figma" applies special scaling (300/96). Anything else ("adobe",
        "affinity", "inkscape") does not. Default is "default".

    Yields
    ------
    None

    See Also
    --------
    get_rc_params : Get the rcParams dictionary and scaler function directly.
    scale : Scale values according to the current context.

    Examples
    --------
    >>> with destination("figma"):
    ...     fig, ax = plt.subplots(figsize=scale(2, 2))
    ...     # scale() automatically uses figma scaling (300/96)
    """
    params, scaler = get_rc_params(destination)

    token = _scaling_ctx.set(scaler(1.0))
    try:
        with mpl.rc_context(params):
            yield
    finally:
        _scaling_ctx.reset(token)
