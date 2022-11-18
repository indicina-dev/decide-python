from enum import Enum


class Currency(Enum):
    NGN = "NGN"
    EGP = "EGP"
    KES = "KES"


class Bank(Enum):
    ACCESS = "044"
    CIB = "818147"
    FBN = "011"
    GTB = "058"
    HSBC = "818039"
    UBA = "033"
    MBS = "041"
    MPESA = "404001"
    ZENITH = "057"


class StatementType(Enum):
    JSON = "json"
    CSV = "csv"
    PDF = "pdf"


class StatementFormat(Enum):
    CUSTOM = "custom"
    MBS = "mbs"
    MONO = "mono"
    OKRA = "okra"


class PDFStatus(Enum):
    DONE = "DONE"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
