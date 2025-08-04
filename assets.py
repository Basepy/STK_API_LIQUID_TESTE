from enum import Enum, StrEnum


class AssetEnum(str, Enum):
    DEPIX: str = "DEPIX"
    BTC: str = "BTC"


class AssetContractEnum(StrEnum):
    DEPIX: str = "02f22f8d9c76ab41661a2729e4752e2c5d1a263012141b86ea98af5472df5189"
    BTC: str = "6f0279e9ed041c3d710a9f57d0c02928416460c4b722ae3457a11eec381c526d"


ASSETS = list(map(str, AssetEnum))