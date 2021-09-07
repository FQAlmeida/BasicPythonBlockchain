from datetime import date, datetime

from rsa.key import PublicKey
from models.Transaction import Transaction
from typing import List
from models.Block import Block
from dataclasses import dataclass, field


@dataclass
class Blockchain:
    chain: List[Block] = field(default_factory=list)
    difficulty: int = 2
    pending_transactions: List[Transaction] = field(default_factory=list)
    mining_reward: float = 100
    qtd_transactions_per_block: int = 10

    def __post_init__(self):
        self.chain.append(Blockchain.create_genesis())

    @staticmethod
    def create_genesis() -> Block:
        return Block(
            None,
            list(),
            time_stamp=datetime.strptime(
                "01/07/2021 13:00:00", "%d/%m/%Y %H:%M:%S")
        )

    def latest_block(self) -> Block:
        return self.chain[-1]

    def mine_pending_transactions(self, mining_reward_address: PublicKey):
        reward_transaction = Transaction(
            None, mining_reward_address, self.mining_reward)

        self.pending_transactions.append(reward_transaction)

        block = Block(
            self.latest_block().block_hash,
            self.pending_transactions[:self.qtd_transactions_per_block]
        )

        block.mine(self.difficulty)

        self.chain.append(block)
        self.pending_transactions = self.pending_transactions[self.qtd_transactions_per_block:]

    def add_transaction(self, transaction: Transaction):
        if transaction.from_address == None or transaction.to_address == None:
            raise Exception("Transaction should have addresses")
        elif not transaction.is_valid():
            raise Exception("Transaction should be valid")
        elif transaction.value <= 0:
            raise Exception(
                "Transaction should have a positive value being transfered")
        elif self.get_balance(transaction.from_address) < transaction.value:
            raise Exception("Not enough balance on the origin address")
        self.pending_transactions.append(transaction)

    def get_balance(self, address: PublicKey) -> float:
        amount: float = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction.from_address == address:
                    amount -= transaction.value
                elif transaction.to_address == address:
                    amount += transaction.value
        return amount

    def get_all_transactions(self, address: PublicKey) -> List[Transaction]:
        transactions: List[Transaction] = list()
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.from_address == address or transaction.to_address == address:
                    transactions.append(transaction)
        return transactions

    def is_chain_valid(self) -> bool:
        genesis = self.create_genesis()
        if genesis != self.chain[0]:
            return False
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]
            if previousBlock.hash != currentBlock.previousHash:
                return False
            elif not currentBlock.hasValidTransactions():
                return False
            elif currentBlock.hash != currentBlock.calculateHash():
                return False
        return True
