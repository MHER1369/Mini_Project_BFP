"""تعریف خطاهای اختصاصی مورد استفاده در خط پردازش BioForge."""


class BioForgeError(Exception):
    pass


class FastaFormatError(BioForgeError):
    pass


class InvalidSequenceError(BioForgeError):
    pass


class DataFileError(BioForgeError):
    pass
