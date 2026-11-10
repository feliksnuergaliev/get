# Построение графиков RC-цепи и оценка постоянной времени tau.
# Запуск: python3 plot_rc.py [rc_data.csv]

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

FILE_NAME = sys.argv[1] if len(sys.argv) > 1 else "rc_data.csv"

# Необязательно: если известны номиналы, для сравнения выводится RC
R_OHM = None      # например, 10e3
C_F = None        # например, 100e-6

# ---------- Загрузка данных ----------
data = np.loadtxt(FILE_NAME, delimiter=",", skiprows=1)
t, u = data[:, 0], data[:, 1]

# Делим запись на зарядку (до максимума) и разрядку (после максимума)
i_peak = int(np.argmax(u))
t_c, u_c = t[: i_peak + 1], u[: i_peak + 1]
t_d, u_d = t[i_peak:], u[i_peak:]
t_c = t_c - t_c[0]          # время от начала зарядки
t_d = t_d - t_d[0]          # время от пика (начала разрядки)


# ---------- Модели ----------
def charge_model(t, A, tau, c):
    return c + A * (1.0 - np.exp(-t / tau))


def discharge_model(t, A, tau, c):
    return c + A * np.exp(-t / tau)


# ---------- Аппроксимация ----------
p0_c = [u_c.max() - u_c.min(), t_c[-1] / 3, u_c.min()]
p0_d = [u_d.max() - u_d.min(), t_d[-1] / 3, u_d.min()]

pc, _ = curve_fit(charge_model, t_c, u_c, p0=p0_c, maxfev=10000)
pd, _ = curve_fit(discharge_model, t_d, u_d, p0=p0_d, maxfev=10000)

A_c, tau_c, c_c = pc
A_d, tau_d, c_d = pd

# Уровни 63 % (зарядка) и 37 % (разрядка)
level_63 = c_c + 0.632 * A_c
level_37 = c_d + 0.368 * A_d

# Полулогарифмическая аппроксимация для разрядки: ln(U - c) = ln(A) - t/tau
mask = (u_d - c_d) > 0
slope, intercept = np.polyfit(t_d[mask], np.log(u_d[mask] - c_d), 1)
tau_log = -1.0 / slope

print(f"tau (зарядка, экспонента):    {tau_c:.4f} с")
print(f"tau (разрядка, экспонента):   {tau_d:.4f} с")
print(f"tau (разрядка, ln-линейная):  {tau_log:.4f} с")
if R_OHM is not None and C_F is not None:
    print(f"tau = R*C (теория):           {R_OHM * C_F:.4f} с")


# ---------- Оформление ----------
try:
    plt.style.use("seaborn-v0_8-whitegrid")
except OSError:
    plt.style.use("ggplot")

plt.rcParams.update({"figure.dpi": 100, "savefig.dpi": 200, "font.size": 11})
C_MEAS = "#1f77b4"
C_FIT = "#d62728"
C_LEVEL = "#2ca02c"


def finish(fig, name):
    fig.tight_layout()
    fig.savefig(name, dpi=200, bbox_inches="tight")
    print(f"сохранено: {name}")
    plt.close(fig)


# ---------- Рисунок 3: общий график ----------
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(t_c + 0, u_c, ".", ms=3, color=C_MEAS, label="зарядка")
ax.plot(t[i_peak:] - t[i_peak], u_d, ".", ms=3, color="#ff7f0e", label="разрядка")
ax.plot(t, u, "-", lw=0.6, color="gray", alpha=0.4)
ax.set_xlabel("Время, с")
ax.set_ylabel("Напряжение на C1, В")
ax.set_title("Рисунок 3 — Напряжение на конденсаторе при зарядке и разрядке")
ax.legend()
finish(fig, "rc_fig3_obshchij.png")

# ---------- Рисунок 4: зарядка ----------
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(t_c, u_c, ".", ms=4, color=C_MEAS, label="измерение")
tt = np.linspace(0, t_c[-1], 500)
ax.plot(tt, charge_model(tt, *pc), "-", lw=2, color=C_FIT,
        label=f"аппроксимация, τ = {tau_c:.3f} с")
ax.axhline(level_63, ls="--", color=C_LEVEL, label="уровень 63 %")
ax.axvline(tau_c, ls=":", color="k", label="τ")
ax.set_xlabel("Время от начала зарядки, с")
ax.set_ylabel("Напряжение на C1, В")
ax.set_title("Рисунок 4 — Зарядка конденсатора: измерение, аппроксимация экспонентой и уровень 63 %")
ax.legend()
finish(fig, "rc_fig4_zaryadka.png")

# ---------- Рисунок 5: разрядка ----------
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(t_d, u_d, ".", ms=4, color="#ff7f0e", label="измерение")
tt = np.linspace(0, t_d[-1], 500)
ax.plot(tt, discharge_model(tt, *pd), "-", lw=2, color=C_FIT,
        label=f"аппроксимация, τ = {tau_d:.3f} с")
ax.axhline(level_37, ls="--", color=C_LEVEL, label="уровень 37 %")
ax.axvline(tau_d, ls=":", color="k", label="τ")
ax.set_xlabel("Время от начала разрядки, с")
ax.set_ylabel("Напряжение на C1, В")
ax.set_title("Рисунок 5 — Разрядка конденсатора: измерение, аппроксимация экспонентой и уровень 37 %")
ax.legend()
finish(fig, "rc_fig5_razryadka.png")

# ---------- Рисунок 6: полулогарифмический масштаб ----------
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(t_d[mask], np.log(u_d[mask] - c_d), ".", ms=4, color="#ff7f0e", label="измерение")
ax.plot(t_d[mask], slope * t_d[mask] + intercept, "-", lw=2, color=C_FIT,
        label=f"линейная аппроксимация, наклон = {slope:.3f} 1/с")
ax.set_xlabel("Время от начала разрядки, с")
ax.set_ylabel("ln(U − U₀), ln(В)")
ax.set_title("Рисунок 6 — Разрядка в полулогарифмическом масштабе: зависимость линейна, наклон равен −1/τ")
ax.legend()
finish(fig, "rc_fig6_polulog.png")