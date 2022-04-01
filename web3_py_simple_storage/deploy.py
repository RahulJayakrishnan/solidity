import solcx
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
print(compiled_sol)