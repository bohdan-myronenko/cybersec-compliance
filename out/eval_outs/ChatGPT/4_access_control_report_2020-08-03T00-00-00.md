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


For the 90-day window ending 2020-08-03, the organization shows a severe authentication control gap: MFA is not enabled for any user (0% coverage), including zero MFA coverage for admins (admins count reported as 0, with last review date unknown). Authentication attempts exhibit a high and persistent failure rate (~55.5%), with the largest concentration of failures coming from a small set of source IPs (e.g., 23.137.225.33 with 128,728 failures). While no account takeovers or “attack IP attempts” are detected in the computed metrics, the lack of MFA and the elevated failure rate represent major NIS2 compliance risks related to access control and incident prevention/detection.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any of the 1,529,697 distinct users in the analyzed dataset. This is a direct and material failure of baseline access control hardening expected under NIS2 for reducing the likelihood and impact of compromised credentials. The same condition is present in all provided historical baselines, indicating a long-standing control deficiency rather than a transient issue.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0% (2020-05-05), 0.0% (2020-02-05), 0.0% (2019-11-07)

- deviation: No improvement over time; remains at 0.0% across all baselines




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient access control measures (no MFA) increases risk of unauthorized access and undermines required security of network and information systems.



**Recommendation:** Implement MFA for all users with a phased rollout (start with privileged/admin and high-risk user groups), enforce MFA at authentication boundaries, and require re-authentication for existing sessions. Provide an auditable control mapping and evidence (MFA enablement logs, policy configuration, and coverage reports) to demonstrate compliance.

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


#### HIGH: High authentication failure rate (~55.5%) persists vs baseline

Authentication failures are high: total failures are 3,623,191 with 2,908,013 successes, producing a fail rate of 0.5548 (55.48%). Compared to the previous baseline period (2020-05-05), the fail rate increased from 0.5469 to 0.5548 (~+0.79 percentage points). Elevated failure rates can indicate credential stuffing, misconfiguration, or brute-force attempts; even though computed metrics show no account takeovers, the failure volume increases operational risk and may signal ongoing hostile activity or systemic authentication issues.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5548 (55.48%)

- baseline_value: 0.5469 (54.69%) on 2020-05-05

- deviation: +0.79 percentage points (approx. +1.4% relative increase)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Weak or ineffective authentication resilience and monitoring can lead to unauthorized access attempts and insufficient prevention/detection of security incidents.



**Recommendation:** Tune and enforce rate limiting and lockout/backoff policies for authentication endpoints, deploy/validate bot and credential-stuffing protections, and correlate failure spikes with user/account and geo/device signals. Produce a weekly report of top failure sources and affected accounts, and ensure alerting thresholds are aligned to the observed baseline.

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


#### HIGH: Concentrated authentication failures from a small set of IPs

The top source IP 23.137.225.33 accounts for 128,728 authentication failures, far exceeding other listed sources (e.g., 10.0.181.232: 23,631; 109.203.1.148: 19,053). This concentration suggests automated activity (credential stuffing/brute force) or a misrouted integration. Although computed metrics report attack_ip_attempts=0 and account_takeovers=0, the failure concentration warrants investigation and targeted mitigation.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: 23.137.225.33=128,728 failures; next highest=10.0.181.232=23,631

- baseline_value: Top IP changed vs 2020-05-05 (23.137.225.33=63,681 then; 158.149.114.95=21,443 then)

- deviation: 23.137.225.33 failures increased from 63,681 (2020-05-05) to 128,728 (2020-08-03 window), ~+102%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent suspicious authentication activity indicates inadequate protective controls and/or insufficient monitoring and response processes.



**Recommendation:** Investigate the top IPs: determine whether they belong to known services, VPNs, NAT gateways, or threat infrastructure. If not authorized, block or challenge them (WAF/Firewall rules, geo/IP reputation, or step-up authentication). If authorized, remediate the integration causing repeated failures (credentials, token handling, clock skew, or endpoint mismatch).

---


#### MEDIUM: Privileged access governance evidence missing (admins count=0, last_review_date unknown)

The computed metrics report admins.count=0 and admins.with_mfa=0 with last_review_date='unknown'. This is inconsistent with typical enterprise environments and prevents validation of privileged access controls and MFA coverage for administrators. Even if the dataset does not include admin accounts, the absence of review evidence is a compliance and auditability concern.


**Evidence:**

- metric: admins.last_review_date

- current_value: unknown

- baseline_value: unknown (all provided baselines)

- deviation: No evidence of privileged access review; cannot verify MFA coverage for privileged accounts




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of auditable privileged access governance undermines access control assurance required for NIS2-aligned security measures.



**Recommendation:** Establish and report an authoritative inventory of privileged accounts (admins/roles) and their MFA status. Implement a recurring privileged access review process with documented evidence (review dates, approvers, and remediation actions).

---




### Positive Observations

- No account takeovers detected in computed metrics (account_takeovers=0; users_with_takeover=0), suggesting no confirmed credential compromise events within the analyzed window.

- No 'attack_ip_attempts' or 'attack_ip_distinct_ips' were detected by the computation logic (both 0), indicating the detection pipeline did not flag explicit attack-IP patterns beyond general authentication failures.




### Trend Analysis


**Degrading:** Authentication failure rate increased from 0.5469 (2020-05-05) to 0.5548 (2020-08-03 window), an increase of ~0.79 percentage points.


**Stable:** MFA coverage remained at 0.0% across all provided baselines (2019-11-07, 2020-02-05, 2020-05-05, and current window)., No account takeovers detected (0) across provided baselines.





## Compliance Observations
### Access-Control Compliance (Cybersecurity Risk-Management)

- The entity shall implement access control policies and asset management as part of cybersecurity risk-management measures. [NIS2 Art. 21(2)(i)]

- Multi-factor authentication or continuous authentication solutions shall be used, where appropriate, to strengthen access control. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1529697). [METRICS: mfa.coverage_pct, mfa.enabled_users, mfa.total_users]

- No administrator accounts are recorded (admins.count: 0) and no administrators have MFA (admins.with_mfa: 0). [METRICS: admins.count, admins.with_mfa]

- Authentication failures total 3,623,191 with success_total 2,908,013 (fail_rate: 0.5548). [METRICS: auth_failures.total, auth_failures.success_total, auth_failures.fail_rate]

- Top source IPs for authentication failures include 23.137.225.33 (128728) and 10.0.181.232 (23631). [METRICS: auth_failures.top_ips]

- If the entity does not comply with required measures, it shall take necessary, appropriate, and proportionate corrective measures without undue delay. [NIS2 Art. 21(4)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures