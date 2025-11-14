"""Date calculation service."""

from datetime import datetime, timedelta
from typing import Tuple


class DateCalculator:
    """Calculates dates based on week information."""
    
    @staticmethod
    def calculate_title_date(year: int, month: int, week: int) -> str:
        """Calculate title date string.
        
        Args:
            year: Year (YYYY)
            month: Month (1-12)
            week: Week (1-5)
        
        Returns:
            Formatted string like "11월 1주차"
        """
        return f"{month}월 {week}주차"
    
    @staticmethod
    def calculate_payment_date(year: int, month: int, week: int) -> str:
        """Calculate payment date string.
        
        Args:
            year: Year (YYYY)
            month: Month (1-12)
            week: Week (1-5)
        
        Returns:
            Formatted string like "24.11.15" (YY.MM.DD)
        """
        friday = DateCalculator.get_week_friday(year, month, week)
        return friday.strftime("%y.%m.%d")
    
    @staticmethod
    def calculate_date_range(year: int, month: int, week: int) -> str:
        """Calculate date range string.
        
        Args:
            year: Year (YYYY)
            month: Month (1-12)
            week: Week (1-5)
        
        Returns:
            Formatted string like "11.06 ~ 11.12"
        """
        start_date, end_date = DateCalculator.get_week_range(year, month, week)
        return f"{start_date.strftime('%m.%d')} ~ {end_date.strftime('%m.%d')}"
    
    @staticmethod
    def get_week_friday(year: int, month: int, week: int) -> datetime:
        """Get Friday date for the week.
        
        Args:
            year: Year (YYYY)
            month: Month (1-12)
            week: Week (1-5)
        
        Returns:
            Friday date for the week
        """
        first_day = datetime(year, month, 1)
        
        first_monday = first_day + timedelta(days=(7 - first_day.weekday()) % 7)
        if first_day.weekday() == 0:
            first_monday = first_day
        
        week_start = first_monday + timedelta(weeks=week - 1)
        friday = week_start + timedelta(days=4)
        
        return friday
    
    @staticmethod
    def get_week_range(year: int, month: int, week: int) -> Tuple[datetime, datetime]:
        """Get week date range (previous Tuesday to current Monday).
        
        Args:
            year: Year (YYYY)
            month: Month (1-12)
            week: Week (1-5)
        
        Returns:
            Tuple of (start_date, end_date)
        """
        friday = DateCalculator.get_week_friday(year, month, week)
        
        if month == 11 and week == 1:
            start_date = datetime(year, 10, 29)
        else:
            previous_tuesday = friday - timedelta(days=10)
            start_date = previous_tuesday
        
        current_monday = friday - timedelta(days=4)
        end_date = current_monday
        
        return (start_date, end_date)

