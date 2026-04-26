# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-08-03T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **6531204**
- Distinct users: **1529697**
- Distinct source IPs: **1234264**

### Authentication
- Successful logins: **2908013**
- Failed logins: **3623191**
- Failure rate: **0.5548**
- Top failing IPs:  

  
  - 23.137.225.33 (128728)
  
  - 10.0.181.232 (23631)
  
  - 109.203.1.148 (19053)
  
  - 10.0.181.229 (16826)
  
  - 10.0.181.228 (16411)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


For the 90-day window ending 2020-08-03, the environment shows a severe and persistent MFA non-compliance posture: MFA is effectively disabled for all users (0/1,529,697 enabled; 0.0% coverage). Authentication activity is high with a fail rate of 55.48% (3,623,191 total failures vs 2,908,013 successes), and the same top source IP (23.137.225.33) remains dominant across periods, indicating ongoing repeated authentication attempts. While no account takeovers or explicit “attack IP attempts” are detected in the computed metrics, the combination of zero MFA coverage and elevated authentication failure rates represents a critical risk to NIS2-aligned security of network and information systems.


### Security Findings


#### CRITICAL: MFA coverage is 0% for all users (system-wide non-compliance)

Multi-factor authentication (MFA) is not enabled for any user accounts. With 1,529,697 distinct users and 0 enabled users, the organization lacks a key compensating control for account compromise risk. This is a persistent condition across multiple historical baselines (0% coverage in all provided periods), indicating a systemic configuration or governance failure rather than a transient outage.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0

- baseline_value: 0.0

- deviation: No change; persistent 0.0% coverage across all compared periods (2019-11-07, 2020-02-05, 2020-05-05, and current).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate technical and organizational measures (e.g., strong authentication) increases the likelihood of unauthorized access and undermines the security of network and information systems.



**Recommendation:** Implement MFA for all user accounts, starting with privileged/admin and externally accessible authentication flows. Enforce MFA at identity provider level (not per-application), require re-authentication for existing sessions, and document exceptions (if any) with compensating controls and time-bound remediation. Provide an auditable rollout plan and target date for 100% coverage.

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 55.5%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 55.5%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: High authentication failure rate (~55%) indicates persistent unsuccessful login attempts

The authentication failure rate is 55.48% (3,623,191 failures vs 2,908,013 successes). This level of failure suggests either widespread user misconfiguration/incorrect credentials, automated credential stuffing/brute-force attempts, or integration issues. Even though computed metrics show 0 account takeovers and 0 detected “attack IP attempts,” the volume and rate of failures materially increase exposure and operational risk.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5548

- baseline_value: 0.5469

- deviation: Increased by ~0.79 percentage points vs 2020-05-05 (55.48% vs 54.69%).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Elevated authentication failures indicate insufficient protective measures and monitoring to prevent or detect unauthorized access attempts.



**Recommendation:** Triage the cause of failures: (1) segment failures by user population (privileged vs standard), geography, and application; (2) correlate with identity provider logs for error codes (invalid password, locked account, MFA required, etc.); (3) enable/verify rate limiting, progressive throttling, and account lockout policies; (4) deploy alerting for abnormal failure spikes per IP/user; (5) validate that MFA enforcement is actually required on all relevant flows (since current MFA coverage is 0%).

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/1529697 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### HIGH: Top source IP remains dominant across periods, suggesting persistent automated attempts

The IP 23.137.225.33 is the top source of authentication failures in the current period (128,728 attempts). It was also the top IP in the 2020-05-05 baseline (63,681 attempts), indicating persistence and potentially increasing activity. This pattern is consistent with repeated automated login attempts from a single source or a small set of sources.


**Evidence:**

- metric: auth_failures.top_ips[0].count

- current_value: 128728

- baseline_value: 63681

- deviation: Approximately +102% vs 2020-05-05 (128,728 vs 63,681).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent suspicious authentication activity indicates inadequate detection/prevention controls for unauthorized access attempts.



**Recommendation:** Investigate 23.137.225.33 and the other top IPs (10.0.181.232, 109.203.1.148, 10.0.181.229, 10.0.181.228). Determine whether these are legitimate internal services, NAT gateways, or hostile sources. Apply targeted controls: IP reputation checks, firewall/WAF rules for external endpoints, and stricter throttling for high-failure sources. If internal, fix routing/logging to ensure failures are correctly attributed and protected.

---


#### MEDIUM: No admins identified and no MFA for admins (governance/visibility gap)

The computed metrics report admins.count = 0 and admins.with_mfa = 0 with last_review_date = 'unknown'. This is likely a data quality/visibility issue (e.g., privileged accounts not tagged as admins) or a governance gap where privileged roles are not being tracked. Under NIS2, privileged access management and review processes must be demonstrable.


**Evidence:**

- metric: admins.count

- current_value: 0

- baseline_value: 0

- deviation: No change; remains 0 across all provided periods, suggesting persistent reporting/labeling gap.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of auditable privileged access governance and review evidence can prevent demonstrating that appropriate access control measures are in place.



**Recommendation:** Ensure privileged accounts are correctly identified and reported (e.g., map IdP roles/groups to 'admin' classification). Establish an admin access review cadence with recorded last_review_date, and require MFA for all privileged roles immediately (even if standard users are still in rollout).

---




### Positive Observations

- No account takeovers detected in computed metrics (account_takeovers = 0; users_with_takeover = 0), suggesting either effective prevention/detection so far or limited visibility into takeover signals.

- No explicit 'attack_ip_attempts' or 'attack_ip_distinct_ips' detected (both 0), which may indicate that automated attack classification is not triggered or that attempts are not meeting detection thresholds—still worth validating.




### Trend Analysis


**Degrading:** Authentication failure rate increased slightly vs 2020-05-05 (54.69% -> 55.48%)., Top failing IP 23.137.225.33 increased substantially vs 2020-05-05 (63,681 -> 128,728 failures).


**Stable:** MFA coverage remained at 0.0% across all compared periods (persistent non-compliance)., Account takeover indicators remained at 0 across compared periods.





## Compliance Observations
## Access-control compliance (Article 21)

- The entity shall implement access control policies as part of cybersecurity risk-management measures. [NIS2 Art. 21(2)(i)]

- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1529697). [METRICS mfa]

- No administrator accounts are recorded (admins.count: 0; admins.with_mfa: 0). [METRICS admins]

- Authentication failures total 3,623,191 with success_total 2,908,013 (fail_rate 0.5548). [METRICS auth_failures]

- No account takeovers are recorded (account_takeovers: 0; users_with_takeover: 0). [METRICS auth_failures]

- No data available in the provided evidence for access-control policy effectiveness assessments. [NIS2 Art. 21(2)(f)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures