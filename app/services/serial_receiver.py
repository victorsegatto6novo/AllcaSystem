from __future__ import annotations

import serial


class CafCm4000Receiver:
    """
    Leitura básica da receptora CAF CM4000 pela porta serial.

    A decodificação do protocolo pode variar de acordo com configuração da receptora.
    """

    def __init__(self, port: str = "COM3", baudrate: int = 9600, timeout: float = 0.5):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def read_line(self) -> str | None:
        with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser:
            raw = ser.readline().decode(errors="ignore").strip()
            return raw or None
