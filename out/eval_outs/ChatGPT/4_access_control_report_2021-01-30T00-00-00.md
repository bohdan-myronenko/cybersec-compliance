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


Across the last 90 days (ending 2021-01-30), the environment shows a severe and persistent non-compliance posture for NIS2 authentication requirements: MFA is effectively not deployed (0/635,091 users enabled; 0.0% coverage), including zero MFA for admins (admins count=0, with_mfa=0). Authentication activity also shows a high overall failure rate (fail_rate=0.6421; 1,511,918 total failures vs 842,679 successes), with the largest concentration of failures coming from a small set of source IPs (e.g., 170.39.78.106 with 67,563 failures). While no account takeovers and no “attack IP attempts” are flagged in the computed metrics, the combination of zero MFA coverage and elevated authentication failures represents a critical control gap and a likely increased likelihood of credential compromise and unauthorized access under NIS2.


### Security Findings


#### CRITICAL: MFA coverage is 0% for all users (including no MFA for admins)

Multi-factor authentication is not enabled for any user accounts. Current metrics show 635,091 distinct users with 0 enabled for MFA (coverage_pct=0.0). Additionally, the admins dataset indicates 0 admins and 0 with MFA, and last_review_date is unknown—suggesting either missing admin inventory or lack of MFA enforcement for privileged roles. Under NIS2, organizations must implement appropriate measures to secure network and information systems, including access control and authentication hardening; lack of MFA is a direct violation of expected baseline security controls and materially increases risk of account compromise.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement; persistent 0% MFA coverage across historical periods (2020-05-05, 2020-08-03, 2020-11-01).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate technical and organizational measures for securing access/authentication increases the likelihood of unauthorized access and undermines required security of network and information systems.



**Recommendation:** Implement MFA for all users as a mandatory control (start with privileged/admin accounts and then all remaining users). Enforce via centralized identity provider policies (e.g., conditional access / authentication policy), require MFA for every interactive login, and add monitoring/alerting for accounts without MFA. Provide an admin inventory and ensure privileged roles are included in MFA enforcement.

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


#### HIGH: High authentication failure rate indicates persistent unsuccessful login attempts

The system records 1,511,918 total authentication failures versus 842,679 successes, resulting in a fail_rate of 0.6421 (64.21%). This is higher than the 2020-05-05 baseline (fail_rate=0.5469) and higher than 2020-08-03 (0.5548), and slightly lower than 2020-11-01 (0.6968). Even though computed metrics show attack_ip_attempts=0 and account_takeovers=0, the elevated failure rate combined with zero MFA coverage increases the probability of credential stuffing, brute-force attempts, or misconfiguration causing repeated failures.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6421 (64.21%)

- baseline_value: 0.6968 (2020-11-01) / 0.5548 (2020-08-03) / 0.5469 (2020-05-05)

- deviation: Compared to 2020-08-03: +15.7 percentage points (0.6421 - 0.5548). Compared to 2020-05-05: +9.7 percentage points (0.6421 - 0.5469).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inadequate authentication resilience and insufficient detection/response to repeated failed logins can lead to unauthorized access and does not demonstrate effective security measures for access to systems.



**Recommendation:** Tune and enforce protective controls: (1) enable MFA (Finding 001), (2) implement rate limiting and progressive backoff for failed logins, (3) enforce account lockout or risk-based throttling for repeated failures, (4) require strong password policies and block known-bad credentials where applicable, and (5) investigate top failure sources (e.g., 170.39.78.106 with 67,563 failures; 10.0.77.230 with 35,558) to determine whether they are legitimate services/users or hostile activity. Add alerts for spikes in fail_rate and for repeated failures per account/IP.

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


#### HIGH: Concentration of failures in a small set of source IPs suggests targeted attempts or misconfiguration

Authentication failures are heavily concentrated. The top IPs account for a large share of failures (e.g., 170.39.78.106: 67,563; 10.0.77.230: 35,558; 10.1.6.103: 9,507; 10.0.181.231: 8,202; 10.0.181.232: 8,092). This pattern is consistent with either (a) automated credential attempts from a limited set of hosts, or (b) internal integration/service accounts repeatedly failing authentication due to configuration drift. With MFA disabled, both scenarios increase risk of compromise and operational instability.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IP failure counts: 67,563 (170.39.78.106), 35,558 (10.0.77.230), 9,507 (10.1.6.103), 8,202 (10.0.181.231), 8,092 (10.0.181.232)

- baseline_value: Historical top IPs differed (e.g., 10.3.205.197: 443,523 in 2020-11-01; 23.137.225.33: 128,728 in 2020-08-03)

- deviation: Different top IPs across periods, but persistent concentration behavior indicates recurring sources of failed authentication.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of effective monitoring/response to repeated failed authentication attempts undermines the ability to ensure security of access to network and information systems.



**Recommendation:** Perform targeted investigations for the top failure IPs: identify whether they correspond to known NAT gateways, VPN endpoints, service accounts, or third-party integrations. If legitimate, remediate authentication configuration and ensure MFA/service authentication patterns are correctly implemented (e.g., use appropriate non-interactive auth methods for services). If not legitimate, block/limit at the network and identity layers and create incident tickets. Implement per-IP and per-account anomaly detection.

---


#### MEDIUM: Admin role inventory and review status are missing/unknown

The admins metric reports count=0 and last_review_date='unknown'. This prevents validation that privileged accounts exist, are identified, and are covered by required security controls (notably MFA). Even if the count is correct, the absence of a review date indicates weak governance evidence for NIS2 compliance reporting.


**Evidence:**

- metric: admins.last_review_date

- current_value: unknown

- baseline_value: unknown

- deviation: No evidence of governance improvement; review status remains unavailable.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient governance evidence for access control and authentication measures reduces assurance that appropriate security measures are maintained for privileged access.



**Recommendation:** Create/maintain an authoritative privileged access inventory (admins/roles) and record last review dates. Ensure privileged accounts are included in MFA enforcement and that periodic access reviews are auditable. Provide compliance evidence artifacts (policy, configuration screenshots/exports, and review logs).

---




### Positive Observations

- No account takeovers detected in computed metrics (account_takeovers=0; users_with_takeover=0), suggesting either effective detection or limited successful compromise events during the window.

- No “attack_ip_attempts” or “attack_ip_distinct_ips” are flagged (both 0), indicating the detection pipeline did not classify these failures as confirmed attack-IP patterns—useful as a starting point for tuning rather than immediate escalation based solely on that label.




### Trend Analysis

**Improving:** Authentication failure rate is slightly lower than the 2020-11-01 baseline (current 0.6421 vs 0.6968), indicating some reduction in failure intensity compared to that earlier period.


**Degrading:** Authentication failure rate is higher than 2020-08-03 (0.6421 vs 0.5548) and 2020-05-05 (0.6421 vs 0.5469), indicating worsening compared to those baselines., MFA coverage remains at 0.0% across all compared historical periods (persistent degradation/no progress).


**Stable:** MFA coverage is consistently 0.0% across all provided historical snapshots (no change)., No account takeovers are detected across current and historical snapshots (account_takeovers=0).





## Compliance Observations
## Access-Control Compliance (Concise)

- The entity shall implement access control policies as part of human resources security and asset management measures. [NIS2 Art. 21(2)(i)]

- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 635091). [METRICS mfa]

- Administrators count is 0; administrators with MFA is 0; last_review_date is “unknown”. [METRICS admins]

- Authentication failures total 1511918 with success_total 842679 (fail_rate 0.6421). [METRICS auth_failures]

- Top authentication failure IPs include 170.39.78.106 (67563) and 10.0.77.230 (35558). [METRICS auth_failures.top_ips]

- If the entity does not comply with required measures, it shall take corrective measures without undue delay. [NIS2 Art. 21(4)]

- No data available in the provided evidence for access-control policy existence, effectiveness assessments, or cryptography/encryption usage. [NIS2 Art. 21(2)(f),(h),(i)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures