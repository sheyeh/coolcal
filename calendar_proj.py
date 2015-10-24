import calendar
import datetime
import os
from bottle import route, run, SimpleTemplate

PORT = int(os.environ.get("PORT", 5000))

CENTER_START = '<center><font face="verdana">'
CENTER_END = "</center></font>"
PREV_NEXT = SimpleTemplate(
    '<font size="5"><a href="{{prev}}">{{prev}}</a> {{year}} <a href="{{next}}">{{next}}</a></font>'
)
LINK_MONTH = SimpleTemplate(
    '<a href="{{year}}/{{month_num}}">{{month_name}}</a>'
)
LINK_YEAR = SimpleTemplate(
    '<a href="../{{year}}">{{year}}</a>'
)

def year_cal_with_links(cal, year):
    for month_num, month_name in enumerate(calendar.month_name):
        if month_num:
            cal = cal.replace(month_name, LINK_MONTH.render(year=year, month_num=month_num, month_name=month_name))
    return cal

def month_cal_with_links(cal, year):
    cal = cal.replace(" " + str(year), " " + LINK_YEAR.render(year=year))
    return cal

def repad_respace(cal):
    cal = cal.replace('cellpadding="0"', 'cellpadding="2"')
    cal = cal.replace('cellspacing="0"', 'cellspacing="2"')
    return cal

@route('/')
@route('/<year:int>')
def cal_year(year=None):
    if year is None:
        year = datetime.date.today().year
    year = max((year, 2))
    yearly_cal = CENTER_START
    yearly_cal += calendar.HTMLCalendar(6).formatyear(theyear=year)
    bottom = PREV_NEXT.render(next=year+1, year=year, prev=year-1)
    yearly_cal +=  "<br>" + bottom
    yearly_cal += CENTER_END
    yearly_cal = year_cal_with_links(yearly_cal, year)
    return repad_respace(yearly_cal)

@route('/<year:int>/<month:int>')
def cal_month(year, month):
    monthly_cal = CENTER_START
    monthly_cal += calendar.HTMLCalendar(6).formatmonth(themonth=month, theyear=year)
    monthly_cal += CENTER_END
    monthly_cal = month_cal_with_links(monthly_cal, year)
    return repad_respace(monthly_cal)

if __name__ == "__main__":
    run(host='0.0.0.0', port=PORT, debug=True, reloader=True)