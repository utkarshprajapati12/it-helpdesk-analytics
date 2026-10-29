"""Step 1: Create a sample IT helpdesk ticket dataset (tickets.csv).

Real helpdesk exports (from ServiceNow, Freshdesk, Jira) look like this,
so the analysis works the same way on real data later.
"""
import random
from datetime import datetime, timedelta

import pandas as pd

random.seed(7)
N_TICKETS = 1000

CATEGORIES = {
    "Password reset": ("Identity", ["Forgot password, account locked", "Cannot log in after password change"]),
    "Email issue": ("Email", ["Outlook not syncing", "Cannot send email with attachment"]),
    "VPN / Remote access": ("Network", ["VPN keeps disconnecting", "Cannot connect to office VPN from home"]),
    "Wi-Fi": ("Network", ["No internet at desk", "Wi-Fi drops every hour"]),
    "Printer": ("Hardware", ["Printer offline on floor 2", "Cannot print from laptop"]),
    "Slow computer": ("Hardware", ["Laptop very slow since update", "Blue screen on startup"]),
    "Software install": ("Software", ["Need Excel installed", "Software license expired"]),
}
CATEGORY_WEIGHTS = [25, 15, 12, 10, 12, 13, 13]

PRIORITIES = ["Low", "Medium", "High", "Critical"]
PRIORITY_WEIGHTS = [35, 40, 20, 5]
# Typical hours to resolve each priority
BASE_HOURS = {"Low": 40, "Medium": 16, "High": 6, "Critical": 3}
# Some categories take longer to fix
CATEGORY_FACTOR = {"VPN / Remote access": 1.6, "Slow computer": 1.4, "Printer": 0.7, "Password reset": 0.5}

AGENTS = ["Ravi", "Anjali", "Mohit", "Priya", "Sameer"]

start = datetime(2026, 1, 1)
rows = []
for i in range(1, N_TICKETS + 1):
    created = start + timedelta(minutes=random.randint(0, 60 * 24 * 280))
    category = random.choices(list(CATEGORIES), weights=CATEGORY_WEIGHTS)[0]
    team, descriptions = CATEGORIES[category]
    priority = random.choices(PRIORITIES, weights=PRIORITY_WEIGHTS)[0]

    # 2% of tickets are still open (no resolved time)
    if random.random() < 0.02:
        resolved = None
        satisfaction = None
    else:
        factor = CATEGORY_FACTOR.get(category, 1.0)
        hours = BASE_HOURS[priority] * factor * random.uniform(0.5, 1.8)
        resolved = (created + timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
        satisfaction = random.choices([1, 2, 3, 4, 5], weights=[5, 8, 17, 35, 35])[0]

    rows.append({
        "ticket_id": f"INC{100000 + i}",
        "created_at": created.strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "team": team,
        "description": random.choice(descriptions),
        "priority": priority,
        "agent": random.choice(AGENTS),
        "resolved_at": resolved,
        "satisfaction": satisfaction,
    })

pd.DataFrame(rows).to_csv("tickets.csv", index=False)
print(f"Saved {N_TICKETS} tickets to tickets.csv")
