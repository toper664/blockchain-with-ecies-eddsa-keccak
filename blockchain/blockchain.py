import binascii
import keccak
import json
from collections import OrderedDict
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import Crypto
import Crypto.Random
import requests
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

dummy_sender = "Hatsune Miku"
dummy_reward = 1
dummy_difficulty = 2


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.node_id = str(uuid4()).replace("-", "")
        self.new_block(0, "00")

    def new_block(self, nonce: int, previous_hash: str) -> dict:
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.transactions,
            "nonce": nonce,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        # reset the current list of transactions
        self.transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        self.transactions.append(
            {"sender": sender, "recipient": recipient, "amount": amount}
        )

        return self.last_block["index"] + 1

    @staticmethod
    def hash(block: dict) -> str:
        block_string = json.dumps(block, sort_keys=True)
        return keccak.sha3(block_string, 256)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self) -> int:
        last_block = self.chain[-1]
        last_hash = self.hash(last_block)

        nonce = 0
        while self.valid_proof(self.transactions, last_hash, nonce) is False:
            nonce += 1

        return nonce

    @staticmethod
    def valid_proof(transactions, last_hash, nonce, difficulty=dummy_difficulty):
        guess = (str(transactions) + str(last_hash) + str(nonce))
        guess_hash = keccak.sha3(guess, 256)
        return guess_hash[:difficulty] == "0" * difficulty

    def register_node(self, address: str) -> None:
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError("Invalid URL")

    @staticmethod
    def verify_transaction_signature(sender_address, signature, transaction):
        public_key = RSA.importKey(binascii.unhexlify(sender_address))
        verifier = PKCS1_v1_5.new(public_key)

        hash = SHA.new(str(transaction).encode("utf8"))
        return verifier.verify(hash, binascii.unhexlify(signature))

    def submit_transaction(self, sender_address, recipient_address, value, signature):
        transaction = OrderedDict(
            {
                "sender_address": sender_address,
                "recipient_address": recipient_address,
                "value": value,
            }
        )

        if sender_address == dummy_sender:
            self.transactions.append(transaction)
            return len(self.chain) + 1
        else:
            transaction_verification = self.verify_transaction_signature(
                sender_address, signature, transaction
            )
            if transaction_verification:
                self.transactions.append(transaction)
                return len(self.chain) + 1
            else:
                return False

    def valid_chain(self, chain: list) -> bool:
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if block["previous_hash"] != self.hash(last_block):
                return False

            transactions = block["transactions"][:-1]
            transaction_elements = ["sender_address", "recipient_address", "value"]
            transactions = [
                OrderedDict((k, transaction[k]) for k in transaction_elements)
                for transaction in transactions
            ]

            if not self.valid_proof(
                transactions, block["previous_hash"], block["nonce"], dummy_difficulty
            ):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self) -> bool:
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f"http://{node}/chain")

            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False