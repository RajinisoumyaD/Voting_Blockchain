import hashlib
import json
import sys
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# ------------------------------
# Data Models
# ------------------------------
@dataclass
class Voter:
    voter_id: str
    name: str
    has_voted: bool = False

@dataclass
class Candidate:
    candidate_id: str
    name: str

@dataclass
class Transaction:
    tx_type: str
    payload: Dict[str, Any]
    timestamp: float

    @staticmethod
    def add_voter(voter: Voter) -> "Transaction":
        return Transaction("ADD_VOTER", asdict(voter), time.time())

    @staticmethod
    def add_candidate(candidate: Candidate) -> "Transaction":
        return Transaction("ADD_CANDIDATE", asdict(candidate), time.time())

    @staticmethod
    def cast_vote(voter_id: str, candidate_id: str) -> "Transaction":
        return Transaction("CAST_VOTE", {"voter_id": voter_id, "candidate_id": candidate_id}, time.time())

# ------------------------------
# Blockchain Implementation
# ------------------------------
class Block:
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str, difficulty: int = 3):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.mine_block()

    def calculate_hash(self) -> str:
        tx_str = json.dumps([asdict(tx) for tx in self.transactions], sort_keys=True)
        block_string = f"{self.index}{self.timestamp}{tx_str}{self.previous_hash}{self.nonce}{self.difficulty}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self) -> str:
        prefix = "0" * self.difficulty
        h = self.calculate_hash()
        while not h.startswith(prefix):
            self.nonce += 1
            h = self.calculate_hash()
        return h

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [asdict(tx) for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "difficulty": self.difficulty,
            "hash": self.hash,
        }

class Blockchain:
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain: List[Block] = [self._create_genesis_block()]
        self.voters: Dict[str, Voter] = {}
        self.candidates: Dict[str, Candidate] = {}

    def _create_genesis_block(self):
        genesis_tx = Transaction("GENESIS", {"message": "Voting chain initiated"}, time.time())
        return Block(0, [genesis_tx], "0" * 64, self.difficulty)

    def get_latest_block(self):
        return self.chain[-1]

    def _add_block(self, txs: List[Transaction]):
        b = Block(len(self.chain), txs, self.get_latest_block().hash, self.difficulty)
        self.chain.append(b)
        return b

    # ---------- Admin actions ----------
    def add_voter(self, voter_id: str, name: str):
        voter_id = voter_id.strip()
        name = name.strip()
        if not voter_id or not name:
            print("❌ Voter ID and name cannot be empty.")
            return False
        if voter_id in self.voters:
            print(f"❌ Duplicate Voter ID '{voter_id}'.")
            return False
        voter = Voter(voter_id, name)
        self.voters[voter_id] = voter
        self._add_block([Transaction.add_voter(voter)])
        print(f"✅ Voter '{name}' ({voter_id}) added.")
        return True

    def add_candidate(self, candidate_id: str, name: str):
        candidate_id = candidate_id.strip()
        name = name.strip()
        if not candidate_id or not name:
            print("❌ Candidate ID and name cannot be empty.")
            return False
        if candidate_id in self.candidates:
            print(f"❌ Duplicate Candidate ID '{candidate_id}'.")
            return False
        candidate = Candidate(candidate_id, name)
        self.candidates[candidate_id] = candidate
        self._add_block([Transaction.add_candidate(candidate)])
        print(f"✅ Candidate '{name}' ({candidate_id}) added.")
        return True

    # ---------- Voting ----------
    def cast_vote(self, voter_id: str, candidate_id: str):
        voter_id = voter_id.strip()
        candidate_id = candidate_id.strip()
        if voter_id not in self.voters:
            print(f"❌ Voter '{voter_id}' not found.")
            return False
        if candidate_id not in self.candidates:
            print(f"❌ Candidate '{candidate_id}' not found.")
            return False
        if self.voters[voter_id].has_voted:
            print("❌ Double-voting is not allowed.")
            return False
        self.voters[voter_id].has_voted = True
        self._add_block([Transaction.cast_vote(voter_id, candidate_id)])
        print(f"✅ Vote cast: {voter_id} → {candidate_id}")
        return True

    # ---------- Chain utilities ----------
    def validate_chain(self):
        prefix = "0" * self.difficulty
        for i in range(1, len(self.chain)):
            cur, prev = self.chain[i], self.chain[i-1]
            if cur.hash != cur.calculate_hash():
                print(f"❌ Invalid block hash at index {i}.")
                return False
            if not cur.hash.startswith(prefix):
                print(f"❌ Invalid proof-of-work at index {i}.")
                return False
            if cur.previous_hash != prev.hash:
                print(f"❌ Invalid previous_hash link at index {i}.")
                return False
        print("✅ Blockchain is valid.")
        return True

    def print_blockchain(self):
        print("\n========== BLOCKCHAIN ==========")
        for block in self.chain:
            b = block.to_dict()
            print(f"\nBlock #{b['index']}")
            print(f" Timestamp : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(b['timestamp']))}")
            print(f" Prev Hash : {b['previous_hash']}")
            print(f" Nonce     : {b['nonce']}")
            print(f" Difficulty: {b['difficulty']}")
            print(f" Hash      : {b['hash']}")
            print(" Transactions:")
            for tx in b["transactions"]:
                when = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tx['timestamp']))
                print(f"  - {tx['tx_type']} @ {when} -> {json.dumps(tx['payload'], ensure_ascii=False)}")
        print("================================\n")

# ------------------------------
# Menu-driven Console App
# ------------------------------
def print_menu():
    print("""
================ VOTING SYSTEM ================
1. Add Candidate
2. Add Voter
3. Cast Vote
4. Print Blockchain
5. Validate Chain
6. Exit
===============================================
""")

def main():
    chain = Blockchain(difficulty=3)
    while True:
        print_menu()
        choice = input("Enter choice (1-6): ").strip()
        if choice == "1":
            cid = input("Candidate ID: ")
            name = input("Candidate Name: ")
            chain.add_candidate(cid, name)
        elif choice == "2":
            vid = input("Voter ID: ")
            name = input("Voter Name: ")
            chain.add_voter(vid, name)
        elif choice == "3":
            vid = input("Enter Voter ID: ")
            cid = input("Enter Candidate ID: ")
            chain.cast_vote(vid, cid)
        elif choice == "4":
            chain.print_blockchain()
        elif choice == "5":
            chain.validate_chain()
        elif choice == "6":
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please use 1–6.")

if __name__ == "__main__":
    main()
