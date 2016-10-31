import datetime
date1 = "2017-01-11"
dt = datetime.datetime.strptime(date1, '%Y-%m-%d')
date = '{0:02}/{1}/{2}'.format(dt.month, dt.day, dt.year % 100)

dateEnd = '{0:02}/{1}/{2}'.format(dt.month, dt.day+1, dt.year)
print date,dateEnd