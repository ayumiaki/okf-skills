---
type: Service
title: Auth API
description: Issues and verifies short-lived access tokens for internal services.
resource: https://github.com/scaccogatto/example/tree/main/services/auth
tags: [auth, security, platform]
timestamp: 2026-06-14T10:00:00Z
---

# Overview

Stateless HTTP service that issues signed JWTs and verifies them for other
internal services. Knowledge here is derived from the service source and its
README.

# Endpoints

| Method | Path             | Description                                  |
|--------|------------------|----------------------------------------------|
| `POST` | `/token`         | Exchange credentials for a short-lived JWT.  |
| `POST` | `/verify`        | Validate a JWT and return its claims.        |

# Dependencies

Token signing keys are governed by the [OKF adoption decision](/decisions/use-okf.md)
process for documenting platform choices.

# Citations

[1] [Service README](https://github.com/scaccogatto/example/tree/main/services/auth)
