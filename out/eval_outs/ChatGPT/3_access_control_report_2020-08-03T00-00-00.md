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


For the 90-day window ending 2020-08-03, the organization shows a severe authentication control gap: MFA is effectively not deployed (0% coverage across 1,529,697 users, including 0/0 admins with MFA). At the same time, authentication failure activity is high (fail rate 55.48% with 3,623,191 total failures vs 2,908,013 successes), indicating either widespread incorrect authentication attempts or potential brute-force/credential-stuffing patterns, even though the dataset reports 0 detected attack-IP attempts and 0 account takeovers. Compared with prior periods, the MFA posture remains unchanged (0% coverage), while the authentication failure rate has slightly increased versus the immediately prior baseline (55.48% vs 54.69%). Overall, this is a critical NIS2 compliance risk driven by missing essential access control measures.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any user accounts. This is a direct violation of the intent of NIS2 security measures requiring appropriate authentication controls for network and information systems. The metric indicates enabled_users=0 out of total_users=1,529,697, resulting in 0.0% MFA coverage. This leaves the environment vulnerable to credential compromise and increases the likelihood and impact of unauthorized access.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0% (2020-05-05), 0.0% (2020-02-05), 0.0% (2019-11-07)

- deviation: No improvement across all compared periods; remains at 0.0%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient access control/authentication measures (no MFA) increases risk of unauthorized access and undermines required security of network and information systems.



**Recommendation:** Implement MFA for all users with a phased rollout prioritizing privileged accounts first. Enforce MFA at authentication layer (IdP) and block sign-in for accounts without MFA after a defined deadline. Provide an auditable control report showing enabled_users and coverage_pct reaching >95% within 30–60 days, and 100% for admins immediately.

---


#### CRITICAL: No MFA for administrators (privileged access not protected)

The dataset indicates admins.count=0 and with_mfa=0, which strongly suggests either (a) privileged accounts are not correctly classified in telemetry or (b) privileged accounts exist but are not protected by MFA. Regardless, the absence of MFA coverage for administrative access is a critical access-control weakness because privileged accounts are the highest-impact targets.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0 (with_mfa=0, admins.count=0)

- baseline_value: 0 (with_mfa=0, admins.count=0) across all provided periods

- deviation: No measurable improvement; privileged MFA coverage cannot be demonstrated




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of demonstrable MFA protection for privileged access fails to meet appropriate access control requirements.



**Recommendation:** Reconcile and validate privileged account inventory (admins) in the identity system and ensure telemetry correctly identifies admin roles. Then enforce MFA for all privileged roles immediately and require step-up authentication for sensitive actions. Produce evidence: list of admin accounts and MFA status, plus IdP configuration screenshots/log exports.

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


#### HIGH: High authentication failure rate (55.48%) indicates persistent auth risk

Authentication failures are extremely high relative to successes. In the current window, total auth failures are 3,623,191 with success_total=2,908,013, producing fail_rate=55.48%. This is slightly worse than the 2020-05-05 baseline fail_rate=54.69% and suggests ongoing incorrect authentication attempts or automated attack activity. Even though the dataset reports attack_ip_attempts=0 and account_takeovers=0, the failure volume itself is a strong indicator of elevated risk and potential brute-force/credential-stuffing attempts.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5548 (55.48%)

- baseline_value: 0.5469 (54.69%) on 2020-05-05

- deviation: Increase of ~0.79 percentage points (~1.4% relative increase)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Elevated authentication failure rates indicate inadequate protective controls and monitoring effectiveness for access attempts.



**Recommendation:** Triage top failing sources and authentication events: (1) review top_ips by failure count (e.g., 23.137.225.33=128,728; 10.0.181.232=23,631; 109.203.1.148=19,053), (2) check whether these IPs correspond to known services/NATs or external threat actors, (3) enable/verify rate limiting, lockout/backoff, and bot/credential-stuffing protections at the authentication boundary, and (4) correlate failures with user accounts to identify targeted accounts and enforce MFA/step-up for high-risk attempts.

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


#### MEDIUM: Telemetry indicates 0 detected attacks and 0 account takeovers despite high failure volume

The metrics report attack_ip_attempts=0, attack_ip_distinct_ips=0, and account_takeovers=0, even while auth_failures are very high (3,623,191 failures). This mismatch may indicate detection logic gaps (e.g., thresholds too high, missing correlation between failures and account compromise signals) or incomplete logging. For compliance, detection and response capabilities must be demonstrable and effective.


**Evidence:**

- metric: auth_failures.attack_ip_attempts / account_takeovers

- current_value: attack_ip_attempts=0; account_takeovers=0

- baseline_value: attack_ip_attempts=0; account_takeovers=0 (all provided periods)

- deviation: No change; potential detection coverage gap given high fail_rate=55.48%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): If attack detection is ineffective or not aligned with observed failure patterns, access security monitoring may not meet required effectiveness.



**Recommendation:** Validate detection rules and data pipelines: confirm that account takeover detection is fed by the same identity events used for failures; review thresholds and correlation windows; run a test by simulating controlled failed logins and verify alerts/attack classification. Document detection coverage and provide evidence of alerting/response workflows.

---




### Positive Observations

- Account takeover indicators are currently reported as zero (account_takeovers=0; users_with_takeover=0), suggesting no confirmed compromise events in the analyzed dataset.

- No attack-IP attempts are flagged (attack_ip_attempts=0), which may indicate either strong prevention or conservative detection; this should be validated but is a potentially positive sign.




### Trend Analysis


**Degrading:** Authentication failure rate increased slightly versus the 2020-05-05 baseline: 55.48% (current) vs 54.69% (baseline), an increase of ~0.79 percentage points.


**Stable:** MFA coverage remains unchanged at 0.0% across all compared periods (2019-11-07, 2020-02-05, 2020-05-05, and current window)., Reported attack_ip_attempts and account_takeovers remain at 0 across all provided periods.





## Compliance Observations
### Access-control compliance (Article 21)

- The entity shall implement access control policies and asset management as part of cybersecurity risk-management measures. [NIS2 Art. 21(2)(i)]  
- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1529697), indicating non-implementation of MFA/continuous authentication. [METRICS mfa; NIS2 Art. 21(2)(j)]  
- Administrators count is 0, with_mfa 0, and last_review_date is “unknown”; no evidence supports access-control review. [METRICS admins; NIS2 Art. 21(2)(i)]  
- Authentication failures total 3623191 with success_total 2908013 (fail_rate 0.5548); access-control effectiveness cannot be confirmed. [METRICS auth_failures; NIS2 Art. 21(2)(i)]  
- No data is provided for access-control exception handling; exceptions list is empty. [METRICS exceptions; NIS2 Art. 21(2)(i)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures