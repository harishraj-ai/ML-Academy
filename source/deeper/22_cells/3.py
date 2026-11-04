# Rolling, point-in-time features with a window frame: viewings in the 7 days up to and including each day
daily = pd.DataFrame({"house_id": [1] * 10, "day": range(1, 11), "views": [0, 2, 1, 0, 3, 1, 0, 0, 4, 1]})
daily.to_sql("daily", con, index=False)
q = """SELECT day, views,
              SUM(views) OVER (PARTITION BY house_id ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS views_7d,
              LAG(views) OVER (PARTITION BY house_id ORDER BY day) AS views_yesterday
       FROM daily"""
print(pd.read_sql(q, con).to_string(index=False))
