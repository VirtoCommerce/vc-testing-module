"""Shared fixtures for the WebAPI test suite.

Currently:
- `har_recorder` (autouse): captures every HTTP request/response during a test
  and writes a HAR 1.2 file to `har-output/<module>/<test_name>.har` on disk.
  Auth headers and cookies are redacted before serialization. The on-disk tree
  is uploaded as a workflow artifact so the network trace survives outside
  Allure.
"""

import re
from pathlib import Path

import pytest

from fixtures.har_recorder import HARRecorder
from fixtures.webapi_client import WebAPISession

# Characters that are invalid in filenames on Windows (and a superset is invalid
# on other OSes too) — replace with underscore before using a pytest node name
# as a filename. Parametrized nodes contain `[` and `]`, which are valid on
# every target FS, so we leave those alone for readability.
_INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*]')


def _module_folder(node_path: Path) -> str:
    """Return the `tests_webapi/<module>/` segment for a test's file path.

    Falls back to the direct parent folder name if the path doesn't contain
    a `tests_webapi` segment — e.g. someone dropped a test into an unusual
    location. We never want the HAR writer to be the thing that breaks a run.
    """
    parts = node_path.parts
    try:
        idx = parts.index("tests_webapi")
        # Expect layout tests_webapi/<module>/test_*.py — module is parts[idx+1].
        # If a test ever lives directly under tests_webapi/, parts[idx+1] is
        # the file itself; bucket those under `_root` so they don't pollute
        # a real module folder.
        candidate = parts[idx + 1]
        if candidate.endswith(".py"):
            return "_root"
        return candidate
    except (ValueError, IndexError):
        return node_path.parent.name or "_unknown"


@pytest.fixture(autouse=True)
def har_recorder(request, webapi_client: WebAPISession):
    """Record every webapi_client HTTP call for the duration of a test and
    write the HAR 1.2 file to `har-output/<module>/<test_name>.har`.

    On-disk layout mirrors the test-folder layout so a reviewer scanning the
    workflow artifact can jump straight to the module they care about without
    opening Allure. Written on both pass and fail.
    """
    recorder = HARRecorder()
    webapi_client.hooks["response"].append(recorder.hook)
    try:
        yield recorder
    finally:
        try:
            webapi_client.hooks["response"].remove(recorder.hook)
        except ValueError:
            pass  # hook already gone — don't fail teardown

        if recorder.has_entries():
            root_dir = Path(request.config.rootpath)
            module = _module_folder(Path(request.node.path))
            out_dir = root_dir / "har-output" / module
            out_dir.mkdir(parents=True, exist_ok=True)

            safe_name = _INVALID_FILENAME_CHARS.sub("_", request.node.name)
            (out_dir / f"{safe_name}.har").write_text(recorder.serialize(), encoding="utf-8")
