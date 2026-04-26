# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-05-05T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **6399979**
- Distinct users: **1510016**
- Distinct source IPs: **1251718**

### Authentication
- Successful logins: **2899642**
- Failed logins: **3500337**
- Failure rate: **0.5469**
- Top failing IPs:  

  
  - 23.137.225.33 (63681)
  
  - 158.149.114.95 (21443)
  
  - 10.0.181.232 (14249)
  
  - 10.0.181.221 (14188)
  
  - 10.0.181.231 (11737)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


Across the 90-day window ending 2020-05-05, the organization shows a severe NIS2 compliance gap in multi-factor authentication (MFA): 0% of 1,510,016 users have MFA enabled, including 0/0 admins with MFA (and no evidence of admin MFA coverage). Authentication activity also shows a persistently high failure rate (54.69%) with 3,500,337 total auth failures, and the top offending source IPs are dominated by a small set of internal/private and one public IP. While no account takeovers or explicit attack-IP attempts were detected (0), the combination of zero MFA coverage and high auth failure volume represents a critical risk to availability and integrity and indicates likely brute-force/credential-stuffing attempts or misconfiguration. Immediate remediation is required to meet NIS2 expectations for risk-based access control and authentication controls.


### Security Findings


#### CRITICAL: Zero MFA coverage for all users (0% enabled)

MFA is not enabled for any user accounts. This is a direct control failure for NIS2-aligned access control and authentication hardening, significantly increasing the likelihood and impact of credential compromise. The metric indicates 1,510,016 total users with 0 enabled for MFA, resulting in 0.0% coverage.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement vs baseline; remains at 0.0% across periods (e.g., 2020-02-05: 0.0%).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate measures for network and information system security, including access control and authentication strengthening, increases risk of unauthorized access.



**Recommendation:** Implement MFA for all users using a phased rollout with enforced enrollment (no exceptions without documented risk acceptance). Prioritize privileged accounts first, then high-risk user groups. Add monitoring for MFA enrollment failures and require MFA for all interactive logins. Provide an auditable policy and evidence of enforcement (e.g., configuration exports and enrollment reports).

---


#### CRITICAL: High authentication failure rate (~54.69%) indicating likely credential attacks or misconfiguration

Authentication failures are extremely high: 3,500,337 total failures with 2,899,642 successes, producing a fail rate of 54.69%. This level of failure is consistent with brute-force/credential-stuffing patterns or systemic authentication issues. Even though explicit 'attack_ip_attempts' and 'account_takeovers' are reported as 0, the failure volume combined with zero MFA coverage materially increases compromise likelihood and operational risk.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5469 (54.69%)

- baseline_value: 0.5408 (54.08%)

- deviation: +0.61 percentage points vs 2020-02-05




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inadequate authentication resilience and insufficient detection/response to repeated authentication failures undermines access security and increases risk of incidents.



**Recommendation:** Triage the top source IPs and failure patterns: (1) correlate failures with user accounts, geolocation, and login endpoints; (2) check for rate limiting, lockout policies, and CAPTCHA/step-up authentication; (3) enable alerting for abnormal failure spikes per IP/user; (4) validate that authentication logs are complete and that 'account takeover' detection is correctly configured. Implement rate limiting and progressive throttling for repeated failures, and require MFA/step-up for high-risk attempts.

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 54.7%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 54.7%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: Concentration of auth failures in a small set of source IPs

Auth failures are concentrated in a few IP addresses, suggesting targeted activity rather than uniform background noise. The top IP 23.137.225.33 has 63,681 failures, and multiple 10.0.181.x internal/private IPs appear among the top sources (e.g., 10.0.181.232: 14,249; 10.0.181.221: 14,188; 10.0.181.231: 11,737). This concentration warrants investigation for compromised internal hosts, misconfigured services, or automated retry loops.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IPs: 23.137.225.33 (63,681), 158.149.114.95 (21,443), 10.0.181.232 (14,249), 10.0.181.221 (14,188), 10.0.181.231 (11,737)

- baseline_value: 2020-02-05 top IPs included 158.149.114.95 (12,584) and 10.0.181.227 (10,967)

- deviation: Different top IP ordering vs baseline; continued presence of 158.149.114.95 and 10.0.181.* ranges indicates persistent sources.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent suspicious authentication sources indicate insufficient monitoring and control of access attempts, increasing likelihood of security incidents.



**Recommendation:** Perform incident-style triage on the top source IPs: identify owning systems for 10.0.181.* addresses, verify whether they are legitimate NAT/proxies, and check for credential stuffing/retry behavior. Block or throttle clearly malicious sources where appropriate, and ensure internal systems are hardened (patching, credential hygiene, and MFA where applicable). Document actions taken for auditability.

---


#### HIGH: No admin population recorded and no evidence of privileged MFA review

The metrics report admins.count = 0 and admins.with_mfa = 0 with last_review_date = 'unknown'. This is a governance and auditability concern: either privileged accounts are not being tracked in the dataset, or privileged MFA enforcement/review is not implemented or not measurable. For NIS2, demonstrating control coverage for privileged access is essential.


**Evidence:**

- metric: admins.count / admins.last_review_date

- current_value: admins.count=0; with_mfa=0; last_review_date='unknown'

- baseline_value: Same as baseline (2020-02-05): admins.count=0; with_mfa=0; last_review_date='unknown'

- deviation: No improvement; control evidence is missing.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of auditable privileged access control evidence undermines the ability to demonstrate appropriate security measures.



**Recommendation:** Fix privileged account inventory and reporting: ensure all admin/privileged roles are correctly classified in telemetry. Establish a recurring review cadence for privileged access and MFA status, and populate last_review_date with actual review timestamps. Produce evidence artifacts (role membership exports, MFA enforcement reports).

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/1510016 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---




### Positive Observations

- No detected account takeovers in the dataset (account_takeovers=0; users_with_takeover=0), suggesting either strong prevention/detection or that compromise has not been observed during this window.

- No explicit 'attack_ip_attempts' or 'attack_ip_distinct_ips' were flagged (both 0), which may indicate the detection logic is conservative or that attacks are not being categorized as such—still, it should be validated given the high failure rate.




### Trend Analysis


**Degrading:** Authentication failure rate slightly increased vs baseline: 54.08% (2020-02-05) to 54.69% (2020-05-05), a +0.61 percentage point change.


**Stable:** MFA coverage remains unchanged at 0.0% (enabled_users=0) across periods (2020-02-05 and current)., No account takeovers detected (account_takeovers=0) across compared periods.





## Compliance Observations
### Access-Control Compliance (Cybersecurity Risk-Management)

- The entity shall implement access control policies as part of cybersecurity risk-management measures. [NIS2 Art. 21(2)(i)]  
- Multi-factor authentication (or continuous authentication) solutions shall be used where appropriate. [NIS2 Art. 21(2)(j)]  
- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1510016). [METRICS mfa]  
- Administrators count is 0; administrators with MFA is 0. [METRICS admins]  
- Authentication failures total 3,500,337 with success_total 2,899,642 (fail_rate 0.5469). [METRICS auth_failures]  
- Top source IPs with failures include 23.137.225.33 (63,681) and 158.149.114.95 (21,443). [METRICS auth_failures.top_ips]  
- No data available in the provided evidence for access-control policy effectiveness assessments. [NIS2 Art. 21(2)(f)]  
- No data available in the provided evidence for corrective measures taken for non-compliance. [NIS2 Art. 21(4)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures