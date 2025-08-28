🗳️ Voting Management System on a Simple Blockchain
📌 Overview

This project is a menu-driven console application that demonstrates how a blockchain can be applied to a voting management system. It ensures transparency, immutability, and security of votes by recording every transaction (vote) on a blockchain.

The application allows an admin to register voters and candidates, while voters can securely cast their votes. The blockchain structure guarantees that no duplicate votes, voter IDs, or candidate IDs exist, and that all votes are tamper-proof.

---

🎯 Objectives

 - Build a simple blockchain-based voting system.
 - Provide a menu-driven console interface.
 - Ensure data integrity using blockchain validation.

---

✅ Features
 # Entities

- Voter → voter_id, name, has_voted
- Candidate → candidate_id, name

---

# Menu Options

* ➕ Add Candidate
* 👤 Add Voter
* 🗳️ Cast Vote
* 📑 Print Blockchain (show blocks, transactions, and hashes)
* 🔍 Validate Blockchain
* 🚪 Exit

---

# Input Validation

* No duplicate voter IDs
* No duplicate candidate IDs
* No double voting

---

⚙️ Tech Stack

* Language: Python
* Concepts: Blockchain, Data Structures, OOP, Console-based Menu System

---

🔐 Blockchain Validation

Each block contains:

- Block index
- Transactions (votes)
- Previous block hash
- Current block hash

The Validate Chain option ensures no tampering has occurred.

---

📸 Sample Output (Console)
1. Add Candidate
2. Add Voter
3. Cast Vote
4. Print Blockchain
5. Validate Blockchain
6. Exit
Enter your choice:

---

📌 Assignment Details

- Module: Blockchain Development - Module 10
- Task: Implement a blockchain-based voting management system
- Submission: Upload to GitHub and share repo link

---

👤 Author

@ Developed by Rajinisoumya ✨
@ For academic and learning purposes.

