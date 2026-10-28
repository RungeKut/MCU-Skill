# -*- coding: utf-8 -*-
"""Собрать, прошить, доказать, что код идёт.

Запуск:  python run.py            собрать, прошить, проверить
         python run.py --build    только собрать
         python run.py --kit <папка скилла mcu> ...
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import project as P         # noqa: E402


def is_kit(d):
    """Папка скилла, а не одноимённая рабочая папка mcukit в Temp."""
    return os.path.isfile(os.path.join(d, "SKILL.md")) and \
        os.path.isfile(os.path.join(d, "mcukit", "__init__.py"))


def kit_root(argv):
    """Корень скилла mcu (папка с mcukit/): --kit <папка>, иначе KIT из
    project.py, иначе вверх от проекта — сам набор (шаблон запущен на
    месте) или соседний скилл mcu (проект внутри папки скиллов)."""
    given = getattr(P, "KIT", None)
    if "--kit" in argv:
        i = argv.index("--kit")
        given = argv[i + 1] if i + 1 < len(argv) else ""
    if given is not None:
        if is_kit(given):
            return os.path.abspath(given)
        raise RuntimeError("в %r нет mcukit/ — нужна папка скилла mcu"
                           % given)
    d = HERE
    while os.path.dirname(d) != d:
        d = os.path.dirname(d)
        for cand in (d, os.path.join(d, "mcu")):
            if is_kit(cand):
                return cand
    raise RuntimeError("скилл mcu не найден: python run.py --kit <папка "
                       "скилла mcu> или KIT в project.py")


sys.path.insert(0, kit_root(sys.argv[1:]))
import mcukit as mk         # noqa: E402


def main(argv):
    mk.utf8_console()
    b = mk.build(HERE).check()
    sp, reset = mk.vectors(b.bin)
    print("сборка:", b.size, "SP=0x%08X Reset=0x%08X" % (sp, reset))
    if "--build" in argv:
        return 0

    p = mk.probe(serial=P.PROBE_SERIAL)
    print("зонд:", p["product"], p["serial"], "VTref=%s В" % p["vtref"])

    if P.BACKUP:
        addr, size = P.BACKUP
        path = os.path.join(HERE, "backup_%s.bin" % time.strftime(
            "%Y%m%d_%H%M%S"))
        mk.save(path, addr, size, serial=P.PROBE_SERIAL)
        print("сохранено:", path)

    r = mk.flash(b.bin, device=P.DEVICE, min_vtref=P.MIN_VTREF,
                 serial=P.PROBE_SERIAL)
    print("прошито:", r, "сверка:", r.verified)

    addr = mk.symbol(b.elf, "blink_count")
    vals = mk.watch(addr, times=3, interval_ms=1000, serial=P.PROBE_SERIAL)
    print("blink_count:", vals)
    if not all(b2 > a for a, b2 in zip(vals, vals[1:])):
        print("СЧЁТЧИК НЕ РАСТЁТ — код не идёт")
        return 1
    print("Код идёт. Глазами: светодиоды должны мигать.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
