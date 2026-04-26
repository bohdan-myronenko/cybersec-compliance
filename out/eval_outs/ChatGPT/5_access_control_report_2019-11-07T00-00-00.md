# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2019-11-07T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **121411**
- Distinct users: **50215**
- Distinct source IPs: **55426**

### Authentication
- Successful logins: **59871**
- Failed logins: **61540**
- Failure rate: **0.5069**
- Top failing IPs:  

  
  - 10.0.181.226 (187)
  
  - 10.0.181.227 (183)
  
  - 10.0.77.228 (108)
  
  - 10.0.77.226 (104)
  
  - 10.0.77.229 (94)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


For the last 90 days (ending 2019-11-07 window), the organization shows a critical authentication control gap: MFA is not enabled for any user (0/50,215; 0.0% coverage), including zero MFA coverage for admins (admins count=0, with_mfa=0). Concurrently, authentication failure activity is substantial (61,540 total auth events with a 50.69% failure rate), though no account takeovers or attack-IP clustering is detected by the provided metrics. Compared with prior periods, the MFA posture remains consistently at 0% coverage, while the auth failure rate is somewhat lower than earlier baselines but still indicates significant unsuccessful authentication attempts that require investigation and remediation under NIS2 security requirements.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any account in the current measurement period. With 50,215 distinct users and 0 enabled users, the environment lacks a core compensating control against credential theft and unauthorized access. This is a direct compliance and risk concern under NIS2 requirements for appropriate security measures for network and information systems.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0% (enabled_users=0 / total_users=50215)

- baseline_value: 0.0% (2021-01-30: enabled_users=0 / total_users=635091; 2020-11-01: enabled_users=0 / total_users=1596182)

- deviation: No improvement; MFA coverage remains at 0% across all available baseline periods.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate authentication controls (e.g., MFA) undermines the obligation to ensure security of network and information systems, increasing likelihood of unauthorized access.



**Recommendation:** Implement MFA for all users with a phased rollout (e.g., 100% for admins first, then all users). Enforce MFA at authentication entry points (IdP/SSO), require phishing-resistant MFA where feasible, and block sign-in for accounts that cannot enroll after a defined deadline. Provide an exception process with documented risk acceptance and time limits.

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 50.7%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 50.7%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: High authentication failure rate (50.69%) indicates persistent unsuccessful access attempts

Authentication failures are substantial: 61,540 total auth events with 59,871 successes, resulting in a 50.69% failure rate. While the metrics show no detected account takeovers and no attack-IP attempts, the volume and rate of failures suggest either widespread incorrect credentials, misconfiguration, or ongoing brute-force/credential-stuffing attempts that are not being flagged as 'attack_ip_attempts' by the current detection logic.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5069 (50.69%)

- baseline_value: 0.6421 (2021-01-30) and 0.6968 (2020-11-01)

- deviation: Improved vs prior periods, but still high (down from 64.21% and 69.68% to 50.69%).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Elevated authentication failure rates indicate insufficient protective controls and monitoring for access attempts, conflicting with requirements for appropriate security measures and incident prevention/detection.



**Recommendation:** Investigate the top failing source IPs and authentication endpoints. The top IPs by failure count are internal-range addresses (e.g., 10.0.181.226=187, 10.0.181.227=183, 10.0.77.228=108, 10.0.77.226=104, 10.0.77.229=94). Validate whether these represent legitimate services, NAT/proxies, or compromised systems. Implement/verify rate limiting, lockout/backoff policies, and anomaly detection for repeated failures per user/IP/device. Ensure logs include username, IdP/app, geo/device, and failure reason to support accurate detection of credential attacks.

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/50215 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### HIGH: Admin MFA coverage cannot be verified; admins count is 0 while MFA is also 0

The metrics report admins.count=0 and with_mfa=0. This may indicate either (a) the dataset does not correctly identify admin accounts, or (b) there are no admin accounts in scope (unlikely for a production environment). Regardless, the inability to verify admin MFA coverage is a compliance and governance gap, especially given the overall 0% MFA coverage for all users.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0 (admins.count=0, last_review_date=unknown)

- baseline_value: 0 (2021-01-30 and 2020-11-01 also show admins.count=0, with_mfa=0, last_review_date=unknown)

- deviation: No change; admin review/coverage visibility remains missing.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of verifiable privileged access controls and missing review evidence weakens compliance with requirements for appropriate security measures for access management.



**Recommendation:** Fix privileged account classification and reporting: ensure admin roles/groups are correctly mapped into the metrics pipeline. Establish a recurring privileged access review (set last_review_date and audit trail). Require MFA for all privileged roles and validate enforcement via IdP policy reports.

---


#### MEDIUM: No detected account takeovers or attack-IP attempts despite high auth failures

The metrics show account_takeovers=0 and attack_ip_attempts=0, even though auth failures are high (50.69% failure rate). This could mean attacks are not occurring, or that detection thresholds/logic are insufficient (false negatives). For compliance, it is important to ensure that monitoring and detection are capable of identifying credential attacks and account compromise attempts.


**Evidence:**

- metric: auth_failures.account_takeovers

- current_value: 0

- baseline_value: 0 (2021-01-30 and 2020-11-01)

- deviation: No change; however, the presence of high failure rates warrants validation of detection coverage.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): If detection is not effective, the organization may not meet expectations for appropriate security measures, including monitoring and response to unauthorized access attempts.



**Recommendation:** Validate detection logic for credential attacks and account takeover: review SIEM/IdP rules, thresholds, and required fields. Add correlation rules for repeated failures followed by success, impossible travel, password reset events, and MFA bypass attempts. Perform a tabletop exercise and/or controlled test (where permitted) to confirm alerts fire under simulated attack conditions.

---




### Positive Observations

- Authentication failure rate has improved compared to earlier baselines (current 50.69% vs 64.21% on 2021-01-30 and 69.68% on 2020-11-01).

- No account takeovers detected in the provided metrics (account_takeovers=0; users_with_takeover=0).

- No attack-IP clustering detected by the current metric fields (attack_ip_attempts=0; attack_ip_distinct_ips=0), suggesting either limited external attack activity or detection gaps to be validated.




### Trend Analysis

**Improving:** auth_failures.fail_rate decreased to 0.5069 from 0.6421 (2021-01-30) and 0.6968 (2020-11-01).


**Degrading:** No degradation in MFA posture is observed because it is already at the worst state; however, the lack of MFA remains a persistent critical issue (0.0% coverage).


**Stable:** MFA coverage remains at 0.0% across all available periods (enabled_users=0)., account_takeovers remains 0 across periods., attack_ip_attempts remains 0 across periods.





## Compliance Observations
## Access-Control Compliance (Cybersecurity Risk-Management)

- The entity must implement access control policies as part of cybersecurity risk-management measures. [NIS2 Art. 21(2)(i)]

- The entity must apply multi-factor authentication (or continuous authentication) solutions where appropriate. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0%: enabled_users = 0 out of total_users = 50215. [METRICS mfa]

- Admin accounts are not evidenced: admins count = 0; with_mfa = 0; last_review_date = “unknown”. [METRICS admins]

- Authentication failures total 61540; success_total 59871; fail_rate 0.5069. [METRICS auth_failures]

- Top authentication-failure source IPs include 10.0.181.226 (187) and 10.0.181.227 (183). [METRICS auth_failures.top_ips]

- No account takeovers are evidenced: account_takeovers = 0; users_with_takeover = 0. [METRICS auth_failures]

- If non-compliance with required measures is identified, corrective measures must be taken without undue delay. [NIS2 Art. 21(4)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures