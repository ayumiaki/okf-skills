# Update Log

## 2026-07-09
* **Structure**: Renamed `datasets/` to `data/` and `runbooks/` to `processes/` to align with produce-mode taxonomy.
* **Update**: Changed Orders database type from `Schema` to `Table` per taxonomy conventions.

## 2026-06-18
* **Operations**: Added the [Payment failures runbook](/processes/payment-failures.md)
  and the [Checkout conversion](/metrics/checkout-conversion.md) metric.
* **Schema**: Documented the [Orders database](/data/orders-db.md).

## 2026-06-16
* **Services**: Added [Orders API](/services/orders-api.md) and
  [Payments API](/services/payments-api.md); recorded the
  [event-driven decision](/decisions/event-driven.md).

## 2026-06-14
* **Creation**: Established the bundle with the [Auth API](/services/auth-api.md)
  service concept and the [OKF adoption decision](/decisions/use-okf.md).
