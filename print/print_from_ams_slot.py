#!/usr/bin/env python3
"""Query AMS inventory, validate a requested slot/material, and start a sliced job."""

import argparse
import os
import sys
import time

import bambulabs_api as bl


def load_env(path="~/.config/bambu/p2s.env"):
    values = {}
    with open(os.path.expanduser(path), encoding="utf-8") as stream:
        for raw_line in stream:
            line = raw_line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key] = value
    return values


def connect(env):
    printer = bl.Printer(env["BAMBU_HOST"], env["BAMBU_CODE"], env["BAMBU_SERIAL"])
    printer.connect()
    for _ in range(15):
        time.sleep(1)
        try:
            if printer.mqtt_client_connected() and printer.get_state():
                return printer
        except Exception:
            pass
    raise RuntimeError("printer telemetry did not become ready")


def ams_trays(printer):
    for _ in range(15):
        report = printer.mqtt_dump().get("print", {})
        units = report.get("ams", {}).get("ams", [])
        if units and units[0].get("tray"):
            return units[0]["tray"]
        time.sleep(1)
    return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument("--slot", default="A4", help="AMS slot, such as A4")
    parser.add_argument("--material", default="PETG", help="required material reported by the AMS")
    parser.add_argument("--list-materials", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--no-monitor", action="store_true")
    args = parser.parse_args()

    printer = connect(load_env())
    try:
        trays = ams_trays(printer)
        for index, item in enumerate(trays, start=1):
            print(f"A{index}={item.get('tray_type', 'EMPTY')} color={item.get('tray_color', '')}")
        if args.list_materials:
            return
        if len(args.slot) != 2 or args.slot[0].upper() != "A" or not args.slot[1].isdigit():
            raise RuntimeError(f"unsupported slot notation: {args.slot}")
        tray_index = int(args.slot[1]) - 1
        if tray_index < 0 or tray_index >= len(trays):
            raise RuntimeError(f"AMS slot {args.slot} is not present")
        tray = trays[tray_index]
        material = str(tray.get("tray_type", "")).upper()
        requested = args.material.upper()
        print(f"printer={printer.get_state()} {args.slot.upper()}={material} color={tray.get('tray_color')}", flush=True)
        if requested not in material:
            raise RuntimeError(f"refusing print: {args.slot.upper()} contains {material or 'unknown material'}, not {requested}")
        if args.check_only:
            return
        if not args.file:
            parser.error("file is required unless --check-only is used")
        state = str(printer.get_state()).upper()
        if any(word in state for word in ("RUNNING", "PREPARE", "PAUSE")):
            raise RuntimeError(f"refusing print: printer state is {state}")

        filename = os.path.basename(args.file)
        with open(args.file, "rb") as stream:
            uploaded = printer.upload_file(stream, filename)
        print(f"upload={uploaded} file={filename}", flush=True)
        started = printer.start_print(
            filename,
            1,
            use_ams=True,
            ams_mapping=[tray_index],
            flow_calibration=False,
        )
        print(f"start={started} ams_mapping=[{tray_index}] ({args.slot.upper()})", flush=True)
        if not started:
            raise RuntimeError("printer rejected the start command")
        if args.no_monitor:
            return
        while True:
            time.sleep(10)
            state = str(printer.get_state())
            print(f"{state} {printer.get_percentage()}% layer {printer.current_layer_num}/{printer.total_layer_num}", flush=True)
            if any(word in state.upper() for word in ("FINISH", "FAILED", "IDLE")):
                return
    finally:
        printer.disconnect()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise
