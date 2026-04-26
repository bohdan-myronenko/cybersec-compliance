# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2021-01-30T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **2354597**
- Distinct users: **635091**
- Distinct source IPs: **505308**

### Authentication
- Successful logins: **842679**
- Failed logins: **1511918**
- Failure rate: **0.6421**
- Top failing IPs:  

  
  - 170.39.78.106 (67563)
  
  - 10.0.77.230 (35558)
  
  - 10.1.6.103 (9507)
  
  - 10.0.181.231 (8202)
  
  - 10.0.181.232 (8092)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


For the 90-day window ending 2021-01-30, the environment shows a severe NIS2 compliance gap in authentication hardening: MFA is effectively not deployed (0/635,091 users enabled), including zero MFA coverage for admins (0 admins identified, with_mfa=0). Authentication activity also indicates a very high overall authentication failure rate (64.21% failures), with the majority of failures concentrated in a small set of source IPs (top IP 170.39.78.106 with 67,563 failures). While no account takeovers or attack-IP patterns were detected by the provided metrics, the combination of zero MFA coverage and elevated failure rates represents a critical risk to availability and account security under NIS2 requirements for risk management and incident prevention.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any user accounts. With MFA coverage at 0.0%, the organization is not meeting baseline expectations for strong authentication controls, increasing the likelihood and impact of credential compromise and unauthorized access. This is a direct, measurable control failure across the entire user population.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement; remains at 0.0% across the compared baseline periods (2020-05-05, 2020-08-03, 2020-11-01).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate technical and organizational measures for risk management (including access control/authentication hardening) increases the likelihood of incidents and undermines required security measures.



**Recommendation:** Implement MFA for all users using a phased rollout with enforced enrollment (e.g., require MFA at next login, then block non-MFA logins). Prioritize privileged accounts first (admins/service accounts), then high-risk user groups. Provide an auditable control report showing % enabled and exceptions (with documented risk acceptance).

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 64.2%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 64.2%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: High authentication failure rate (64.21%) indicates potential brute-force/credential issues

Authentication failures are high relative to successes, with a computed fail rate of 64.21%. This can indicate brute-force attempts, misconfigured clients, expired credentials, or widespread credential stuffing. Even though the metrics report attack_ip_attempts=0 and account_takeovers=0, the concentration of failures in top IPs suggests automated or repeated attempts from specific sources that should be investigated and mitigated.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6421 (64.21%)

- baseline_value: 0.6968 (69.68%)

- deviation: Improved by ~5.47 percentage points vs 2020-11-01 baseline, but still very high.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Elevated authentication failures increase the risk of security incidents and indicate insufficient preventive controls (e.g., rate limiting, lockout policies, monitoring, and strong authentication).



**Recommendation:** Investigate the top failure sources and authentication flows: (1) review logs for the top IPs (170.39.78.106: 67,563 failures; 10.0.77.230: 35,558; 10.1.6.103: 9,507; 10.0.181.231: 8,202; 10.0.181.232: 8,092) and map them to user agents/tenants; (2) enable/verify rate limiting and progressive throttling on authentication endpoints; (3) enforce account lockout or step-up verification after repeated failures; (4) ensure MFA is enabled to reduce credential-only attacks.

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/635091 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### HIGH: Authentication failure volume remains substantial despite reduced fail rate

While the failure rate improved compared to the 2020-11-01 baseline, the absolute volume of authentication events remains large (1,511,918 total failures in the current window). This suggests persistent authentication instability or ongoing repeated attempts. The distinct source IP count is also high (505,308 distinct src IPs), indicating broad exposure to repeated authentication attempts across many sources.


**Evidence:**

- metric: auth_failures.total

- current_value: 1511918

- baseline_value: 6487620

- deviation: Lower than 2020-11-01 baseline total failures, but still high in absolute terms for the analyzed 90-day window.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent high-volume authentication failures indicate ongoing risk and insufficient preventive/detective controls, impacting the organization’s ability to manage security risks effectively.



**Recommendation:** Quantify and classify failures: break down by failure reason (invalid password, unknown user, MFA required, expired token, etc.), and by geography/ASN and client type. Use this to tune detection rules and to remediate misconfigurations (e.g., stale credentials) and to block/limit abusive traffic.

---


#### MEDIUM: Privileged account MFA posture cannot be validated (admins count=0, last_review_date unknown)

The metrics show admins.count=0 and last_review_date='unknown'. This prevents validation that privileged accounts are protected with MFA and reviewed. Even if the admin count is correct, the lack of review metadata indicates weak governance and auditability for privileged access controls.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0

- deviation: No change; however, privileged access governance is not verifiable due to admins.count=0 and last_review_date='unknown'.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient governance/auditability of access control measures undermines the ability to demonstrate appropriate risk management and security measures.



**Recommendation:** Establish and maintain an authoritative inventory of privileged accounts (admins/service accounts) and record last review dates. Require MFA for all privileged roles and produce an auditable report (admin list, MFA enabled status, review timestamp, and exceptions with approvals).

---




### Positive Observations

- No account takeovers detected in the provided metrics (account_takeovers=0; users_with_takeover=0).

- Attack-IP specific detections are not present in the computed metrics (attack_ip_attempts=0; attack_ip_distinct_ips=0), suggesting no confirmed takeover/attack-IP pattern by this logic.

- Authentication failure rate improved versus the 2020-11-01 baseline (fail_rate 64.21% current vs 69.68% baseline), indicating some reduction in failure intensity.




### Trend Analysis

**Improving:** Authentication failure rate decreased vs 2020-11-01 baseline (0.6421 vs 0.6968; ~-5.47 percentage points).


**Degrading:** MFA coverage remains at 0.0% (no improvement across all compared baseline periods).


**Stable:** No detected account takeovers across current and baseline periods (account_takeovers=0; users_with_takeover=0).





## Compliance Observations
### Access-Control Compliance (Concise)

- The entity shall implement access control policies as part of cybersecurity risk-management measures [NIS2 Art. 21(2)(i)].  
- The entity shall apply human resources security and access control policies, supported by asset management [NIS2 Art. 21(2)(i)].  
- Multi-factor authentication or continuous authentication solutions shall be used where appropriate [NIS2 Art. 21(2)(j)].  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 635091) [METRICS mfa].  
- Administrators count is 0; MFA for administrators is 0; last_review_date is “unknown” [METRICS admins].  
- Authentication failures total 1511918 with success_total 842679 (fail_rate 0.6421) [METRICS auth_failures].  
- No data available in the provided evidence for access-control policy existence or effectiveness assessment [NIS2 Art. 21(2)(f); METRICS].  
- No data available in the provided evidence for corrective measures taken “without undue delay” [NIS2 Art. 21(4); METRICS].

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures