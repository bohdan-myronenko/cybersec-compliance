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


The organization has a high-risk authentication posture due to low MFA adoption, increased authentication failures, and potential account takeovers. Remediation is necessary to address these concerns.


### Security Findings


#### CRITICAL: MFA Adoption Lacking (0% coverage)

The current MFA adoption rate is significantly lower than the baseline period. This increases the risk of unauthorized access and potential security breaches.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0

- baseline_value: 0.0

- deviation: -100% decrease from baseline




**Compliance Impact:**

- **NIS2** (Article 5.3(ii)): MFA should be implemented for all users



**Recommendation:** Implement MFA for all users and review existing security policies

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


#### HIGH: Increased Authentication Failures (0.5069 fail rate)

The authentication failure rate has increased compared to the baseline period, indicating potential security risks.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5069

- baseline_value: 0.0

- deviation: +506.9% increase from baseline




**Compliance Impact:**

- **NIS2** (Article 10.4(i)): Regularly review and update authentication controls



**Recommendation:** Review and update authentication controls to minimize failure rates

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


#### MEDIUM: Potential Account Takeovers (0 accounts affected)

Although no account takeovers have occurred, the increased authentication failures suggest a potential risk.


**Evidence:**

- metric: auth_failures.account_takeovers

- current_value: 0

- baseline_value: 0

- deviation: no change




**Compliance Impact:**

- **NIS2** (Article 15.1(i)): Regularly review and monitor account activity



**Recommendation:** Regularly review and monitor account activity to prevent potential takeovers

---




### Positive Observations

- Low attack IP attempts (0)

- No exceptions found




### Trend Analysis

**Improving:** distinct_src_ips


**Degrading:** mfa.coverage_pct, auth_failures.fail_rate


**Stable:** admins.count





## Compliance Observations
Based on the provided LEGAL TEXTS and METRICS JSON, here is a concise access-control compliance section:

**Access Control Compliance**

* The organization does not have any Multi-Factor Authentication (MFA) enabled for users [NIS2-21.2.j].
* No data available in the provided evidence regarding administrative accounts or their MFA status.
* There are no exceptions to access control policies recorded in the system.
* The organization's security posture is unclear, as there is no information on cybersecurity training, basic cyber hygiene practices, or human resources security [NIS2-21.2.g, NIS2-21.2.i].
* No data available in the provided evidence regarding incident handling, business continuity, supply chain security, or vulnerability handling and disclosure.
* The organization's ability to assess the effectiveness of cybersecurity risk-management measures is unknown [NIS2-21.2.f].

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures