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


For the 90-day window ending 2020-08-03, the organization shows a severe NIS2-relevant authentication control gap: MFA is effectively not deployed (0% coverage across 1,529,697 users, including 0/0 admins with MFA). At the same time, authentication failure activity remains high (fail rate 55.48% with 3,623,191 total failures), though no account takeovers or “attack IP attempts” were detected by the provided metrics. Compared with prior periods, the MFA posture is unchanged (still 0% coverage), while the authentication failure rate has slightly worsened versus earlier baselines, indicating persistent exposure to credential-stuffing/brute-force risk and non-compliance with baseline security measures.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any user accounts. This represents a fundamental weakness in access control and authentication assurance, increasing the likelihood and impact of credential compromise. The issue persists across historical baselines, indicating a systemic control failure rather than a transient outage.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0% (2020-05-05), 0.0% (2020-02-05), 0.0% (2019-11-07)

- deviation: No improvement across all compared periods; remains at 0.0%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate technical and organizational measures for network and information security, specifically strengthening authentication to reduce risk of unauthorized access.



**Recommendation:** Implement MFA for all users with a phased rollout (start with privileged/admin accounts and high-risk user groups), enforce MFA at authentication policy level, and require re-authentication for existing sessions. Provide an auditable implementation plan with target dates and measurable coverage milestones (e.g., 50% in 30 days, 100% in 90 days).

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


#### CRITICAL: No MFA for administrators (0/0 admins with MFA) and no admin review evidence

The dataset indicates zero administrators are recorded and zero have MFA enabled, with the last review date marked as 'unknown'. Even if the 'admins.count' is a data artifact, the absence of verifiable privileged-account MFA coverage and review evidence is a major compliance and security gap for NIS2 expectations around access control and governance.


**Evidence:**

- metric: admins.with_mfa / admins.last_review_date

- current_value: with_mfa=0; last_review_date='unknown'; admins.count=0

- baseline_value: admins.count=0; with_mfa=0; last_review_date='unknown' (all provided historical periods)

- deviation: No change; privileged-account governance evidence is missing




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of demonstrable controls for privileged access management undermines the effectiveness of security measures intended to prevent unauthorized access.



**Recommendation:** Establish and validate an authoritative privileged account inventory (admins/roles), ensure MFA is enforced for all privileged accounts, and implement periodic access reviews with recorded dates. If 'admins.count=0' is incorrect, fix telemetry/inventory mapping so compliance reporting reflects reality.

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


#### HIGH: High authentication failure rate (~55%) indicates persistent brute-force/credential-stuffing risk

Authentication failures are extremely frequent: 3,623,191 total failures with a 55.48% fail rate (success_total=2,908,013). While no account takeovers were detected, the high failure volume is consistent with ongoing automated login attempts. This elevates the likelihood of eventual compromise, especially in the absence of MFA.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5548 (55.48%)

- baseline_value: 0.5469 (2020-05-05), 0.5408 (2020-02-05), 0.5069 (2019-11-07)

- deviation: Up vs 2020-05-05 by +0.0079 (+0.79 percentage points); up vs 2020-02-05 by +0.0140 (+1.40 percentage points); up vs 2019-11-07 by +0.0479 (+4.79 percentage points)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient authentication hardening and monitoring increases risk of unauthorized access events, which NIS2 expects organizations to mitigate through appropriate security measures.



**Recommendation:** Tune and enforce protective controls: rate limiting, IP/account lockout thresholds with safe recovery, bot detection, and credential-stuffing defenses. Prioritize investigation of top failing source IPs (e.g., 23.137.225.33 with 128,728 failures) for whether they represent legitimate services or hostile traffic; implement allowlists only where justified.

---


#### MEDIUM: Top source IPs dominate failures; potential concentration of hostile traffic

The failure distribution is concentrated among a small set of IPs. The top IP (23.137.225.33) accounts for 128,728 failures in the current window, and several internal-range IPs (10.0.181.232, 10.0.181.229, 10.0.181.228) also appear among the top sources. This pattern may indicate either internal misconfiguration (e.g., services repeatedly failing auth) or targeted external attempts routed through NAT/proxies.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IP 23.137.225.33 count=128,728; next 10.0.181.232 count=23,631; 109.203.1.148 count=19,053; 10.0.181.229 count=16,826; 10.0.181.228 count=16,411

- baseline_value: Top IP 23.137.225.33 count=63,681 (2020-05-05); other top IPs differed (e.g., 158.149.114.95=21,443 in 2020-05-05)

- deviation: 23.137.225.33 failures increased from 63,681 to 128,728 (approx. +102%) vs 2020-05-05




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Concentrated suspicious authentication activity suggests inadequate detection/response controls, increasing the probability of security incidents.



**Recommendation:** Classify each top source IP as 'expected' vs 'unexpected' (service accounts, NAT gateways, monitoring systems). For unexpected sources, block or challenge (WAF/IdP protections), and create alerting thresholds for spikes by IP and by user. For internal IPs, verify service credentials, rotate secrets if misused, and correct failing integrations.

---




### Positive Observations

- No account takeovers detected in the provided metrics (account_takeovers=0; users_with_takeover=0), suggesting either effective prevention/detection so far or that compromise has not yet occurred.

- No 'attack_ip_attempts' or 'attack_ip_distinct_ips' were flagged by the metric set (both 0), indicating the current detection logic did not identify explicit attack-IP patterns (though this does not mitigate the MFA gap).




### Trend Analysis


**Degrading:** Authentication failure rate increased vs earlier baselines: 55.48% (current) vs 54.69% (2020-05-05) and 54.08% (2020-02-05)., Concentration of failures from 23.137.225.33 increased substantially vs 2020-05-05 (63,681 to 128,728).


**Stable:** MFA coverage remains unchanged at 0.0% across all compared periods (systemic lack of MFA deployment)., Account takeover indicators remain at 0 across current and historical periods.





## Compliance Observations
### Access-Control Compliance (Article 21)

- The entity shall implement access control policies as part of cybersecurity risk-management measures. [NIS2 Art. 21(2)(i)]  
- Multi-factor authentication (or continuous authentication) solutions shall be used where appropriate. [NIS2 Art. 21(2)(j)]  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1529697). [METRICS mfa]  
- Administrators count is 0; MFA for admins is 0; last_review_date is “unknown.” [METRICS admins]  
- Authentication failures total 3623191 with success_total 2908013; fail_rate is 0.5548. [METRICS auth_failures]  
- Top source IPs for authentication failures include 23.137.225.33 (128728) and 10.0.181.232 (23631). [METRICS auth_failures.top_ips]  
- No data available in the provided evidence for account takeovers or users_with_takeover. [METRICS auth_failures]  
- The entity shall take corrective measures without undue delay if it does not comply with Article 21(2) measures. [NIS2 Art. 21(4)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures