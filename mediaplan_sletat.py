#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Медиаплан теста для Слетать.ру (запрос директора по маркетингу, 02.09.2026):
сколько вкладываем — сколько получаем показов и кликов.

Договорённость: в IV квартале 2026 запускаем только Ozon Performance (площадка предварительно одобрила).
Яндекс Urban Ads — возможный второй шаг после ответа площадки и результатов первого флайта; в расчёт не входит.
WB Media для Слетать.ру недоступен (конфликт с WB Тревел).
Бенчмарки — из benchmarks.csv по сегментам клиента (Ozon — из кабинета площадки).
Стиль — CSS аудитов (generate.py). Выход: sletat-ru-mediaplan.html + sletat-ru-mediaplan.xlsx.

Запуск: python3 mediaplan_sletat.py
"""
import pathlib
from generate import CSS, BENCHMARKS
from clients_data import CLIENTS

CLIENT = "sletat-ru"
SOURCE_KEY, SOURCE_NAME, SEG_FIELD = "ozon", "Ozon Performance", "ozon_bench_rows"
SUPPORT = 50_000        # сопровождение одного источника, в месяц
FREQ = 3                # средняя частота показа на человека — допущение для оценки охвата
CR_LIST = (0.01, 0.015, 0.02)   # конверсия клика в заявку — подставить свою
SCENARIOS = [
    ("Тест", 120_000, "Минимальный порог площадки: 120 000 ₽ в месяц"),
    ("Рекомендуем", 200_000, "Быстрый набор статистики по сегментам для федеральной сети"),
    ("Федеральный флайт", 400_000, "Ускоренный набор охвата под окно раннего бронирования; расход выше 360 000 ₽ открывает бонусные рубли по шкале Церебро"),
]


def num(s):
    """'170,00 ₽' → 170.0 · '0,23%' → 0.0023 · '19 458 325' → 19458325"""
    s = s.replace("₽", "").replace("\xa0", " ").strip()
    pct = s.endswith("%")
    s = s.replace("%", "").replace(" ", "").replace(",", ".")
    v = float(s)
    return v / 100 if pct else v


def segments():
    """[(segment, cpm, ctr, unique_users)]"""
    out = []
    for seg in CLIENTS[CLIENT][SEG_FIELD]:
        b = BENCHMARKS[(CLIENT, SOURCE_KEY, seg)]
        out.append((seg, num(b["cpm"]), num(b["ctr"]), int(num(b["уникальные пользователи"]))))
    return out


SEGS = segments()


def fmt(n):
    return f"{int(round(n)):,}".replace(",", " ")


def money(n):
    return fmt(n) + " ₽"


def calc(budget):
    """Бюджет делится поровну между сегментами."""
    rows = []
    for seg, cpm, ctr, uu in SEGS:
        b = budget / len(SEGS)
        imps = b / cpm * 1000
        clicks = imps * ctr
        rows.append({"seg": seg, "budget": b, "cpm": cpm, "imps": imps, "ctr": ctr, "clicks": clicks,
                     "cpc": b / clicks, "reach": imps / FREQ, "uu": uu})
    return rows


def totals(rows, support=SUPPORT):
    media = sum(r["budget"] for r in rows)
    imps = sum(r["imps"] for r in rows)
    clicks = sum(r["clicks"] for r in rows)
    reach = sum(r["reach"] for r in rows)
    return {"media": media, "support": support, "total": media + support, "imps": imps, "clicks": clicks,
            "cpm": media / imps * 1000, "ctr": clicks / imps,
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
  <div class="kicker"><div class="bar"></div><span>Медиаплан теста · IV квартал 2026 · Направление Click Out</span></div>
  <h1>Медиаплан теста:<br>Слетать.ру · Ozon Performance</h1>
  <p class="sub">Короткая смета по вашему запросу: сколько вкладываем — сколько получаем показов, кликов и по какой цене.
  Как договорились, первый флайт — только Ozon Performance: площадка предварительно одобрила размещение.
  Расчёт по бенчмаркам ваших сегментов из рекламного кабинета Ozon (те же цифры, что в предварительном аудите);
  перед стартом значения сверяем прогнозатором кабинета.</p>
  <div class="yline">Ozon Performance · старт в октябре</div>
  <div class="mark">Ц</div>
</section>""")

    # 02 Статусы площадок и рамка плана
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Рамка плана · статусы площадок на 3 сентября</span></div>
  <h2>Один источник в первом флайте,<br>и почему именно он</h2>
  <div class="cards">
    <div class="card"><div class="big">✓</div><h3>Ozon Performance — в плане</h3>
      <p>Площадка предварительно одобрила размещение: «Клиента к размещению примем, путешествия — это хорошо. Можем сразу добавить
      сегмент с высокой пользовательской активностью или под бюджет согласовать кастомный сегмент путешественников».
      Кабинет открывается за 3–5 рабочих дней, запуск — от 7 дней.</p></div>
    <div class="card"><div class="big">…</div><h3>Яндекс Urban Ads — второй шаг</h3>
      <p>Запрос на согласовании, ждём ответ площадки. В IV квартале в расчёт не входит; решение о подключении — после
      ответа площадки и первых результатов Ozon, отдельным расчётом.</p></div>
    <div class="card"><div class="big">—</div><h3>WB Media — недоступен</h3>
      <p>У Wildberries собственный сервис WB Тревел, конкурирующие тревел-бренды к размещению не допускаются.</p></div>
  </div>
  <div class="mark">Ц</div>
</section>""")

    # 03 Три сценария
    trs = ""
    for title, per, note in SCENARIOS:
        t = totals(calc(per))
        trs += f"""
      <tr><td>{title}</td><td>{money(t['media'])}</td><td>{money(t['support'])}</td><td><b style="color:var(--yellow)">{money(t['total'])}</b></td><td>{fmt(t['imps'])}</td><td>{fmt(t['reach'])}</td><td>{fmt(t['clicks'])}</td><td>{money(t['cpc_media'])}</td><td>{money(t['cpc_full'])}</td></tr>"""
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Три сценария · в месяц · Ozon Performance</span></div>
  <h2>Сколько вкладываем —<br>сколько получаем</h2>
  <div style="overflow-x:auto">
  <table class="bench">
    <tr><th>Сценарий</th><th>Медиабюджет</th><th>Сопровождение</th><th>Итого / мес</th><th>Показы</th><th>Охват*</th><th>Клики</th><th>CPC медиа</th><th>CPC с сопровождением</th></tr>{trs}
  </table>
  </div>
  <div class="note"><b>Сопровождение одного источника — {money(SUPPORT)}/мес</b>: ведение кампаний, креативы, аналитический контур,
  замеры, недельная и месячная отчётность. Показы и клики — расчёт по CPM и CTR ваших сегментов из кабинета Ozon
  при равном делении бюджета между тремя сегментами.</div>
  <div class="foot">* Охват — оценка при средней частоте {FREQ} показа на человека; точный охват отдаёт прогнозатор кабинета перед стартом.<br>
  {"<br>".join(f"<b>{t}</b> — {nt}." for t, _, nt in SCENARIOS)}</div>
  <div class="mark">Ц</div>
</section>""")

    # 04 Разбивка по сегментам — сценарий «Рекомендуем»
    per = SCENARIOS[1][1]
    rows = calc(per)
    t = totals(rows)
    trs = "".join(f"""
      <tr><td>{r['seg']}</td><td>{money(r['budget'])}</td><td>{r['cpm']:.2f} ₽</td><td>{fmt(r['imps'])}</td><td>{r['ctr']*100:.2f}%</td><td>{fmt(r['clicks'])}</td><td>{r['cpc']:.2f} ₽</td><td>{fmt(r['uu'])}</td></tr>""" for r in rows)
    trs += f"""
      <tr><td>Итого Ozon Performance</td><td>{money(t['media'])}</td><td>{t['cpm']:.2f} ₽</td><td>{fmt(t['imps'])}</td><td>{t['ctr']*100:.2f}%</td><td>{fmt(t['clicks'])}</td><td>{t['cpc_media']:.2f} ₽</td><td></td></tr>"""
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Разбивка по сегментам · сценарий «Рекомендуем» · {money(per)} в месяц</span></div>
  <h2>Что даёт каждый сегмент<br>за месяц</h2>
  <div style="overflow-x:auto">
  <table class="bench">
    <tr><th>Сегмент</th><th>Бюджет</th><th>CPM</th><th>Показы</th><th>CTR</th><th>Клики</th><th>CPC</th><th>Ёмкость: уникальных пользователей / мес</th></tr>{trs}
  </table>
  </div>
  <div class="foot">Ёмкость — размер сегмента в кабинете Ozon; бюджет теста выкупает доли процента показов, есть куда масштабироваться.
  Четвёртым сегментом площадка предлагает добавить аудиторию с высокой пользовательской активностью, под бюджет — кастомный сегмент
  путешественников; их бенчмарки появятся после открытия кабинета. Оценка охвата теста при частоте {FREQ}: {fmt(t['reach'])} человек в месяц.</div>
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
  <div class="kicker"><div class="bar"></div><span>Календарь флайта · IV квартал</span></div>
  <h2>Старт в октябре — в пик<br>раннего бронирования лета</h2>
  <div class="rows">
    <div class="row"><div class="l">До старта · 1–2 недели</div><div class="r">Кабинет Ozon открывается за 3–5 рабочих дней (площадка одобрила), запуск кампании — от 7 дней. Посадочные под сегменты («туры к морю», «семейные туры»), пиксели площадки и UTM, замер «до» по Вордстату — бесплатно, до договора.</div></div>
    <div class="row"><div class="l">Недели 1–2 · тест</div><div class="r">Три сегмента из аудита плюс сегмент с высокой пользовательской активностью от площадки; первые бенчмарки CPM/CTR/CPC по факту, а не по прогнозу.</div></div>
    <div class="row"><div class="l">Недели 3–6 · связка</div><div class="r">Отключаем слабые сегменты, перераспределяем бюджет по стоимости клика и заявки; под бюджет согласовываем с Ozon кастомный сегмент путешественников; креативы под раннее бронирование.</div></div>
    <div class="row"><div class="l">Недели 7–8 · масштабирование</div><div class="r">Наращиваем лучшие связки; документ-решение по итогам теста: что продолжаем, что останавливаем — по вашим критериям. Тогда же — решение по Urban Ads как второму источнику.</div></div>
    <div class="row"><div class="l">Замеры</div><div class="r">Search lift по Вордстату («слетать ру», «слетать туры» против контрольного «горящие туры») и post-view отчёт Ozon (заказы и заявки после показов, окно до 30 дней) — с первого дня, на любом бюджете.</div></div>
  </div>
  <div class="mark">Ц</div>
</section>""")

    # 07 Условия и следующий шаг
    t_min = totals(calc(SCENARIOS[0][1]))
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Условия и следующий шаг</span></div>
  <h2>Что нужно, чтобы стартовать<br>в октябре</h2>
  <div class="rows">
    <div class="row"><div class="l">Бюджет</div><div class="r">От 120 000 ₽ в месяц на Ozon Performance — итого {money(t_min['total'])} с сопровождением. Рекомендуем 200 000 ₽ — {money(t['total'])} в месяц, {fmt(t['clicks'])} кликов. Расход от 360 001 ₽ в месяц открывает бонусные рубли по шкале Церебро (экран «Ozon Performance · Условия» в аудите).</div></div>
    <div class="row"><div class="l">Срок</div><div class="r">Контракт от шести месяцев, первые 8 недель — тестовый период. Медийный эффект читается на горизонте 6–8 недель, решения по бюджету — по кварталу.</div></div>
    <div class="row"><div class="l">Данные</div><div class="r">Ваша конверсия в заявку, доступ к Метрике, база туристов для собственного сегмента (хэш телефонов) — под look-a-like в кабинете Ozon.</div></div>
    <div class="row"><div class="l">Что дальше</div><div class="r">Urban Ads — по ответу площадки и результатам первого флайта, отдельным расчётом. Параллельно открываем кабинеты для инхаус-команды: Директ, VK Ads, Telegram Ads и ещё 10 систем в одном окне.</div></div>
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
<title>Медиаплан теста · Слетать.ру · Ozon Performance · Cerebro Click Out</title>
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
    ws["A1"] = "Медиаплан теста · Слетать.ру · Ozon Performance · IV квартал 2026 · Cerebro Click Out"
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = ("Жёлтые ячейки — входные параметры, меняйте их: расчёт пересчитается автоматически. "
                "CPM/CTR — бенчмарки ваших сегментов из кабинета Ozon. Urban Ads — второй шаг отдельным расчётом, WB Media недоступен (WB Тревел).")
    ws["A4"] = "Параметры"; ws["A4"].font = bold
    params = [("Медиабюджет Ozon Performance, ₽/мес", 200000), ("Сопровождение 1 источник, ₽/мес", SUPPORT),
              ("Конверсия клика в заявку", 0.015), ("Средняя частота показа (для охвата)", FREQ), ("Срок теста, мес", 2)]
    for i, (k, v) in enumerate(params, start=5):
        ws.cell(row=i, column=1, value=k)
        c = ws.cell(row=i, column=2, value=v); c.fill = yellow
    ws["B7"].number_format = "0.0%"
    hdr = ["Сегмент", "Бюджет, ₽", "CPM, ₽", "CTR", "Показы", "Охват (оценка)", "Клики", "CPC, ₽", "Заявки", "CPL медиа, ₽", "Ёмкость: уникальных / мес"]
    r0 = 12
    ws.cell(row=r0 - 1, column=1, value="Расчёт по сегментам (бюджет делится поровну между сегментами)").font = bold
    for j, h in enumerate(hdr, start=1):
        ws.cell(row=r0, column=j, value=h).font = bold
    r = r0 + 1
    first = r
    for seg, cpm, ctr, uu in SEGS:
        ws.cell(row=r, column=1, value=seg)
        ws.cell(row=r, column=2, value=f"=$B$5/{len(SEGS)}")
        c = ws.cell(row=r, column=3, value=cpm); c.fill = yellow
        c = ws.cell(row=r, column=4, value=ctr); c.fill = yellow; c.number_format = "0.00%"
        ws.cell(row=r, column=5, value=f"=B{r}/C{r}*1000")
        ws.cell(row=r, column=6, value=f"=E{r}/$B$8")
        ws.cell(row=r, column=7, value=f"=E{r}*D{r}")
        ws.cell(row=r, column=8, value=f"=B{r}/G{r}")
        ws.cell(row=r, column=9, value=f"=G{r}*$B$7")
        ws.cell(row=r, column=10, value=f"=B{r}/I{r}")
        ws.cell(row=r, column=11, value=uu)
        r += 1
    last = r - 1
    tr = r
    ws.cell(row=tr, column=1, value="Итого медиа Ozon Performance").font = bold
    for col in (2, 5, 6, 7, 9):
        L = get_column_letter(col)
        ws.cell(row=tr, column=col, value=f"=SUM({L}{first}:{L}{last})").font = bold
    ws.cell(row=tr, column=3, value=f"=B{tr}/E{tr}*1000")
    ws.cell(row=tr, column=4, value=f"=G{tr}/E{tr}").number_format = "0.00%"
    ws.cell(row=tr, column=8, value=f"=B{tr}/G{tr}")
    ws.cell(row=tr, column=10, value=f"=B{tr}/I{tr}")
    ws.cell(row=tr + 1, column=1, value="Сопровождение"); ws.cell(row=tr + 1, column=2, value="=$B$6")
    ws.cell(row=tr + 2, column=1, value="Итого в месяц").font = bold; ws.cell(row=tr + 2, column=2, value=f"=B{tr}+B{tr+1}").font = bold
    ws.cell(row=tr + 3, column=1, value="CPC с сопровождением, ₽"); ws.cell(row=tr + 3, column=2, value=f"=B{tr+2}/G{tr}")
    ws.cell(row=tr + 4, column=1, value="CPL с сопровождением, ₽"); ws.cell(row=tr + 4, column=2, value=f"=B{tr+2}/I{tr}")
    ws.cell(row=tr + 5, column=1, value="Итого за срок теста, ₽").font = bold; ws.cell(row=tr + 5, column=2, value=f"=B{tr+2}*$B$9").font = bold
    ws.cell(row=tr + 6, column=1, value="Кликов за срок теста"); ws.cell(row=tr + 6, column=2, value=f"=G{tr}*$B$9")
    ws.cell(row=tr + 7, column=1, value="Заявок за срок теста"); ws.cell(row=tr + 7, column=2, value=f"=I{tr}*$B$9")
    for row in ws.iter_rows(min_row=r0 + 1, max_row=tr + 7):
        for c in row:
            if c.column in (2, 3, 5, 6, 7, 8, 9, 10, 11) and c.number_format == "General":
                c.number_format = "#,##0"
    ws.column_dimensions["A"].width = 44
    for col in range(2, 12):
        ws.column_dimensions[get_column_letter(col)].width = 16
    ws["A" + str(tr + 9)] = ("Условия: бюджет от 120 000 ₽/мес, контракт от 6 мес, тестовый период 8 недель, сопровождение 1 источника — 50 000 ₽/мес. "
                             "Бонусные рубли по шкале Церебро — с расхода от 360 001 ₽/мес.")
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
        print(f"{title:18s} медиа {t['media']:>9,.0f} + {t['support']:,} = {t['total']:>9,.0f} ₽ · показы {t['imps']:>10,.0f} · "
              f"охват ~{t['reach']:>8,.0f} · клики {t['clicks']:>6,.0f} · CPC {t['cpc_media']:.2f} / {t['cpc_full']:.2f}")
