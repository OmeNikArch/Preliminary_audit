#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Медиаплан теста для Слетать.ру (запрос директора по маркетингу, 02.09.2026):
сколько вкладываем — сколько получаем показов и кликов по каждому источнику.

Источники: Ozon Performance (предварительно одобрен) + Яндекс Urban Ads (на согласовании).
WB Media для Слетать.ру недоступен (конфликт с WB Тревел) — в план не входит.
Бенчмарки — из benchmarks.csv по сегментам клиента (Ozon — из кабинета, Urban — расчётные до ответа площадки).
Стиль — CSS аудитов (generate.py). Выход: sletat-ru-mediaplan.html + sletat-ru-mediaplan.xlsx.

Запуск: python3 mediaplan_sletat.py
"""
import pathlib
from generate import CSS, BENCHMARKS
from clients_data import CLIENTS

CLIENT = "sletat-ru"
SOURCES = [
    ("ozon",  "Ozon Performance", "ozon_bench_rows", "предварительно одобрен", "бенчмарки из кабинета"),
    ("urban", "Яндекс Urban Ads", "ym_bench_rows",   "на согласовании",       "бенчмарки расчётные до ответа площадки"),
]
SUPPORT = 80_000        # сопровождение двух источников, тестовый период
FREQ = 3                # средняя частота показа на человека — допущение для оценки охвата
CR_LIST = (0.01, 0.015, 0.02)   # конверсия клика в заявку — подставить свою
SCENARIOS = [
    ("Тест", 120_000, "Минимальный порог площадок: 120 000 ₽ на источник"),
    ("Рекомендуем", 200_000, "Быстрый набор статистики по сегментам для федеральной сети"),
    ("Федеральный флайт", 400_000, "Ускоренный набор охвата под окно раннего бронирования"),
]


def num(s):
    """'170,00 ₽' → 170.0 · '0,23%' → 0.0023 · '19 458 325' → 19458325"""
    s = s.replace("₽", "").replace("\xa0", " ").strip()
    pct = s.endswith("%")
    s = s.replace("%", "").replace(" ", "").replace(",", ".")
    v = float(s)
    return v / 100 if pct else v


def segments():
    """[(source_key, source_name, segment, cpm, ctr, unique_users)]"""
    out = []
    c = CLIENTS[CLIENT]
    for key, name, field, *_ in SOURCES:
        for seg in c[field]:
            b = BENCHMARKS[(CLIENT, key, seg)]
            out.append((key, name, seg, num(b["cpm"]), num(b["ctr"]), int(num(b["уникальные пользователи"]))))
    return out


SEGS = segments()


def fmt(n):
    return f"{int(round(n)):,}".replace(",", " ")


def money(n):
    return fmt(n) + " ₽"


def calc(per_source):
    """Бюджет источника делится поровну между его сегментами."""
    rows = []
    for key, name, seg, cpm, ctr, uu in SEGS:
        n_seg = sum(1 for s in SEGS if s[0] == key)
        b = per_source / n_seg
        imps = b / cpm * 1000
        clicks = imps * ctr
        rows.append({"key": key, "name": name, "seg": seg, "budget": b, "cpm": cpm, "imps": imps,
                     "ctr": ctr, "clicks": clicks, "cpc": b / clicks, "reach": imps / FREQ, "uu": uu})
    return rows


def by_source(rows):
    out = {}
    for r in rows:
        d = out.setdefault(r["key"], {"name": r["name"], "budget": 0, "imps": 0, "clicks": 0, "reach": 0})
        for k in ("budget", "imps", "clicks", "reach"):
            d[k] += r[k]
    for d in out.values():
        d["cpm"] = d["budget"] / d["imps"] * 1000
        d["ctr"] = d["clicks"] / d["imps"]
        d["cpc"] = d["budget"] / d["clicks"]
    return out


def totals(rows, support=SUPPORT):
    media = sum(r["budget"] for r in rows)
    imps = sum(r["imps"] for r in rows)
    clicks = sum(r["clicks"] for r in rows)
    reach = sum(r["reach"] for r in rows)
    return {"media": media, "support": support, "total": media + support, "imps": imps, "clicks": clicks,
            "cpc_media": media / clicks, "cpc_full": (media + support) / clicks, "reach": reach}


def build_html():
    s = []
    n = [0]

    def nxt():
        n[0] += 1
        return f"{n[0]:02d}"

    # 01 Титул
    nxt()
    s.append(f"""
<section>
  <div class="logo"><div class="sign">Ц</div><div class="nm">Церебро<br>Таргет</div></div>
  <div class="kicker"><div class="bar"></div><span>Медиаплан теста · Направление Click Out</span></div>
  <h1>Медиаплан теста:<br>Слетать.ру</h1>
  <p class="sub">Короткая смета по вашему запросу: сколько вкладываем в каждый источник — сколько получаем
  показов, кликов и по какой цене. Расчёт по бенчмаркам ваших сегментов из рекламных кабинетов площадок
  (те же цифры, что в предварительном аудите); перед стартом значения сверяем прогнозаторами кабинетов.</p>
  <div class="yline">Ozon Performance · Яндекс Urban Ads</div>
  <div class="mark">Ц</div>
</section>""")

    # 02 Статусы площадок
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Статусы согласования · на 3 сентября</span></div>
  <h2>Два источника в плане,<br>третий недоступен</h2>
  <div class="cards">
    <div class="card"><div class="big">✓</div><h3>Ozon Performance — предварительно одобрен</h3>
      <p>Ответ площадки: «Клиента к размещению примем, путешествия — это хорошо. Можем сразу добавить сегмент
      с высокой пользовательской активностью или под бюджет согласовать кастомный сегмент путешественников».</p></div>
    <div class="card"><div class="big">…</div><h3>Яндекс Urban Ads — на согласовании</h3>
      <p>Запрос отправлен, ждём ответ площадки. В плане стоит вторым флайтом; бенчмарки по сегментам — расчётные,
      уточним после ответа.</p></div>
    <div class="card"><div class="big">—</div><h3>WB Media — недоступен</h3>
      <p>У Wildberries собственный сервис WB Тревел, конкурирующие тревел-бренды к размещению не допускаются.
      Бюджет этого источника концентрируем в двух других.</p></div>
  </div>
  <div class="mark">Ц</div>
</section>""")

    # 03 Три сценария
    trs = ""
    for title, per, note in SCENARIOS:
        t = totals(calc(per))
        trs += f"""
      <tr><td>{title}</td><td>{money(per)}</td><td>{money(t['media'])}</td><td>{money(t['support'])}</td><td><b style="color:var(--yellow)">{money(t['total'])}</b></td><td>{fmt(t['imps'])}</td><td>{fmt(t['clicks'])}</td><td>{money(t['cpc_media'])}</td><td>{money(t['cpc_full'])}</td></tr>"""
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Три сценария · в месяц · Ozon + Urban Ads</span></div>
  <h2>Сколько вкладываем —<br>сколько получаем</h2>
  <div style="overflow-x:auto">
  <table class="bench">
    <tr><th>Сценарий</th><th>На источник</th><th>Медиабюджет</th><th>Сопровождение</th><th>Итого / мес</th><th>Показы</th><th>Клики</th><th>CPC медиа</th><th>CPC с сопровождением</th></tr>{trs}
  </table>
  </div>
  <div class="note"><b>Сопровождение двух источников — {money(SUPPORT)}/мес</b> на тестовый период (скидка 20% от прайса 100 000 ₽):
  ведение кампаний, креативы, аналитический контур, замеры, недельная и месячная отчётность. Показы и клики — расчёт по CPM и CTR
  ваших сегментов из кабинетов площадок при равном делении бюджета источника между тремя сегментами.</div>
  <div class="foot">{"<br>".join(f"<b>{t}</b> — {nt}." for t, _, nt in SCENARIOS)}</div>
  <div class="mark">Ц</div>
</section>""")

    # 04 Разбивка по сегментам — сценарий «Рекомендуем»
    per = SCENARIOS[1][1]
    rows = calc(per)
    t = totals(rows)
    bs = by_source(rows)
    trs = ""
    for key, name, *_ in SOURCES:
        for r in [r for r in rows if r["key"] == key]:
            trs += f"""
      <tr><td>{r['seg']}</td><td>{name}</td><td>{money(r['budget'])}</td><td>{r['cpm']:.2f} ₽</td><td>{fmt(r['imps'])}</td><td>{r['ctr']*100:.2f}%</td><td>{fmt(r['clicks'])}</td><td>{r['cpc']:.2f} ₽</td><td>{fmt(r['uu'])}</td></tr>"""
        d = bs[key]
        trs += f"""
      <tr><td>Итого {name}</td><td></td><td>{money(d['budget'])}</td><td>{d['cpm']:.2f} ₽</td><td>{fmt(d['imps'])}</td><td>{d['ctr']*100:.2f}%</td><td>{fmt(d['clicks'])}</td><td>{d['cpc']:.2f} ₽</td><td></td></tr>"""
    trs += f"""
      <tr><td>Итого два источника</td><td></td><td>{money(t['media'])}</td><td>—</td><td>{fmt(t['imps'])}</td><td>—</td><td>{fmt(t['clicks'])}</td><td>{t['cpc_media']:.2f} ₽</td><td></td></tr>"""
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Разбивка по сегментам · сценарий «Рекомендуем» · {money(per)} на источник</span></div>
  <h2>Что даёт каждый сегмент<br>за месяц</h2>
  <div style="overflow-x:auto">
  <table class="bench">
    <tr><th>Сегмент</th><th>Источник</th><th>Бюджет</th><th>CPM</th><th>Показы</th><th>CTR</th><th>Клики</th><th>CPC</th><th>Ёмкость: уникальных пользователей / мес</th></tr>{trs}
  </table>
  </div>
  <div class="foot">Ёмкость — размер сегмента в кабинете площадки; бюджет теста выкупает доли процента показов, есть куда масштабироваться.
  Оценка охвата теста при средней частоте {FREQ} показа на человека: {fmt(t['reach'])} человек в месяц. Аудитории площадок не складываются —
  один человек может быть и на Ozon, и в сервисах Яндекса. Urban Ads: бенчмарки расчётные до ответа площадки.</div>
  <div class="mark">Ц</div>
</section>""")

    # 05 Заявки при разной конверсии
    cards = ""
    for cr in CR_LIST:
        leads = t["clicks"] * cr
        cards += f"""
    <div class="card"><div class="big">{fmt(leads)}</div><h3>заявок в месяц при конверсии {cr*100:g}%</h3>
      <p>Стоимость заявки: <b>{money(t['total']/leads)}</b> с учётом сопровождения · {money(t['media']/leads)} по медиабюджету</p></div>"""
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Заявки · сценарий «Рекомендуем» · {fmt(t['clicks'])} кликов в месяц</span></div>
  <h2>Подставьте свою конверсию —<br>получите цену заявки</h2>
  <div class="cards">{cards}
  </div>
  <div class="note"><b>Конверсия клика в заявку — ваша цифра.</b> Для агрегатора туров заявка — подбор тура, звонок или заявка в офис сети.
  На созвоне подставим вашу конверсию с трафика Директа и таргета: расчёт в приложенном Excel пересчитывается автоматически.
  Медийный трафик в моменте конвертирует ниже перформанса и добирает post-view: увидел баннер, пришёл сам через две недели —
  этот слой считаем отдельно, при цикле покупки тура 1–6 месяцев без него до 99% эффекта не видно в отчётах по последнему клику.</div>
  <div class="mark">Ц</div>
</section>""")

    # 06 Календарь теста и замеры
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Календарь теста · 8 недель</span></div>
  <h2>Старт в октябре — в пик<br>раннего бронирования лета</h2>
  <div class="rows">
    <div class="row"><div class="l">До старта · 1–2 недели</div><div class="r">Кабинет Ozon открывается за 3–5 рабочих дней (площадка одобрила), запуск кампании — от 7 дней. Посадочные под сегменты («туры к морю», «семейные туры»), пиксели площадок и UTM, замер «до» по Вордстату — бесплатно, до договора.</div></div>
    <div class="row"><div class="l">Недели 1–2 · тест</div><div class="r">Ozon: три сегмента плюс сегмент с высокой пользовательской активностью от площадки; первые бенчмарки CPM/CTR/CPC по факту. Urban Ads — подключаем по ответу площадки вторым флайтом.</div></div>
    <div class="row"><div class="l">Недели 3–6 · связка</div><div class="r">Отключаем слабые сегменты, перераспределяем бюджет по стоимости клика и заявки; под бюджет согласовываем с Ozon кастомный сегмент путешественников; креативы под раннее бронирование.</div></div>
    <div class="row"><div class="l">Недели 7–8 · масштабирование</div><div class="r">Наращиваем лучшие связки; документ-решение по итогам теста: что продолжаем, что останавливаем — по вашим критериям.</div></div>
    <div class="row"><div class="l">Замеры</div><div class="r">Search lift по Вордстату («слетать ру», «слетать туры» против контрольного «горящие туры») и post-view слой — с первого дня, на любом бюджете. Brand Lift Яндекса — бесплатно при охвате от 2 млн, после подключения Urban Ads.</div></div>
  </div>
  <div class="mark">Ц</div>
</section>""")

    # 07 Условия и следующий шаг
    t1 = totals(calc(per), support=50_000)
    rows_ozon = [r for r in calc(per) if r["key"] == "ozon"]
    ozon_only = totals(rows_ozon, support=50_000)
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Условия и следующий шаг</span></div>
  <h2>Что нужно, чтобы стартовать<br>в октябре</h2>
  <div class="rows">
    <div class="row"><div class="l">Бюджет</div><div class="r">От 120 000 ₽ в месяц на источник; рекомендуем 200 000 ₽ — итого {money(t['total'])} в месяц на два источника с сопровождением. Старт только с Ozon до ответа Urban Ads: {money(ozon_only['media'])} медиа + 50 000 ₽ сопровождение = {money(ozon_only['total'])}, {fmt(ozon_only['clicks'])} кликов в месяц.</div></div>
    <div class="row"><div class="l">Срок</div><div class="r">Контракт от шести месяцев, первые 8 недель — тестовый период со скидкой на сопровождение. Медийный эффект читается на горизонте 6–8 недель, решения по бюджету — по кварталу.</div></div>
    <div class="row"><div class="l">Данные</div><div class="r">Ваша конверсия в заявку, доступ к Метрике, база туристов для CRM-сегмента (хэш телефонов) — под look-a-like на обеих площадках.</div></div>
    <div class="row"><div class="l">Рессейлинг</div><div class="r">Параллельно открываем кабинеты для инхаус-команды: Директ, VK Ads, Telegram Ads и ещё 10 систем в одном окне; бонусные рубли по шкале Церебро с расхода от 360 001 ₽ в месяц.</div></div>
  </div>
  <div class="yline">Следующий шаг — созвон на 20 минут: подставляем вашу конверсию, фиксируем сценарий и дату старта.<br>Церебро Таргет · направление Click Out · clickout.cerebrotarget.ru</div>
  <div class="mark">Ц</div>
</section>""")

    body = "".join(s)
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Медиаплан теста · Слетать.ру · Cerebro Click Out</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700&display=swap" rel="stylesheet">
<style>{CSS}
  table.bench td, table.bench th{{white-space:nowrap}}
  table.bench td:first-child{{white-space:normal;min-width:220px}}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def build_xlsx(path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    from openpyxl.utils import get_column_letter
    wb = Workbook()
    ws = wb.active
    ws.title = "Медиаплан"
    yellow = PatternFill("solid", fgColor="FDD101")
    bold = Font(bold=True)
    ws["A1"] = "Медиаплан теста · Слетать.ру · Cerebro Click Out · Ozon Performance + Яндекс Urban Ads"
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = ("Жёлтые ячейки — входные параметры, меняйте их: расчёт пересчитается автоматически. "
                "CPM/CTR — бенчмарки ваших сегментов из кабинетов площадок (Ozon — факт кабинета, Urban — расчёт до ответа площадки). "
                "WB Media недоступен (WB Тревел).")
    ws["A4"] = "Параметры"; ws["A4"].font = bold
    params = [("Бюджет на источник, ₽/мес", 200000), ("Сопровождение 2 источника, ₽/мес", SUPPORT),
              ("Конверсия клика в заявку", 0.015), ("Средняя частота показа (для охвата)", FREQ), ("Срок теста, мес", 2)]
    for i, (k, v) in enumerate(params, start=5):
        ws.cell(row=i, column=1, value=k)
        c = ws.cell(row=i, column=2, value=v); c.fill = yellow
    ws["B7"].number_format = "0.0%"
    hdr = ["Сегмент", "Источник", "Бюджет, ₽", "CPM, ₽", "CTR", "Показы", "Охват (оценка)", "Клики", "CPC, ₽", "Заявки", "CPL медиа, ₽", "Ёмкость: уникальных / мес"]
    r0 = 12
    ws.cell(row=r0 - 1, column=1, value="Расчёт по сегментам (бюджет источника делится поровну между его сегментами)").font = bold
    for j, h in enumerate(hdr, start=1):
        ws.cell(row=r0, column=j, value=h).font = bold
    r = r0 + 1
    src_rows = {}
    for key, name, *_ in SOURCES:
        segs = [s for s in SEGS if s[0] == key]
        first = r
        for _, _, seg, cpm, ctr, uu in segs:
            ws.cell(row=r, column=1, value=seg)
            ws.cell(row=r, column=2, value=name)
            ws.cell(row=r, column=3, value=f"=$B$5/{len(segs)}")
            c = ws.cell(row=r, column=4, value=cpm); c.fill = yellow
            c = ws.cell(row=r, column=5, value=ctr); c.fill = yellow; c.number_format = "0.00%"
            ws.cell(row=r, column=6, value=f"=C{r}/D{r}*1000")
            ws.cell(row=r, column=7, value=f"=F{r}/$B$8")
            ws.cell(row=r, column=8, value=f"=F{r}*E{r}")
            ws.cell(row=r, column=9, value=f"=C{r}/H{r}")
            ws.cell(row=r, column=10, value=f"=H{r}*$B$7")
            ws.cell(row=r, column=11, value=f"=C{r}/J{r}")
            ws.cell(row=r, column=12, value=uu)
            r += 1
        last = r - 1
        ws.cell(row=r, column=1, value=f"Итого {name}").font = bold
        for col in (3, 6, 7, 8, 10):
            L = get_column_letter(col)
            ws.cell(row=r, column=col, value=f"=SUM({L}{first}:{L}{last})").font = bold
        ws.cell(row=r, column=4, value=f"=C{r}/F{r}*1000")
        ws.cell(row=r, column=5, value=f"=H{r}/F{r}").number_format = "0.00%"
        ws.cell(row=r, column=9, value=f"=C{r}/H{r}")
        ws.cell(row=r, column=11, value=f"=C{r}/J{r}")
        src_rows[key] = r
        r += 1
    tr = r
    ws.cell(row=tr, column=1, value="Итого медиа (два источника)").font = bold
    for col in (3, 6, 7, 8, 10):
        L = get_column_letter(col)
        ws.cell(row=tr, column=col, value="=" + "+".join(f"{L}{x}" for x in src_rows.values())).font = bold
    ws.cell(row=tr, column=9, value=f"=C{tr}/H{tr}")
    ws.cell(row=tr, column=11, value=f"=C{tr}/J{tr}")
    ws.cell(row=tr + 1, column=1, value="Сопровождение"); ws.cell(row=tr + 1, column=3, value="=$B$6")
    ws.cell(row=tr + 2, column=1, value="Итого в месяц").font = bold; ws.cell(row=tr + 2, column=3, value=f"=C{tr}+C{tr+1}").font = bold
    ws.cell(row=tr + 3, column=1, value="CPC с сопровождением, ₽"); ws.cell(row=tr + 3, column=3, value=f"=C{tr+2}/H{tr}")
    ws.cell(row=tr + 4, column=1, value="CPL с сопровождением, ₽"); ws.cell(row=tr + 4, column=3, value=f"=C{tr+2}/J{tr}")
    ws.cell(row=tr + 5, column=1, value="Итого за срок теста, ₽").font = bold; ws.cell(row=tr + 5, column=3, value=f"=C{tr+2}*$B$9").font = bold
    ws.cell(row=tr + 6, column=1, value="Кликов за срок теста"); ws.cell(row=tr + 6, column=3, value=f"=H{tr}*$B$9")
    ws.cell(row=tr + 7, column=1, value="Заявок за срок теста"); ws.cell(row=tr + 7, column=3, value=f"=J{tr}*$B$9")
    for row in ws.iter_rows(min_row=r0 + 1, max_row=tr + 7):
        for c in row:
            if c.column in (3, 4, 6, 7, 8, 9, 10, 11, 12) and c.number_format == "General":
                c.number_format = "#,##0"
    ws.column_dimensions["A"].width = 44
    ws.column_dimensions["B"].width = 20
    for col in range(3, 13):
        ws.column_dimensions[get_column_letter(col)].width = 16
    ws["A" + str(tr + 9)] = ("Условия: бюджет от 120 000 ₽/мес на источник, контракт от 6 мес, тестовый период 8 недель. "
                             "Сопровождение: 1 источник — 50 000, 2 — 80 000 ₽/мес (тестовый период).")
    ws["A" + str(tr + 10)] = "Церебро Таргет · направление Click Out · clickout.cerebrotarget.ru"
    wb.save(path)


if __name__ == "__main__":
    root = pathlib.Path(__file__).parent
    html = build_html()
    (root / "sletat-ru-mediaplan.html").write_text(html, encoding="utf-8")
    print(f"OK sletat-ru-mediaplan.html ({len(html)} bytes)")
    build_xlsx(root / "sletat-ru-mediaplan.xlsx")
    print("OK sletat-ru-mediaplan.xlsx")
    for title, per, _ in SCENARIOS:
        t = totals(calc(per))
        print(f"{title:18s} {per:>8,} на источник → медиа {t['media']:>10,.0f} + {t['support']:,} = {t['total']:>10,.0f} ₽ · "
              f"показы {t['imps']:>10,.0f} · клики {t['clicks']:>7,.0f} · CPC {t['cpc_media']:.2f} / {t['cpc_full']:.2f}")
    for k, d in by_source(calc(200_000)).items():
        print(f"  {d['name']:18s} CPM {d['cpm']:.2f} · CTR {d['ctr']*100:.2f}% · клики {d['clicks']:,.0f} · CPC {d['cpc']:.2f}")
