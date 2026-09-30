from datetime import date,time,datetime,timedelta,timezone
from calendar import monthrange
from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import utc_now
from app.modules.dashboard.repository import StatRepository
from app.modules.dashboard.schemas import (
  StatSchema,
  DaySchema,
  WeekSchema
)
from app.core.exceptions import (
  TimeCredentialsError,
  InvalidMonthError,
  RangeCredentialsError,
  InvalidRangeError
)

class StatService:
  """all services related to dashboard statistics."""

  @staticmethod
  async def _build_activity(start:date,end:date,rows)->list[WeekSchema]:
    """maps the activity schema witht the repo result"""
    #structure with schema
    act_map={
      date.fromisoformat(row.date): {
        "total_requests": row.total_requests,
        "blocked_requests": row.blocked_requests
      }
      for row in rows
    }
    #day wise activity
    days=[]
    curr=start
    while curr<=end:
      data=act_map.get(
        curr,
        {
          "total_requests":0,
          "blocked_requests":0
        }
      )
      days.append(DaySchema(
        date=curr,
        total_requests=data["total_requests"],
        blocked_requests=data["blocked_requests"]
      ))
      curr+=timedelta(days=1)
    #week wise activity
    week=[]
    curr=[]
    week_no=1
    for day in days:
      curr.append(day)
      if day.date.weekday()==6 or day.date==days[-1].date:
        week.append(WeekSchema(
          week=week_no,
          start_date=curr[0].date,
          end_date=curr[-1].date,
          days=curr
        ))
        week_no+=1
        curr=[]

    return week
    
  @staticmethod
  async def get_stats(
    user_id:int,
    db:AsyncSession,
    period:Literal["lifetime","monthly","range"]="lifetime",
    year:int|None=None,
    month:int|None=None,
    to_date:date|None=None,
    from_date:date|None=None
    )->StatSchema:
    """fetch and create the statistics for the dashboard"""
    today=utc_now().date() #makes the datetime into date

    # adjusting time period for queries
    if period == "lifetime":
      stats_start=None
      stats_end=None
      activity_start=today-timedelta(days=6)
      activity_end=today
    elif period == "monthly":
      if year is None or month is None:
        raise TimeCredentialsError()
      if month<1 or month>12:
        raise InvalidMonthError()
      start = date(year, month, 1)
      if month == 12:
        end = date(year + 1, 1, 1)
      else:
        end = date(year, month + 1, 1)
      activity_start=start
      stats_start=datetime.combine(
        start,
        time.min,
        tzinfo=timezone.utc
      )
      activity_end=end-timedelta(days=1)
      stats_end=datetime.combine( 
        end,
        time.min, 
        tzinfo=timezone.utc 
      )
    elif period=="range":
      if from_date is None or to_date is None:
        raise RangeCredentialsError()
      if from_date>to_date:
        raise InvalidRangeError()
      activity_start=from_date
      stats_start=datetime.combine( 
        from_date, 
        time.min, 
        tzinfo=timezone.utc
      )
      activity_end=to_date
      stats_end=datetime.combine(
        to_date+timedelta(days=1),
        time.min,
        tzinfo=timezone.utc
      )
    else:
      raise InvalidRangeError()

    # fetching statistical records    
    repo=StatRepository(db)
    log_stats=await repo.get_log_stats(
      user_id=user_id,
      start_date=stats_start,
      end_date=stats_end
    )
    key_stats=await repo.get_key_stats(user_id)
    activity_rows=await repo.get_activity(
      user_id=user_id,
      start_date=datetime.combine(activity_start,time.min,tzinfo=timezone.utc),
      end_date=datetime.combine(activity_end+timedelta(days=1),time.min,tzinfo=timezone.utc)
    )

    # error check
    print("ACTIVITY ROWS:")
    for row in activity_rows:
      print(row.date, type(row.date), row.total_requests, row.blocked_requests)

    # returning in form of schema
    return StatSchema(
      total_requests=log_stats.total_requests,
      allowed_requests=log_stats.total_requests-log_stats.blocked_requests,
      blocked_requests=log_stats.blocked_requests,
      block_rate=round(
        (log_stats.blocked_requests/log_stats.total_requests)*100
        if log_stats.total_requests>0
        else 0.0,
        2
      ),
      avg_latency_ms=round(log_stats.avg_latency_ms or 0.0,2),
      avg_threat_score=round(log_stats.avg_threat_score or 0.0,2),
      highest_threat_score=round(log_stats.highest_threat_score or 0.0,2),
      total_keys=key_stats.total_keys,
      active_keys=key_stats.active_keys,
      # activity builder for mapping to schema
      activity=await StatService._build_activity(
        activity_start,
        activity_end,
        activity_rows
      )
    )



