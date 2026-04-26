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


Across the 90-day window ending 2019-11-07, the organization shows a severe NIS2 compliance gap in authentication hardening: MFA coverage is 0% (0 of 50,215 users) and there are no recorded MFA-enabled admins (admins count=0, with_mfa=0). Authentication activity also shows a high overall authentication failure rate (fail_rate=0.5069; 61,540 total failures vs 59,871 successes), with repeated attempts concentrated in a small set of internal source IPs (top IPs 10.0.181.226=187, 10.0.181.227=183, 10.0.77.228=108, 10.0.77.226=104, 10.0.77.229=94). While no account takeovers or attack-IP indicators were detected (attack_ip_attempts=0; account_takeovers=0), the lack of MFA and elevated failure rates represent a critical risk to availability and integrity under NIS2.


### Security Findings


#### CRITICAL: MFA is not enabled for any users (0% coverage)

MFA coverage is currently 0.0%, meaning none of the 50,215 distinct users have MFA enabled. This is a direct control failure for NIS2 authentication/secure access requirements and materially increases the likelihood and impact of credential compromise. The issue is persistent across historical periods where MFA enabled_users remained 0 and coverage_pct stayed at 0.0%.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0% (enabled_users=0 / total_users=50215)

- baseline_value: 0.0% (e.g., 2021-01-30: enabled_users=0 / total_users=635091; 2020-11-01: enabled_users=0 / total_users=1596182)

- deviation: No improvement; remains at 0% across current and historical periods




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate measures for secure authentication and access control (e.g., MFA) undermines compliance with NIS2 requirements for security of network and information systems.



**Recommendation:** Implement MFA for all users with a phased rollout (start with privileged/admin accounts and high-risk user groups), enforce MFA at authentication policy level, and remove any legacy authentication paths that bypass MFA. Provide an auditable policy and target date; require proof of enforcement (e.g., IAM configuration export) and monitor coverage until it reaches >95% within a defined SLA.

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


#### CRITICAL: High authentication failure rate indicating potential brute-force/credential stuffing or misconfiguration

The system records 61,540 total authentication failures with a fail_rate of 0.5069 (59,871 successes). While no account takeovers were detected (account_takeovers=0), the failure volume at ~50% indicates either repeated incorrect authentication attempts or systemic authentication issues. This elevates risk of account lockouts, service degradation, and increased likelihood of eventual compromise—especially in the absence of MFA.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5069 (total=61540; success_total=59871)

- baseline_value: 0.6421 (2021-01-30) and 0.6968 (2020-11-01)

- deviation: Improved vs baseline by ~13.1 percentage points vs 2021-01-30 (0.6421-0.5069) and ~19.6 percentage points vs 2020-11-01 (0.6968-0.5069)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inadequate authentication resilience and monitoring can fail to meet NIS2 expectations for protecting systems against unauthorized access attempts and ensuring appropriate security controls.



**Recommendation:** Triage the authentication failures: (1) identify the affected applications/tenants and authentication endpoints; (2) correlate failures with user accounts and time windows; (3) validate rate-limiting, lockout policies, and bot/abuse detection; (4) confirm whether failures are driven by a small set of internal IPs (see finding_003) suggesting misconfigured clients or automated retries. Implement/verify MFA (finding_001) and add adaptive throttling for repeated failures per source IP and per account.

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


#### HIGH: Authentication failures concentrated in a small set of source IPs (internal IP clustering)

Top source IPs account for repeated authentication failures: 10.0.181.226 (187), 10.0.181.227 (183), 10.0.77.228 (108), 10.0.77.226 (104), 10.0.77.229 (94). This clustering suggests either automated processes (e.g., misconfigured service accounts/clients) or internal-origin abuse. Even though attack_ip_attempts=0 and account_takeovers=0, the concentration warrants investigation because it can indicate systemic issues that increase failure rates and potentially enable lateral movement or credential attacks.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IP counts: 187, 183, 108, 104, 94 (total failures=61540)

- baseline_value: Baseline top_ips exist but differ; e.g., 2021-01-30 top IP 170.39.78.106 count=67563 (much larger scale)

- deviation: Current failures are lower in absolute terms than historical, but remain non-trivial and clustered




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of effective detection/response to suspicious authentication patterns can indicate insufficient security monitoring and control effectiveness under NIS2.



**Recommendation:** Investigate the five top IPs: determine owning systems (DHCP/static mapping), associated service accounts, and whether these IPs correspond to legitimate automation. If legitimate, fix credentials/rotation and reduce retry aggressiveness. If not legitimate, block or throttle at the network/WAF/IdP layer and enforce stronger authentication (MFA) and conditional access for those sources.

---


#### HIGH: Privileged access governance data is missing/inconsistent (admins count=0, last_review_date=unknown)

The metrics report admins.count=0 and last_review_date='unknown', with with_mfa=0. This is inconsistent with typical enterprise environments and prevents assurance that privileged accounts are protected (especially given MFA is disabled for all users). The absence of admin inventory and review evidence is itself a compliance and auditability concern.


**Evidence:**

- metric: admins.count / admins.last_review_date

- current_value: admins.count=0; with_mfa=0; last_review_date=unknown

- baseline_value: Historical periods also show admins.count=0 and last_review_date=unknown

- deviation: No improvement; privileged account governance visibility remains absent




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient governance and inability to demonstrate secure access controls for privileged accounts undermines compliance evidence for NIS2.



**Recommendation:** Establish and export a verified privileged account inventory (IdP/AD/SSO roles, admin groups, break-glass accounts). Implement periodic access reviews with recorded timestamps and ensure MFA enforcement for all privileged roles. Update reporting so admins.count reflects actual privileged identities and last_review_date is populated from the review system.

---




### Positive Observations

- Authentication failure rate has improved versus historical baselines: current fail_rate=0.5069 vs 0.6421 (2021-01-30) and 0.6968 (2020-11-01).

- No account takeovers detected in the current period (account_takeovers=0; users_with_takeover=0).

- No attack-IP attempts were flagged by the metric logic (attack_ip_attempts=0; attack_ip_distinct_ips=0), suggesting no confirmed external attack pattern in this dataset.




### Trend Analysis

**Improving:** auth_failures.fail_rate decreased to 0.5069 from 0.6421 (2021-01-30) and 0.6968 (2020-11-01)., Absolute authentication failure volume appears lower than historical periods (current total=61,540 vs 1,511,918 in 2021-01-30 and 6,487,620 in 2020-11-01).


**Degrading:** No degradation is indicated in failure rate relative to historical; however, the critical control gap persists: MFA coverage remains 0.0% (no improvement across periods).


**Stable:** MFA coverage is consistently 0.0% across current and historical periods (enabled_users=0)., No account takeovers detected (account_takeovers=0) across current and historical snapshots provided.





## Compliance Observations
### Access-Control Compliance (Cybersecurity Risk-Management)

- The entity shall implement access control policies as part of human resources security and asset management measures. [NIS2 Art. 21(2)(i)]

- The entity shall use multi-factor authentication (or continuous authentication solutions) where appropriate. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 50215). [METRICS mfa]

- Administrators count is 0; MFA for admins is 0; last_review_date is “unknown”. [METRICS admins]

- Authentication failures total 61540; success_total 59871; fail_rate 0.5069. [METRICS auth_failures]

- Top authentication-failure source IPs include 10.0.181.226 (187) and 10.0.181.227 (183). [METRICS auth_failures.top_ips]

- No data indicates account takeovers (account_takeovers: 0; users_with_takeover: 0). [METRICS auth_failures]

- If the entity does not comply with the required measures, it shall take corrective measures without undue delay. [NIS2 Art. 21(4)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures