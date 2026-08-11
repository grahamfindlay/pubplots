---
title: Using pp.scale and letting rcParams drive font sizes
updated: 2026-07-26
---

# Inside `pp.destination(...)`: scale sizes, never hardcode font sizes

Two rules for any plotting code running under
`with pubplots.destination("figma"):` (imported as `pp`).

## 1. Wrap every literal numeric size in `pp.scale(...)`

So it tracks the destination's scaling factor (figma scale = 300/96 ≈ 3.125). Applies
to `figsize`, `linewidth`/`lw`, `markersize`/`ms`, `capsize`, and similar.
`pp.scale(w, h)` returns a scaled tuple → `figsize=pp.scale(8.0, 5.0)`.

**The number you pass IS the desired final (in-Figma) dimension.** `pp.scale`
multiplies *up* by 300/96 to compensate for Figma importing SVGs at 96 DPI, so
`pp.scale(w, 5)` renders 5 in tall in Figma even though the raw matplotlib figsize is
~15 in. Author at true target size — `pp.scale(1.5, 2)` is a 2-in panel. Do **not**
pre-divide to "leave room" for scaling; that inverts it.

## 2. Never hardcode font sizes

The pubplots rcParams already set `font.size`, `axes.titlesize`, `axes.labelsize`,
`xtick.labelsize`, `ytick.labelsize`, and `figure.titlesize`. Passing `fontsize=` /
`labelsize=` (including `ax.tick_params(labelsize=...)`) overrides and fights them.
Call `ax.set_title(text)` / `ax.set_ylabel(text)` / `fig.suptitle(text)` with no size
kwargs and let rcParams drive.

## Why

pubplots exists to produce consistently-sized publication figures; hardcoded sizes and
unscaled dimensions break that consistency.

## How to apply

When authoring or editing plotting code under `pp.destination(...)`, scan for raw
`figsize=(...)`, `lw=<num>`, `fontsize=`, `labelsize=` — convert sizes to
`pp.scale(...)` and delete the fontsize kwargs.

Correct existing example:
`offproj/src/offproj/bugnon/mua/pipeline/full48h.py` (`figsize=pp.scale(...)`,
`lw=pp.scale(...)`).
