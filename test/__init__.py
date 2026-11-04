# Ensure local src-based packages resolve during tests.
import sys

import sitecustomize  # noqa: F401

from . import test_mocks

sys.modules.setdefault("test_mocks", test_mocks)
