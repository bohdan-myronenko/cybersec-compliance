# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-11-01T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **9309939**
- Distinct users: **1596182**
- Distinct source IPs: **1237098**

### Authentication
- Successful logins: **2822319**
- Failed logins: **6487620**
- Failure rate: **0.6968**
- Top failing IPs:  

  
  - 10.3.205.197 (443523)
  
  - 10.3.205.196 (257018)
  
  - 10.3.205.195 (236489)
  
  - 10.3.205.194 (177160)
  
  - 10.3.205.193 (152239)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


For the 90-day window ending 2020-11-01, the organization shows a severe NIS2 compliance gap in authentication hardening: MFA coverage is 0% across 1,596,182 users and there are 0 recorded admins with MFA. In parallel, authentication attempts exhibit a very high failure rate (69.68% failures vs 55.48% in the prior period), indicating either widespread misconfiguration, credential stuffing, or other authentication issues. While no account takeovers or “attack IP attempts” are detected by the current metrics, the combination of zero MFA and rising failure rates materially increases the likelihood and impact of account compromise under NIS2 requirements.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any user accounts. This creates a direct control failure for NIS2 expectations around ensuring security of network and information systems, particularly for authentication and access control. With 0% MFA coverage, the risk of credential compromise leading to unauthorized access is substantially higher.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement; remains at 0.0% across all provided historical periods




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate measures to ensure security of network and information systems, including access control and authentication protections; MFA absence increases likelihood of unauthorized access.



**Recommendation:** Implement MFA for all users with a phased rollout that prioritizes privileged accounts first. Enforce MFA at identity provider level (e.g., SSO) and block sign-in for accounts that do not meet MFA policy. Provide an exception process with time-bound approvals and compensating controls (e.g., device trust, conditional access). Target: 100% MFA coverage within a defined remediation SLA (e.g., 30–60 days).

---


#### CRITICAL: No admins recorded; privileged access not demonstrably protected with MFA

The dataset reports 0 admins and 0 admins with MFA, with last_review_date marked as 'unknown'. Even if the admin population is managed elsewhere, the absence of recorded privileged accounts and MFA status prevents demonstrating compliance and increases the likelihood that privileged access is not adequately protected.


**Evidence:**

- metric: admins.count / admins.with_mfa

- current_value: 0 / 0

- baseline_value: 0 / 0

- deviation: No change; privileged account MFA posture cannot be validated




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inability to evidence adequate access control for privileged roles undermines the security measures expected for protecting network and information systems.



**Recommendation:** Establish and maintain an authoritative inventory of privileged accounts (admins) and ensure MFA is enforced for all privileged roles. Update reporting so admins are correctly identified and include last review dates. Conduct an immediate privileged access review and require MFA for any account with elevated permissions (including break-glass accounts).

---


#### HIGH: Authentication failure rate increased sharply (possible credential stuffing or systemic auth issues)

The authentication failure rate is extremely high and has worsened versus the previous baseline. Current fail_rate is 69.68% (6,487,620 total failures; 2,822,319 successes), compared to 55.48% previously. This indicates a significant increase in unsuccessful authentication attempts, which can be consistent with credential stuffing, misconfigured clients, or degraded authentication flows.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6968 (69.68%)

- baseline_value: 0.5548 (55.48%)

- deviation: Increase of ~14.20 percentage points (~25.6% relative increase)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Elevated authentication failures indicate potential weaknesses in access security and may reflect ongoing attack attempts or control misconfigurations that increase risk of unauthorized access.



**Recommendation:** Perform an authentication failure investigation focused on: (1) top source IPs and user agents, (2) whether failures correlate with specific endpoints/tenants, and (3) whether failures are due to wrong credentials vs. policy blocks. Implement/verify rate limiting, account lockout/step-up challenges, and conditional access for suspicious patterns. Ensure logs capture enough fields to distinguish credential errors from MFA/policy failures. Validate whether the 'attack_ip_attempts' metric is correctly configured; currently it reports 0, which may mask detection gaps.

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 69.7%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 69.7%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: Top failing source IPs are concentrated in internal/private ranges

The top IPs by failure count are concentrated around 10.3.205.193–10.3.205.197, suggesting either internal systems generating repeated failed authentication attempts (e.g., misconfigured service accounts, broken integrations) or internal traffic being used for automated attempts. Concentration increases the likelihood of a systemic issue and provides a clear target for remediation.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: 10.3.205.197=443,523; 10.3.205.196=257,018; 10.3.205.195=236,489; 10.3.205.194=177,160; 10.3.205.193=152,239

- baseline_value: Different top IPs observed previously (e.g., 23.137.225.33=128,728)

- deviation: Shift in top sources; current concentration in 10.3.205.x private range




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Concentrated repeated authentication failures indicate inadequate monitoring/response and potential weaknesses in access control and identity hygiene.



**Recommendation:** Identify which systems correspond to the 10.3.205.x sources and review their authentication configuration (service principals, API clients, scheduled jobs). Temporarily block or quarantine offending sources if they are not expected. Add detection rules for anomalous internal auth failure patterns and require step-up authentication or stronger controls for affected integrations.

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/1596182 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### MEDIUM: No detected account takeovers despite very high failure volume

The metrics report 0 account_takeovers and 0 users_with_takeover while failures are extremely high. This may indicate that takeover detection logic is incomplete or that the environment is experiencing mostly credential errors rather than successful compromise. Either way, the lack of detected takeovers reduces confidence in threat detection coverage.


**Evidence:**

- metric: auth_failures.account_takeovers / users_with_takeover

- current_value: 0 / 0

- baseline_value: 0 / 0

- deviation: No change; detection coverage may be insufficient given high fail_rate




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient detection/response capability can undermine the effectiveness of security measures expected for protecting systems and accounts.



**Recommendation:** Validate and tune account takeover detection: ensure signals include impossible travel, new device/session anomalies, password reset/change events, and suspicious MFA bypass attempts. Confirm that 'attack_ip_attempts' and takeover analytics are correctly wired to identity logs. Produce a sample-based validation (e.g., review last N suspicious events) to confirm detection accuracy.

---




### Positive Observations

- No account takeovers detected in the available metrics (account_takeovers=0; users_with_takeover=0), suggesting either limited successful compromise or gaps in detection that can be validated.

- Authentication activity is measurable and attributable at scale (frame.rows=9,309,939; distinct_users=1,596,182; distinct_src_ips=1,237,098), enabling targeted investigation of failure sources.




### Trend Analysis


**Degrading:** Authentication failure rate increased from 55.48% (baseline period) to 69.68% currently (increase of ~14.20 percentage points)., Total authentication failures increased from 3,623,191 (baseline) to 6,487,620 currently (increase of 2,864,429).


**Stable:** MFA coverage remains at 0.0% across all compared periods (no improvement)., Account takeover indicators remain at 0 (account_takeovers=0; users_with_takeover=0) across periods.





## Compliance Observations
### Access-Control Compliance (Cybersecurity Risk-Management)

- The entity must implement appropriate and proportionate access-control-related measures to manage risks to network and information systems security [NIS2 Art. 21(1)].  
- Access-control measures must be based on an all-hazards approach protecting network and information systems and the physical environment [NIS2 Art. 21(2)].  
- The entity must establish human resources security, access control policies, and asset management [NIS2 Art. 21(2)(i)].  
- The entity must use multi-factor authentication or continuous authentication solutions, where applicable [NIS2 Art. 21(2)(j)].  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1596182) [METRICS mfa].  
- Authentication failures occurred: total 6487620; success_total 2822319; fail_rate 0.6968 [METRICS auth_failures].  
- No data indicates account takeovers (account_takeovers: 0; users_with_takeover: 0) [METRICS auth_failures].  
- If the entity does not comply with required measures, it must take corrective measures without undue delay [NIS2 Art. 21(4)].

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures