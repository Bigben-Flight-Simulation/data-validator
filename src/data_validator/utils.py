# 预留工具函数
def safe_int(value, default=None):
    try:
        return int(value)
    except Exception:
        return default

class SafeRow(dict):
    def __getitem__(self, key):
        if self is None:
            return None
        return super().get(key, None)