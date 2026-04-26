# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-02-05T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **6552134**
- Distinct users: **1536866**
- Distinct source IPs: **1328745**

### Authentication
- Successful logins: **3008918**
- Failed logins: **3543216**
- Failure rate: **0.5408**
- Top failing IPs:  

  
  - 158.149.114.95 (12584)
  
  - 10.0.181.227 (10967)
  
  - 10.0.181.226 (10254)
  
  - 10.0.181.221 (7558)
  
  - 10.0.181.200 (7256)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


Across the 90-day window (ending 2020-02-05), the environment shows a severe NIS2-relevant authentication control gap: MFA is effectively not deployed (0% coverage for 1,536,866 users) and there are very high authentication failure rates (fail rate 54.08% with 3,543,216 total auth attempts). While no account takeovers or “attack IP attempts” are detected (0 in both categories), the combination of zero MFA coverage and elevated failure volume represents a critical compliance and security risk under NIS2, especially for protecting network and information systems against unauthorized access.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any user accounts. With 1,536,866 total users and 0 enabled for MFA, the organization lacks a key compensating control for preventing unauthorized access and credential misuse. This is a direct and material control deficiency for NIS2 expectations around access control and protection against unauthorized access.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0% (enabled_users=0 / total_users=1,536,866)

- baseline_value: 0.0% (2019-11-07: enabled_users=0 / total_users=50,215; 2021-01-30: enabled_users=0 / total_users=635,091)

- deviation: No improvement across observed periods; remains at 0% coverage.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate access control measures (e.g., strong authentication such as MFA) increases the likelihood of unauthorized access to network and information systems.



**Recommendation:** Implement MFA for all users, starting with privileged/admin and high-risk populations. Enforce MFA at authentication policy level (not just optional enrollment), require re-authentication for existing sessions, and set a measurable rollout target (e.g., 100% within 30–60 days). Validate via periodic reporting that enabled_users/total_users reaches 100% and that exceptions are explicitly approved and time-bound.

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 54.1%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 54.1%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: High authentication failure rate indicates persistent access attempts or misconfiguration

Authentication failures are extremely high relative to successes. Total auth failures are 3,543,216 with a fail rate of 54.08% (success_total=3,008,918). This pattern can indicate credential stuffing/brute-force attempts, incorrect client configuration, or widespread user authentication issues. Even though account takeover detection is 0, the volume and rate of failures materially increase risk and operational exposure.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5408 (54.08%)

- baseline_value: 2019-11-07: 0.5069 (50.69%); 2021-01-30: 0.6421 (64.21%)

- deviation: Current fail rate is higher than 2019-11-07 by ~3.39 percentage points; lower than 2021-01-30 by ~10.41 percentage points (still high overall).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Elevated authentication failure rates suggest increased likelihood of unauthorized access attempts and insufficient resilience of authentication controls.



**Recommendation:** Perform an authentication failure root-cause analysis: (1) correlate failures with identity provider logs, user agents, and geo/IP reputation; (2) check for misconfigured authentication flows (e.g., wrong realm/tenant, expired passwords, broken SSO); (3) enable/verify rate limiting, lockout/backoff, and bot detection; (4) ensure MFA is enforced to reduce successful compromise likelihood. Produce a weekly report of top failure sources and top affected accounts.

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/1536866 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### HIGH: Top source IPs show concentrated repeated authentication failures

Authentication failures are concentrated among a small set of source IPs. The top IP (158.149.114.95) has 12,584 failures, and multiple internal/private IPs (10.0.181.227, 10.0.181.226, 10.0.181.221, 10.0.181.200) each have thousands of failures. This concentration suggests either automated activity (e.g., scripted attempts) or systemic issues from specific network segments/services.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IPs: 158.149.114.95 (12,584), 10.0.181.227 (10,967), 10.0.181.226 (10,254), 10.0.181.221 (7,558), 10.0.181.200 (7,256)

- baseline_value: 2019-11-07 top IP counts were much lower (e.g., 10.0.181.226: 187; 10.0.181.227: 183)

- deviation: Orders-of-magnitude increase in top-IP failure counts versus 2019-11-07, indicating a significant change in failure dynamics.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Concentrated repeated authentication failures indicate potential unauthorized access attempts or weaknesses in access control monitoring and response.



**Recommendation:** Investigate each top IP: determine whether they belong to known services, NAT gateways, proxies, or automation. If not expected, block or challenge at the edge (WAF/IdP) and add IP reputation/rate-limit rules. If expected (e.g., internal services), remediate the service authentication configuration and rotate credentials/secrets. Ensure alerts are triggered on abnormal failure concentration per IP/subnet.

---


#### MEDIUM: No admins recorded; MFA and review status unavailable/unknown

The metrics report admins.count=0 and admins.with_mfa=0 with last_review_date='unknown'. This is likely a data quality or instrumentation gap rather than a true absence of administrators. For NIS2 compliance, privileged access must be explicitly identified, reviewed, and protected with strong authentication.


**Evidence:**

- metric: admins

- current_value: count=0, with_mfa=0, last_review_date='unknown'

- baseline_value: 2019-11-07: count=0, with_mfa=0, last_review_date='unknown'

- deviation: No change; persistent lack of privileged access visibility.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inability to demonstrate privileged access governance and strong authentication coverage undermines compliance evidence for access control measures.



**Recommendation:** Fix identity/role mapping so privileged accounts are correctly classified as admins. Establish a privileged access inventory, record last review dates, and require MFA for all privileged roles. Add a compliance control report that fails if admin inventory is empty or review dates are missing.

---




### Positive Observations

- No detected account takeovers (account_takeovers=0; users_with_takeover=0) during the analyzed period.

- No detected 'attack_ip_attempts' or 'attack_ip_distinct_ips' (both 0), suggesting either effective detection logic or that failures are not being classified as successful attack patterns.




### Trend Analysis

**Improving:** Authentication fail rate is lower than 2021-01-30 (current 54.08% vs baseline 64.21%), indicating some reduction in failure intensity compared to that period.


**Degrading:** Authentication failure concentration increased substantially versus 2019-11-07 (top IP failure counts grew from ~187–183 range to thousands+).


**Stable:** MFA coverage remains at 0.0% across all observed periods (2019-11-07, 2021-01-30, and current), indicating persistent lack of deployment.





## Compliance Observations
### Access-Control Compliance (Article 21)

- The entity shall implement human resources security, access control policies, and asset management to manage risks to network and information systems. [NIS2 Art. 21(2)(i)]

- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate, to strengthen access control. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1536866), indicating non-implementation of MFA/continuous authentication. [METRICS mfa]

- No admin accounts are recorded (admins.count: 0; admins.with_mfa: 0), preventing verification of access-control enforcement for privileged users. [METRICS admins]

- Authentication failures total 3,543,216 with success_total 3,008,918 (fail_rate 0.5408), requiring access-control measures to manage incident risk. [METRICS auth_failures; NIS2 Art. 21(1)]

- The evidence shows auth_failures.attack_ip_attempts: 0 and attack_ip_distinct_ips: 0; no attack-IP-based access-control conclusions can be drawn. [METRICS auth_failures]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures