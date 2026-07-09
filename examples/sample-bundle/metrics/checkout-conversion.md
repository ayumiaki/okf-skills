---
type: Metric
title: Checkout conversion
description: Share of started checkouts that end in a paid order.
tags: [kpi, growth, payments]
timestamp: "2026-06-18T12:00:00Z"
---

# Definition

```
checkout_conversion = orders[status = paid] / checkouts_started
```

Measured per hour from the [Orders API](/services/orders-api.md) checkout funnel;
the denominator is `checkout.started` events, the numerator is `order.paid`.

# Targets

| Window  | Target | Page on-call below |
|---------|--------|--------------------|
| Hourly  | ≥ 96%  | 90%                |
| 28-day  | ≥ 98%  | —                  |

# Watch-outs

A sudden drop usually means failed charges in
[Payments API](/services/payments-api.md), not buyer behaviour — start with the
[Payment failures runbook](/processes/payment-failures.md) before assuming a
funnel regression.
