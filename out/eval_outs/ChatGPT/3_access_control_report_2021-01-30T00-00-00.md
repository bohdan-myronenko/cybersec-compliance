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


Across the last 90 days (ending 2021-01-30), the environment shows a severe and persistent NIS2 compliance gap: MFA is effectively not deployed (0% coverage) for 635,091 users, including zero identified admins with MFA. Authentication activity also shows a high overall failure rate (64.21% of attempts failing: 1,511,918 total failures vs 842,679 successes), with the majority of failures concentrated in a small set of source IPs. While no account takeovers or explicit “attack IP attempts” were detected by the metric set, the combination of missing MFA and elevated authentication failures represents a high likelihood of successful credential-based compromise and non-compliance with NIS2 security requirements.


### Security Findings


#### CRITICAL: MFA coverage is 0% for all users (no MFA enforcement)

Multi-factor authentication is not enabled for any user accounts. This is a direct control failure for identity security and significantly increases the risk of account compromise via stolen credentials, phishing, or brute-force attempts. The issue is persistent across historical baselines, indicating systemic misconfiguration or a control not implemented at all.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0% (enabled_users=0 / total_users=635,091)

- baseline_value: 0.0% (enabled_users=0 / total_users=1,596,182 on 2020-11-01; also 0.0% on 2020-08-03 and 2020-05-05)

- deviation: No improvement; control remains absent across all compared periods




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate measures for network and information system security, including access control and authentication hardening, increases the likelihood of incidents and indicates non-compliance.



**Recommendation:** Implement MFA for all users with a phased enforcement plan: (1) immediately require MFA for all privileged/admin and high-risk accounts, (2) then enforce MFA for all remaining users, (3) block sign-in without MFA where supported, and (4) document exceptions (if any) with time-bound risk acceptance and compensating controls. Validate via an automated control report showing enabled_users > 0 and coverage trending toward 100%.

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


#### CRITICAL: High authentication failure rate indicates credential attacks or misconfiguration

Authentication failures are extremely high: 1,511,918 failures vs 842,679 successes, producing a 64.21% failure rate. This level of failure is consistent with brute-force attempts, repeated incorrect credentials, or systemic authentication issues. Even though the metric set reports 0 detected account takeovers, the absence of MFA makes successful compromise more likely.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6421 (64.21%)

- baseline_value: 0.6968 (69.68%) on 2020-11-01; 0.5548 (55.48%) on 2020-08-03; 0.5469 (54.69%) on 2020-05-05

- deviation: Decreased vs 2020-11-01 by ~5.47 percentage points, but remains very high and above earlier baselines (still worse than 2020-08-03 and 2020-05-05)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent abnormal authentication behavior without strong compensating controls (e.g., MFA) undermines the effectiveness of security measures and increases incident risk.



**Recommendation:** Perform an authentication failure investigation focused on: (1) top failing source IPs (170.39.78.106 count=67,563; 10.0.77.230 count=35,558; 10.1.6.103 count=9,507; 10.0.181.231 count=8,202; 10.0.181.232 count=8,092), (2) implement/verify rate limiting and lockout/backoff policies, (3) ensure account lockout thresholds are safe (avoid DoS), (4) review password policy and credential stuffing protections, and (5) correlate failures with user agents and geolocation to distinguish attack traffic from legitimate misconfiguration.

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


#### HIGH: No admins identified and no admin MFA coverage (privileged access control gap)

The dataset reports admins.count=0 and admins.with_mfa=0 with last_review_date='unknown'. This suggests either (a) privileged accounts are not being classified/monitored, or (b) privileged access is not governed with auditable controls. Under NIS2, privileged access must be explicitly managed and reviewed.


**Evidence:**

- metric: admins.count / admins.with_mfa

- current_value: admins.count=0, admins.with_mfa=0, last_review_date=unknown

- baseline_value: admins.count=0, admins.with_mfa=0, last_review_date=unknown (all historical snapshots provided)

- deviation: No change; privileged access governance appears untracked




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of auditable privileged access management and review undermines access control measures required for reducing security incident likelihood.



**Recommendation:** Establish a definitive privileged identity inventory: (1) define admin roles/groups in the identity provider, (2) ensure the monitoring pipeline correctly populates admins.count, (3) require MFA for all privileged roles, and (4) set a documented review cadence (e.g., monthly) with last_review_date populated by the reporting system.

---


#### MEDIUM: Authentication failures concentrated in a small set of IPs

Top source IPs account for large portions of failures, indicating targeted activity or a small number of misbehaving clients. This concentration can be a sign of credential stuffing, automated probing, or internal service misconfiguration generating repeated failed logins.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IPs: 170.39.78.106 (67,563), 10.0.77.230 (35,558), 10.1.6.103 (9,507), 10.0.181.231 (8,202), 10.0.181.232 (8,092)

- baseline_value: Different top IPs in earlier periods (e.g., 10.3.205.197=443,523 on 2020-11-01; 23.137.225.33=128,728 on 2020-08-03)

- deviation: Concentration persists, but the specific IPs change across periods




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Concentrated abnormal authentication activity indicates the need for effective monitoring and incident prevention controls.



**Recommendation:** For each top IP, determine ownership and intent: (1) check whether IPs belong to known NAT gateways, VPNs, or corporate networks, (2) if external/unknown, add temporary blocking or challenge controls, (3) if internal, identify the affected application/service and correct authentication behavior, and (4) create detection rules for spikes in failure rate per IP/user.

---




### Positive Observations

- No account takeovers detected by the provided metrics (account_takeovers=0; users_with_takeover=0), suggesting either detection is effective or compromise has not been observed in this window.

- Attack-IP attempt metrics are reported as zero (attack_ip_attempts=0; attack_ip_distinct_ips=0), indicating the specific attack classification used by the metric set did not trigger.




### Trend Analysis

**Improving:** Authentication failure rate decreased vs 2020-11-01: 69.68% -> 64.21% (approx. -5.47 percentage points).


**Degrading:** MFA coverage remains at 0.0% across all compared periods (no progress toward compliance).


**Stable:** No detected account takeovers across all provided snapshots (0 in current and historical)., Admins inventory remains unpopulated (admins.count=0) with last_review_date='unknown' in current and historical data.





## Compliance Observations
## Access-Control Compliance (Concise)

- The entity shall implement access control policies as part of human resources security and asset management measures. [NIS2 Art. 21(2)(i)]

- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 635091). [METRICS mfa]

- Administrators count is 0; administrators with MFA is 0; last_review_date is “unknown”. [METRICS admins]

- No data available in the provided evidence regarding access-control policy effectiveness assessment. [NIS2 Art. 21(2)(f)]

- No data available in the provided evidence regarding cryptography/encryption use supporting access control. [NIS2 Art. 21(2)(h)]

- No data available in the provided evidence regarding corrective measures taken for non-compliance. [NIS2 Art. 21(4)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures