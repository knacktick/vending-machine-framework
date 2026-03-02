class Debugger:
    IS_DEBUGGING: bool = True

    @staticmethod
    def print(
        s, *args, **kwargs
    ):  # For decoupling logs from core since its a framework/library
        if not s:
            return
        if Debugger.IS_DEBUGGING:
            print(f"[Debugger] {s}", *args, **kwargs)
