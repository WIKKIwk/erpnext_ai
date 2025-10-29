from __future__ import annotations

import frappe

from erpnext_ai.erpnext_ai.doctype.ai_settings.ai_settings import AISettings
from erpnext_ai.services.report_runner import generate_admin_report


def generate_daily_admin_summary() -> None:
    try:
        settings = AISettings.get_settings()
    except (frappe.DoesNotExistError, frappe.ValidationError):
        return

    api_key = getattr(settings, "_resolved_api_key", None)
    if not api_key:
        return

    previous_user = frappe.session.user
    try:
        frappe.set_user("Administrator")
        generate_admin_report(title="Daily AI Admin Summary", days=1)
    except Exception as exc:  # pragma: no cover - scheduler safety
        frappe.log_error(str(exc), "AI Daily Summary")
    finally:
        frappe.set_user(previous_user or "Administrator")
