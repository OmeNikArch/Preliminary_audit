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
Сопровождение — по шкале премирования Церебро (экран «Ozon Performance · Условия» в аудитах).
Формат — по просьбе клиента простой текст без таблиц, 4 экрана. Выход: sletat-ru-mediaplan.html (+ sletat-ru-mediaplan.xlsx для внутреннего расчёта).

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
# Ступени оборота для экрана мотивации: (расход в месяц, подпись)
TIERS = [
    (350_000, "Сокращённый тест"),
    (500_000, "Оговорённый тест"),
    (750_000, "Расширение после теста"),
    (1_100_000, "Рост: вторая ступень шкалы"),
    (2_000_000, "Федеральный флайт"),
    (7_000_000, "Сеть 350+ офисов, все источники"),
    (10_000_000, "Верхняя ступень шкалы"),
]


def srk(spend):
    """Сопровождение по шкале премирования Церебро: (первый месяц, со скидкой со второго месяца)."""
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

    t = totals(calc(MAIN))
    less = totals(calc(350_000))
    s1m, s2m = srk(MAIN)
    tiers = {spend: srk(spend)[1] / spend * 100 for spend in (1_100_000, 2_000_000, 10_000_000)}
    mln = lambda v: f"{v/1e6:.1f}".replace(".", ",") + " млн"

    # 01 Титул
    nxt()
    s.append(f"""
<section>
  <div class="logo"><div class="sign">Ц</div><div class="nm">Церебро<br>Таргет</div></div>
  <div class="kicker"><div class="bar"></div><span>Медиаплан теста · IV квартал 2026 · Направление Click Out</span></div>
  <h1>Медиаплан теста:<br>Слетать.ру · Ozon Performance</h1>
  <p class="sub">Как договорились: первый флайт — только Ozon Performance, площадка уже предварительно одобрила размещение.
  Тестовый бюджет — <b>{money(MAIN)} в месяц</b>, старт в октябре, в пик раннего бронирования лета.
  Цифры ниже — по бенчмаркам ваших сегментов из рекламного кабинета Ozon; перед стартом сверим их прогнозатором кабинета.</p>
  <div class="yline">Ozon Performance · {money(MAIN)} в месяц · старт в октябре</div>
  <div class="mark">Ц</div>
</section>""")

    # 02 Что получаете
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Что получаете за {money(MAIN)} в месяц</span></div>
  <h2>{mln(t['imps'])} показов, {fmt(t['clicks'])} переходов<br>на sletat.ru — каждый месяц</h2>
  <div class="stats">
    <div class="stat"><div class="n">{mln(t['imps'])}</div><div class="t">показов в месяц</div></div>
    <div class="stat"><div class="n">~{mln(t['reach'])}</div><div class="t">человек охвата при частоте {FREQ} показа</div></div>
    <div class="stat"><div class="n">{fmt(t['clicks'])}</div><div class="t">переходов на сайт в месяц</div></div>
    <div class="stat"><div class="n">{t['cpc_media']:.0f} ₽</div><div class="t">стоимость перехода</div></div>
  </div>
  <p class="sub" style="margin-top:34px">Показываем баннеры трём аудиториям из аудита: пользователям Ozon Travel и покупателям товаров в дорогу,
  покупателям пляжной одежды и солнцезащиты, широкой аудитории 25–55 в городах вылета. Площадка добавит к ним свой сегмент
  с высокой активностью и соберёт под бюджет кастомный сегмент путешественников. Слабые сегменты отключаем через две недели,
  бюджет переводим в сильные.</p>
  <p class="sub" style="margin-top:18px"><b>Сколько стоит.</b> {money(MAIN)} — рекламный бюджет в кабинете Ozon. Сопровождение — {money(s1m)} в первый месяц
  и {money(s2m)} со второго. Итого {money(t['total1'])} в первый месяц, {money(t['total2'])} дальше; за два месяца теста — {money(t['test_total'])}.
  Если бюджет будет меньше, например 350 000 ₽: {fmt(less['clicks'])} переходов в месяц, сопровождение {money(less['srk2'])}, итого {money(less['total2'])}.</p>
  <div class="foot">Сколько из переходов станет заявками — зависит от вашей конверсии, подставим её на созвоне. При конверсии 1,5% это около
  {fmt(t['clicks']*0.015)} заявок в месяц по {money(t['total2']/(t['clicks']*0.015))}. Это медийный трафик: часть людей приходит позже сама,
  без клика — этот слой Ozon показывает отдельным отчётом, окно до 30 дней.</div>
  <div class="mark">Ц</div>
</section>""")

    # 03 Сопровождение дешевеет с оборотом
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Сопровождение · скидка от рекламного оборота</span></div>
  <h2>Чем больше оборот —<br>тем дешевле сопровождение</h2>
  <p class="sub">Сопровождение считается от расхода в кабинете. Базовая ставка — 20%, она действует в первый месяц.
  Со второго месяца включается скидка по обороту: на вашем тестовом бюджете {money(MAIN)} это <b>10%</b> — {money(s2m)} вместо {money(s1m)},
  экономия {money(s1m - s2m)} каждый месяц.</p>
  <p class="sub" style="margin-top:18px">Дальше ставка снижается ступенями: от 1,1 млн ₽ в месяц — <b>{tiers[1_100_000]:.0f}%</b>, от 2 млн ₽ — <b>{tiers[2_000_000]:.0f}%</b>,
  от 10 млн ₽ — <b>{tiers[10_000_000]:.0f}%</b>. Чем больше вы откручиваете, тем меньшую долю забирает наша работа.</p>
  <div class="foot">Скидка начисляется на следующий месяц, если в текущем выдержан порог ступени. Оплата сопровождения — раз в месяц.
  Расход считается без НДС, стоимость сопровождения — с НДС. Полная шкала — на экране «Ozon Performance · Условия» в аудите.</div>
  <div class="mark">Ц</div>
</section>""")

    # 04 Как пойдёт тест и следующий шаг
    s.append(f"""
<section>
  <div class="num">{nxt()}</div>
  <div class="kicker"><div class="bar"></div><span>Как пойдёт тест · следующий шаг</span></div>
  <h2>Восемь недель<br>с октября</h2>
  <p class="sub">Кабинет Ozon открывается за 3–5 рабочих дней, запуск кампании — от 7 дней. До старта делаем посадочные под сегменты
  («туры к морю», «семейные туры»), ставим пиксели площадки и снимаем замер «до» по Вордстату — бесплатно, до договора.
  Первые две недели — тест сегментов, с третьей по шестую — отключаем слабые и перераспределяем бюджет, седьмая и восьмая —
  наращиваем лучшие связки. В конце — документ-решение: что продолжаем, что останавливаем, по вашим критериям.</p>
  <p class="sub" style="margin-top:18px">Что измеряем: прирост запросов «слетать ру» в Вордстате против контрольного «горящие туры»
  и отчёт Ozon по заявкам после показов. Urban Ads подключаем вторым шагом после ответа площадки и результатов Ozon, отдельным расчётом.
  WB для тревел-брендов закрыт — у Wildberries свой WB Тревел.</p>
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
<style>{CSS}</style>
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
    # шкала сопровождения
    ws["D4"] = "Шкала сопровождения, доля от расхода"; ws["D4"].font = bold
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
    # лист «Мотивация»: скидка на сопровождение от оборота
    ws2 = wb.create_sheet("Мотивация")
    ws2["A1"] = "Скидка на сопровождение от рекламного оборота · шкала Церебро"; ws2["A1"].font = Font(bold=True, size=14)
    ws2["A2"] = "Жёлтая колонка — расход в месяц, меняйте: ставки и суммы пересчитаются. Первый месяц — 20%, со второго — ставка ступени при соблюдении её порога в предыдущем месяце."
    hdr2 = ["Расход в месяц, ₽", "Сценарий", "Ставка без скидки", "Ставка со скидкой", "Сопровождение без скидки, ₽", "Со скидкой, ₽", "Экономия в месяц, ₽", "Экономия за 11 мес, ₽"]
    for j, h in enumerate(hdr2, start=1):
        ws2.cell(row=4, column=j, value=h).font = bold
    f1 = "=IF(A{r}<=200000,50000,A{r}*0.2)"
    f2 = ("=IF(A{r}<=200000,50000,IF(A{r}<=360000,A{r}*0.2,IF(A{r}<=1099999,A{r}*0.1,"
          "IF(A{r}<=1999999,A{r}*0.08,IF(A{r}<=6999999,A{r}*0.06,IF(A{r}<=9999999,A{r}*0.04,A{r}*0.02))))))")
    for i, (spend, label) in enumerate(TIERS, start=5):
        c = ws2.cell(row=i, column=1, value=spend); c.fill = yellow; c.number_format = "#,##0"
        ws2.cell(row=i, column=2, value=label)
        ws2.cell(row=i, column=3, value=f"=E{i}/A{i}").number_format = "0%"
        ws2.cell(row=i, column=4, value=f"=F{i}/A{i}").number_format = "0%"
        ws2.cell(row=i, column=5, value=f1.format(r=i)).number_format = "#,##0"
        ws2.cell(row=i, column=6, value=f2.format(r=i)).number_format = "#,##0"
        ws2.cell(row=i, column=7, value=f"=E{i}-F{i}").number_format = "#,##0"
        ws2.cell(row=i, column=8, value=f"=G{i}*11").number_format = "#,##0"
    ws2["A" + str(5 + len(TIERS) + 1)] = "Расход указан без НДС, стоимость сопровождения — с НДС. При сопровождении бонусные рубли не начисляются — действует только скидка."
    ws2.column_dimensions["A"].width = 20; ws2.column_dimensions["B"].width = 34
    for col in range(3, 9):
        ws2.column_dimensions[get_column_letter(col)].width = 24
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
        print(f"{title:18s} медиа {t['media']:>9,.0f} · сопровождение {t['srk1']:>7,.0f}/{t['srk2']:>7,.0f} · мес {t['total1']:>9,.0f}/{t['total2']:>9,.0f} · "
              f"тест {t['test_total']:>10,.0f} · показы {t['imps']:>10,.0f} · охват ~{t['reach']:>9,.0f} · клики {t['clicks']:>6,.0f} · "
              f"CPC {t['cpc_media']:.2f}/{t['cpc_full']:.2f} · заявки@1,5% {t['clicks']*0.015:.0f} · CPL {t['total2']/(t['clicks']*0.015):,.0f}")
