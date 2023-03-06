from enum import Enum


class Currency(Enum):
    NGN = "NGN"
    EGP = "EGP"
    KES = "KES"


class Bank(Enum):
    ACCESS = "044"
    ALAT = "035A"
    CIB = "818147"
    ECOBANK = "050"
    FBN = "011"
    FCMB = "214"
    FIDELITY = "070"
    GLOBUS = "00103"
    GTB = "058"
    HSBC = "818039"
    KEYSTONE = "082"
    KUDA = "50211"
    MBS = "041"
    MPESA = "404001"
    PROVIDUS ="101"
    POLARIS = "076"
    STANBIC = "221"
    STERLING = "232"
    UBA = "033"
    UNITY = "215"
    UNION = "032"
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
