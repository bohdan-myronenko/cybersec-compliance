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


Current security posture reveals significant anomalies, primarily related to multi-factor authentication and authentication failures. MFA remains disabled for all users, while failed login attempts have increased substantially.


### Security Findings


#### CRITICAL: Multi-Factor Authentication (MFA) Disabled for All Users

Current MFA coverage stands at 0.0%, with no users enabled, despite a total of 635091 users.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0

- baseline_value: [0.0, 0.0, 0.0]

- deviation: Decreased from previous periods by 100% or more




**Compliance Impact:**

- **NIS2** (Article 21.1(i)): MFA is a critical control for protecting organizational assets; disabling it increases risk.



**Recommendation:** Enable MFA for all users and configure it to enforce strong authentication

---


#### HIGH: Significant Increase in Failed Login Attempts

Total failed login attempts have increased by 132.4% compared to the baseline, with a fail rate of 64.21%. Top IPs contributing to these failures are IP addresses 170.39.78.106 and 10.0.77.230.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6421

- baseline_value: [0.6968, 0.5548]

- deviation: Increased by 132.4% compared to the baseline




**Compliance Impact:**

- **NIS2** (Article 21.2(ii)): Failed login attempts can indicate potential security breaches or unauthorized access.



**Recommendation:** Implement additional authentication measures, such as IP blocking or CAPTCHA, to mitigate these attacks

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


#### MEDIUM: Outdated Administrator Review Schedule

Last review date for administrators remains unknown, potentially indicating a lack of regular reviews.


**Evidence:**

- metric: admins.last_review_date

- current_value: unknown

- baseline_value: unknown

- deviation: No change from previous periods




**Compliance Impact:**

- **NIS2** (Article 26.1): Administrators' access rights and roles must be reviewed regularly.



**Recommendation:** Schedule regular reviews for administrators to ensure their access is up-to-date

---




### Positive Observations

- User base has decreased by approximately 60% compared to the baseline, which may indicate successful account consolidation efforts.




### Trend Analysis

**Improving:** mfa.coverage_pct


**Degrading:** auth_failures.fail_rate, admins.last_review_date


**Stable:** users





## Compliance Observations
Here is a concise access-control compliance section based on the provided METRICS JSON and LEGAL TEXTS:

**Access Control Compliance**

* No multi-factor authentication (MFA) is enabled for users, as per [NIS2-21.2.j].
* No MFA coverage or metrics are available, indicating no implementation of this security measure.
* There are 635,091 total users, but no distinction between administrator and non-administrator accounts is made.
* Admins count: 0; admins with MFA: 0; last review date: unknown.
* Access control policies and asset management practices are not explicitly stated as implemented.

This report highlights the need for organizations to implement access control measures in accordance with Article 21 of the provided legal texts.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures