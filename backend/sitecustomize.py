import os
import typing

os.environ.setdefault("PYDANTIC_V1_USE_LEGACY_TYPING", "1")

ForwardRef = getattr(typing, "ForwardRef", None)
if ForwardRef is not None and hasattr(ForwardRef, "_evaluate"):
    original_evaluate = ForwardRef._evaluate

    def _patched_evaluate(self, globalns, localns, *args, **kwargs):
        if "recursive_guard" not in kwargs:
            if args:
                kwargs["recursive_guard"] = args[0]
                args = args[1:]
            else:
                kwargs["recursive_guard"] = set()
        return original_evaluate(self, globalns, localns, *args, **kwargs)

    ForwardRef._evaluate = _patched_evaluate
