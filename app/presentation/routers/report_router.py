from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Query, Response
from app.application.use_cases.report_use_cases import ReportUseCases
from app.presentation.schemas.report_schema import ReportSummary, AccessReportItem
from app.presentation.dependencies.audit_dependencies import get_report_use_cases
from app.presentation.dependencies.auth_dependencies import require_ti_or_admin
from app.domain.entities.user import User
from app.infrastructure.services.report_generator import ReportGenerator

router = APIRouter(prefix="/reports", tags=["Reports"])


# Reusable dependency for common report parameters
def get_report_common_params(
    start_date: datetime = Query(..., description="Start date (ISO format)"),
    end_date: datetime = Query(..., description="End date (ISO format)"),
    report_use_cases: ReportUseCases = Depends(get_report_use_cases),
    current_user: User = Depends(require_ti_or_admin),
):
    """Reusable dependency for report date range and authorization"""
    return {
        "start_date": start_date,
        "end_date": end_date,
        "report_use_cases": report_use_cases,
        "current_user": current_user,
    }


@router.get("/summary", response_model=ReportSummary)
async def get_summary_report(params=Depends(get_report_common_params)):
    """
    Get a summary report for a date range.

    Returns aggregated statistics about equipment access
    during the specified period.
    """
    return params["report_use_cases"].generate_summary_report(
        params["start_date"], params["end_date"]
    )


@router.get("/equipment", response_model=List[AccessReportItem])
async def get_equipment_report(params=Depends(get_report_common_params)):
    """
    Get a detailed equipment access report.

    Returns all equipment access records between the specified dates.
    """
    return params["report_use_cases"].generate_equipment_report(
        params["start_date"], params["end_date"]
    )


@router.get("/equipment/pdf")
async def get_equipment_report_pdf(params=Depends(get_report_common_params)):
    """
    Generate a detailed equipment access report in PDF format.
    """
    start, end = params["start_date"], params["end_date"]
    report_use_cases = params["report_use_cases"]

    summary = report_use_cases.generate_summary_report(start, end)
    report_data = report_use_cases.generate_equipment_report(start, end)

    headers = [
        "equipment_name",
        "user_full_name",
        "entry_time",
        "exit_time",
        "status",
        "days_inside",
    ]

    pdf_bytes = ReportGenerator.generate_pdf_report(
        title="Equipment Access Report - Hospital San Rafael",
        data=report_data,
        headers=headers,
        summary=summary,
    )

    filename = f"equipment_report_{start.date()}_{end.date()}_{datetime.now().strftime('%H%M%S')}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/equipment/excel")
async def get_equipment_report_excel(params=Depends(get_report_common_params)):
    """
    Generate a detailed equipment access report in Excel format.
    """
    start, end = params["start_date"], params["end_date"]
    report_use_cases = params["report_use_cases"]

    summary = report_use_cases.generate_summary_report(start, end)
    report_data = report_use_cases.generate_equipment_report(start, end)

    headers = [
        "equipment_name",
        "user_full_name",
        "entry_time",
        "exit_time",
        "status",
        "days_inside",
    ]

    excel_bytes = ReportGenerator.generate_excel_report(
        title="Equipment Access Report - Hospital San Rafael",
        data=report_data,
        headers=headers,
        summary=summary,
    )

    filename = f"equipment_report_{start.date()}_{end.date()}_{datetime.now().strftime('%H%M%S')}.xlsx"

    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/user-activity")
async def get_user_activity_report(params=Depends(get_report_common_params)):
    """
    Get a report of user activity within a given date range.
    """
    return params["report_use_cases"].generate_user_activity_report(
        params["start_date"], params["end_date"]
    )
