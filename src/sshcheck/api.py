# Legacy support for Union as |
from __future__ import annotations

# Builtins
import re
import socket
from enum import Enum, auto
from ipaddress import ip_address

# Dependency imports
from paramiko import Transport
from .exceptions import InvalidTargetException

# Default socket timeout is way too long for this
socket.setdefaulttimeout(3)


class PolicyStatus(Enum):
    APPROVED = auto
    UNAPPROVED = auto
    CONTAINED = auto
    OTHER = auto


class SshCheck(Transport):
    def __int__(self, *args, **kwargs):
        self.kex = []  # Key Exchange Algorithm
        self.hka = []  # Host Key Algorithm
        self.ciphers = []  # Message Exchange Encryption
        self.mac = []  # Message Hash
        self.compress = []  # Compression algorithms
        self.lang_list = []  # Supported languages? I've never seen this populated.
        super.__init__(*args, **kwargs)

    def _parse_kex_init(self, m):
        parsed = self._really_parse_kex_init(m)
        self.kex = parsed["kex_algo_list"]
        self.hka = parsed["server_key_algo_list"]
        self.ciphers = parsed["server_encrypt_algo_list"]
        self.mac = parsed["server_mac_algo_list"]
        self.compress = parsed["server_compress_algo_list"]
        self.lang_list = parsed["server_lang_list"]
        m.rewind()
        super()._parse_kex_init(m)


def dns_ptr_lookup(addr):
    try:
        return socket.gethostbyaddr(addr)
    except socket.herror:
        return None, None, None


# noinspection SpellCheckingInspection
class CheckedServer:
    """
    A class to hold the checked server computed results
    """

    def __init__(self, hostname: str, port: int, policy: dict[str, dict[str, str]]):
        self.hostname: str = hostname
        self.port: int = port
        self.ip_address: str = hostname
        self.resolve_address()
        self.kex: dict[str, set] = {}
        self.hka: dict[str, set] = {}
        self.ciphers: dict[str, set] = {}
        self.mac: dict[str, set] = {}
        self.compress: set[str] = set()
        self.lang_list: set[str] = set()
        self.host_key_type: str = ""
        self.host_key_status: PolicyStatus | None = None
        self.policy: dict[str, dict[str, str]] = policy

    def resolve_address(self):
        if re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", self.ip_address):
            # User provided an ip address, so get the hostname and set it
            try:
                _ = ip_address(self.ip_address)
            except ValueError as e:
                raise InvalidTargetException(e)
            self.hostname = dns_ptr_lookup(self.ip_address)[0] or "No DNS"
        else:
            # The user provided a hostname, so get the ip and set it
            try:
                self.ip_address = socket.gethostbyname(self.hostname)
            except socket.gaierror:
                raise InvalidTargetException(f"DNS lookup failed for {self.hostname}.")

    def check_ssh(self):
        """
        Check the server's advertised ssh security capabilities against the yaml policy
        :return:
        """
        t = SshCheck(f"{self.ip_address}:{self.port}")
        t.connect()

        # set the easy ones
        self.lang_list = t.lang_list
        self.compress = t.compress
        self.host_key_type = t.host_key_type

        for idx in ["kex", "hka", "ciphers", "mac"]:
            config_attr: dict[str, set] = getattr(self, idx)
            server_attr: dict[str, set] = getattr(t, idx)

            # Within policy APPROVED
            config_attr["approved"] = set(server_attr).intersection(
                self.policy[idx]["approved"]
            ) or {"None"}
            # Everything else, used for getting contained, bad, unknown
            config_attr["unapproved"] = set(server_attr) - set(
                self.policy[idx]["approved"]
            ) or {"None"}
            # Contained
            config_attr["contained"] = config_attr["unapproved"].intersection(
                self.policy[idx]["contained"]
            ) or {"None"}
            # Stuff that that's outside your official policy, but can't/won't be fixed
            # e.g. chacha20-poly1305@openssh.com in some orgs
            config_attr["unknown"] = config_attr["unapproved"].intersection(
                self.policy[idx]["policy_overrides"]
            ) or {"None"}
            # Known bad stuff
            config_attr["bad"] = config_attr["unapproved"] - config_attr[
                "contained"
            ] - config_attr["unknown"] or {"None"}

        # What kind of key did the server send us after negotiations?
        if self.host_key_type in self.policy["key_format"]["approved"]:
            self.host_key_status = PolicyStatus.APPROVED
        elif self.host_key_type in self.policy["key_format"]["contained"]:
            self.host_key_status = PolicyStatus.CONTAINED
        elif self.host_key_type in self.policy["key_format"]["policy_overrides"]:
            self.host_key_status = PolicyStatus.OTHER
        else:
            self.host_key_status = PolicyStatus.UNAPPROVED

        # Clean up the connection
        t.close()
