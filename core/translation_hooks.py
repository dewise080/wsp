import threading
from django.core.management import call_command


def trigger_auto_translate(model_label: str, pk, source_lang: str | None = None, target_lang: str | None = None):
    """Fire the auto_translate_models command asynchronously for a single object.

    Runs with --force and --pks to refresh translations after inline edits without
    blocking the request thread.
    """

    def _run():
        cmd_kwargs = {
            "model": model_label,
            "force": True,
            "verbosity": 0,
            "pks": [str(pk)],
        }
        if source_lang:
            cmd_kwargs["source_lang"] = source_lang
        if target_lang:
            cmd_kwargs["target_lang"] = target_lang
        try:
            call_command("auto_translate_models", **cmd_kwargs)
        except Exception:
            # Fail silently; primary save already succeeded.
            pass

    threading.Thread(target=_run, daemon=True).start()
