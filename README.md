# Final Assignment II4031 Cryptography and Coding
## Authors:
- 18221115 Christopher Febrian Nugraha

# Specifications
- Blockchain-based Databases
- EdDSA for Digital Signage
- ECIES for Encryption and Decryption
- Keccak for Hash Function

# How to Run App on Windows OS
## Part 1: Preparation and Installation
1. Clone this repository to your device using GitHub Desktop or the following command:
    > git clone https://github.com/toper664/blockchain-with-ecies-eddsa-keccak
2. Make a new _virtual environment_ by running this code in Windows CLI:
    > py -m venv venv
    - Make sure you alreay have _Python 3_ installed. If not, you can check out the following [link](https://docs.python.org/3/using/windows.html#using-on-windows).
    - Also make sure that you are currently on the _root_ folder of this repository before making a _virtual environment_.
3. Run the _virtual environment_ using this code:
    > venv/Scripts/activate
4. Install the needed dependencies for this project, which is:
    > pip install pipenv
    - The **pipenv** module is an environment control system that serves as a basic project manager for Python-based projects.
5. Run the following code in order to ensure every dependencies needed is installed by pipenv:
    > pipenv sync

## Part 2: Execution and Usage
1. Run the client.py file on port 8080 by using the following command:
    > pipenv run py -m client 8080
2. The program will show a screen GUI of blockchain wallet creation for users at http://localhost:8080.
3. Run the blockchain.py file by using the following command:
    > pipenv run py -m blockchain
4. The program will show a screen GUI of blockchain mining and waiting orders for users at http://localhost:5000.
5. Good luck and have fun.
