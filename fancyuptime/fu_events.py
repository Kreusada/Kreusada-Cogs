SELECT_TEMP_GLOBAL = """
SELECT sum(quantity) 
FROM bot_stats_temp 
WHERE event = :event
GROUP BY event;
"""

SELECT_TEMP_SINGLE = """
SELECT sum(quantity) 
FROM bot_stats_temp 
WHERE event = :event AND guild_id = :guild_id
GROUP BY event;
"""
