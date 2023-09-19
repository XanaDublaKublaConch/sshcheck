import re
import socket

# Dependency imports
from paramiko import Transport

socket.setdefaulttimeout(3)


class SshCheck(Transport):
    def __int__(self, *args, **kwargs):
        self.kex = []        # Key Exchange Algorithm
        self.hka = []        # Host Key Algorithm
        self.ciphers = []    # Message Exchange Encryption
        self.mac = []        # Message Hash
        self.compress = []   # Compression algorithms
        self.lang_list = []  # Supported languages? I've never seen this populated.
        super.__init__(*args, **kwargs)

    def _parse_kex_init(self, m):
        parsed = self._really_parse_kex_init(m)
        self.kex = parsed['kex_algo_list']
        self.hka = parsed['server_key_algo_list']
        self.ciphers = parsed['server_encrypt_algo_list']
        self.mac = parsed['server_mac_algo_list']
        self.compress = parsed['server_compress_algo_list']
        self.lang_list = parsed['server_lang_list']
        m.rewind()
        super()._parse_kex_init(m)


def dns_ptr_lookup(addr):
    try:
        return socket.gethostbyaddr(addr)
    except socket.herror:
        return None, None, None


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
        self.server_key_str: str = ""
        self.policy: dict[str, dict[str, str]] = policy

    def resolve_address(self):
        if re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", self.ip_address):
            # User provided an ip address, so get the hostname and set it
            self.hostname = dns_ptr_lookup(self.ip_address)[0] or "No DNS"
        else:
            # The user provided a hostname, so get the ip and set it
            try:
                self.ip_address = socket.gethostbyname(self.hostname)
            except socket.gaierror:
                self.ip_address = "Lookup failed"

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

        for idx in ['kex', 'hka', 'ciphers', 'mac']:
            config_attr: dict[str, set] = getattr(self, idx)
            server_attr: dict[str, set] = getattr(t, idx)

            # Within policy APPROVED
            config_attr['approved'] = set(server_attr).intersection(self.policy[idx]['approved']) or {'None'}
            # Everything else, used for getting contained, bad, unknown
            config_attr['unapproved'] = set(server_attr) - set(self.policy[idx]['approved']) or {'None'}
            # Contained
            config_attr['contained'] = \
                config_attr['unapproved'].intersection(self.policy[idx]['contained']) or {'None'}
            # Stuff that the scanner found, but it's not in the official policy. Qualys doesn't seem to mind these
            # e.g. chacha
            config_attr['unknown'] = \
                config_attr['unapproved'].intersection(self.policy[idx]['qualys_approved']) or {'None'}
            # Known bad stuff
            config_attr['bad'] = \
                config_attr['unapproved'] - config_attr['contained'] - config_attr['unknown'] or {'None'}

        # What kind of key did the server send us after negotiations?
        if t.host_key_type in self.policy['key_format']['approved']:
            self.server_key_str = f"[bold green]approved {t.host_key_type}[/bold green]"
        elif t.host_key_type in self.policy['key_format']['contained']:
            self.server_key_str = f"[bold red]contained {t.host_key_type}[/bold red]"
        elif t.host_key_type in self.policy['key_format']['qualys_approved']:
            self.server_key_str = f"[bold yellow]uncategorized {t.host_key_type}[/bold yellow]"
        else:
            self.server_key_str = f"[bold red]bad {t.host_key_type}[/bold red]"

        t.close()
