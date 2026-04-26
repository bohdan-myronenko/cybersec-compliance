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


Across the 90-day window ending 2020-08-03, the organization shows a severe NIS2-relevant authentication control gap: MFA is effectively not deployed (0% coverage for 1,529,697 users, including 0/0 admins with MFA). At the same time, authentication failures are high and remain elevated versus prior periods (current fail rate 55.48% vs ~54.69% in the previous baseline period), indicating persistent login instability and/or brute-force/credential-stuffing attempts, even though the dataset reports 0 detected attack-IP attempts and 0 account takeovers. Overall, the posture is non-compliant for core access control expectations and requires immediate remediation and validation of detection/telemetry.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any user accounts. This is a direct and material control deficiency for NIS2 access security requirements. With 0 enabled users out of 1,529,697 total users, the environment is effectively relying on single-factor authentication, increasing the likelihood and impact of credential compromise.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0% (2020-05-05), 0.0% (2020-02-05), 0.0% (2019-11-07)

- deviation: No improvement across all compared periods; remains at 0.0%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate measures to secure network and information systems, including access control protections such as MFA, undermines the required security of access to systems and accounts.



**Recommendation:** Implement MFA for all users as a mandatory control (start with privileged/admin accounts and then all remaining users). Enforce MFA at authentication layer (IdP) and block logins without MFA after a defined cutover date. Provide an exception process with time-bound approvals and compensating controls (e.g., device trust, conditional access). Validate coverage by producing an auditable report: total users, MFA-enabled users, and enforcement status.

---


#### CRITICAL: No MFA for administrators (privileged access not protected)

The dataset indicates 0 administrators and 0 admins with MFA. In practice, this suggests either (a) privileged accounts are not being inventoried/represented in the telemetry, or (b) privileged access is not protected by MFA. Either scenario is a compliance and security risk because privileged accounts are the highest-value targets.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0 (2020-05-05), 0 (2020-02-05), 0 (2019-11-07)

- deviation: No change; also indicates potential telemetry/inventory gap (admins.count=0)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inadequate protection of privileged access and/or lack of auditable privileged account inventory prevents demonstrating appropriate access control measures.



**Recommendation:** Reconcile administrator inventory with the identity provider and privileged access management (PAM) systems. Ensure all privileged roles (admins, service admins, support roles) are identified and required to use MFA. If admins.count is truly zero, confirm whether the organization uses a different privileged account model (e.g., shared accounts, break-glass accounts) and bring those under MFA/conditional access enforcement with logging.

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


#### HIGH: High authentication failure rate persists and is slightly worse than baseline

Authentication failures are substantial: 3,623,191 total auth attempts with 2,908,013 successes, yielding a fail rate of 55.48%. Compared to the previous baseline (2020-05-05), the fail rate increased from 54.69% to 55.48% (an increase of ~0.79 percentage points). This pattern is consistent with ongoing brute-force/credential-stuffing attempts, misconfigurations, or user friction, and it increases the operational and security risk—especially in the absence of MFA.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5548 (55.48%)

- baseline_value: 0.5469 (54.69%)

- deviation: Increase of ~0.79 percentage points vs 2020-05-05




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent authentication failures indicate insufficient protective measures and/or inadequate detection/response controls for access attempts, undermining the security of network and information systems.



**Recommendation:** Triage the failure causes: (1) identify whether failures are concentrated on specific accounts, geographies, or user agents; (2) verify rate limiting, lockout/step-up authentication, and bot protections; (3) correlate with IdP logs to distinguish misconfiguration vs attack traffic. Deploy conditional access policies (risk-based step-up, IP reputation, impossible travel) and require MFA for all interactive logins. Produce a weekly report of top failing accounts and top failing IPs with remediation status.

---


#### HIGH: Potential detection/telemetry gap: 0 attack-IP attempts and 0 account takeovers despite high failure volume

Despite a very high overall authentication failure rate (55.48%) and large volumes of attempts, the metrics report attack_ip_attempts=0, attack_ip_distinct_ips=0, account_takeovers=0, and users_with_takeover=0. This mismatch suggests either (a) the detection logic is not identifying attacks, (b) the dataset is incomplete, or (c) failures are primarily due to legitimate causes (e.g., user errors) rather than attacks. For compliance, the organization must be able to demonstrate effective monitoring and incident detection.


**Evidence:**

- metric: auth_failures.attack_ip_attempts

- current_value: 0

- baseline_value: 0 (2020-05-05), 0 (2020-02-05), 0 (2019-11-07)

- deviation: No detected attacks across periods despite high fail rate (55.48% current)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): If monitoring/detection is ineffective or not evidenced, the organization cannot demonstrate appropriate measures to protect access and respond to security events.



**Recommendation:** Validate and tune detection rules: confirm how 'attack_ip_attempts' and 'account_takeovers' are computed, ensure thresholds are appropriate, and verify that logs include required fields (account identifier, outcome codes, session context). Run a controlled test (e.g., simulated credential-stuffing in a lab or using a sanctioned test account) to confirm detections fire. Document detection coverage and alerting SLAs for authentication anomalies.

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


#### MEDIUM: Top source IPs show large volumes of auth failures (possible concentration risk)

The top IP 23.137.225.33 has 128,728 auth failures (highest in the current period). Several internal/private-range IPs (10.0.181.232, 10.0.181.229, 10.0.181.228) also appear among the top sources, which may indicate internal scanning, misconfigured services, or NAT/proxy behavior. Concentration of failures increases the likelihood of targeted attacks or systemic issues.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IP 23.137.225.33 count=128,728; next 10.0.181.232 count=23,631; 109.203.1.148 count=19,053

- baseline_value: Top IP 23.137.225.33 count=63,681 (2020-05-05)

- deviation: 23.137.225.33 failures increased by ~65,047 vs 2020-05-05 (approx. +102%)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Concentrated authentication failures without effective protective controls (e.g., MFA, rate limiting) indicates insufficient access security measures.



**Recommendation:** Investigate the top IPs: determine whether they belong to known services, proxies, or legitimate clients. If external and not expected, apply IP reputation controls, rate limiting, and block/allow-list policies where appropriate. If internal, identify the responsible systems and correct authentication flows to prevent repeated failures. Track remediation outcomes and re-measure fail rates after changes.

---




### Positive Observations

- No account takeovers detected in the dataset (account_takeovers=0; users_with_takeover=0), which is a favorable indicator if detection is reliable.

- No 'attack_ip_attempts' detected (attack_ip_attempts=0), suggesting either limited successful compromise activity or that attack detection is not triggering—worth validating rather than assuming.




### Trend Analysis


**Degrading:** Authentication failure rate increased from 54.69% (2020-05-05) to 55.48% (current), a degradation of ~0.79 percentage points.


**Stable:** MFA coverage remains at 0.0% across all compared periods (2019-11-07, 2020-02-05, 2020-05-05, and current)., Detected account takeovers and attack-IP attempts remain at 0 across compared periods.





## Compliance Observations
### Access-Control Compliance (Article 21)

- The entity shall implement access control policies as part of cybersecurity risk-management measures. [NIS2 Art. 21(2)(i)]  
- Multi-factor authentication or continuous authentication solutions shall be used, where appropriate. [NIS2 Art. 21(2)(j)]  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1529697). [METRICS mfa]  
- Administrators count is 0; MFA for administrators is 0. [METRICS admins]  
- Authentication failures total 3623191; success_total 2908013; fail_rate 0.5548. [METRICS auth_failures]  
- Top source IPs for authentication failures include 23.137.225.33 (128728) and 10.0.181.232 (23631). [METRICS auth_failures.top_ips]  
- If non-compliance with required measures is identified, corrective measures shall be taken without undue delay. [NIS2 Art. 21(4)]  

**No data available in the provided evidence** for: access control policy existence, administrator review dates, and whether MFA/continuous authentication is “appropriate.” [METRICS admins]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures