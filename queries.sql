-- name: kpis
SELECT COUNT(*) AS tickets,
       ROUND(100.0 * SUM(CASE WHEN resolved_at IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS resolved_pct,
       ROUND(AVG(resolution_hours), 1) AS avg_resolution_hours,
       ROUND(100.0 * AVG(sla_breached), 1) AS sla_breach_pct,
       ROUND(AVG(satisfaction), 2) AS avg_satisfaction
FROM tickets;

-- name: by_priority
SELECT priority,
       COUNT(*) AS tickets,
       ROUND(AVG(resolution_hours), 1) AS avg_hours,
       ROUND(100.0 * AVG(sla_breached), 1) AS sla_breach_pct
FROM tickets
GROUP BY priority
ORDER BY CASE priority WHEN 'Critical' THEN 1 WHEN 'High' THEN 2 WHEN 'Medium' THEN 3 ELSE 4 END;

-- name: top_problem_categories
SELECT category,
       COUNT(*) AS tickets,
       ROUND(AVG(resolution_hours), 1) AS avg_hours,
       ROUND(100.0 * AVG(sla_breached), 1) AS sla_breach_pct
FROM tickets
GROUP BY category
ORDER BY tickets DESC;

-- name: agent_performance
SELECT agent,
       COUNT(*) AS tickets_closed,
       ROUND(AVG(resolution_hours), 1) AS avg_hours,
       ROUND(100.0 * AVG(sla_breached), 1) AS sla_breach_pct,
       ROUND(AVG(satisfaction), 2) AS avg_satisfaction
FROM tickets
WHERE resolved_at IS NOT NULL
GROUP BY agent
ORDER BY avg_hours;

-- name: monthly_volume
SELECT created_month AS month,
       COUNT(*) AS tickets,
       ROUND(AVG(resolution_hours), 1) AS avg_hours
FROM tickets
GROUP BY created_month
ORDER BY created_month;

-- name: open_tickets_by_priority
SELECT priority, COUNT(*) AS open_tickets
FROM tickets
WHERE resolved_at IS NULL
GROUP BY priority
ORDER BY open_tickets DESC;
