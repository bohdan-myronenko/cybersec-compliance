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


For the 90-day window ending 2020-11-01, the organization shows a severe NIS2 compliance gap in authentication hardening: MFA coverage is 0% across 1,596,182 users and there are 0 recorded admins with MFA. In parallel, authentication failures are extremely high (6,487,620 total failures vs 2,822,319 successes; fail rate 69.68%), and the failure volume increased materially versus prior periods (fail rate rose from 55.48% on 2020-08-03). While no account takeovers or attack-IP attempts were detected by the provided metrics, the combination of zero MFA and rising failure rates indicates elevated risk of credential stuffing/brute-force and non-compliance with NIS2 security requirements for access control and incident resilience.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any of the 1,596,182 users in scope (enabled_users=0; coverage_pct=0.0). This represents a direct failure to implement strong authentication controls expected for network and information system security, especially for remote access and privileged actions. The absence of MFA significantly increases the likelihood and impact of credential compromise.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0% (2020-08-03; 2020-05-05; 2020-02-05)

- deviation: No improvement across all provided historical periods; persistent 0% coverage




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate measures for securing network and information systems, including access control and authentication hardening; increases risk of unauthorized access.



**Recommendation:** Implement MFA for all users with a phased rollout starting with privileged/admin accounts and high-risk roles. Enforce MFA at authentication layer (IdP) with phishing-resistant options where feasible. Provide an auditable control statement and evidence (MFA policy configuration + user enrollment reports) to demonstrate compliance.

---


#### CRITICAL: No admins recorded; no admin MFA coverage and no review cadence

The metrics indicate admins.count=0 and admins.with_mfa=0 with last_review_date='unknown'. This suggests either (a) privileged accounts are not being tracked in the dataset, or (b) there are no privileged accounts defined—both are compliance and operational red flags. Regardless, the lack of verifiable privileged-account governance prevents assurance that the most critical access paths are protected with MFA and reviewed.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0 (2020-08-03; 2020-05-05; 2020-02-05)

- deviation: No improvement; privileged-account MFA governance not evidenced




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient evidence of access control governance for privileged accounts; undermines the ability to demonstrate that appropriate security measures are in place.



**Recommendation:** Establish and maintain an authoritative inventory of privileged/admin accounts (source of truth: IdP/Directory). Require MFA for all privileged accounts and implement a periodic access review with a recorded last_review_date. Ensure the reporting pipeline captures admin population and MFA status for auditability.

---


#### HIGH: Authentication failure rate sharply increased (possible credential attacks or misconfiguration)

Authentication failures are very high and have worsened versus baseline. Current fail_rate is 69.68% (6,487,620 failures; 2,822,319 successes). Compared to 2020-08-03, fail_rate increased from 55.48% to 69.68% (an increase of ~14.20 percentage points). This pattern is consistent with credential stuffing/brute-force attempts, widespread user authentication issues, or incorrect authentication policy changes. Even though the provided metrics show attack_ip_attempts=0 and account_takeovers=0, the sheer failure volume warrants investigation.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6968 (69.68%)

- baseline_value: 0.5548 (55.48%) on 2020-08-03

- deviation: +14.20 percentage points (~25.6% relative increase)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Elevated authentication failure rates indicate potential weaknesses in access security and resilience; may increase likelihood of successful unauthorized access.



**Recommendation:** Perform an authentication failure root-cause analysis: (1) correlate failures by username, geo, device, and time; (2) check for password spray/credential stuffing indicators; (3) validate rate limiting, lockout policies, and bot detection; (4) review recent changes to authentication/IdP configuration. Produce an incident-style report even if account_takeovers=0, and implement controls to reduce failure-driven risk (rate limits, adaptive MFA triggers, and IP reputation controls).

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


#### HIGH: Concentration of failures from internal IP range suggests targeted activity or logging/segmentation issues

Top failure sources are concentrated in the 10.3.205.193–10.3.205.197 range with the highest counts: 443,523 (10.3.205.197), 257,018 (10.3.205.196), 236,489 (10.3.205.195), 177,160 (10.3.205.194), and 152,239 (10.3.205.193). This concentration can indicate a small number of hosts generating repeated failed authentications (e.g., misconfigured service accounts, compromised hosts, or automated attack tooling).


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IP counts: 443,523 (10.3.205.197) down to 152,239 (10.3.205.193)

- baseline_value: Different top IPs in prior periods (e.g., 23.137.225.33 at 128,728 on 2020-08-03)

- deviation: Shift in top failure sources; current concentration in 10.3.205.x internal range




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Potentially indicates inadequate monitoring/segmentation and insufficient controls to prevent or detect unauthorized access attempts.



**Recommendation:** Map the top failure IPs to owning systems/roles (CMDB/asset inventory). For each top IP, identify the authenticating client/service and validate credentials and configuration. If IPs correspond to user-facing access, investigate for compromise. If they correspond to services, remediate misconfiguration and rotate credentials. Ensure logs include correlation IDs and user identifiers to support attribution.

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


#### MEDIUM: No detected account takeovers despite very high failure volume—validate detection coverage

The metrics report account_takeovers=0 and users_with_takeover=0 while failures are extremely high (6.49M). This may be accurate, but it also raises the possibility that takeover detection logic is incomplete or not aligned with the authentication events being measured.


**Evidence:**

- metric: auth_failures.account_takeovers

- current_value: 0

- baseline_value: 0 (2020-08-03; 2020-05-05; 2020-02-05)

- deviation: No change; detection may be consistently non-sensitive




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient assurance that unauthorized access is being detected and mitigated, affecting the effectiveness of security measures.



**Recommendation:** Review and test account takeover detection rules (e.g., impossible travel, anomalous session creation, credential reuse, MFA fatigue patterns). Validate that the detection pipeline consumes the same authentication telemetry used to compute failures. Run a tabletop exercise using simulated takeover scenarios to confirm alerting and response.

---




### Positive Observations

- No account takeovers detected in the provided metrics (account_takeovers=0; users_with_takeover=0), suggesting either strong prevention/detection or that detection logic may need validation.

- Attack-IP attempt counters are 0 (attack_ip_attempts=0; attack_ip_distinct_ips=0), indicating no explicit attack-IP classification triggered by the current logic.




### Trend Analysis


**Degrading:** Authentication fail rate increased from 55.48% (2020-08-03) to 69.68% (current), a +14.20 percentage point degradation., Total authentication failures increased from 3,623,191 (2020-08-03) to 6,487,620 (current), indicating higher authentication friction/attempt volume.


**Stable:** MFA coverage remains at 0.0% across all provided historical periods (persistent non-compliance)., Account takeover indicators remain at 0 across all provided periods.





## Compliance Observations
### Access-Control Compliance (Article 21)

- The entity shall implement access control policies as part of cybersecurity risk-management measures. [article_21_cybersecurity_risk-management_measures Art. 21(2)(i)]

- Multi-factor authentication (or continuous authentication) solutions shall be used where appropriate. [article_21_cybersecurity_risk-management_measures Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1596182). [METRICS JSON mfa]

- Authentication failures total 6,487,620; success_total 2,822,319; fail_rate 0.6968. [METRICS JSON auth_failures]

- Top authentication failure IPs include 10.3.205.197 (443,523) and 10.3.205.196 (257,018). [METRICS JSON auth_failures.top_ips]

- No data available in the provided evidence for admin access-control review status (admins.count: 0; last_review_date: unknown). [METRICS JSON admins]

- No data available in the provided evidence for corrective actions taken “without undue delay” for non-compliance. [article_21_cybersecurity_risk-management_measures Art. 21(4)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures