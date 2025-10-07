import subprocess
import platform
import logging

logger = logging.getLogger(__name__)

class Pinger:
    def __init__(self, host: str, count: int = 4, infinite: bool = False):
        """
        :param host: De host of IP om te pingen
        :param count: Aantal echo requests (genegeerd als infinite=True)
        :param infinite: Oneindig pingen (zoals 'ping -t' op Windows)
        """
        self.host = host
        self.count = count
        self.infinite = infinite
        self._process = None  # verwijzing naar het subprocess
        self._stopped = False

    def build_command(self):
        """Stelt het juiste ping-commando samen voor Windows of Linux/macOS."""
        system = platform.system().lower()

        if system == "windows":
            if self.infinite:
                cmd = ["ping", self.host, "-t"]
            else:
                cmd = ["ping", self.host, "-n", str(self.count)]
        else:  # Linux/macOS
            if self.infinite:
                cmd = ["ping", self.host]  # standaard oneindig
            else:
                cmd = ["ping", "-c", str(self.count), self.host]

        logger.debug(f"Ping command: {' '.join(cmd)}")
        return cmd

    def run(self):
        """
        Start het ping-commando en yield elke regel uitvoer in real time.
        Stop automatisch als het proces eindigt of via stop().
        """
        cmd = self.build_command()
        self._stopped = False

        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            logger.info(f"Start ping naar {self.host} (infinite={self.infinite})")

            # Lees regel voor regel totdat gestopt
            for line in self._process.stdout:
                if self._stopped:
                    logger.info("Ping handmatig gestopt.")
                    break

                clean_line = line.rstrip()
                logger.debug(f"[PING OUTPUT] {clean_line}")
                yield clean_line

            # Wacht op het einde (of na stop())
            if not self._stopped:
                self._process.wait()
                if self._process.returncode not in (0, None):
                    msg = f"Ping beëindigd met code {self._process.returncode}"
                    logger.warning(msg)
                    yield msg

        except Exception as e:
            msg = f"Fout bij uitvoeren van ping: {e}"
            logger.exception(msg)
            yield msg

        finally:
            if self._process and self._process.poll() is None:
                self._process.terminate()
            self._process = None

    def stop(self):
        """Stop het lopende ping-proces (alleen relevant bij infinite=True)."""
        self._stopped = True
        if self._process and self._process.poll() is None:
            try:
                self._process.terminate()
                logger.info("Ping-proces is gestopt.")
            except Exception as e:
                logger.error(f"Kon ping-proces niet stoppen: {e}")
