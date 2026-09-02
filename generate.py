#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор предварительных аудитов Cerebro Click Out.
Дизайн-код: omenikarch.github.io/Click_Out_Expo/presenter.html
Один клиент = один HTML-файл. Данные клиентов — clients_data.py.

Запуск: python3 generate.py
"""

from clients_data import CLIENTS, BENCH_AVG, LIFTS_COMMON, RESALE_COMMON

CSS = """
  :root{
    --bg:#000; --card:#272727; --card2:#111;
    --txt:#E7E6E6; --mute:#A5A5A5; --yellow:#FDD101; --white:#fff;
    --head:'Unbounded', Arial, sans-serif; --body:Arial, Helvetica, sans-serif;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{background:var(--bg);color:var(--txt);font-family:var(--body)}
  section{min-height:100vh;padding:6vh 7vw;display:flex;flex-direction:column;justify-content:center;position:relative;border-bottom:1px solid #1a1a1a}
  .kicker{display:flex;align-items:center;gap:14px;margin-bottom:26px}
  .kicker .bar{width:44px;height:8px;background:var(--yellow)}
  .kicker span{font-family:var(--head);font-weight:700;font-size:13px;letter-spacing:.08em;color:var(--yellow);text-transform:uppercase}
  .num{position:absolute;top:5vh;right:7vw;color:var(--mute);font-size:14px}
  h1{font-family:var(--head);font-weight:700;color:var(--white);font-size:clamp(28px,4.6vw,58px);line-height:1.1;margin-bottom:24px}
  h2{font-family:var(--head);font-weight:700;color:var(--white);font-size:clamp(23px,3.2vw,42px);line-height:1.14;margin-bottom:26px}
  .sub{font-size:clamp(16px,1.6vw,22px);line-height:1.45;max-width:70ch}
  .sub b{color:var(--white)}
  .yline{color:var(--yellow);font-family:var(--head);font-weight:700;font-size:clamp(16px,1.7vw,24px);margin-top:32px;line-height:1.3}
  .logo{display:flex;align-items:center;gap:16px;margin-bottom:44px}
  .logo .sign{width:56px;height:56px;background:var(--white);border:7px solid var(--yellow);display:flex;align-items:center;justify-content:center;font-family:var(--head);font-weight:700;color:#000;font-size:26px}
  .logo .nm{font-family:var(--head);font-weight:700;color:var(--white);font-size:18px;line-height:1.25}
  .mark{position:absolute;bottom:5vh;right:7vw;width:38px;height:38px;background:var(--white);border:5px solid var(--yellow);display:flex;align-items:center;justify-content:center;font-family:var(--head);font-weight:700;color:#000;font-size:17px;opacity:.9}
  .cards{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));margin-top:10px}
  .card{background:var(--card);border-radius:18px;padding:26px 28px}
  .card h3{font-family:var(--head);font-weight:700;color:var(--white);font-size:clamp(15px,1.4vw,20px);margin-bottom:12px}
  .card p{font-size:clamp(13px,1.15vw,17px);line-height:1.5;color:var(--txt)}
  .card .big{font-family:var(--head);font-weight:700;color:var(--yellow);font-size:clamp(26px,3.2vw,44px);line-height:1;margin-bottom:10px}
  .card .cap{color:var(--mute);font-size:13px;margin-top:12px;line-height:1.4}
  .stats{display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));margin-top:14px}
  .stat .n{font-family:var(--head);font-weight:700;color:var(--yellow);font-size:clamp(30px,4vw,56px);line-height:1}
  .stat .t{color:var(--txt);font-size:clamp(13px,1.15vw,17px);margin-top:10px;line-height:1.4}
  .rows{margin-top:12px;max-width:1150px}
  .row{display:grid;grid-template-columns:minmax(150px,240px) 1fr;gap:26px;padding:20px 0;border-top:1px solid #232323;align-items:start}
  .row .l{font-family:var(--head);font-weight:700;color:var(--yellow);font-size:clamp(14px,1.3vw,19px)}
  .row .r{font-size:clamp(14px,1.2vw,18px);line-height:1.5}
  .foot{margin-top:34px;color:var(--mute);font-size:clamp(12px,1vw,15px);line-height:1.5;max-width:80ch}
  .price{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin-top:10px}
  .p{background:var(--card2);border:1px solid #262626;border-radius:18px;padding:26px 28px;position:relative}
  .p.best{border-color:var(--yellow)}
  .p .tag{position:absolute;top:-13px;left:26px;background:var(--yellow);color:#000;font-family:var(--head);font-weight:700;font-size:11px;letter-spacing:.06em;text-transform:uppercase;padding:5px 12px;border-radius:100px}
  .p h3{font-family:var(--head);font-weight:700;color:var(--white);font-size:clamp(15px,1.4vw,20px);margin-bottom:16px}
  .p .was{color:var(--mute);text-decoration:line-through;font-size:15px}
  .p .now{font-family:var(--head);font-weight:700;color:var(--yellow);font-size:clamp(24px,2.8vw,38px);line-height:1.1;margin:6px 0 4px}
  .p .per{color:var(--mute);font-size:13px}
  .p ul{list-style:none;margin-top:16px}
  .p li{font-size:clamp(13px,1.1vw,16px);line-height:1.5;padding-left:18px;position:relative;margin-bottom:8px}
  .p li:before{content:"";position:absolute;left:0;top:9px;width:7px;height:7px;background:var(--yellow)}
  ul.seg{list-style:none;margin-top:6px}
  ul.seg li{font-size:clamp(14px,1.2vw,18px);line-height:1.55;padding-left:20px;position:relative;margin-bottom:9px}
  ul.seg li:before{content:"";position:absolute;left:0;top:10px;width:7px;height:7px;background:var(--yellow)}
  ul.seg li b{color:var(--white)}
  .grid2{display:grid;gap:34px;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));margin-top:10px}
  .colh{font-family:var(--head);font-weight:700;color:var(--white);font-size:clamp(15px,1.5vw,21px);margin-bottom:14px}
  table.bench{border-collapse:collapse;margin-top:14px;width:100%;max-width:1100px}
  table.bench th{font-family:var(--head);font-weight:700;color:var(--yellow);font-size:clamp(12px,1.05vw,15px);text-align:left;padding:12px 16px;border-bottom:2px solid var(--yellow);text-transform:uppercase;letter-spacing:.05em}
  table.bench td{font-size:clamp(13px,1.15vw,17px);padding:12px 16px;border-bottom:1px solid #232323;line-height:1.45}
  table.bench td:first-child{font-family:var(--head);font-weight:700;color:var(--white)}
  table.bench .tbd{color:var(--mute)}
  .pill{display:inline-block;background:#151515;border:1px solid #333;border-radius:100px;color:var(--txt);font-size:clamp(12px,1.05vw,15px);padding:8px 16px;margin:0 8px 10px 0;line-height:1.4}
  .pill b{color:var(--yellow);font-family:var(--head);font-weight:700}
  .note{display:inline-block;background:#0d0d0d;border-left:5px solid var(--yellow);border-radius:0 12px 12px 0;padding:16px 20px;margin-top:24px;font-size:clamp(13px,1.1vw,16px);line-height:1.55;color:#cfcfcf;max-width:80ch}
  .note b{color:var(--white)}
  @media screen and (max-width:1100px){
    .price{grid-template-columns:1fr}
    .cards{grid-template-columns:1fr}
    .row{grid-template-columns:1fr;gap:8px}
    .grid2{grid-template-columns:1fr}
    section{padding:7vh 8vw}
  }
  @media print{
    @page{size:1600px 1500px;margin:0}
    *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
    html,body{background:#000}
    section{min-height:auto;height:auto;page-break-inside:avoid;page-break-after:always;padding:70px 90px;border-bottom:none;justify-content:flex-start}
    .num{top:60px;right:90px}
    .mark{bottom:60px;right:90px}
  }
"""

def seg_list(items):
    return '<ul class="seg">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def pills(items):
    return "".join(f'<div class="pill">{i}</div>' for i in items)

def load_benchmarks():
    """benchmarks.csv (разделитель ;) → {(client_key, source, segment): {метрика: значение}}.
    Пустые ячейки = ещё не собрано."""
    import csv, pathlib
    path = pathlib.Path(__file__).parent / "benchmarks.csv"
    data = {}
    if not path.exists():
        return data
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            key = (row["client_key"].strip(), row["source"].strip(), row["segment"].strip())
            data[key] = {m: (row.get(m) or "").strip() for m in
                         ("охват", "показы", "клики", "cpm", "ctr", "cpc")}
    return data


BENCHMARKS = load_benchmarks()
_METRIC_ORDER = ("охват", "показы", "клики", "cpm", "ctr", "cpc")


def bench_table(client_key, source_key, niche_rows):
    """Таблица бенчмарков: средние Click Out + строки под нишу.
    Значения берутся из benchmarks.csv; пустая ячейка → «после сбора»."""
    avg = BENCH_AVG[source_key]
    rows = f"""
      <tr><td>Средние Click Out (клиенты СРК)</td><td>—</td><td>—</td><td>—</td><td>{avg['cpm']}</td><td>{avg['ctr']}</td><td>{avg['cpc']}</td></tr>"""
    filled_any = False
    for r in niche_rows:
        vals = BENCHMARKS.get((client_key, source_key, r), {})
        cells = ""
        for m in _METRIC_ORDER:
            v = vals.get(m, "")
            if v:
                filled_any = True
                cells += f"<td>{v}</td>"
            else:
                cells += '<td class="tbd">после сбора</td>'
        rows += f"""
      <tr><td>{r}</td>{cells}</tr>"""
    note = ("<b>Часть бенчмарков уже снята из кабинетов площадки</b> — оставшиеся ячейки будут "
            "добавлены в финальную версию аудита." if filled_any else
            "<b>Бенчмарки по выбранным сегментам собираются в рекламных кабинетах площадки</b> — "
            "охват, показы, клики, CPM, CTR, CPC по каждому сегменту будут добавлены в финальную версию аудита.")
    return f"""
    <table class="bench">
      <tr><th>Сегмент / формат</th><th>Охват</th><th>Показы</th><th>Клики</th><th>CPM</th><th>CTR</th><th>CPC</th></tr>{rows}
    </table>
    <div class="note">{note}</div>"""


def build(client_key, c):
    n = [0]
    def num():
        n[0] += 1
        return f"{n[0]:02d}"

    s = []

    # ---------- 01 Титул ----------
    num()
    s.append(f"""
<section>
  <div class="logo"><div class="sign">Ц</div><div class="nm">Церебро<br>Таргет</div></div>
  <div class="kicker"><div class="bar"></div><span>Предварительный аудит · Направление Click Out</span></div>
  <h1>{c['title_h1']}</h1>
  <p class="sub">{c['title_sub']}</p>
  <div class="yline">Ozon Performance · Яндекс Urban Ads · WB Media</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- 02 Резюме встречи ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Что мы услышали на встрече</span></div>
  <h2>Точка старта: как это устроено<br>у вас сейчас</h2>
  <div class="rows">{"".join(f'<div class="row"><div class="l">{l}</div><div class="r">{r}</div></div>' for l, r in c['meeting_rows'])}
  </div>
  <div class="foot">Источник: разговор на выставке {c['expo']}. Формулировки сохранены близко к сказанному — если что-то передано неточно, поправим на созвоне.</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- 03 О компании клиента / ниша в цифрах ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Ваша ниша в цифрах</span></div>
  <h2>{c['niche_h2']}</h2>
  <div class="stats">{"".join(f'<div class="stat"><div class="n">{v}</div><div class="t">{t}</div></div>' for v, t in c['niche_stats'])}
  </div>
  <p class="sub" style="margin-top:34px">{c['niche_text']}</p>
  <div class="foot">{c['niche_sources']}</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- 04 Согласование проекта ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Согласование проекта</span></div>
  <h2>Запуск с Ozon Performance,<br>Яндекс Urban Ads и WB Media</h2>
  <p class="sub">Для запуска проекта с рекламными платформами Ozon Performance, Яндекс Urban Ads и
  Wildberries Click Out необходимо предварительное согласование площадок. При положительном решении
  создание кабинетов занимает <b>3–5 рабочих дней</b>.</p>
  <div class="cards" style="margin-top:26px">
    <div class="card"><h3>Кабинеты для внешнего трафика</h3>
      <p>В Ozon, Яндекс Urban Ads и Wildberries есть рекламные кабинеты, с которых можно вести трафик
      внешним рекламодателям — на ваш сайт, а не на карточку товара.</p></div>
    <div class="card"><h3>Аудитория в режиме покупки</h3>
      <p>Люди приходят на маркетплейс с уже сформированным желанием купить. Услуги в каталогах площадок
      не продаются — за эту аудиторию с вами почти никто не конкурирует.</p></div>
    <div class="card"><h3>Прогноз по вашему проекту</h3>
      <p>{c['approval_forecast']}</p></div>
  </div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Ozon: таргетинги ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Ozon Performance · Таргетинги</span></div>
  <h2>Ozon Performance: кого можем<br>выбирать для показа</h2>
  <div class="rows">
    <div class="row"><div class="l">Авторизация</div><div class="r">Все покупатели · Неавторизованные · Авторизованные</div></div>
    <div class="row"><div class="l">Демография</div><div class="r">Пол, возраст</div></div>
    <div class="row"><div class="l">Регион</div><div class="r">Область, город</div></div>
    <div class="row"><div class="l">Сегменты</div><div class="r">Покупают в категории · Смотрят категорию · Активный Premium · Клиент B2B · Собственный сегмент из номеров телефонов (хэш)</div></div>
  </div>
  <div class="foot">Форматы: видеобаннер, баннер на главной и в поиске, размещение в карточке товара, экран «заказ выполнен». 65 млн активных покупателей за 2025 год, в среднем 38 заказов на человека.</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Ozon: сегменты ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Ozon Performance · Сегменты</span></div>
  <h2>Сегменты под {c['name_short_accus']}</h2>
  <p class="sub">Сегменты собраны из категорий каталога Ozon 1-го и 2-го уровня, которые формируют
  ваших потенциальных клиентов:</p>
  <div class="grid2">
    <div><div class="colh">Основные сегменты</div>{seg_list(c['ozon_segments'])}</div>
    <div><div class="colh">Дополнительные фильтры</div>{seg_list(c['ozon_filters'])}</div>
  </div>
  <div class="note">{c['ozon_note']}</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Ozon: бенчмарки ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Ozon Performance · Бенчмарки</span></div>
  <h2>Бенчмарки для предварительного расчёта</h2>
  {bench_table(client_key, 'ozon', c['ozon_bench_rows'])}
  <div class="mark">Ц</div>
</section>""")

    # ---------- Urban: форматы ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Яндекс Urban Ads · Форматы</span></div>
  <h2>Яндекс Urban Ads: форматы<br>и площадки показа</h2>
  <div class="cards">
    <div class="card"><div class="big">0,64%</div><h3>Видеобаннер</h3>
      <p>ср. CPM 641 ₽ · ср. CPC 100 ₽. Главная страница Маркета, десктоп и мобайл.</p></div>
    <div class="card"><div class="big">0,41%</div><h3>Баннер-растяжка</h3>
      <p>ср. CPM 182 ₽ · ср. CPC 44 ₽. Все страницы Маркета, кроме корзины и оплаты.</p></div>
    <div class="card"><div class="big">0,35%</div><h3>Горизонтальный баннер</h3>
      <p>ср. CPM 342 ₽ · ср. CPC 98 ₽. Маркет, Go, Деливери, Еда, Лавка, Кинопоиск — главная, лента, карточка товара.</p></div>
    <div class="card"><div class="big">0,33%</div><h3>Вертикальный баннер</h3>
      <p>ср. CPM 96 ₽ · ср. CPC 29 ₽. Лента товаров на главной Маркета, карточка товара на десктопе.</p></div>
  </div>
  <div class="foot">До 94 млн аудитории в месяц по сервисам Яндекса: Маркет, Еда, Лавка, Go. 60% — доход средний и выше.
  Оплата по CPM, минимальная ставка 50 ₽. Таргетинги: гео, интересы и покупки на Маркете, соцдем, доход,
  подписка Плюс, CRM-ретаргетинг по вашей базе.</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Urban: сегменты ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Яндекс Urban Ads · Сегменты</span></div>
  <h2>Сегменты под {c['name_short_accus']}</h2>
  <p class="sub">Сегменты «интересуются категорией» и «покупали в категории» по каталогу Яндекс Маркета
  1-го и 2-го уровня плюс look-a-like и ретаргетинг:</p>
  <div class="grid2">
    <div><div class="colh">Основные сегменты</div>{seg_list(c['ym_segments'])}</div>
    <div><div class="colh">Дополнительные фильтры</div>{seg_list(c['ym_filters'])}</div>
  </div>
  <div class="note">{c['ym_note']}</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Urban: бенчмарки ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Яндекс Urban Ads · Бенчмарки</span></div>
  <h2>Бенчмарки для предварительного расчёта</h2>
  {bench_table(client_key, 'urban', c['ym_bench_rows'])}
  <div class="mark">Ц</div>
</section>""")

    # ---------- WB: сегменты ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>WB Media · Сегменты</span></div>
  <h2>Сегменты под {c['name_short_accus']}</h2>
  <p class="sub">79 млн посетителей, из них 49 млн покупателей; 78% — женщины 25–44. Поведенческие
  сегменты DMP на основе реальных покупок, по каталогу WB 1-го и 2-го уровня:</p>
  <div class="grid2">
    <div><div class="colh">Основные сегменты</div>{seg_list(c['wb_segments'])}</div>
    <div><div class="colh">Дополнительные фильтры</div>{seg_list(c['wb_filters'])}</div>
  </div>
  <div class="note">{c['wb_note']}</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- WB: бенчмарки ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>WB Media · Бенчмарки</span></div>
  <h2>Бенчмарки для предварительного расчёта</h2>
  {bench_table(client_key, 'wb', c['wb_bench_rows'])}
  <div class="mark">Ц</div>
</section>""")

    # ---------- Сравнение источников ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Сравнение источников</span></div>
  <h2>Средние показатели клиентов СРК<br>в направлении Click Out</h2>
  <div class="cards">
    <div class="card"><div class="big">{BENCH_AVG['ozon']['ctr']}</div><h3>Ozon Performance</h3>
      <p>CPC — {BENCH_AVG['ozon']['cpc']} · CPM — {BENCH_AVG['ozon']['cpm']}</p></div>
    <div class="card"><div class="big">{BENCH_AVG['urban']['ctr']}</div><h3>Яндекс Urban Ads</h3>
      <p>CPC — {BENCH_AVG['urban']['cpc']} · CPM — {BENCH_AVG['urban']['cpm']}</p></div>
    <div class="card"><div class="big">{BENCH_AVG['wb']['ctr']}</div><h3>WB Media</h3>
      <p>CPC — {BENCH_AVG['wb']['cpc']} · CPM — {BENCH_AVG['wb']['cpm']}</p></div>
  </div>
  <div class="foot">Аудитории площадок не складываются: это три разные среды, и человек может быть сразу в нескольких.
  Комплекс из трёх источников нужен не ради суммы охвата, а ради частоты касаний и разных сценариев показа.
  Данные основаны на реальных кампаниях клиентов СРК; показатели по вашей нише будут уточнены после сбора бенчмарков по выбранным сегментам.</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Замеры (лифты) — общий экран ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Чем отличаемся</span></div>
  <h2>Мы доказываем, что спрос<br>создала реклама</h2>
  <p class="sub">Обычный отчёт показывает показы, клики и заявки по последнему клику. Он не отвечает
  на главный вопрос: <b>сколько обращений пришло бы и без рекламы.</b> Мы отвечаем — четырьмя замерами.</p>
  <div class="rows">
    <div class="row"><div class="l">Search lift</div><div class="r">{LIFTS_COMMON['search']}</div></div>
    <div class="row"><div class="l">Brand lift</div><div class="r">{LIFTS_COMMON['brand']}</div></div>
    <div class="row"><div class="l">Sales lift</div><div class="r">{LIFTS_COMMON['sales']}</div></div>
    <div class="row"><div class="l">Post-view</div><div class="r">{LIFTS_COMMON['postview']}</div></div>
  </div>
  <div class="foot">Часть замеров — наш собственный контур, доступен на любом бюджете. Исследования площадок
  (Brand Lift Study, Sales Lift, post-view отчёт) подключаются от своих порогов и работают как подтверждение от третьей стороны.</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Замеры — данные под нишу ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Замеры · Что говорят данные</span></div>
  <h2>Что показывают исследования<br>в вашей нише</h2>
  <div class="rows">{"".join(f'<div class="row"><div class="l">{l}</div><div class="r">{r}</div></div>' for l, r in c['lift_rows'])}
  </div>
  <div class="foot">{c['lift_foot']}</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- План замеров для клиента ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Замеры · План для вас</span></div>
  <h2>Какие замеры поставим<br>на вашем проекте</h2>
  <div class="cards">{"".join(f'<div class="card"><h3>{h}</h3><p>{p}</p></div>' for h, p in c['lift_plan'])}
  </div>
  <div class="yline">Замер «до» снимаем в рамках бесплатного аудита — ещё до подписания договора</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Рессейлинг: 13 кабинетов ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Рессейлинг · Другие площадки</span></div>
  <h2>Тринадцать рекламных кабинетов<br>в одном окне</h2>
  <p class="sub">Через Церебро открываются кабинеты всех ключевых рекламных систем РФ — софт позволяет
  создавать кабинеты, выдавать доступы и распределять деньги между ними в несколько кликов.</p>
  <div class="yline" style="margin-top:26px;font-size:clamp(14px,1.35vw,19px);line-height:1.6">
  VK Ads · VK AdBlogger · Telega.in · Яндекс Директ · Telegram Ads · Яндекс Бизнес · Авито Реклама ·
  Яндекс ПромоСтраницы · SberAds · Bidfox · Hybrid · Яндекс Навигатор · Ozon Performance</div>
  <div class="cards" style="margin-top:30px">{"".join(f'<div class="card"><h3>{h}</h3><p>{p}</p></div>' for h, p in RESALE_COMMON)}
  </div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Рессейлинг: под нишу клиента ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Рессейлинг · Каналы под вашу нишу</span></div>
  <h2>{c['resale_h2']}</h2>
  <div class="rows">{"".join(f'<div class="row"><div class="l">{l}</div><div class="r">{r}</div></div>' for l, r in c['resale_rows'])}
  </div>
  <div class="foot">{c['resale_foot']}</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Сайт / готовность к трафику ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Готовность к приёму трафика</span></div>
  <h2>Сайт и аналитика:<br>что проверить до старта</h2>
  <div class="rows">{"".join(f'<div class="row"><div class="l">{l}</div><div class="r">{r}</div></div>' for l, r in c['site_rows'])}
  </div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Условия ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Условия работы</span></div>
  <h2>Сопровождение: чем больше<br>источников, тем ниже цена</h2>
  <div class="price">
    <div class="p">
      <h3>Один источник</h3>
      <div class="now">50 000 ₽</div>
      <div class="per">в месяц за сопровождение</div>
      <ul><li>Ozon, Urban Ads или WB на выбор</li><li>Полный аналитический контур</li><li>Недельная и месячная отчётность</li></ul>
    </div>
    <div class="p">
      <h3>Два источника</h3>
      <div class="was">100 000 ₽</div>
      <div class="now">80 000 ₽</div>
      <div class="per">в месяц · скидка 20% на тестовый период</div>
      <ul><li>Любые два из трёх</li><li>Сравнение источников на ваших данных</li><li>Перераспределение бюджета между ними</li></ul>
    </div>
    <div class="p best">
      <div class="tag">Максимум охвата</div>
      <h3>Три источника</h3>
      <div class="was">150 000 ₽</div>
      <div class="now">90 000 ₽</div>
      <div class="per">в месяц · скидка 40% на тестовый период</div>
      <ul><li>Ozon + Urban Ads + WB</li><li>Разные среды и сценарии показа</li><li>Частота касаний, которую не даёт один канал</li></ul>
    </div>
  </div>
  <div class="rows" style="margin-top:26px">
    <div class="row"><div class="l">Рекламный бюджет</div><div class="r">От 120 000 ₽ в месяц на каждый источник — порог, ниже которого площадка не набирает объём для выводов. Минимальный бюджет на тест источника — 50 000 ₽.</div></div>
    <div class="row"><div class="l">Срок контракта</div><div class="r">От шести месяцев. Медийный эффект читается на горизонте 6–8 недель, решения по бюджету принимаются по кварталу.</div></div>
    <div class="row"><div class="l">Что входит</div><div class="r">Ведение кампаний, креативы, аналитический контур, замеры, отчётность и документ-решение в конце цикла.</div></div>
  </div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Рекомендации ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Рекомендации и выводы</span></div>
  <h2>Рекомендации по запуску</h2>
  {seg_list(c['recommendations'])}
  <div class="foot">Все данные основаны на реальных бенчмарках Ozon Performance, Urban Ads и WB Media.
  Показатели по вашей нише будут уточнены после сбора бенчмарков по выбранным сегментам.</div>
  <div class="mark">Ц</div>
</section>""")

    # ---------- Следующий шаг ----------
    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Следующий шаг</span></div>
  <h1>{c['next_h1']}</h1>
  <p class="sub">{c['next_sub']}</p>
  <div class="yline">Церебро Таргет · направление Click Out<br>clickout.cerebrotarget.ru</div>
  <div class="mark">Ц</div>
</section>""")

    body = "".join(s)
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{c['page_title']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""


def build_index():
    items = "".join(
        f'<div class="card"><h3><a href="{c["file"]}" style="color:var(--yellow);text-decoration:none">{c["name_ru"]}</a></h3>'
        f'<p>{c["niche_ru"]} · {c["site"]}</p></div>'
        for c in CLIENTS.values()
    )
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Предварительные аудиты · Cerebro Click Out</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<section>
  <div class="logo"><div class="sign">Ц</div><div class="nm">Церебро<br>Таргет</div></div>
  <div class="kicker"><div class="bar"></div><span>Предварительные аудиты · ОТДЫХ Leisure 02–04.09</span></div>
  <h1>Аудиты по заявкам<br>с выставки</h1>
  <div class="cards" style="margin-top:20px">{items}</div>
  <div class="mark">Ц</div>
</section>
</body>
</html>
"""


if __name__ == "__main__":
    import pathlib
    root = pathlib.Path(__file__).parent
    for key, c in CLIENTS.items():
        html = build(key, c)
        (root / c["file"]).write_text(html, encoding="utf-8")
        print(f"OK {c['file']} ({len(html)} bytes)")
    (root / "index.html").write_text(build_index(), encoding="utf-8")
    print("OK index.html")
