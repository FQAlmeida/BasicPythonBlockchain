__version__ = '0.1.0'

from models.Transaction import Transaction
from rsa.key import newkeys
from models.Blockchain import Blockchain


blockchain = Blockchain()

(genesis_pub_key, genesis_priv_key) = newkeys(512)
(p1_pub_key, p1_priv_key) = newkeys(512)
(p2_pub_key, p2_priv_key) = newkeys(512)

blockchain.mine_pending_transactions(genesis_pub_key)

print(blockchain.get_balance(genesis_pub_key))
print(blockchain.get_all_transactions(genesis_pub_key))

tx1 = Transaction(genesis_pub_key, p1_pub_key, 15)
tx1.signTransaction(genesis_priv_key)
blockchain.add_transaction(tx1)

tx2 = Transaction(genesis_pub_key, p2_pub_key, 30)
tx2.signTransaction(genesis_priv_key)
blockchain.add_transaction(tx2)

blockchain.mine_pending_transactions(genesis_pub_key)

tx3 = Transaction(p2_pub_key, p1_pub_key, 10)
tx3.signTransaction(p2_priv_key)
blockchain.add_transaction(tx3)

blockchain.mine_pending_transactions(genesis_pub_key)

print(blockchain.get_balance(genesis_pub_key))
print(blockchain.get_balance(p1_pub_key))
print(blockchain.get_balance(p2_pub_key))

print(blockchain.get_all_transactions(genesis_pub_key))
print(blockchain.get_all_transactions(p1_pub_key))
print(blockchain.get_all_transactions(p2_pub_key))
