class BioForgeError(Exception):
    """کلاس پایهٔ خطاهای اختصاصی پروژهٔ بیوفورج."""
    pass


class FastaFormatError(BioForgeError):
    """خطا در ساختار فایل فستا، مانند نبودن سرآیند یا توالی."""
    pass


class InvalidSequenceError(BioForgeError):
    """وجود کاراکتر نامعتبر در توالی ژنتیکی."""
    pass


class DataFileError(BioForgeError):
    """خطا در خواندن یا محتوای جدول کدون و وزن آمینواسیدها."""
    pass
