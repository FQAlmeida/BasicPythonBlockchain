from dataclasses import dataclass, field
from datetime import datetime
from hashlib import sha256
from logging import debug
from rsa import PublicKey
import rsa
from rsa.key import PrivateKey
from rsa.pkcs1 import verify


@dataclass
class Transaction:
    from_address: PublicKey
    to_address: PublicKey
    value: float
    signature: bytes = None
    time_stamp: datetime = field(default_factory=datetime.now)

    def calculate_hash(self) -> str:
        debug(
            f"Processing Transaction Hash: {self.from_address} -> {self.to_address}")
        return sha256(
            f"{self.from_address}{self.to_address}{self.value}{self.time_stamp.isoformat()}".encode()
        ).hexdigest()

    def signTransaction(self, signingKey: PrivateKey):
        if PublicKey(signingKey.n, signingKey.e) != self.from_address:
            raise Exception('You cannot sign transactions for other wallets!')

        hashTx = self.calculate_hash()
        sig = rsa.sign(hashTx.encode(), signingKey, 'SHA-256')

        self.signature = sig

    def is_valid(self):
        if self.from_address == None:
            return True
        if(self.signature == None or len(self.signature) == 0):
            raise Exception("No signature")
        return verify(self.calculate_hash().encode(), self.signature, self.from_address)
