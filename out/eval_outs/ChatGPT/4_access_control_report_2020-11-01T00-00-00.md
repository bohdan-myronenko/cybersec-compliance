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


Across the last 90 days (ending 2020-11-01), the environment shows a severe NIS2 compliance gap: MFA is effectively not deployed (0% coverage for 1,596,182 users, including 0/0 admins with MFA). In parallel, authentication activity is dominated by failures (6,487,620 total auth events with a 69.68% fail rate), and the failure volume increased versus prior periods (e.g., fail rate rose from 55.48% in the 2020-08-03 baseline). While no account takeovers or “attack IP attempts” were detected (0 in both current and baseline), the combination of missing MFA and elevated failure rates indicates heightened risk of credential-based compromise and non-compliance with NIS2 security requirements.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any user accounts. Current metrics show 1,596,182 total users with 0 enabled for MFA, resulting in 0.0% coverage. This is a direct control failure for NIS2 baseline security measures intended to reduce the likelihood and impact of compromised credentials.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement across historical baselines; remains at 0.0% (2020-02-05, 2020-05-05, 2020-08-03).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate measures for network and information security, including access control protections such as MFA, increases the risk of unauthorized access.



**Recommendation:** Implement MFA for all users with a phased rollout (e.g., 100% for admins first, then remaining users). Enforce MFA at authentication layer (IdP) and block sign-in for accounts without MFA after a defined deadline. Provide compensating controls temporarily only if explicitly approved and time-bound.

---


#### CRITICAL: Authentication failures are extremely high (69.68% fail rate)

Authentication events are heavily skewed toward failures: 6,487,620 total auth events with 2,822,319 successes, yielding a 69.68% fail rate. This indicates either widespread incorrect credential attempts, misconfiguration, or active credential stuffing/brute-force attempts. Even though account takeovers are currently detected as 0, the failure rate itself is a strong indicator of elevated risk and potential ongoing attack attempts.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6968 (69.68%)

- baseline_value: 0.5548 (55.48%)

- deviation: Fail rate increased by ~14.20 percentage points vs 2020-08-03 baseline.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inadequate authentication hardening and monitoring can undermine the effectiveness of access control measures and increase the likelihood of security incidents.



**Recommendation:** Triage the top failure sources and root cause: (1) correlate the top IPs with known internal networks vs external sources; (2) review IdP/auth logs for error codes (invalid password vs locked account vs policy failures); (3) enable/verify rate limiting, lockout policies, and anomaly detection; (4) ensure MFA is enforced to reduce successful compromise probability; (5) create an incident playbook for sustained high fail rates.

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


#### HIGH: Top authentication failure IPs are concentrated in a private IP range

The highest-volume authentication failures originate from a small set of IPs in the 10.3.205.193–10.3.205.197 range. This concentration suggests either a single misconfigured client/service repeatedly attempting authentication, an internal automation issue, or an internal threat actor. Concentration increases the likelihood of systemic misconfiguration or targeted activity.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: 10.3.205.197=443,523; 10.3.205.196=257,018; 10.3.205.195=236,489; 10.3.205.194=177,160; 10.3.205.193=152,239

- baseline_value: Baseline top IPs differed (e.g., 23.137.225.33=128,728 in 2020-08-03).

- deviation: Failure concentration shifted from prior top external IPs to a private internal range; indicates a change in source behavior.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of effective detection/response to anomalous authentication patterns can lead to prolonged exposure and delayed incident handling.



**Recommendation:** Identify the owning systems for 10.3.205.193–197 (asset inventory + network ownership). Validate whether these are legitimate services (e.g., batch jobs, SSO gateways). If legitimate, fix credentials/flows and ensure correct auth policies. If not, block/limit at network or IdP level and investigate for internal compromise.

---


#### HIGH: No MFA coverage for administrators (0/0) and no admin review evidence

The metrics indicate 0 admins are recorded, with 0 admins having MFA and last_review_date reported as 'unknown'. This prevents assurance that privileged accounts are protected and reviewed. For NIS2, governance and access control over privileged accounts are critical to reduce risk of high-impact compromise.


**Evidence:**

- metric: admins.with_mfa / admins.last_review_date

- current_value: with_mfa=0; last_review_date=unknown; admins.count=0

- baseline_value: with_mfa=0; last_review_date=unknown; admins.count=0

- deviation: No improvement; also indicates potential data quality/instrumentation gap (admins not enumerated).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient evidence of privileged access management and review undermines compliance with required security measures.



**Recommendation:** Fix privileged account inventory: ensure admin roles are correctly classified and reported. Establish a recurring review process (with auditable timestamps) and require MFA for all privileged accounts immediately. Validate reporting pipelines so 'admins.count' reflects reality.

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


#### MEDIUM: No detected account takeovers despite high failure rates

Account takeover indicators are 0 (users_with_takeover=0; account_takeovers=0) and attack_ip_attempts=0. Given the very high fail rate (69.68%), this may indicate either (a) attacks are not succeeding, or (b) detection logic is incomplete/overly conservative. Either way, the mismatch warrants validation of detection coverage.


**Evidence:**

- metric: auth_failures.account_takeovers / auth_failures.attack_ip_attempts

- current_value: account_takeovers=0; attack_ip_attempts=0

- baseline_value: account_takeovers=0; attack_ip_attempts=0

- deviation: Stable at 0 across periods; does not explain the increased fail rate.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): If detection/monitoring is insufficient, security incidents may not be identified promptly, reducing the effectiveness of security measures.



**Recommendation:** Validate detection logic for account takeover and attack attempts: run test cases, review SIEM/IdP correlation rules, and confirm that successful compromise patterns (impossible travel, new device, privilege changes, anomalous session behavior) are covered. Ensure alerting thresholds are tuned for high-failure scenarios.

---




### Positive Observations

- No account takeovers detected in the current window (account_takeovers=0; users_with_takeover=0), consistent with historical baselines.

- No 'attack_ip_attempts' detected (0) and no distinct attack IPs identified (attack_ip_distinct_ips=0), suggesting either mitigations are limiting success or detection needs validation.




### Trend Analysis


**Degrading:** Authentication fail rate increased from 55.48% (2020-08-03 baseline) to 69.68% currently (degradation of ~14.20 percentage points)., Total authentication events increased (auth_failures.total=6,487,620 currently vs 3,623,191 in 2020-08-03), indicating higher authentication activity and/or more repeated attempts.


**Stable:** MFA coverage remains at 0.0% across all provided historical baselines and the current period., Account takeover and attack IP attempt indicators remain at 0 across current and historical periods.





## Compliance Observations
### Access-Control Compliance (Article 21)

- The entity shall implement access control policies as part of cybersecurity risk-management measures. [NIS2 Art. 21(2)(i)]  
- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1596182). [METRICS mfa]  
- Authentication failures total 6,487,620; success_total 2,822,319; fail_rate 0.6968. [METRICS auth_failures]  
- Top authentication failure IPs include 10.3.205.197 (443,523) and 10.3.205.196 (257,018). [METRICS auth_failures.top_ips]  
- If non-compliance with paragraph 2 measures is identified, corrective measures shall be taken without undue delay. [NIS2 Art. 21(4)]  
- Admin access review status is unavailable: admins.count is 0; last_review_date is “unknown”. No data available in the provided evidence. [METRICS admins]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures