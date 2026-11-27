"""План реализации SecureBooking: три версии плана, диаграммы Ганта и расчёт стоимости.

Запуск: python plan.py <папка_вывода>
Создаёт: plan-v1.png, plan-v2.png, plan-v3.png, plan.json (все цифры для документов).
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

START = date(2026, 11, 23)          # понедельник, начало итерации 1
ITER_DAYS = 7                       # длина итерации — 1 неделя (5 рабочих дней)
DEADLINE = date(2026, 12, 25)       # согласованная дата выпуска (конец итерации 5)
MIDDLE_HOURS = 30                   # часов в неделю у основного разработчика (Исполнитель)
JUNIOR_HOURS = 20                   # часов в неделю у junior-разработчика
RATE_MIDDLE = 25                    # у.е. в час
RATE_JUNIOR = 10                    # у.е. в час
JUNIOR_FACTOR = 1.5                 # junior тратит в 1,5 раза больше времени на ту же задачу
MENTORING = 6                       # часов основного разработчика на ввод junior в проект

# id: (title EN, название RU, оценка ч, приоритет, зависимости)
F = {
    "F01": ("Data core: encrypted storage", "Ядро данных: шифрование ПД, ключи DPAPI, HMAC файла", 26, 10, []),
    "F02": ("Authentication", "Регистрация и вход, PBKDF2, блокировка перебора", 16, 10, ["F01"]),
    "F03": ("GUI shell", "Каркас интерфейса WinAPI: окна, меню, формы", 20, 10, []),
    "F04": ("Room management", "Управление переговорными (администратор)", 8, 20, ["F01", "F03"]),
    "F05": ("Schedule and booking", "Расписание и бронирование с проверкой пересечений", 22, 10, ["F02", "F04"]),
    "F06": ("Cancel and my bookings", "Отмена и список «Мои бронирования»", 8, 20, ["F05"]),
    "F07": ("Role-based PII masking", "Маскирование чужих ПД по ролям", 6, 20, ["F05"]),
    "F08": ("Profile editing", "Изменение своих ПД и пароля", 8, 30, ["F02"]),
    "F09": ("Admin: users and storage audit", "Администрирование: пользователи и аудит хранилища", 10, 40, ["F02"]),
    "F10": ("Dashboard cards", "Карточки главного окна (показатели, переговорные)", 10, 40, ["F05"]),
    "F11": ("Unit tests and security check", "Модульные тесты и проверка безопасности", 14, 20, ["F01", "F02", "F05"]),
    "F12": ("Recurring bookings", "Повторяющиеся (еженедельные) бронирования", 20, 20, ["F05"]),
    "F13": ("Schedule export", "Экспорт расписания в CSV и печать", 8, 30, ["F05"]),
}


def iteration_dates(i):
    s = START + timedelta(days=ITER_DAYS * (i - 1))
    return s, s + timedelta(days=4)


def schedule(order, est, workers):
    """Планирование по исполнителям: workers = {имя: (часов_в_неделю, неделя_начала, [задачи])}.
    Задача начинается не раньше, чем закончены её зависимости (время — в неделях)."""
    tasks, done = [], {}
    for who, (per_week, first_week, items) in workers.items():
        t = float(first_week - 1)
        for fid in items:
            deps = [done[d] for d in F.get(fid, ("", "", 0, 0, []))[4] if d in done]
            t = max([t] + deps)
            end = t + est[fid] / per_week
            tasks.append(dict(id=fid, who=who, start=t, end=end, hours=est[fid]))
            done[fid] = end
            t = end
    order_index = {f: i for i, f in enumerate(order)}
    tasks.sort(key=lambda x: order_index[x["id"]])
    return tasks


def iterations_of(tasks):
    res = {}
    for t in tasks:
        a, b = int(t["start"]) + 1, int(t["end"] - 1e-9) + 1
        res[t["id"]] = f"I{a}" if a == b else f"I{a}–I{b}"
    return res


def gantt(tasks, title, path, weeks, deadline_week=5):
    fig, ax = plt.subplots(figsize=(11, 0.42 * len(tasks) + 1.6), dpi=160)
    colors = {"Исполнитель": "#2f6fde", "Junior": "#e8913a", "Исполнитель (ввод junior)": "#9aa5b1"}
    for i, t in enumerate(tasks):
        ax.barh(i, t["end"] - t["start"], left=t["start"], color=colors[t["who"]], edgecolor="white", height=0.62)
        ax.text(t["end"] + 0.05, i, f'{t["hours"]:g} ч', va="center", fontsize=8, color="#333")
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([f'{t["id"]} {F[t["id"]][0] if t["id"] in F else t["id"]}' for t in tasks], fontsize=9)
    ax.set_xlim(0, weeks + 0.9)
    ticks = list(range(weeks + 1))
    ax.set_xticks(ticks)
    ax.set_xticklabels([(START + timedelta(days=7 * w)).strftime("%d.%m") for w in ticks], fontsize=8)
    for w in range(weeks):
        ax.text(w + 0.5, -0.75, f"Итерация {w + 1}", ha="center", fontsize=8, color="#555")
        if w % 2 == 0:
            ax.axvspan(w, w + 1, color="#f3f5f8", zorder=0)
    ax.axvline(deadline_week, color="#c0392b", lw=1.6, ls="--")
    ax.text(deadline_week + 0.05, -0.2, "дедлайн\n25.12", color="#c0392b", fontsize=8, va="top")
    ax.set_title(title, fontsize=11, loc="left", pad=18)
    ax.set_ylim(len(tasks) - 0.4, -1.1)
    used = sorted({t["who"] for t in tasks})
    ax.legend(handles=[Patch(color=colors[u], label=u) for u in used], loc="lower right", fontsize=8, frameon=True, framealpha=1)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


result = {"features": {k: dict(title=v[0], name=v[1], hours=v[2], priority=v[3], deps=v[4]) for k, v in F.items()},
          "params": dict(start=str(START), deadline=str(DEADLINE), iter_days=ITER_DAYS, middle_hours=MIDDLE_HOURS,
                         junior_hours=JUNIOR_HOURS, rate_middle=RATE_MIDDLE, rate_junior=RATE_JUNIOR,
                         junior_factor=JUNIOR_FACTOR, mentoring=MENTORING),
          "iterations": {f"I{i}": [str(d) for d in iteration_dates(i)] for i in range(1, 8)}}

# ---------- план v1: предложение Исполнителя ----------
est1 = {k: v[2] for k, v in F.items()}
order1 = ["F01", "F03", "F02", "F04", "F05", "F11", "F06", "F07", "F08", "F09", "F10"]
prio1 = {k: F[k][3] for k in order1}
t1 = schedule(order1, est1, {"Исполнитель": (MIDDLE_HOURS, 1, order1)})
h1 = sum(est1[k] for k in order1)
gantt(t1, f"План v1 (предложение Исполнителя): {h1} ч, 1 разработчик", OUT / "plan-v1.png", 6)
result["v1"] = dict(order=order1, priority=prio1, hours=h1, cost=h1 * RATE_MIDDLE, iter=iterations_of(t1),
                    weeks=round(h1 / MIDDLE_HOURS, 2))

# ---------- план v2: после 1-го раунда ----------
# Заказчик поднял приоритет карточек (F10: 40 -> 20) и понизил профиль (F08: 30 -> 40) и аудит (F09: 40 -> 50).
# Исполнитель упростил аудит хранилища: только просмотр файла без поиска и подсветки (F09: 10 -> 6 ч).
est2 = dict(est1, F09=6)
prio2 = dict(prio1, F10=20, F08=40, F09=50)
order2 = ["F01", "F03", "F02", "F04", "F05", "F10", "F07", "F06", "F11", "F08", "F09"]
t2 = schedule(order2, est2, {"Исполнитель": (MIDDLE_HOURS, 1, order2)})
h2 = sum(est2[k] for k in order2)
gantt(t2, f"План v2 (после 1-го раунда): {h2} ч, 1 разработчик", OUT / "plan-v2.png", 6)
result["v2"] = dict(order=order2, priority=prio2, hours=h2, cost=h2 * RATE_MIDDLE, iter=iterations_of(t2),
                    weeks=round(h2 / MIDDLE_HOURS, 2))

# ---------- 2-й раунд: изменения объёма ----------
# Заказчик отказался от аудита хранилища (F09) и добавил F12 (повторяющиеся брони) и F13 (экспорт).
order_r2 = ["F01", "F03", "F02", "F04", "F05", "F10", "F12", "F07", "F06", "F11", "F13", "F08"]
prio_r2 = dict({k: prio2[k] for k in order_r2 if k in prio2}, F12=20, F13=30)
h_r2 = sum(est1[k] if k not in est2 else est2[k] for k in order_r2)
shift_weeks = -(-h_r2 // MIDDLE_HOURS)  # округление вверх
est_r2 = {k: (est2[k] if k in est2 else est1[k]) for k in order_r2}
t_r2 = schedule(order_r2, est_r2, {"Исполнитель": (MIDDLE_HOURS, 1, order_r2)})
gantt(t_r2, f"Вариант после 2-го раунда без изменений команды: {h_r2} ч, 1 разработчик", OUT / "plan-r2-shift.png", 6)
result["round2"] = dict(iter=iterations_of(t_r2), order=order_r2, priority=prio_r2, hours=h_r2, overflow=h_r2 - 5 * MIDDLE_HOURS,
                        shift_release=str(START + timedelta(days=7 * (shift_weeks - 1) + 4)),
                        shift_cost=h_r2 * RATE_MIDDLE)

# ---------- план v3: junior-разработчик с итерации 3 ----------
junior_tasks = ["F08", "F06", "F13"]                     # простые, слабо связанные задачи
est3 = dict(est2)
for k in junior_tasks:
    est3[k] = est1[k] * JUNIOR_FACTOR
est3["MENTOR"] = MENTORING
middle_tasks = ["F01", "F03", "F02", "MENTOR", "F04", "F05", "F10", "F12", "F07", "F11"]
F["MENTOR"] = ("Junior onboarding", "Ввод junior-разработчика в проект", MENTORING, 10, [])
t3 = schedule(middle_tasks + junior_tasks, est3,
              {"Исполнитель": (MIDDLE_HOURS, 1, middle_tasks), "Junior": (JUNIOR_HOURS, 3, junior_tasks)})
for t in t3:
    if t["id"] == "MENTOR":
        t["who"] = "Исполнитель (ввод junior)"
hm = sum(est3[k] for k in middle_tasks)
hj = sum(est3[k] for k in junior_tasks)
gantt(t3, f"План v3 (согласованный): Исполнитель {hm:g} ч + Junior {hj:g} ч", OUT / "plan-v3.png", 6)
result["v3"] = dict(middle=middle_tasks, junior=junior_tasks, priority=prio_r2, hours_middle=hm, hours_junior=hj,
                    cost_middle=hm * RATE_MIDDLE, cost_junior=hj * RATE_JUNIOR,
                    cost=hm * RATE_MIDDLE + hj * RATE_JUNIOR, iter=iterations_of(t3),
                    end_middle=max(t["end"] for t in t3 if t["who"] != "Junior"),
                    end_junior=max(t["end"] for t in t3 if t["who"] == "Junior"),
                    junior_capacity=3 * JUNIOR_HOURS)

(OUT / "plan.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
print({k: (result[k].get("hours"), result[k].get("cost")) for k in ("v1","v2","round2")}, result["v3"]["cost"], result["v3"]["hours_middle"], result["v3"]["hours_junior"])
for t in t3: print(t["id"], t["who"], round(t["start"],2), round(t["end"],2))
print(result["v1"]["iter"]); print(result["v2"]["iter"])
