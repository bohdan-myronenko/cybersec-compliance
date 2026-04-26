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


Across the 90-day window (ending 2019-11-07), the organization shows a severe NIS2-relevant authentication control gap: MFA is not enabled for any user (0% coverage), including zero MFA coverage for admins. In parallel, authentication activity shows a high overall failure rate (fail_rate 0.5069; 61,540 total failures vs 59,871 successes), indicating persistent unsuccessful authentication attempts. While no account takeovers or attack-IP patterns were detected (attack_ip_attempts=0; account_takeovers=0), the combination of zero MFA coverage and elevated auth failures represents a critical compliance and security risk under NIS2 requirements for risk management and access control.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any of the 50,215 distinct users observed in the period. This creates a single-factor authentication exposure for all accounts, substantially increasing the likelihood and impact of credential compromise. For NIS2, this is a direct failure to implement appropriate technical and organizational measures for access control and risk reduction.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0% (2021-01-30 and 2020-11-01)

- deviation: No improvement; remains at 0.0% across historical periods




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of MFA undermines appropriate measures for securing network and information systems, particularly access control and resilience against unauthorized access.



**Recommendation:** Implement MFA for all users with a phased rollout (e.g., 100% for admins immediately, then all users within a defined SLA such as 30–60 days). Enforce MFA at authentication policy level (IdP/SAML/OIDC), disable legacy non-MFA auth paths, and require re-authentication for existing sessions after enforcement.

---


#### CRITICAL: No MFA coverage for administrators (admins count=0 / with_mfa=0)

The metrics report 0 administrators and 0 admins with MFA. This is either (a) an instrumentation/data quality issue (admins not correctly identified), or (b) a governance failure where privileged accounts are not being tracked and protected with MFA. Either way, it prevents assurance that privileged access is adequately secured.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0 (2021-01-30 and 2020-11-01)

- deviation: No improvement; privileged MFA assurance is absent




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inadequate or unverified privileged access controls reduce the effectiveness of measures intended to prevent unauthorized access and limit impact of compromise.



**Recommendation:** Fix privileged-account inventory and monitoring: (1) ensure admin/privileged roles are correctly mapped in the identity system and reporting pipeline; (2) require MFA for all privileged roles immediately; (3) add periodic access reviews and evidence generation for compliance reporting.

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


#### HIGH: High authentication failure rate (50.69%) indicating persistent unsuccessful logins

Authentication failures are substantial: 61,540 total auth failures with 59,871 successes, producing a fail_rate of 0.5069. This level of failure can indicate credential stuffing, misconfiguration, user error, or brute-force attempts. Even though account takeover and attack-IP detection are currently zero, the failure volume increases the probability of eventual compromise and can also indicate weaknesses in authentication throttling and monitoring.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5069

- baseline_value: 0.6421 (2021-01-30) and 0.6968 (2020-11-01)

- deviation: Improved vs 2021-01-30 by ~-13.12 percentage points; improved vs 2020-11-01 by ~-19.59 percentage points




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Elevated authentication failures suggest insufficient protective measures (e.g., rate limiting, monitoring, and access control hardening) to prevent unauthorized access attempts.



**Recommendation:** Triage and harden authentication: (1) enable/verify rate limiting and lockout/backoff policies for repeated failures; (2) review authentication logs for patterns by username, client, and geolocation; (3) implement alerting for spikes in failures and for repeated failures from the same source; (4) validate that MFA enforcement (once implemented) is applied to all authentication flows to reduce successful compromise risk.

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


#### MEDIUM: Concentrated auth failures from internal source IPs

Top source IPs generating failures are concentrated in a small set of internal addresses (e.g., 10.0.181.226 count=187; 10.0.181.227 count=183; 10.0.77.228 count=108; 10.0.77.226 count=104; 10.0.77.229 count=94). This may reflect internal automation, misconfigured services, or internal credential misuse. The absence of detected attack-IP attempts (attack_ip_attempts=0) suggests the detection logic may not classify these as attacks, or that the activity is internal/benign—either way it warrants investigation.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IP counts: 187, 183, 108, 104, 94 (total failures=61,540)

- baseline_value: Different top IPs in prior periods; no comparable internal concentration provided

- deviation: New concentration pattern in current period; requires validation against expected internal traffic




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Unexplained or unmanaged authentication failure sources can indicate inadequate monitoring and incident prevention controls.



**Recommendation:** Investigate the top failing IPs: map each IP to owning system/service, confirm expected authentication behavior, and correct misconfigurations. If unexpected, apply targeted controls (block/allow lists, service account remediation, and stricter auth policies for those sources).

---




### Positive Observations

- Authentication failure rate has improved compared to historical periods (current fail_rate 0.5069 vs 0.6421 in 2021-01-30 and 0.6968 in 2020-11-01).

- No account takeovers detected in the period (account_takeovers=0; users_with_takeover=0), suggesting either effective detection/controls or lack of successful compromise events.




### Trend Analysis

**Improving:** auth_failures.fail_rate decreased to 0.5069 from 0.6421 (2021-01-30) and 0.6968 (2020-11-01).


**Degrading:** No degradation in MFA metrics is shown, but the current state remains at 0% coverage, indicating a persistent control gap rather than improvement.


**Stable:** attack_ip_attempts remains 0 and account_takeovers remains 0 across current and historical snapshots.





## Compliance Observations
## Access-Control Compliance (Cybersecurity Risk-Management)

- The entity shall implement access control policies as part of cybersecurity risk-management measures. [NIS2 Art. 21(2)(i)]

- The entity shall use multi-factor authentication (or continuous authentication solutions) where appropriate. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 50215). [METRICS mfa]

- MFA is not enabled for administrators (admins count: 0; with_mfa: 0). [METRICS admins]

- Authentication failures total 61540; success_total 59871; fail_rate 0.5069. [METRICS auth_failures]

- Top authentication-failure source IPs include 10.0.181.226 (187) and 10.0.181.227 (183). [METRICS auth_failures.top_ips]

- No attack-IP attempts or distinct attack IPs were recorded (attack_ip_attempts: 0; attack_ip_distinct_ips: 0). [METRICS auth_failures]

- If the entity does not comply with required measures, corrective actions shall be taken without undue delay. [NIS2 Art. 21(4)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures