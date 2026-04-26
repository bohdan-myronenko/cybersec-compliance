# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-02-05T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **6552134**
- Distinct users: **1536866**
- Distinct source IPs: **1328745**

### Authentication
- Successful logins: **3008918**
- Failed logins: **3543216**
- Failure rate: **0.5408**
- Top failing IPs:  

  
  - 158.149.114.95 (12584)
  
  - 10.0.181.227 (10967)
  
  - 10.0.181.226 (10254)
  
  - 10.0.181.221 (7558)
  
  - 10.0.181.200 (7256)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


Across the 90-day window (2020-02-05), the environment shows a severe NIS2-relevant authentication control gap: MFA is effectively not deployed (0% coverage) for 1,536,866 users, including 0 identified admins with MFA. At the same time, authentication attempts exhibit a very high failure rate (54.08% failures), with the largest concentration of failures coming from a small set of top source IPs (e.g., 158.149.114.95 with 12,584 failures). While the metrics report no detected account takeovers and no “attack IP attempts”/distinct attack IPs, the combination of zero MFA coverage and elevated auth failure activity represents a critical compliance and security risk under NIS2 requirements for risk management and security of network and information systems.


### Security Findings


#### CRITICAL: MFA coverage is 0% for all users (major NIS2 control failure)

Multi-factor authentication (MFA) is not enabled for any of the 1,536,866 users in scope. This indicates a systemic failure to implement strong authentication controls, significantly increasing the likelihood and impact of credential compromise. The issue is consistent with historical periods where MFA coverage was also 0%.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0% (2019-11-07), 0.0% (2021-01-30)

- deviation: No improvement; remains at 0% across observed periods




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate technical and organizational measures for risk management and security of network and information systems, including strengthening authentication to reduce unauthorized access risk.



**Recommendation:** Implement MFA for all users with a phased rollout (prioritize privileged/admin and high-risk user groups first). Enforce MFA at authentication entry points (IdP/SSO) and block non-MFA sessions where feasible. Provide an auditable policy and completion target (e.g., 100% within 30–60 days) and validate via periodic reporting of enabled_users and coverage_pct.

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 54.1%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 54.1%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: High authentication failure rate suggests credential stuffing/brute-force risk

Authentication failures are high: 3,543,216 total failures vs 3,008,918 successes, yielding a fail rate of 54.08%. This is materially elevated compared to the 2019-11-07 baseline fail rate of 50.69% and also higher than the 2021-01-30 baseline of 64.21% (still, the current level remains concerning). Failures are concentrated in a small number of source IPs, indicating automated attempts or targeted activity. No account takeovers are detected, but the failure pattern still indicates increased exposure and potential ongoing attack attempts.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5408 (54.08%)

- baseline_value: 0.5069 (50.69%) on 2019-11-07; 0.6421 (64.21%) on 2021-01-30

- deviation: Up vs 2019-11-07 by ~3.39 percentage points; still very high overall




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Elevated authentication failure activity indicates insufficient preventive/detective controls to protect systems against unauthorized access attempts.



**Recommendation:** Triage top failure sources and implement/verify rate limiting and bot/credential-stuffing protections at the authentication layer (IdP/WAF/reverse proxy). Add detection rules for abnormal auth failure spikes per IP/user/device, and require MFA (once enabled) to reduce successful compromise. Review whether failures correlate with specific accounts, geographies, or time windows; then block or challenge the top offending IPs (e.g., 158.149.114.95 with 12,584 failures; 10.0.181.227 with 10,967; 10.0.181.226 with 10,254).

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/1536866 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### HIGH: No admins identified and no admin MFA coverage (privileged access governance gap)

The metrics show admins.count = 0 and with_mfa = 0, with last_review_date = 'unknown'. This prevents assurance that privileged accounts are identified, reviewed, and protected with MFA. Under NIS2, governance and accountability for access control are essential; missing/unknown admin visibility is itself a compliance and operational risk.


**Evidence:**

- metric: admins.count / admins.with_mfa / admins.last_review_date

- current_value: count=0, with_mfa=0, last_review_date=unknown

- baseline_value: count=0, with_mfa=0, last_review_date=unknown (2019-11-07; 2021-01-30)

- deviation: No improvement; admin governance visibility remains absent




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of demonstrable privileged access governance and protective controls (e.g., MFA for admins) undermines the organization’s ability to manage risks to network and information systems.



**Recommendation:** Establish a definitive privileged access inventory: define admin roles, map them to identities, and populate admins.count accurately. Enforce MFA for all privileged roles and set a measurable review cadence (e.g., monthly access review) with a recorded last_review_date. Produce an auditable report showing admin identities and MFA status.

---


#### MEDIUM: Authentication activity volume increased substantially vs 2019 baseline

The current period shows a much larger authentication event volume (frame.rows = 6,552,134) compared to 2019-11-07 (121,411). Distinct users also increased (1,536,866 vs 50,215). While growth may reflect scaling, the combination of scale and high failure rate increases the operational impact of any authentication weakness.


**Evidence:**

- metric: frame.rows / frame.distinct_users

- current_value: rows=6,552,134; distinct_users=1,536,866

- baseline_value: rows=121,411; distinct_users=50,215 (2019-11-07)

- deviation: Rows increased by ~53.96x; distinct users increased by ~30.6x




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): As system usage scales, risk management measures must scale accordingly; current authentication control posture (0% MFA) does not align with increased exposure.



**Recommendation:** Re-baseline security controls for the current scale: ensure rate limiting, anomaly detection, and MFA enforcement are tuned for higher volumes. Validate that monitoring thresholds and alerting remain effective at the new scale (e.g., per-IP/per-user failure thresholds).

---




### Positive Observations

- No account takeovers detected in the metrics (account_takeovers=0; users_with_takeover=0), suggesting either effective prevention/detection or that compromise attempts are not succeeding.

- No “attack_ip_attempts” or “attack_ip_distinct_ips” were recorded (both 0), which may indicate that the detection logic is not flagging these events as confirmed attacks—useful for tuning and validation rather than immediate incident response.




### Trend Analysis


**Degrading:** MFA coverage remains at 0.0% (no improvement from 2019-11-07 and 2021-01-30), representing a persistent degradation in security control maturity., Authentication failure rate is elevated vs 2019-11-07 (54.08% current vs 50.69% baseline).


**Stable:** Account takeover indicators are stable at 0 across the provided periods (no detected takeovers).





## Compliance Observations
### Access-Control Compliance (Article 21)

- The entity shall implement access control policies and asset management as part of cybersecurity risk-management measures. [NIS2 Art. 21(2)(i)]  
- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1536866). [METRICS mfa.coverage_pct; METRICS mfa.enabled_users; METRICS mfa.total_users]  
- Admin accounts are not evidenced: admins count is 0; with_mfa is 0; last_review_date is “unknown”. [METRICS admins.count; METRICS admins.with_mfa; METRICS admins.last_review_date]  
- Authentication failures total 3543216 with success_total 3008918; fail_rate is 0.5408. [METRICS auth_failures.total; METRICS auth_failures.success_total; METRICS auth_failures.fail_rate]  
- Top authentication failure IPs include 158.149.114.95 (12584) and 10.0.181.227 (10967). [METRICS auth_failures.top_ips]  
- If the entity does not comply with required measures, it shall take corrective measures without undue delay. [NIS2 Art. 21(4)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures