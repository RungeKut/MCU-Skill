---
name: mcu
description: "Микроконтроллеры Cortex-M (GD32, STM32) скриптами — сборка прошивки GCC без IDE, прошивка и чтение через SEGGER J-Link или ST-Link (STM32CubeProgrammer) по SWD, проверка связи и питания, чтение защиты и содержимого флеша, сохранение старой прошивки, проверка, что код идёт. Используй ВСЕГДА, когда речь о J-Link, SEGGER, JLink.exe, ST-Link, STLink, STM32CubeProgrammer, STM32_Programmer_CLI, SWD, JTAG, программаторе, прошивке, прошить, залить, blink, микроконтроллере, МК, GD32, STM32, Cortex-M, arm-none-eabi-gcc, .bin/.hex/.elf прошивки, startup, линкер-скрипте; а также при ошибках «Could not connect to the target device», «Device will be unsecured now», «TDO is constant high», «undefined reference to memcpy», VTref, «No such file» от arm-none-eabi-nm. Содержит библиотеку mcukit и базу проверенного опытом знания."
---

# Микроконтроллеры: сборка и прошивка скриптами

Корень набора — папка, из которой прочитан этот файл (клон
`RungeKut/MCU-Skill`). Библиотека `mcukit`, шаблоны `templates/`, база
`knowledge/` (карта и поиск по симптому — `INDEX.md`). Общие правила —
соседний скилл skill-skill.

**Первым делом:** `git -C <корень> pull --rebase`; конфликт — разобрать до
работы.

```python
import sys; sys.path.insert(0, r"<корень>")
import mcukit as mk
mk.utf8_console()          # иначе print с кириллицей упадёт
print(mk.jlink_version(), mk.stlink_version(), mk.gcc_version())
print(mk.probe())          # J-Link: зонд, VTref
print(mk.stlink.probe())   # ST-Link: зонд(ы), к чипу не лезет
```

GD32 — только J-Link (`mk.*`), штатные STM32 — ST-Link (`mk.stlink.*`),
20-04. Рабочие циклы, шаблоны (`KIT` в `project.py`), состав библиотеки —
20-05; версии, на которых собрана база, — `00_ПРАВИЛА.md`.

## Железные правила

1. **Без спроса — только чтение**: `probe`, `info`, `read32`, `watch`,
   `sample`, `save`. `flash`, байты настройки, снятие защиты, `reset_run` —
   только с согласия человека и после `save()` старого содержимого (20-05).
2. **J-Link: связь — профилем `Cortex-M4`, не профилем чипа**: без связи
   скрипт производителя стирает флеш (20-01, 30-02).
3. **ST-Link, чтение — `mode=HOTPLUG`** (умолчание `mcukit.stlink`):
   обычный `connect` сбрасывает ядро (30-08).
4. **«Could not connect» — сначала спросить про общую землю и питание**
   (30-01, 30-03).
5. **Успех — по тексту вывода, не по коду возврата** (30-05, 30-07).
6. **«Прошилось» ≠ «работает»** — счётчик в ОЗУ через `watch()` (20-02).
7. **Сборка и binutils — на путях без кириллицы** (30-06).
8. **Непроверенное — `не проверено`** (00).

## Правка набора

Нашли грабли — запись по `knowledge/00_ПРАВИЛА.md`, строки в `INDEX.md` и
`CHANGELOG.md`, `git diff`, `python tools/check_docs.py --project "<папка
проекта>"`, коммит, push сразу. В набор — ничего об изделии (40-02).
Коммит — без соавторов, автор задан для клона (skill-skill).
