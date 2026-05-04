import datetime
from datetime import datetime as dt
from datetime import date

my_time = datetime.time(17, 35, 50, 1500)

print(type(my_time))
print(my_time)
print(my_time.second)

my_day = datetime.date(2026, 3, 5)

print(type(my_day))
print(my_day)
print(my_day.isoweekday())
# This is another cheeky way of getting the weekday
print(my_day.ctime()[:3])

# This will print today, no matter what data is in the date object.
print(my_day.today())
print(my_day.today().ctime()[:3])
print(f"Today ({my_day.today()}) is a {my_day.today().ctime()[:3]}")

# we can also import datetime from datetime to roll everything up into one
my_date = dt(2026, 5, 15, 22, 10, 15, 2500)

print(my_date)

birth = date(1988, 12, 3)

death = date(2095, 6, 19)

life = death - birth

print(f"Life in years: {(life.days / 365)-1:.0f}")

print(f"Life in days: {life.days:,}")

print(f"Life in hours: {(life.days * 24):,}")

print(f"Life in seconds: {(life.days * 24 * 60 * 60):,}")


# Current date
today_date = date.today()

# current minute
current_minutes = datetime.now().minute