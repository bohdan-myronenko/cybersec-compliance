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


Across the 90-day window (ending 2020-02-05), the environment shows a severe NIS2 compliance gap for authentication hardening: MFA is not enabled for any of 1,536,866 users (0% coverage), including zero identified admins with MFA. Authentication attempts also show a high failure rate (54.08% of 3,543,216 total auth events), with the highest-volume failures concentrated in a small set of source IPs (e.g., 158.149.114.95 with 12,584 failures; 10.0.181.227 with 10,967). While no account takeovers or “attack IP attempts” were detected by the provided metrics, the combination of zero MFA coverage and elevated auth failure activity represents a critical risk to resilience and incident prevention under NIS2.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

MFA coverage is effectively absent: 0 of 1,536,866 users have MFA enabled. This is a direct violation of the security expectation to protect network and information systems against unauthorized access using strong authentication mechanisms. The issue is persistent across historical periods (2019-11-07 and 2021-01-30 also show 0% MFA coverage), indicating a long-standing control failure rather than a transient outage.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0% (2019-11-07); 0.0% (2021-01-30)

- deviation: No improvement; control remains at 0% coverage across periods




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate technical and organizational measures (e.g., strong authentication/MFA) increases likelihood of unauthorized access and undermines resilience requirements.



**Recommendation:** Implement MFA for all users with a phased rollout (start with privileged/admin accounts and high-risk user groups), enforce MFA at authentication policy level, and require re-enrollment where needed. Provide an auditable control report showing % MFA enabled by user cohort and system.

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


#### CRITICAL: No admins identified and no admin MFA coverage

The metrics report admins.count = 0 and admins.with_mfa = 0 with last_review_date = 'unknown'. This suggests either missing inventory/telemetry for privileged accounts or that privileged accounts are not being tracked for MFA compliance. Under NIS2, privileged access must be tightly controlled and monitored; lack of visibility itself is a compliance and operational risk.


**Evidence:**

- metric: admins.count / admins.with_mfa

- current_value: 0 / 0

- baseline_value: 0 / 0 (2019-11-07; 2021-01-30)

- deviation: No change; privileged account governance and MFA enforcement cannot be validated




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inability to demonstrate privileged access controls and MFA enforcement weakens the required security measures against unauthorized access.



**Recommendation:** Create/restore a privileged access inventory (admins/roles) and ensure MFA status is collected for those accounts. Set a recurring review process with a recorded last_review_date and evidence artifacts (role membership export + MFA status report).

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


#### HIGH: High authentication failure rate (54.08%) indicates potential brute force/credential stuffing

Auth failures are high: 3,543,216 total auth events with a fail_rate of 0.5408 (54.08%). While the baseline in 2019-11-07 was 50.69% and in 2021-01-30 was 64.21%, the current period still reflects a persistently elevated failure rate. The top failure sources are concentrated in a few IPs (e.g., 158.149.114.95: 12,584; 10.0.181.227: 10,967; 10.0.181.226: 10,254), consistent with automated attempts. No account takeovers were detected, but the lack of MFA makes successful compromise more likely if credentials are valid.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5408 (54.08%)

- baseline_value: 0.5069 (2019-11-07); 0.6421 (2021-01-30)

- deviation: Current is +3.39 percentage points vs 2019-11-07; below 2021-01-30 but still high




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Elevated authentication failures increase the risk of unauthorized access and indicate insufficient preventive controls (e.g., strong authentication, rate limiting, anomaly detection).



**Recommendation:** Enable/verify rate limiting and lockout/backoff policies, add detection and alerting for credential-stuffing/brute-force patterns, and correlate top failure IPs with known services (to rule out internal misconfigurations). Prioritize remediation for the top source IPs and implement MFA enforcement to reduce impact of compromised credentials.

---


#### MEDIUM: No detected account takeovers despite high failure volume (potential detection gap)

The metrics report account_takeovers = 0 and users_with_takeover = 0, and attack_ip_attempts = 0 with attack_ip_distinct_ips = 0. Given the high auth failure volume and concentrated top IPs, this may indicate either (a) no successful compromise occurred, or (b) the detection logic for takeovers/attack IPs is not functioning or is too narrow. This uncertainty affects confidence in threat monitoring effectiveness.


**Evidence:**

- metric: auth_failures.account_takeovers / auth_failures.attack_ip_attempts

- current_value: 0 / 0

- baseline_value: 0 / 0 (2019-11-07; 2021-01-30)

- deviation: No change; inability to validate takeover detection effectiveness




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): If monitoring/detection is incomplete, the organization may not be able to prevent or respond effectively to unauthorized access attempts.



**Recommendation:** Validate takeover detection by running test cases (simulated compromised credentials in a safe environment), review detection rules/thresholds, and ensure logs include required signals (session anomalies, impossible travel, privilege changes). Document detection coverage for NIS2 audit evidence.

---




### Positive Observations

- No account takeovers detected in the provided metrics (account_takeovers = 0; users_with_takeover = 0), suggesting either limited successful compromise or effective containment at the account level.

- Attack-IP attempt counters are also zero (attack_ip_attempts = 0), which may indicate that the observed failures are not being classified as active attacks by the current logic—useful as a starting point for tuning rather than immediate evidence of compromise.




### Trend Analysis


**Degrading:** MFA coverage remains at 0.0% (no improvement from 2019-11-07 and 2021-01-30), representing a persistent degradation in security posture relative to NIS2 expectations.


**Stable:** Account takeover indicators remain at 0 across periods (2019-11-07, 2021-01-30, and current), suggesting stable (or consistently unmeasured) takeover detection outcomes., Admins inventory remains unreported/zero across periods (admins.count = 0; with_mfa = 0), indicating stable but problematic visibility.





## Compliance Observations
## Access-Control Compliance (Cybersecurity Risk-Management)

- The entity shall implement access control policies as part of human resources security and asset management. [NIS2 Art. 21(2)(i)]  
- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1536866). [METRICS mfa]  
- Administrators count is 0; administrators with MFA is 0; last_review_date is “unknown”. [METRICS admins]  
- Authentication failures total 3,543,216 with success_total 3,008,918 (fail_rate 0.5408). [METRICS auth_failures]  
- The entity shall take corrective measures without undue delay if it does not comply with the measures in paragraph 2. [NIS2 Art. 21(4)]  
- No data available in the provided evidence for access-control policy existence, effectiveness assessments, or cryptography/encryption procedures. [No data available in the provided evidence]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures