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


Across the 90-day window, the organization shows a severe NIS2-relevant authentication control gap: MFA is effectively not deployed (0% coverage) for 1,536,866 users, including 0 identified admins with MFA. At the same time, authentication failure behavior is high (fail rate 54.08% with 3,543,216 total auth failures vs 3,008,918 successes), indicating persistent unsuccessful authentication attempts. While no account takeovers or “attack IP attempts” are detected in the computed metrics, the combination of zero MFA coverage and elevated failure rates represents a critical compliance and security risk under NIS2, requiring immediate remediation and validation of monitoring/telemetry accuracy.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any of the 1,536,866 users in scope, resulting in single-factor authentication exposure. This is a direct control failure for NIS2-aligned baseline security measures for access control and authentication hardening. The same issue is present in historical periods (2019-11-07 and 2021-01-30), indicating a long-standing gap rather than a transient configuration issue.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0% (2019-11-07); 0.0% (2021-01-30)

- deviation: No improvement across observed historical periods; remains at 0.0%.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate measures for network and information system security, including access control and authentication strengthening, increases the likelihood and impact of unauthorized access.



**Recommendation:** Immediately enable MFA for all users (start with privileged/admin accounts and high-risk user groups), enforce MFA at authentication entry points, and require phishing-resistant MFA where feasible. Implement a short-term compensating control: temporarily restrict authentication methods/sessions and increase monitoring for suspicious logins until MFA coverage is restored. Then validate coverage by producing an auditable report showing enabled_users > 0 and coverage_pct approaching 100%.

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


#### HIGH: High authentication failure rate (54.08%) indicates persistent unsuccessful login attempts

Authentication failures are more frequent than successes: 3,543,216 total failures with 3,008,918 successes yields a fail rate of 54.08%. This pattern suggests either widespread incorrect credentials, automated probing, misconfigured clients, or brute-force attempts. Although computed metrics show 0 account takeovers and 0 attack-IP attempts, the elevated failure rate still represents an increased risk of credential stuffing/brute-force and can also indicate operational issues that undermine security monitoring effectiveness.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5408 (54.08%)

- baseline_value: 0.5069 (2019-11-07); 0.6421 (2021-01-30)

- deviation: Current fail rate is +3.39 percentage points vs 2019-11-07, and -10.73 percentage points vs 2021-01-30 (improved vs 2021 but still high).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficiently controlled authentication attempts and elevated failure rates can indicate inadequate protective measures and monitoring for unauthorized access attempts.



**Recommendation:** Triage the top source IPs and authentication endpoints responsible for failures. Implement/verify rate limiting, progressive delays, and account lockout policies (carefully to avoid DoS). Add detection rules for credential stuffing/brute-force patterns and require MFA for all authentication attempts (once MFA is enabled). Produce a breakdown by failure reason (bad password, expired token, invalid MFA, etc.) and by user segment to distinguish misconfiguration from attack traffic.

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


#### HIGH: Authentication telemetry indicates large-scale activity growth without corresponding security hardening

The dataset size and distinct user counts have grown substantially compared to the 2019-11-07 baseline (frame rows 6,552,134 vs 121,411; distinct users 1,536,866 vs 50,215). Despite this scale increase, MFA remains at 0% coverage and admins remain at 0 with MFA, suggesting that security controls did not scale with the environment. This mismatch increases the probability of successful compromise even if account takeover detections are currently zero.


**Evidence:**

- metric: frame.distinct_users

- current_value: 1,536,866

- baseline_value: 50,215 (2019-11-07)

- deviation: Increase of ~2,? (approx. +1,486,651 users; ~30.6x).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Security measures must be appropriate to risk; scaling user base without deploying MFA undermines the adequacy of access control measures.



**Recommendation:** Perform a control-to-risk reassessment for the expanded user population. Ensure privileged access management is explicitly covered: identify all admin/privileged roles and enforce MFA there first. Validate that the computed 'admins.count=0' is not a data quality issue by reconciling with IAM role inventories.

---


#### MEDIUM: Admin MFA coverage cannot be verified (admins count is 0; last_review_date unknown)

The metrics report admins.count=0 and with_mfa=0 with last_review_date='unknown'. This prevents assurance that privileged accounts are protected. Under NIS2, governance and risk management for access controls should be demonstrable and auditable. The 'admins.count=0' value may also indicate missing data mapping between IAM roles and the reporting model.


**Evidence:**

- metric: admins.count

- current_value: 0

- baseline_value: 0 (2019-11-07; 2021-01-30)

- deviation: No change; remains unverified/possibly mis-modeled.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of auditable evidence for privileged access protections weakens compliance posture for access control and authentication measures.



**Recommendation:** Reconcile reporting with IAM: extract the authoritative list of privileged/admin roles and map them to the reporting dataset. Then generate an auditable report showing admin accounts and MFA enabled status, and set a measurable review cadence (populate last_review_date with actual review timestamps).

---




### Positive Observations

- No account takeovers detected in the computed metrics (account_takeovers=0; users_with_takeover=0), suggesting either effective prevention/detection or that attacks are not resulting in confirmed compromise.

- Authentication failure rate improved compared to 2021-01-30 (current 54.08% vs baseline 64.21%), indicating some reduction in unsuccessful authentication intensity over time.




### Trend Analysis

**Improving:** auth_failures.fail_rate decreased vs 2021-01-30 (from 0.6421 to 0.5408; improvement of ~10.73 percentage points).


**Degrading:** Scale of authentication activity increased substantially vs 2019-11-07 (frame.rows 6,552,134 vs 121,411; distinct_users 1,536,866 vs 50,215), while MFA remained at 0% coverage.


**Stable:** MFA coverage remained at 0.0% across observed periods (2019-11-07, 2021-01-30, and current)., No detected account takeovers across periods in the provided metrics (account_takeovers=0).





## Compliance Observations
### Access-Control Compliance (Cybersecurity Risk-Management)

- The entity must implement appropriate, proportionate access-control measures to manage network and information system security risks. [NIS2 Art. 21(1)]

- Access-control measures must be based on an all-hazards approach protecting systems and the physical environment from incidents. [NIS2 Art. 21(2)]

- The entity must implement human resources security, access control policies, and asset management. [NIS2 Art. 21(2)(i)]

- The entity must use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1536866). [METRICS mfa]

- Administrators count is 0; administrators with MFA is 0; last_review_date is “unknown”. [METRICS admins]

- Authentication failures total 3,543,216; success_total 3,008,918; fail_rate 0.5408. [METRICS auth_failures]

- Top authentication-failure IPs include 158.149.114.95 (12,584) and 10.0.181.227 (10,967). [METRICS auth_failures.top_ips]

- No data available in the provided evidence for account takeovers, attack_ip_attempts, and attack_ip_distinct_ips. [METRICS auth_failures]

- If the entity does not comply with required measures, it must take necessary, appropriate, proportionate corrective measures without undue delay. [NIS2 Art. 21(4)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures