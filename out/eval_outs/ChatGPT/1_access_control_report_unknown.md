# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** Unknown period

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **1**
- Distinct users: **0**
- Distinct source IPs: **0**

### Authentication
- Successful logins: **0**
- Failed logins: **0**
- Failure rate: **0.0**
- Top failing IPs:  

  - No failures detected


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


The current computed metrics indicate a severe data/telemetry anomaly and a major compliance gap for NIS2: MFA coverage is 0% (0/0 users enabled) and there are no recorded authentication failures or admin accounts in the current dataset (all counts are 0). Compared to historical periods where MFA coverage was also 0% but authentication failures were substantial (e.g., 1,511,918 failures in 2021-01-30), the present period shows an abrupt drop to zero, suggesting either an ingestion/collection failure or a system state where monitoring is not functioning. This prevents reliable assurance of authentication security controls and undermines NIS2 obligations around risk management and security measures.


### Security Findings


#### CRITICAL: Authentication telemetry shows a complete drop to zero (possible monitoring/collection failure)

In the analyzed period, authentication failure metrics are entirely absent (total auth failures = 0) and there are no recorded source IPs or distinct users in the frame. Historically, the environment recorded large volumes of auth failures (millions over prior periods). This abrupt change strongly suggests that logs/metrics are not being collected, parsed, or attributed correctly for the current period, which blocks compliance reporting and incident detection.


**Evidence:**

- metric: auth_failures.total and frame.distinct_users/distinct_src_ips

- current_value: {'auth_failures.total': 0, 'frame.rows': 1, 'frame.distinct_users': 0, 'frame.distinct_src_ips': 0}

- baseline_value: {'auth_failures.total': 1511918, 'frame.rows': 2354597, 'frame.distinct_users': 635091, 'frame.distinct_src_ips': 505308}

- deviation: Auth failures dropped from 1,511,918 to 0 (100% decrease). Frame activity dropped from 2,354,597 rows to 1 and distinct users from 635,091 to 0 (effectively 100% decrease).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to ensure appropriate risk management and security measures is evidenced by missing/invalid telemetry, preventing effective detection, monitoring, and reporting of security events.



**Recommendation:** Immediately validate the logging/metrics pipeline for the current period: confirm source log availability, ingestion job health, parsing rules, time-window alignment, and dashboard query filters. Re-run the metrics computation on raw logs for the same time window and compare counts to ensure the '0' values are not due to data loss or query misconfiguration.

---


#### CRITICAL: MFA coverage is effectively non-existent (0% enabled) and cannot be validated due to zero user population in current data

MFA coverage is reported as 0.0% with total_users=0 and enabled_users=0 in the current period. While historical periods also show 0% MFA enabled (e.g., 635,091 users with 0 enabled in 2021-01-30), the current period additionally indicates that the user population is not being captured (total_users=0). This prevents assurance that MFA is implemented for access to network and information systems and indicates a major control deficiency.


**Evidence:**

- metric: mfa.coverage_pct and mfa.total_users/enabled_users

- current_value: {'mfa.total_users': 0, 'mfa.enabled_users': 0, 'mfa.coverage_pct': 0.0}

- baseline_value: {'mfa.total_users': 635091, 'mfa.enabled_users': 0, 'mfa.coverage_pct': 0.0}

- deviation: MFA coverage remains at 0.0% (no improvement). Additionally, current total_users is 0 vs 635,091 historically, indicating either missing identity population data or telemetry failure.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of MFA for authentication materially weakens access control and increases the likelihood/impact of account compromise, undermining required security measures.



**Recommendation:** Fix identity population reporting first (ensure user inventory is correctly joined to MFA status). Then implement MFA for all applicable users (especially privileged/admin and remote access). Set an enforcement target (e.g., 100% for privileged accounts immediately, then all users) and track coverage weekly until complete.

---


#### HIGH: No admin accounts detected; MFA for admins cannot be verified

The current dataset reports admins.count=0 and admins.with_mfa=0 with last_review_date='unknown'. Historically, admins were also 0, suggesting either the admin inventory is not being captured or the metric definition is not aligned with the environment. For NIS2, privileged access controls must be demonstrable; inability to identify admin accounts prevents validation of MFA and review processes.


**Evidence:**

- metric: admins.count, admins.with_mfa, admins.last_review_date

- current_value: {'admins.count': 0, 'admins.with_mfa': 0, 'admins.last_review_date': 'unknown'}

- baseline_value: {'admins.count': 0, 'admins.with_mfa': 0, 'admins.last_review_date': 'unknown'}

- deviation: No change from baseline; however, the absence of any admin accounts is likely a data quality/definition issue rather than a true security posture.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inability to evidence privileged access controls (including MFA and review cadence) indicates insufficient demonstrable security measures.



**Recommendation:** Align the 'admin' metric definition with your identity provider roles/groups (e.g., map to privileged roles such as Global Admin/Domain Admin/Root). Populate admins.count from authoritative IAM sources and record last review dates. Require MFA for all privileged roles and implement periodic access reviews with auditable evidence.

---


#### MEDIUM: No attack indicators or account takeover signals in current period (likely due to missing data)

The current period shows auth_failures.attack_ip_attempts=0, attack_ip_distinct_ips=0, account_takeovers=0, users_with_takeover=0. Given the historical presence of large auth failure volumes (e.g., 1,511,918 failures in 2021-01-30) and non-zero top IPs, the complete absence of attack signals again points to missing telemetry rather than a genuinely threat-free period.


**Evidence:**

- metric: auth_failures.attack_ip_attempts / account_takeovers

- current_value: {'attack_ip_attempts': 0, 'attack_ip_distinct_ips': 0, 'account_takeovers': 0, 'users_with_takeover': 0}

- baseline_value: {'attack_ip_attempts': 0, 'attack_ip_distinct_ips': 0, 'account_takeovers': 0, 'users_with_takeover': 0}

- deviation: No change vs baseline for these specific fields, but overall auth_failures.total dropped from 1,511,918 to 0, making attack detection signals unreliable for the current period.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): If monitoring is not producing expected signals, the organization cannot demonstrate effective detection and response capabilities.



**Recommendation:** After fixing telemetry, validate detection logic: confirm thresholds, IP reputation/attack classification rules, and account takeover correlation logic. Produce a backfill for the current period to ensure attack indicators are computed from raw events.

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/0 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---




### Positive Observations

- No account takeover events are reported in the current dataset (account_takeovers=0), though this is not reliable until telemetry is validated.

- No attack IP attempts are flagged (attack_ip_attempts=0), which may indicate either effective prevention or, more likely, missing detection inputs given the zero auth failure volume.




### Trend Analysis


**Degrading:** Authentication failure volume degraded from historical 1,511,918 failures (2021-01-30) to 0 in the current period (100% decrease), indicating a major monitoring/visibility regression., User and source IP visibility degraded from historical distinct_users=635,091 and distinct_src_ips=505,308 to 0 in the current period.


**Stable:** MFA coverage remains at 0.0% (historical and current), indicating no progress on MFA enablement.





## Compliance Observations
### Access-Control Compliance (Cybersecurity Risk-Management)

- The entity shall implement access control policies as part of human resources security and asset management measures. [NIS2 Art. 21(2)(i)]

- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]

- MFA coverage metrics: total_users=0, enabled_users=0, coverage_pct=0.0. [METRICS mfa]

- Admin MFA metrics: admins count=0, with_mfa=0, last_review_date=unknown. [METRICS admins]

- Authentication failure metrics: total=0, success_total=0, fail_rate=0.0. [METRICS auth_failures]

- No data available in the provided evidence for access-control policy effectiveness assessments. [NIS2 Art. 21(2)(f); METRICS exceptions]

- No data available in the provided evidence for corrective measures taken for non-compliance. [NIS2 Art. 21(4); METRICS exceptions]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures