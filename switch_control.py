#!/usr/bin/env python3

import socket

ADDR = "255.255.255.255"
PORT = 8866
DEVICE_ID = "2015117076"
DEVICE_TYPE = "1f"


def send_command(s: socket, cmd: str, frame: bytes) -> None:
    """
    Send a command to the switch using the given socket and frame.
    If the command is not successful after 5 attempts, print an error message.

    Parameters:
    - s: the socket to use to send the command
    - cmd: the command to send, either "on" or "off"
    - frame: the bytes representing the command to send
    """
    for i in range(5):
        s.sendto(frame, (ADDR, PORT))
        i += 1
        try:
            data, addr = s.recvfrom(1024)
        except Exception as e:
            print("Timeout")
            continue
        print(f"Boiler switch turned {cmd}.".title())
        return
    print("Error - could not find switch.".title())


def control_switch(state: str = "on") -> None:
    """
    Control the state of the switch.

    Parameters:
    - state: the desired state of the switch, either "on" or "off"
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("", PORT))
    s.settimeout(3.2)

    state = state.lower() if state.lower() in ["on", "off"] else "off"

    command = {"on": ["45", "01"], "off": ["44", "00"]}

    send_command(
        s,
        state,
        bytes.fromhex(
            "aa21a010"  # Header
            + command[f"{state}"][0]  # Command
            + DEVICE_ID
            + DEVICE_TYPE
            + command[f"{state}"][1]  # Command
            + "0021a010"  # Footer
            + "0" * 34  # Padding
        ),
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("state", type=str, help="on or off")
    args = parser.parse_args()
    control_switch(args.state)
