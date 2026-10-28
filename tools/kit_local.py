# -*- coding: utf-8 -*-
"""Особое MCU-Skill в общей проверке skill-skill/tools/check_docs.py.

GENERIC — слова имени папки проекта, не считающиеся приметой изделия;
TEXT_EXT — сценарии J-Link (.jlink) тоже сверяются со стоп-листом;
PROJECT_EXT — платы, схемы, прошивки и проекты сред разработки в папке
проекта: их имена становятся стоп-словами.
"""
GENERIC = set("""app blink firmware prog переходник переходника""".split())
TEXT_EXT = (".jlink",)
PROJECT_EXT = (".BRD", ".DSN", ".OPJ", ".SCH", ".PCB", ".HEX", ".ELF",
               ".BIN", ".UVPROJX", ".EWP", ".IOC")
