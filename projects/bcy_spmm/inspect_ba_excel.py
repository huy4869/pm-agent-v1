"""Read an XLSX workbook without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def _text(node: ET.Element | None) -> str:
    return "" if node is None else "".join(item.text or "" for item in node.findall(".//m:t", NS))


def _column(reference: str) -> int:
    letters = re.match(r"[A-Z]+", reference).group(0)  # type: ignore[union-attr]
    value = 0
    for letter in letters:
        value = value * 26 + ord(letter) - 64
    return value - 1


def read_workbook(path: Path) -> dict[str, list[list[object]]]:
    with zipfile.ZipFile(path) as archive:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = [_text(item) for item in root.findall("m:si", NS)]

        date_styles: set[int] = set()
        if "xl/styles.xml" in archive.namelist():
            styles = ET.fromstring(archive.read("xl/styles.xml"))
            custom = {
                int(item.attrib["numFmtId"]): item.attrib.get("formatCode", "")
                for item in styles.findall("m:numFmts/m:numFmt", NS)
            }
            xfs = styles.findall("m:cellXfs/m:xf", NS)
            for index, xf in enumerate(xfs):
                fmt_id = int(xf.attrib.get("numFmtId", 0))
                fmt = custom.get(fmt_id, "").lower()
                if fmt_id in set(range(14, 23)) | {45, 46, 47} or (
                    "d" in fmt and ("m" in fmt or "y" in fmt)
                ):
                    date_styles.add(index)

        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in rels.findall("r:Relationship", REL_NS)
        }
        result: dict[str, list[list[object]]] = {}
        for sheet in workbook.findall("m:sheets/m:sheet", NS):
            name = sheet.attrib["name"]
            target = targets[sheet.attrib[RID]].lstrip("/")
            sheet_path = target if target.startswith("xl/") else f"xl/{target}"
            root = ET.fromstring(archive.read(sheet_path))
            rows: list[list[object]] = []
            for row in root.findall("m:sheetData/m:row", NS):
                values: list[object] = []
                for cell in row.findall("m:c", NS):
                    index = _column(cell.attrib["r"])
                    values.extend([""] * (index - len(values) + 1))
                    kind = cell.attrib.get("t")
                    raw = cell.findtext("m:v", default="", namespaces=NS)
                    if kind == "s" and raw:
                        value: object = shared[int(raw)]
                    elif kind == "inlineStr":
                        value = _text(cell.find("m:is", NS))
                    elif kind == "b":
                        value = raw == "1"
                    elif raw and int(cell.attrib.get("s", 0)) in date_styles:
                        value = (datetime(1899, 12, 30) + timedelta(days=float(raw))).strftime("%d/%m/%Y")
                    elif raw:
                        number = float(raw)
                        value = int(number) if number.is_integer() else number
                    else:
                        value = ""
                    values[index] = value
                while values and values[-1] == "":
                    values.pop()
                if any(value != "" for value in values):
                    rows.append(values)
            result[name] = rows
        return result


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: inspect_ba_excel.py <workbook.xlsx>")
    data = read_workbook(Path(sys.argv[1]))
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
