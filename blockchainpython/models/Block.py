from hashlib import sha256
from logging import debug
from models.Transaction import Transaction
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Block:
    previous_hash: str
    transactions: List[Transaction]
    block_hash: str = field(init=False)
    time_stamp: datetime = field(default_factory=datetime.now)
    nonce: int = 0

    def __post_init__(self):
        self.block_hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        return sha256(f"{self.previous_hash}{self.time_stamp.isoformat()}{self.transactions}{self.nonce}".encode()).hexdigest()

    def mine(self, difficulty: int) -> None:
        hash_start = str().zfill(difficulty)
        while not self.block_hash.startswith(hash_start):
            self.nonce += 1
            self.block_hash = self.calculate_hash()
        debug(f"Done mining block with hash {self.block_hash}")

    def has_valid_transactions(self) -> bool:
        for transaction in self.transactions:
            if not transaction.is_valid():
                return False
        return True
