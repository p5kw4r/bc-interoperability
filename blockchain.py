from enum import Enum, unique


@unique
class Blockchain(Enum):
    ETHEREUM = 1
    MULTICHAIN = 2
    BITCOIN = 3
