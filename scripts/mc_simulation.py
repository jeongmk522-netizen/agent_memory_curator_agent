#!/usr/bin/env python3
"""
Monte Carlo simulation of memory hallucination compounding under
uncurated vs curated regimes for the Memory Curator Agent paper.

Reproduces and strengthens the numerical claims in Theorem 1.
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = REPO_ROOT / "assets"
RESULTS_DIR = REPO_ROOT / "results"
ASSETS_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# ---------- Simulation core ----------

def simulate_run(T, lam, h_e, alpha, eta, r0, seed):
    """
    Simulate one trajectory of T days.

    Args:
        T: number of days
        lam: events per day (Poisson rate)
        h_e: per-event intrinsic hallucination probability
        alpha: curator admission rate (alpha=1.0, eta=0.0 = uncurated)
        eta: curator filter accuracy (prob of catching hallucinated event)
        r0: retrieval coverage parameter (r(t) = r0 * log(N_t))
        seed: RNG seed

    Returns:
        days: array of day indices
        P_t: array of per-retrieval hallucination probabilities
        N_t: array of memory sizes
        N_hall_t: array of hallucinated memory counts
    """
    rng = np.random.default_rng(seed)

    days = np.arange(1, T + 1)
    P_t = np.zeros(T)
    N_t = np.zeros(T)
    N_hall_t = np.zeros(T)

    n_total = 0
    n_hall = 0

    for t_idx, day in enumerate(days):
        # Number of events emitted today (Poisson)
        n_events = rng.poisson(lam)

        # Of these, hallucinated independently with prob h_e
        n_hall_emitted = rng.binomial(n_events, h_e)
        n_clean_emitted = n_events - n_hall_emitted

        # Curator processes:
        # - Admits each event with prob alpha (irrespective of hallucination,
        #   to first order)
        # - For admitted events that are hallucinated, additionally drops
        #   with prob eta
        if alpha < 1.0 or eta > 0.0:
            n_clean_admitted = rng.binomial(n_clean_emitted, alpha)
            # Hallucinated: admitted with prob alpha, but then dropped with prob eta
            # Equivalent to: admitted with prob alpha * (1 - eta)
            n_hall_admitted = rng.binomial(n_hall_emitted, alpha * (1 - eta))
        else:
            # Uncurated baseline
            n_clean_admitted = n_clean_emitted
            n_hall_admitted = n_hall_emitted

        n_total += n_clean_admitted + n_hall_admitted
        n_hall += n_hall_admitted

        # Retrieval probability: surface r(t) = r0 * log(max(N_t, 2)) entries
        # Probability that at least one is hallucinated
        if n_total > 0:
            r = max(1, int(r0 * np.log(max(n_total, 2))))
            hall_fraction = n_hall / n_total
            # P(at least one hallucinated in r draws with replacement)
            P_t[t_idx] = 1 - (1 - hall_fraction) ** r
        else:
            P_t[t_idx] = 0.0

        N_t[t_idx] = n_total
        N_hall_t[t_idx] = n_hall

    return days, P_t, N_t, N_hall_t


def aggregate_runs(n_seeds, T, lam, h_e, alpha, eta, r0):
    """Average over multiple seeds."""
    all_P = []
    all_N = []
    all_Nhall = []
    for seed in range(n_seeds):
        days, P_t, N_t, N_hall_t = simulate_run(T, lam, h_e, alpha, eta, r0, seed)
        all_P.append(P_t)
        all_N.append(N_t)
        all_Nhall.append(N_hall_t)
    return (days,
            np.mean(all_P, axis=0),
            np.std(all_P, axis=0),
            np.mean(all_N, axis=0),
            np.mean(all_Nhall, axis=0))


# ---------- Main experiment ----------

T = 365
lam = 10
h_e = 0.1
r0 = 5
n_seeds = 200

configs = [
    {"name": "Uncurated (B1)", "alpha": 1.0, "eta": 0.0,
     "color": "#d62728", "ls": "-", "lw": 2.5},
    {"name": "Curator (α=0.5, η=0.7)", "alpha": 0.5, "eta": 0.7,
     "color": "#ff7f0e", "ls": "--", "lw": 2.0},
    {"name": "Curator (α=0.3, η=0.9)", "alpha": 0.3, "eta": 0.9,
     "color": "#2ca02c", "ls": "-", "lw": 2.5},
    {"name": "Curator (α=0.5, η=0.95)", "alpha": 0.5, "eta": 0.95,
     "color": "#1f77b4", "ls": "-.", "lw": 2.0},
]

results = {}
print("Running Monte Carlo simulations...")
print(f"  T={T} days, lambda={lam}, h_e={h_e}, r0={r0}, n_seeds={n_seeds}")
print()

for cfg in configs:
    print(f"  Simulating: {cfg['name']}")
    days, P_mean, P_std, N_mean, Nhall_mean = aggregate_runs(
        n_seeds, T, lam, h_e, cfg["alpha"], cfg["eta"], r0
    )
    results[cfg["name"]] = {
        "days": days,
        "P_mean": P_mean,
        "P_std": P_std,
        "N_mean": N_mean,
        "Nhall_mean": Nhall_mean,
        "alpha": cfg["alpha"],
        "eta": cfg["eta"],
        "color": cfg["color"],
        "ls": cfg["ls"],
        "lw": cfg["lw"],
    }

# ---------- Print numerical results table ----------

print()
print("=" * 80)
print("RESULTS at key time horizons")
print("=" * 80)
print(f"{'Config':<32} {'t=30':>10} {'t=90':>10} {'t=180':>10} {'t=365':>10}")
print("-" * 80)
for name, r in results.items():
    print(f"{name:<32} "
          f"{r['P_mean'][29]:>10.4f} "
          f"{r['P_mean'][89]:>10.4f} "
          f"{r['P_mean'][179]:>10.4f} "
          f"{r['P_mean'][364]:>10.4f}")
print()

# Compute reductions
print("Reduction factors at t=365 (P_uncurated / P_curated):")
P_unc = results["Uncurated (B1)"]["P_mean"][364]
for name, r in results.items():
    if name == "Uncurated (B1)":
        continue
    reduction = P_unc / r["P_mean"][364] if r["P_mean"][364] > 0 else float('inf')
    print(f"  {name}: {reduction:.2f}x reduction")
print()

# Memory size comparison
print("Memory size at t=365:")
for name, r in results.items():
    print(f"  {name}: N={r['N_mean'][364]:.0f}, N_hall={r['Nhall_mean'][364]:.0f}, "
          f"fraction={r['Nhall_mean'][364]/r['N_mean'][364]:.4f}")
print()

# ---------- Save numerical results as JSON ----------

results_json = {
    name: {
        "alpha": float(r["alpha"]),
        "eta": float(r["eta"]),
        "P_at_t30": float(r["P_mean"][29]),
        "P_at_t90": float(r["P_mean"][89]),
        "P_at_t180": float(r["P_mean"][179]),
        "P_at_t365": float(r["P_mean"][364]),
        "P_std_at_t365": float(r["P_std"][364]),
        "N_at_t365": float(r["N_mean"][364]),
        "Nhall_at_t365": float(r["Nhall_mean"][364]),
    }
    for name, r in results.items()
}
with open(RESULTS_DIR / "mc_results.json", "w") as f:
    json.dump(results_json, f, indent=2)

# ---------- Generate Figure 2: Hallucination Growth Curves ----------

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Subplot (a): Per-retrieval hallucination probability over time
ax1 = axes[0]
for name, r in results.items():
    ax1.plot(r["days"], r["P_mean"],
             label=name, color=r["color"],
             linestyle=r["ls"], linewidth=r["lw"])
    ax1.fill_between(r["days"],
                     r["P_mean"] - r["P_std"],
                     r["P_mean"] + r["P_std"],
                     color=r["color"], alpha=0.12)

ax1.set_xlabel("Deployment time t (days)", fontsize=11)
ax1.set_ylabel("Per-retrieval hallucination probability $P_t$", fontsize=11)
ax1.set_title("(a) Hallucination probability growth over time",
              fontsize=12, loc="left")
ax1.legend(loc="lower right", fontsize=9, framealpha=0.92)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, T)
ax1.set_ylim(0, 1.0)
ax1.axhline(0.5, color="gray", linestyle=":", alpha=0.5, linewidth=0.8)
ax1.text(T*0.02, 0.52, "50% threshold", fontsize=8, color="gray")

# Subplot (b): Memory composition (hallucinated fraction) over time
ax2 = axes[1]
for name, r in results.items():
    fraction = r["Nhall_mean"] / np.maximum(r["N_mean"], 1)
    ax2.plot(r["days"], fraction,
             label=name, color=r["color"],
             linestyle=r["ls"], linewidth=r["lw"])

ax2.set_xlabel("Deployment time t (days)", fontsize=11)
ax2.set_ylabel("Hallucinated fraction of durable memory", fontsize=11)
ax2.set_title("(b) Hallucinated content density in store",
              fontsize=12, loc="left")
ax2.legend(loc="upper right", fontsize=9, framealpha=0.92)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, T)
ax2.set_ylim(0, 0.12)
ax2.axhline(h_e, color="gray", linestyle=":", alpha=0.5, linewidth=0.8)
ax2.text(T*0.02, h_e + 0.002, f"intrinsic emission rate $h_e$ = {h_e}",
         fontsize=8, color="gray")

plt.suptitle(
    f"Figure 2: Monte Carlo simulation of memory hallucination "
    f"compounding\n"
    f"($\\lambda$={lam} events/day, $h_e$={h_e}, $r_0$={r0}, "
    f"averaged over {n_seeds} seeds with $\\pm 1\\sigma$ band)",
    fontsize=12, y=1.02
)
plt.tight_layout()
plt.savefig(ASSETS_DIR / "figure2_hallucination_growth.svg",
            format="svg", bbox_inches="tight")
plt.savefig(ASSETS_DIR / "figure2_hallucination_growth.png",
            format="png", dpi=180, bbox_inches="tight")
plt.close()

print("Saved Figure 2: figure2_hallucination_growth.svg / .png")
print()

# ---------- Generate Figure 3: Parameter Sensitivity ----------

print("Running parameter sweep for Figure 3...")

# Sweep over eta (filter accuracy)
etas = np.linspace(0.0, 1.0, 11)
alphas_sweep = [0.1, 0.3, 0.5, 0.7, 1.0]
T_sweep = 365
n_seeds_sweep = 80

sweep_results = {}
for alpha in alphas_sweep:
    P_finals = []
    for eta in etas:
        _, P_mean, _, _, _ = aggregate_runs(
            n_seeds_sweep, T_sweep, lam, h_e, alpha, eta, r0
        )
        P_finals.append(P_mean[-1])
    sweep_results[alpha] = P_finals
    print(f"  alpha={alpha}: done")

fig, ax = plt.subplots(figsize=(9, 5.5))

cmap = plt.cm.viridis
for i, alpha in enumerate(alphas_sweep):
    color = cmap(i / (len(alphas_sweep) - 1))
    P_finals = sweep_results[alpha]
    ax.plot(etas, P_finals, "o-", color=color,
            label=f"$\\alpha$ = {alpha}", linewidth=2, markersize=7)

ax.set_xlabel("Curator filter accuracy $\\eta$", fontsize=11)
ax.set_ylabel("Per-retrieval hallucination probability $P_{365}$", fontsize=11)
ax.set_title(
    "Figure 3: Sensitivity of long-horizon hallucination rate to "
    "curator parameters\n"
    f"(t=365 days, $\\lambda$={lam}, $h_e$={h_e}, $r_0$={r0}, "
    f"{n_seeds_sweep} seeds per point)",
    fontsize=12)
ax.legend(title="Admission rate", loc="upper right", fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(0, 1.0)
ax.axhline(0.5, color="gray", linestyle=":", alpha=0.5, linewidth=0.8)

# Annotation for the practical regime
ax.annotate(
    "Practical regime\n($\\alpha$=0.3, $\\eta$=0.9):\n3.2× reduction",
    xy=(0.9, sweep_results[0.3][9]),
    xytext=(0.50, 0.65),
    fontsize=9, color="#2ca02c",
    arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.2),
    bbox=dict(boxstyle="round,pad=0.4", fc="#f0f9f0", ec="#2ca02c")
)

plt.tight_layout()
plt.savefig(ASSETS_DIR / "figure3_parameter_sensitivity.svg",
            format="svg", bbox_inches="tight")
plt.savefig(ASSETS_DIR / "figure3_parameter_sensitivity.png",
            format="png", dpi=180, bbox_inches="tight")
plt.close()

print()
print("Saved Figure 3: figure3_parameter_sensitivity.svg / .png")
print()
print("All Monte Carlo work complete.")
