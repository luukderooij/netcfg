from __future__ import annotations

import logging
import webbrowser
from typing import List, Dict

from scapy.all import ARP, Ether, srp, conf


conf.verb = 0

logger = logging.getLogger(__name__)  # module-level logger


class NpcapRequiredError(RuntimeError):
    """Raised when a pcap backend (Npcap/libpcap) is required but not available."""


class ArpScanner:
    """GUI-friendly ARP network scanner.

    Example usage (in your GUI code):
        from arp_scanner import ArpScanner, NpcapRequiredError

        scanner = ArpScanner(open_on_fail=False)
        try:
            results = scanner.scan("192.168.1.0/24", timeout=2)
        except NpcapRequiredError:
            # inform user that Npcap is required and optionally call scanner.open_npcap_page()
            pass

    The scan() method returns a list of dicts with keys: 'ip' and 'mac'.
    """
    
    NPCAP_DOWNLOAD_URL = "https://npcap.com/#download"

    def __init__(self, open_on_fail: bool = True, verbose: bool = False) -> None:
        """Create an ArpScanner.

        Args:
            open_on_fail: if True, ensure_npcap() will open the Npcap download page when missing.
            verbose: if True, set scapy verbose mode on; otherwise keep it quiet.
        """
        self.open_on_fail = open_on_fail
        self.verbose = verbose
        # Keep scapy conf.verb consistent with verbose flag
        conf.verb = 1 if self.verbose else 0
        logger.debug("ArpScanner initialized (open_on_fail=%s, verbose=%s)",
                     self.open_on_fail, self.verbose)

    def ensure_npcap(self) -> None:
        """Verify that a pcap backend is available. If not, either open the download page or raise.

        Raises:
            NpcapRequiredError: when no pcap backend is available.
        """
        logger.debug("Checking for pcap backend...")
        if not conf.use_pcap:
            logger.warning("No pcap backend available (Npcap/libpcap missing).")
            if self.open_on_fail:
                try:
                    logger.info("Opening Npcap download page: %s", self.NPCAP_DOWNLOAD_URL)
                    webbrowser.open(self.NPCAP_DOWNLOAD_URL)
                except Exception as e:
                    logger.exception("Failed to open webbrowser: %s", e)
            raise NpcapRequiredError("Npcap (or other pcap backend) is required for ARP scanning.")
        logger.debug("pcap backend is available.")

    def scan(self, network_cidr: str = "192.168.1.0/24", timeout: float = 2) -> List[Dict[str, str]]:
        """Perform an ARP scan on the given CIDR and return list of found hosts.

        Args:
            network_cidr: network in CIDR notation (e.g. "192.168.1.0/24").
            timeout: how long (seconds) to wait for replies.

        Returns:
            A list of dicts: [{"ip": "192.168.1.10", "mac": "aa:bb:cc:dd:ee:ff"}, ...]

        Raises:
            NpcapRequiredError: if no pcap backend is available.
            ValueError: if the network_cidr parameter is empty.
        """
        if not network_cidr:
            logger.error("Empty network_cidr parameter provided.")
            raise ValueError("network_cidr must be a non-empty string")

        logger.info("Starting ARP scan on network %s with timeout=%s", network_cidr, timeout)
        self.ensure_npcap()

        pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network_cidr)
        answered, _ = srp(pkt, timeout=timeout)

        results: List[Dict[str, str]] = []
        for snd, rcv in answered:
            host_info = {"ip": rcv.psrc, "mac": rcv.hwsrc}
            logger.debug("Found host: %s", host_info)
            results.append(host_info)

        logger.info("ARP scan complete. %d host(s) found.", len(results))
        return results


if __name__ == "__main__":
    # Minimal demo instead of argparse
    scanner = ArpScanner(open_on_fail=True)
    try:
        hosts = scanner.scan("192.168.1.0/24", timeout=2)
    except NpcapRequiredError:
        print("Npcap is required for ARP scanning. To install: ", ArpScanner.NPCAP_DOWNLOAD_URL)
    else:
        for h in hosts:
            print(f"{h['ip']:16}    {h['mac']}")
