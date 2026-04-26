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


For the 90-day window ending 2021-01-30, the environment shows a severe NIS2 compliance gap in authentication hardening: MFA is effectively not deployed (0/635,091 users enabled; 0.0% coverage), and there are very high authentication failure rates (1,511,918 total failures with a 64.21% fail rate). While no account takeovers or “attack IP attempts” are detected in the computed metrics, the combination of zero MFA coverage and elevated failure activity represents a major risk of unauthorized access and non-compliance with NIS2 security requirements. Additionally, there are no recorded admins (0) and no admin MFA coverage/last review date, indicating missing governance/visibility controls.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any user accounts in the analyzed period. This is a direct control failure for NIS2 baseline security measures, significantly increasing the likelihood and impact of credential compromise. With 635,091 distinct users and 0 enabled for MFA, the organization cannot demonstrate that strong authentication is enforced for access to systems/services.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement; remains at 0.0% across baseline periods (2020-05-05, 2020-08-03, 2020-11-01).

- supporting_metric: mfa.enabled_users

- current_value_supporting: 0

- baseline_value_supporting: 0




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate measures to secure network and information systems, including access control and authentication hardening, undermines compliance expectations for risk-based security controls.



**Recommendation:** Implement MFA for all users as a priority, starting with privileged/admin accounts and then expanding to all accounts. Enforce MFA at authentication layer (IdP) with phishing-resistant options where feasible. Provide an auditable rollout plan and evidence (MFA policy configuration, enforcement logs, and coverage reporting) for NIS2 compliance.

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


#### HIGH: High authentication failure rate indicates potential brute-force/credential stuffing or misconfiguration

Authentication failures are extremely high: 1,511,918 total failures with 842,679 successes, resulting in a 64.21% fail rate. Even though computed metrics show 0 detected account takeovers and 0 attack-IP attempts, the failure volume and concentration in top source IPs suggests ongoing unsuccessful login attempts or systemic authentication issues (e.g., incorrect credentials, outdated clients, or weak rate limiting). This increases the risk of eventual compromise and indicates insufficient detection/prevention controls.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6421 (64.21%)

- baseline_value: 0.6968 (69.68%)

- deviation: Improved by ~5.47 percentage points vs 2020-11-01 baseline, but remains very high.

- supporting_metrics: [{'metric': 'auth_failures.total', 'current_value': '1511918', 'baseline_value': '6487620', 'deviation': 'Lower absolute volume than 2020-11-01 baseline, but fail rate remains concerning.'}, {'metric': 'auth_failures.success_total', 'current_value': '842679', 'baseline_value': '2822319', 'deviation': 'Lower absolute volume; interpret with caution due to differing period sizes.'}]

- top_ips_observed: [{'ip': '170.39.78.106', 'count': 67563}, {'ip': '10.0.77.230', 'count': 35558}, {'ip': '10.1.6.103', 'count': 9507}, {'ip': '10.0.181.231', 'count': 8202}, {'ip': '10.0.181.232', 'count': 8092}]




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent authentication failures without strong preventive controls (e.g., MFA, rate limiting, lockout, anomaly detection) indicate inadequate measures to protect systems against unauthorized access.



**Recommendation:** Triage the top failing source IPs and authentication endpoints: (1) verify whether failures are from legitimate services/users (e.g., misconfigured integrations) vs external attempts; (2) enable/verify rate limiting, progressive backoff, and account lockout policies; (3) deploy alerting for abnormal failure spikes and credential-stuffing patterns; (4) ensure MFA is enforced (ties directly to Finding 001) to reduce successful credential replay impact.

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


#### HIGH: Privileged access governance data missing (0 admins recorded; no MFA/last review evidence)

The computed metrics report 0 admins and 0 admins with MFA, with last_review_date marked as 'unknown'. This prevents validation of privileged access controls and review processes. For NIS2, organizations must be able to demonstrate governance over access rights, especially for administrative roles. The absence of admin records may indicate either (a) a data collection gap, or (b) a real lack of privileged account governance.


**Evidence:**

- metric: admins.count

- current_value: 0

- baseline_value: 0

- deviation: No change, but baseline also shows unknown governance evidence.

- supporting_metrics: [{'metric': 'admins.last_review_date', 'current_value': 'unknown', 'baseline_value': 'unknown', 'deviation': 'No evidence of review cadence.'}, {'metric': 'admins.with_mfa', 'current_value': '0', 'baseline_value': '0', 'deviation': 'Cannot validate privileged MFA enforcement.'}]




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inability to evidence privileged access management and review undermines compliance with access control and risk management expectations.



**Recommendation:** Fix privileged access visibility and evidence: (1) ensure admin/privileged role inventory is correctly populated from IAM/IdP; (2) record last review dates and review outcomes; (3) enforce MFA for all privileged roles; (4) implement periodic access reviews (e.g., quarterly) with audit logs retained for NIS2 reporting.

---


#### MEDIUM: Authentication failures concentrated in a small set of source IPs

A small number of source IPs account for a large share of failures (e.g., 170.39.78.106 with 67,563 failures; 10.0.77.230 with 35,558). This concentration can indicate targeted attempts or a misconfigured internal client repeatedly failing authentication. Even without detected account takeovers, concentration suggests the need for targeted mitigation and validation of affected systems.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top 5 IPs: 67,563; 35,558; 9,507; 8,202; 8,092 failures

- baseline_value: Different top IPs in baseline periods; no direct comparable IP-level mapping provided

- deviation: Concentration pattern present in current period; baseline shows different dominant IPs.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Concentrated authentication failures without effective controls can indicate insufficient protective measures against unauthorized access attempts.



**Recommendation:** For each top IP: identify ownership (internal service vs external), map to target applications, and determine root cause. Apply targeted controls (IP allowlists/denylists where appropriate, fix client credentials/configuration, and enforce MFA/rate limiting). Document findings for compliance evidence.

---




### Positive Observations

- No computed account takeovers detected (account_takeovers=0; users_with_takeover=0), suggesting either effective prevention/detection for successful compromise or limited takeover classification in the dataset.

- Authentication fail rate shows improvement vs 2020-11-01 baseline (64.21% current vs 69.68% baseline), indicating some reduction in failure intensity even though the overall level remains high.




### Trend Analysis

**Improving:** auth_failures.fail_rate improved from 0.6968 (69.68%) in 2020-11-01 to 0.6421 (64.21%) in the current 90-day window.


**Degrading:** No improvement in MFA deployment: mfa.coverage_pct remains 0.0% (no progress across all provided baseline periods).


**Stable:** No detected account takeovers across periods (account_takeovers=0 in current and baseline)., Admin governance evidence remains unavailable/unknown (admins.last_review_date='unknown' in current and baseline).





## Compliance Observations
## Access-control compliance (Article 21)

- The entity must implement access control policies as part of cybersecurity risk-management measures [NIS2 Art. 21(2)(i)].  
- Multi-factor authentication (or continuous authentication) must be used where appropriate [NIS2 Art. 21(2)(j)].  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 635091) [METRICS mfa].  
- No administrators are recorded (admins.count: 0) and no administrators have MFA (admins.with_mfa: 0) [METRICS admins].  
- Authentication failures total 1,511,918 with success_total 842,679 (fail_rate 0.6421) [METRICS auth_failures].  
- Top source IPs for authentication failures include 170.39.78.106 (67,563) and 10.0.77.230 (35,558) [METRICS auth_failures.top_ips].  
- No data is available on whether access-control measures are assessed for effectiveness [NIS2 Art. 21(2)(f)] (no related metrics provided).  
- No data is available on cryptography/encryption use for access control [NIS2 Art. 21(2)(h)] (no related metrics provided).  
- No data available in the provided evidence on corrective actions for non-compliance [NIS2 Art. 21(4)].

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures