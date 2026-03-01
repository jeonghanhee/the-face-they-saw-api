from babel.messages import pofile, mofile
from pathlib import Path

def tb(po_file, mo_file):
    with open(po_file, "rb") as fpo:
        catalog = pofile.read_po(fpo)

    with open(mo_file, "wb") as fmo:
        mofile.write_mo(fmo, catalog)

tb("app/locales/ko_KR/LC_MESSAGES/messages.po", "app/locales/ko_KR/LC_MESSAGES/messages.mo")
tb("app/locales/en_US/LC_MESSAGES/messages.po", "app/locales/en_US/LC_MESSAGES/messages.mo")