# Preliminary_audit — предварительные аудиты Cerebro Click Out

Аудиты по заявкам с выставки **ОТДЫХ Leisure · 02–04.09.2026**.
Дизайн-код: [presenter.html](https://omenikarch.github.io/Click_Out_Expo/presenter.html) (Unbounded, чёрный/жёлтый #FDD101).

## Клиенты

| Файл | Клиент | Ниша |
|---|---|---|
| [belarus-tourist.html](belarus-tourist.html) | Беларус турист (kurort.by) | Санатории Беларуси |
| [sletat-ru.html](sletat-ru.html) | Слетать.ру | Агрегатор туров |
| [uzbekistan-airways.html](uzbekistan-airways.html) | Uzbekistan Airways | Авиакомпания |
| [baggage.html](baggage.html) | Баггаж (baggage.ru) | Доставка багажа |
| [sanya-phoenix.html](sanya-phoenix.html) | Sanya Phoenix | Туры на Хайнань |
| [rst-union.html](rst-union.html) | Российский союз туриндустрии | Отраслевой союз |
| [travelmobile24.html](travelmobile24.html) | Travelmobile24 | Тревел-eSIM |

`index.html` — оглавление со ссылками на все аудиты.

## Как обновлять

Контент клиентов — в `clients_data.py` (сегменты, цифры ниш, lift-данные, рессейлинг).
После правки:

```bash
python3 generate.py
```

— файлы перегенерируются. Бенчмарки по сегментам (охват, показы, клики, CPM, CTR, CPC)
помечены в таблицах как «после сбора»: после снятия из кабинетов площадок внести их
в `clients_data.py` нельзя напрямую — они подставляются строками `*_bench_rows`;
проще заменить «после сбора» на цифры прямо в таблицах через правку `generate.py`/`bench_table`
или прислать цифры — обновлю.

## Структура каждого аудита (22 слайда)

1. Титул → 2. Резюме встречи (ответы клиента + диагноз) → 3. Ниша в цифрах →
4. Согласование проекта → 5–7. Ozon (таргетинги, сегменты, бенчмарки) →
8–10. Яндекс Urban Ads (форматы, сегменты, бенчмарки) → 11–12. WB Media (сегменты, бенчмарки) →
13. Сравнение источников → 14–16. Замеры (Search/Brand/Sales lift, Post-view: бенчмарки + план) →
17–18. Рессейлинг (13 кабинетов + каналы под нишу) → 19. Готовность сайта →
20. Условия → 21. Рекомендации → 22. Следующий шаг.
