import json
import solcx
import web3

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

solcx.install_solc('0.8.0')
# Solidity source code
compiled_sol = solcx.compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = web3(web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 5777
my_address = "0xBDefedA4A8662680661FAf3E313ED962C1C971f3"
private_key = "0xa5cd7357171b17d2f1e40c3698b4b1c96ff4df2b71fbe6e609edaae8a016957d"