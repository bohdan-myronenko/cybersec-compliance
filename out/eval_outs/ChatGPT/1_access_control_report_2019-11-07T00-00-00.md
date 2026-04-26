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


For the 90-day window ending 2019-11-07, the environment shows a severe authentication control gap: MFA is effectively not deployed (0 of 50,215 users enabled; 0.0% coverage), and there are substantial authentication failures (61,540 total events with a 50.69% failure rate). No admin accounts are recorded (0 admins; 0 with MFA), which prevents verification of privileged access protections. While no account takeovers or “attack IP” detections are flagged (0 in both categories), the high failure rate combined with zero MFA coverage represents a major NIS2 compliance risk for access control and incident-prevention measures.


### Security Findings


#### CRITICAL: MFA coverage is 0% across all users (major access-control deficiency)

Multi-factor authentication is not enabled for any user in the analyzed dataset. With 50,215 distinct users and 0 enabled for MFA, the organization cannot demonstrate implementation of strong authentication controls for access to network and information systems. This is a direct control failure and materially increases the likelihood and impact of credential compromise.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0% (2021-01-30 and 2020-11-01 also show 0.0%)

- deviation: No improvement; remains at 0.0% across historical periods




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate measures to secure systems and reduce the risk of incidents (e.g., inadequate authentication controls) undermines NIS2 security requirements.



**Recommendation:** Immediately enable MFA for all users, starting with privileged/admin accounts and high-risk roles. Enforce MFA at authentication policy level (not per-app exceptions), require phishing-resistant MFA where feasible, and remove/avoid any MFA bypass paths. Provide an auditable control statement and evidence (policy configuration + user enrollment reports).

---


#### CRITICAL: No admins recorded; privileged access protections cannot be validated

The metrics report 0 admin accounts and 0 admins with MFA. This prevents assurance that privileged accounts are identified, reviewed, and protected with stronger authentication. For NIS2, the inability to demonstrate privileged access governance is a significant compliance and operational risk.


**Evidence:**

- metric: admins.count / admins.with_mfa

- current_value: 0 / 0

- baseline_value: 0 / 0 (historical periods also show 0 / 0)

- deviation: No change; indicates either missing data or a systemic lack of privileged account governance




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inability to demonstrate adequate access control measures for privileged accounts weakens the organization’s security posture and incident prevention capability.



**Recommendation:** Reconcile identity and authorization data sources to ensure admin/privileged roles are correctly enumerated. Implement a privileged access inventory (who/what is admin), require MFA for all privileged accounts, and establish periodic access reviews with documented evidence (last review date should not remain 'unknown').

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


#### HIGH: High authentication failure rate (~50.69%) indicates persistent access attempts or misconfiguration

There were 61,540 authentication failure events with 59,871 successes, producing a 50.69% failure rate. This level of failures can indicate credential stuffing/brute-force attempts, user misconfiguration, or systemic authentication issues. Even though no account takeovers are detected (0), the failure volume combined with 0% MFA coverage increases the probability of eventual compromise and indicates a need for immediate investigation and tuning.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5069 (50.69%)

- baseline_value: 0.6421 (2021-01-30) and 0.6968 (2020-11-01)

- deviation: Improved vs baseline (down from 64.21% and 69.68%), but still very high




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent authentication failures suggest inadequate preventive/detective controls and increase incident likelihood, conflicting with NIS2 expectations for risk management and security measures.



**Recommendation:** Perform an immediate root-cause analysis: (1) validate whether failures are due to incorrect credentials vs. automated attacks; (2) review authentication logs for patterns (time-of-day, usernames, endpoints); (3) implement rate limiting, lockout/backoff, and bot detection; (4) ensure MFA is enforced to reduce successful credential replay. Provide a short-term mitigation plan and a longer-term tuning plan with measurable targets (e.g., reduce failure rate by X% and/or reduce top-IP concentration).

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


#### MEDIUM: Top source IPs show concentrated failure activity (possible internal scanning or NAT concentration)

The top five source IPs account for a meaningful portion of failures (187, 183, 108, 104, 94 respectively). While these are private/internal ranges (10.x), concentration can indicate internal scanning, misconfigured clients, or a NAT gateway generating repeated attempts. This warrants investigation to distinguish benign operational issues from malicious activity.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IP counts: 187, 183, 108, 104, 94 (total failures=61,540)

- baseline_value: Baseline top IPs exist but are different; no comparable concentration metric provided

- deviation: New top-IP set for this period; indicates localized concentration of failures




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Concentrated authentication failures can indicate security-relevant activity; insufficient investigation and control tuning can lead to incidents.



**Recommendation:** Investigate the top source IPs (10.0.181.226/227 and 10.0.77.228/226/229): map them to owning systems/users, check for recent changes (client deployments, password rotation, SSO/MFA policy changes), and verify whether they correspond to legitimate services. If malicious/unauthorized, block at network controls and enforce stronger authentication (MFA) and rate limiting.

---




### Positive Observations

- Authentication failure rate has improved compared to historical periods (50.69% current vs 64.21% in 2021-01-30 and 69.68% in 2020-11-01).

- No account takeovers are detected in the current metrics (account_takeovers=0; users_with_takeover=0), suggesting no confirmed credential compromise in this dataset.




### Trend Analysis

**Improving:** auth_failures.fail_rate decreased to 0.5069 from 0.6421 (2021-01-30) and 0.6968 (2020-11-01).



**Stable:** mfa.coverage_pct remains 0.0% across all provided periods (current and historical)., account_takeovers remains 0 across provided periods (no detected takeovers).





## Compliance Observations
## Access-Control Compliance (Cybersecurity Risk-Management)

- The entity must implement access control policies as part of cybersecurity risk-management measures. [article_21_cybersecurity_risk-management_measures Art. 21(2)(i)]

- The entity must use multi-factor authentication (or continuous authentication solutions) where appropriate. [article_21_cybersecurity_risk-management_measures Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 50215). [METRICS JSON: mfa.coverage_pct, mfa.enabled_users, mfa.total_users]

- Authentication failures total 61540; success_total 59871; fail_rate 0.5069. [METRICS JSON: auth_failures.total, auth_failures.success_total, auth_failures.fail_rate]

- Top source IPs for authentication failures include 10.0.181.226 (187) and 10.0.181.227 (183). [METRICS JSON: auth_failures.top_ips]

- No data available in the provided evidence for admin access-control review status (admins.last_review_date: "unknown"). [METRICS JSON: admins.last_review_date]

- No data available in the provided evidence for exceptions handling related to access control (exceptions: []). [METRICS JSON: exceptions]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures