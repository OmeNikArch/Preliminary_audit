#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Медиаплан теста для Слетать.ру (запрос директора по маркетингу, 02.09.2026):
сколько вкладываем — сколько получаем показов и кликов.

Договорённость: в IV квартале 2026 запускаем только Ozon Performance (площадка предварительно одобрила),
тестовый бюджет — 500 000 ₽ медиа в месяц (может быть меньше, но план раскрывает потенциал именно от 500 000).
Яндекс Urban Ads — возможный второй шаг после ответа площадки и результатов первого флайта; в расчёт не входит.
WB Media для Слетать.ру недоступен (конфликт с WB Тревел).
Бенчмарки — из benchmarks.csv по сегментам клиента (Ozon — из кабинета площадки).
Сопровождение (СРК) — по шкале премирования Церебро (экран «Ozon Performance · Условия» в аудитах).
Стиль — CSS аудитов (generate.py). Выход: sletat-ru-mediaplan.html + sletat-ru-mediaplan.xlsx.

Запуск: python3 mediaplan_sletat.py
"""
import pathlib
from generate import CSS, BENCHMARKS
from clients_data import CLIENTS

CLIENT = "sletat-ru"
SOURCE_KEY, SOURCE_NAME, SEG_FIELD = "ozon", "Ozon Performance", "ozon_bench_rows"
FREQ = 3                # средняя частота показа на человека — допущение для оценки охвата
CR_LIST = (0.01, 0.015, 0.02)   # конверсия клика в заявку — подставить свою
MAIN = 500_000          # тестовый бюджет, оговорённый с клиентом (медиа, в месяц)
SCENARIOS = [
    ("Если меньше", 350_000, "Сокращённый вариант: расход ниже 360 001 ₽ — сопровождение 20% без скидки"),
    ("Оговорённый тест", MAIN, "Тестовый бюджет, который обсуждали на стенде; со второго месяца сопровождение со скидкой — 10%"),
    ("Расширение", 750_000, "После теста: масштабирование лучших связок и кастомного сегмента путешественников"),
]
MONTHS = 2              # тестовый период


def srk(spend):
    """Сопровождение (СРК) по шкале премирования Церебро: (первый месяц, со скидкой со второго месяца)."""
    if spend <= 200_000:
        return 50_000, 50_000
    if spend <= 360_000:
        return spend * 0.20, spend * 0.20
    if spend <= 1_099_999:
        return spend * 0.20, spend * 0.10
    if spend <= 1_999_999:
        return spend * 0.20, spend * 0.08
    if spend <= 6_999_999:
        return spend * 0.20, spend * 0.06
    if spend <= 9_999_999:
        return spend * 0.20, spend * 0.04
    return spend * 0.20, spend * 0.02


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


def totals(rows):
    media = sum(r["budget"] for r in rows)
    imps = sum(r["imps"] for r in rows)
    clicks = sum(r["clicks"] for r in rows)
    reach = sum(r["reach"] for r in rows)
    s1, s2 = srk(media)
    test_total = (media + s1) + (media + s2) * (MONTHS - 1)
    return {"media": media, "srk1": s1, "srk2": s2, "total1": media + s1, "total2": media + s2,
            "test_total": test_total, "imps": imps, "clicks": clicks, "cpm": media / imps * 1000, "ctr": clicks / imps,
            "cpc_media": media / clicks, "cpc_full": (media + s2) / clicks, "reach": reach}


def build_html():
    s = []
    n = [0]

    def nxt():
        n[0] += 1
        return f"{n[0]:02d}"

    main_rows = calc(MAIN)
    t = totals(main_rows)
    cap = sum(uu for _, _, _, uu in SEGS)

    # 01 Титул
    nxt()
    s.append(f"""
<section>
  <div class="logo"><div class="sign">Ц</div><div class="nm">Церебро<br>Таргет</div></div>
  <div class="kicker"><div class="bar"></div><span>Медиаплан теста · IV квартал 2026 · Направление Click Out</span></div>
  <h1>Медиаплан теста:<br>Слетать.ру · Ozon Performance</h1>
  <p class="sub">Короткая смета по вашему запросу: сколько вкладываем — сколько получаем показов, кликов и по какой цене.
  Как договорились, первый флайт — только Ozon Performance (площадка предварительно одобрила размещение),
  тестовый бюджет — <b>{money(MAIN)} в месяц</b>. Расчёт по бенчмаркам ваших сегментов из рекламного кабинета Ozon
  (те же цифры, что в предварительном аудите); перед стартом значения сверяем прогнозатором кабинета.</p>
  <div class="yline">Ozon Performance · {money(MAIN)} в месяц · старт в октябре</div>
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

    # 03 Что даёт 500 000 в месяц
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Потенциал бюджета · {money(MAIN)} в месяц</span></div>
  <h2>Что даёт тестовый бюджет<br>{money(MAIN)} на Ozon Performance</h2>
  <div class="stats">
    <div class="stat"><div class="n">{fmt(t['imps'] / 1e6 * 10) / 10 if False else f"{t['imps']/1e6:.1f}".replace('.', ',')} млн</div><div class="t">показов в месяц по трём сегментам аудита; за тест — {f"{t['imps']*MONTHS/1e6:.1f}".replace('.', ',')} млн</div></div>
    <div class="stat"><div class="n">~{fmt(t['reach'] / 1000)} тыс.</div><div class="t">человек охвата в месяц при частоте {FREQ} — около {t['reach']/cap*100:.0f}% суммарной ёмкости выбранных сегментов ({fmt(cap/1e6*10)/10 if False else f"{cap/1e6:.1f}".replace('.', ',')} млн)</div></div>
    <div class="stat"><div class="n">{fmt(t['clicks'])}</div><div class="t">переходов на sletat.ru в месяц, CPC {t['cpc_media']:.0f} ₽ по медиа</div></div>
    <div class="stat"><div class="n">10%</div><div class="t">сопровождение со второго месяца вместо 20% — расход выше 360 001 ₽ даёт скидку по шкале Церебро</div></div>
  </div>
  <p class="sub" style="margin-top:34px">Бюджет от 500 000 ₽ — верхняя ступень бенчмарка по приросту брендовых запросов из аудита: при широком охвате
  исследование Easy Commerce даёт +80–150% брендового поиска с эффектом на месяцы (до 100 000 ₽ — только +5–12%). На этом бюджете
  к трём сегментам аудита добавляем сегмент с высокой активностью от площадки и кастомный сегмент путешественников — пять связок
  вместо трёх, каждая со своей статистикой за 8 недель.</p>
  <div class="foot">Бюджет может быть меньше: сценарий «Если меньше» на следующем экране. Ниже 360 001 ₽ сопровождение считается по ставке 20% без скидки.</div>
  <div class="mark">Ц</div>
</section>""")

    # 04 Три сценария
    trs = ""
    for title, per, note in SCENARIOS:
        tt = totals(calc(per))
        best = ' style="color:var(--yellow)"' if per == MAIN else ""
        trs += f"""
      <tr><td{best}>{title}</td><td>{money(tt['media'])}</td><td>{money(tt['srk1'])} / {money(tt['srk2'])}</td><td><b style="color:var(--yellow)">{money(tt['total2'])}</b></td><td>{money(tt['test_total'])}</td><td>{fmt(tt['imps'])}</td><td>{fmt(tt['clicks'])}</td><td>{money(tt['cpc_media'])}</td><td>{money(tt['cpc_full'])}</td></tr>"""
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Три сценария · в месяц · Ozon Performance</span></div>
  <h2>Сколько вкладываем —<br>сколько получаем</h2>
  <div style="overflow-x:auto">
  <table class="bench compact">
    <tr><th>Сценарий</th><th>Медиа / мес</th><th>СРК 1-й / со 2-го</th><th>Итого / мес</th><th>За тест</th><th>Показы</th><th>Клики</th><th>CPC</th><th>CPC с СРК</th></tr>{trs}
  </table>
  </div>
  <div class="note"><b>Сопровождение — по шкале премирования Церебро</b> (экран «Ozon Performance · Условия» в аудите): при расходе
  200 001–360 000 ₽ — 20%; 360 001–1 099 999 ₽ — 20% в первый месяц и 10% со скидкой со второго при сохранении расхода.
  В сопровождение входят ведение кампаний, креативы, аналитический контур, замеры, недельная и месячная отчётность.
  Показы и клики — по CPM и CTR ваших сегментов из кабинета Ozon при равном делении бюджета между тремя сегментами.</div>
  <div class="foot">{"<br>".join(f"<b>{tl}</b> — {nt}." for tl, _, nt in SCENARIOS)}<br>Оценка охвата по сценариям — на экранах 03 и 05 (частота {FREQ}); точный охват отдаёт прогнозатор кабинета перед стартом.</div>
  <div class="mark">Ц</div>
</section>""")

    # 05 Разбивка по сегментам — оговорённый тест
    trs = "".join(f"""
      <tr><td>{r['seg']}</td><td>{money(r['budget'])}</td><td>{r['cpm']:.2f} ₽</td><td>{fmt(r['imps'])}</td><td>{r['ctr']*100:.2f}%</td><td>{fmt(r['clicks'])}</td><td>{r['cpc']:.2f} ₽</td><td>{fmt(r['uu'])}</td></tr>""" for r in main_rows)
    trs += f"""
      <tr><td>Итого Ozon Performance</td><td>{money(t['media'])}</td><td>{t['cpm']:.2f} ₽</td><td>{fmt(t['imps'])}</td><td>{t['ctr']*100:.2f}%</td><td>{fmt(t['clicks'])}</td><td>{t['cpc_media']:.2f} ₽</td><td></td></tr>"""
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Разбивка по сегментам · оговорённый тест · {money(MAIN)} в месяц</span></div>
  <h2>Что даёт каждый сегмент<br>за месяц</h2>
  <div style="overflow-x:auto">
  <table class="bench">
    <tr><th>Сегмент</th><th>Бюджет</th><th>CPM</th><th>Показы</th><th>CTR</th><th>Клики</th><th>CPC</th><th>Ёмкость: уникальных пользователей / мес</th></tr>{trs}
  </table>
  </div>
  <div class="foot">Ёмкость — размер сегмента в кабинете Ozon; даже {money(MAIN)} выкупают доли процента показов сегмента, есть куда масштабироваться.
  Четвёртый и пятый сегменты — аудитория с высокой пользовательской активностью и кастомный сегмент путешественников от площадки —
  получают бюджет из перераспределения после первых двух недель; их бенчмарки появятся после открытия кабинета.</div>
  <div class="mark">Ц</div>
</section>""")

    # 06 Заявки при разной конверсии
    cards = ""
    for cr in CR_LIST:
        leads = t["clicks"] * cr
        cards += f"""
    <div class="card"><div class="big">{fmt(leads)}</div><h3>заявок в месяц при конверсии {cr*100:g}%</h3>
      <p>Стоимость заявки: <b>{money(t['total2']/leads)}</b> с сопровождением со скидкой · {money(t['total1']/leads)} в первый месяц · {money(t['media']/leads)} по медиабюджету</p></div>"""
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Заявки · оговорённый тест · {fmt(t['clicks'])} кликов в месяц</span></div>
  <h2>Подставьте свою конверсию —<br>получите цену заявки</h2>
  <div class="cards">{cards}
  </div>
  <div class="note"><b>Конверсия клика в заявку — ваша цифра.</b> Для агрегатора туров заявка — подбор тура, звонок или заявка в офис сети.
  На созвоне подставим вашу конверсию с трафика Директа и таргета: расчёт в приложенном Excel пересчитывается автоматически.
  Медийный трафик в моменте конвертирует ниже перформанса и добирает post-view: увидел баннер, пришёл сам через две недели —
  этот слой считаем отдельно, при цикле покупки тура 1–6 месяцев без него до 99% эффекта не видно в отчётах по последнему клику.</div>
  <div class="mark">Ц</div>
</section>""")

    # 07 Календарь теста и замеры
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
    <div class="row"><div class="l">Замеры</div><div class="r">Search lift по Вордстату («слетать ру», «слетать туры» против контрольного «горящие туры») и post-view отчёт Ozon (заказы и заявки после показов, окно до 30 дней) — с первого дня. На бюджете {money(MAIN)} прирост брендового поиска — главный измеримый результат теста.</div></div>
  </div>
  <div class="mark">Ц</div>
</section>""")

    # 08 Условия и следующий шаг
    t_less = totals(calc(SCENARIOS[0][1]))
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Условия и следующий шаг</span></div>
  <h2>Что нужно, чтобы стартовать<br>в октябре</h2>
  <div class="rows">
    <div class="row"><div class="l">Бюджет</div><div class="r">Оговорённый тест — {money(MAIN)} медиа в месяц: {money(t['total1'])} в первый месяц с сопровождением 20%, {money(t['total2'])} со второго со скидкой 10%; за два месяца теста — {money(t['test_total'])}, {fmt(t['clicks']*MONTHS)} кликов. Если меньше: {money(SCENARIOS[0][1])} медиа — {money(t_less['total2'])} в месяц, {fmt(t_less['clicks'])} кликов.</div></div>
    <div class="row"><div class="l">Срок</div><div class="r">Контракт от шести месяцев, первые 8 недель — тестовый период. Медийный эффект читается на горизонте 6–8 недель, решения по бюджету — по кварталу.</div></div>
    <div class="row"><div class="l">Данные</div><div class="r">Ваша конверсия в заявку, доступ к Метрике, база туристов для собственного сегмента (хэш телефонов) — под look-a-like в кабинете Ozon.</div></div>
    <div class="row"><div class="l">Что дальше</div><div class="r">Urban Ads — по ответу площадки и результатам первого флайта, отдельным расчётом. Параллельно открываем кабинеты для инхаус-команды: Директ, VK Ads, Telegram Ads и ещё 10 систем в одном окне.</div></div>
  </div>
  <div class="yline">Следующий шаг — созвон на 20 минут: подставляем вашу конверсию, фиксируем бюджет и дату старта.<br>Церебро Таргет · направление Click Out · clickout.cerebrotarget.ru</div>
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
  table.bench td:first-child{{white-space:normal;min-width:200px}}
  table.compact th, table.compact td{{padding:10px 10px;font-size:clamp(12px,1vw,15px)}}
  table.compact td:first-child{{min-width:150px}}
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
                "CPM/CTR — бенчмарки ваших сегментов из кабинета Ozon. Сопровождение — по шкале Церебро (см. блок «Шкала» ниже). "
                "Urban Ads — второй шаг отдельным расчётом, WB Media недоступен (WB Тревел).")
    ws["A4"] = "Параметры"; ws["A4"].font = bold
    params = [("Медиабюджет Ozon Performance, ₽/мес", MAIN), ("Конверсия клика в заявку", 0.015),
              ("Средняя частота показа (для охвата)", FREQ), ("Срок теста, мес", MONTHS)]
    for i, (k, v) in enumerate(params, start=5):
        ws.cell(row=i, column=1, value=k)
        c = ws.cell(row=i, column=2, value=v); c.fill = yellow
    ws["B6"].number_format = "0.0%"
    # шкала СРК
    ws["D4"] = "Шкала сопровождения (СРК), доля от расхода"; ws["D4"].font = bold
    ws["D5"], ws["E5"], ws["F5"] = "Расход до, ₽", "1-й месяц", "со 2-го месяца (со скидкой)"
    scale = [(200000, None, None), (360000, 0.20, 0.20), (1099999, 0.20, 0.10), (1999999, 0.20, 0.08),
             (6999999, 0.20, 0.06), (9999999, 0.20, 0.04), (10**12, 0.20, 0.02)]
    ws["D6"], ws["E6"], ws["F6"] = 200000, "50 000 ₽", "50 000 ₽"
    for i, (lim, a, b) in enumerate(scale[1:], start=7):
        ws.cell(row=i, column=4, value=lim if lim < 10**12 else "свыше")
        ws.cell(row=i, column=5, value=a).number_format = "0%"
        ws.cell(row=i, column=6, value=b).number_format = "0%"
    srk1 = '=IF($B$5<=200000,50000,IF($B$5<=360000,$B$5*0.2,$B$5*0.2))'
    srk2 = ('=IF($B$5<=200000,50000,IF($B$5<=360000,$B$5*0.2,IF($B$5<=1099999,$B$5*0.1,'
            'IF($B$5<=1999999,$B$5*0.08,IF($B$5<=6999999,$B$5*0.06,IF($B$5<=9999999,$B$5*0.04,$B$5*0.02))))))')
    hdr = ["Сегмент", "Бюджет, ₽", "CPM, ₽", "CTR", "Показы", "Охват (оценка)", "Клики", "CPC, ₽", "Заявки", "CPL медиа, ₽", "Ёмкость: уникальных / мес"]
    r0 = 15
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
        ws.cell(row=r, column=6, value=f"=E{r}/$B$7")
        ws.cell(row=r, column=7, value=f"=E{r}*D{r}")
        ws.cell(row=r, column=8, value=f"=B{r}/G{r}")
        ws.cell(row=r, column=9, value=f"=G{r}*$B$6")
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
    lines = [
        ("Сопровождение, 1-й месяц (по шкале)", srk1),
        ("Сопровождение, со 2-го месяца (со скидкой)", srk2),
        ("Итого в месяц, 1-й месяц", f"=B{tr}+B{tr+1}"),
        ("Итого в месяц, со 2-го месяца", f"=B{tr}+B{tr+2}"),
        ("CPC с сопровождением (со 2-го мес), ₽", f"=B{tr+4}/G{tr}"),
        ("CPL с сопровождением (со 2-го мес), ₽", f"=B{tr+4}/I{tr}"),
        ("Итого за срок теста, ₽", f"=B{tr+3}+B{tr+4}*($B$8-1)"),
        ("Кликов за срок теста", f"=G{tr}*$B$8"),
        ("Заявок за срок теста", f"=I{tr}*$B$8"),
    ]
    for i, (k, f) in enumerate(lines, start=1):
        ws.cell(row=tr + i, column=1, value=k)
        ws.cell(row=tr + i, column=2, value=f)
    for row in ws.iter_rows(min_row=r0 + 1, max_row=tr + len(lines)):
        for c in row:
            if c.column in (2, 3, 5, 6, 7, 8, 9, 10, 11) and c.number_format == "General":
                c.number_format = "#,##0"
    ws.column_dimensions["A"].width = 46
    for col in range(2, 12):
        ws.column_dimensions[get_column_letter(col)].width = 16
    ws.column_dimensions["F"].width = 26
    ws["A" + str(tr + len(lines) + 2)] = ("Условия: контракт от 6 мес, тестовый период 8 недель. Оговорённый тестовый бюджет — 500 000 ₽/мес, может быть меньше "
                                          "(ниже 360 001 ₽ сопровождение 20% без скидки).")
    ws["A" + str(tr + len(lines) + 3)] = "Церебро Таргет · направление Click Out · clickout.cerebrotarget.ru"
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
        print(f"{title:18s} медиа {t['media']:>9,.0f} · СРК {t['srk1']:>7,.0f}/{t['srk2']:>7,.0f} · мес {t['total1']:>9,.0f}/{t['total2']:>9,.0f} · "
              f"тест {t['test_total']:>10,.0f} · показы {t['imps']:>10,.0f} · охват ~{t['reach']:>9,.0f} · клики {t['clicks']:>6,.0f} · "
              f"CPC {t['cpc_media']:.2f}/{t['cpc_full']:.2f} · заявки@1,5% {t['clicks']*0.015:.0f} · CPL {t['total2']/(t['clicks']*0.015):,.0f}")
