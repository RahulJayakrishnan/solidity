from brownie import SimpleStorage, accounts


def test_deploy():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    assert starting_value == expected


def test_store():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    expected = 69
    transaction = simple_storage.store(expected, {"from": account})
    transaction.wait(1)
    assert simple_storage.retrieve() == expected
