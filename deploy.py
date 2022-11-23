from solcx import compile_standard, install_solc
import json
from web3 import Web3

install_solc( "0.6.0")

with open("SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

#print(simple_storage_file)

#Un string en formato JSON pero que todavia no podemos hacerle nada.
compile_contract = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        }
    },
    solc_version="0.6.0"
)

#print(compile_contract)
with open("compiled_code.json", "w") as file:
    json.dump(compile_contract, file)

### Desplegar el contrato.
#Obtener el bytecode.
bytecode = compile_contract["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
#Obtener el ABI. (configuraciones como un ABI.py)
abi = compile_contract["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#Desplegar el contrato en la red utilizando la informacion de Ganache.
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
address = "0x455EC8A7b66096fE3d5D79F19B66C1d324C25Dbb"
pk = "0x37ec1742807346fcf00d75e78a549f99ca63f419b45f5765a37a462f7692bb8c" #Esto no deberia de hacerse, sin embargo como estamos tratando con redes de prueba, no hay problema alguno.

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
#print(SimpleStorage)

#Se debe de construir la txn primero. NONCE.
nonce = w3.eth.getTransactionCount(address)
txn = SimpleStorage.constructor().buildTransaction({
    "gasPrice": w3.eth.gasPrice,
    "chainId": chain_id,
    "from": address,
    "nonce": nonce
})

#Firmar la txn
signed_txn = w3.eth.account.sign_transaction(txn, private_key=pk)
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

#En algunos casos nos interesa una confimracion de la txn.
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

#print(txn_hash)

#Esto seria lo mas cercano a el contrato que podamos tener en Python.
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)
print(simple_storage.functions.retrieve().call()) #Boton azul.
print(simple_storage.functions.store(15).call()) #Boton naranja, sin modificar el estado de la red.

store_txn = simple_storage.functions.store(15).buildTransaction({ #Boton naranja que modifica el estado de la red.
    "gasPrice": w3.eth.gasPrice,
    "chainId": chain_id,
    "from": address,
    "nonce": nonce+1
})
signed_store_txn = w3.eth.account.sign_transaction(store_txn, private_key=pk)
txn_hash_store = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash_store)
print(simple_storage.functions.retrieve().call())
