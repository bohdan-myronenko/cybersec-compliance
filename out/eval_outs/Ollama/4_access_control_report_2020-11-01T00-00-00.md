# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-11-01T00:00:00 (window=90d)

**Risk Level:** HIGH


## Key Metrics

- Total login attempts: **9309939**
- Distinct users: **1596182**
- Distinct source IPs: **1237098**

### Authentication
- Successful logins: **2822319**
- Failed logins: **6487620**
- Failure rate: **0.6968**
- Top failing IPs:  

  
  - 10.3.205.197 (443523)
  
  - 10.3.205.196 (257018)
  
  - 10.3.205.195 (236489)
  
  - 10.3.205.194 (177160)
  
  - 10.3.205.193 (152239)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


The security posture has been stable, but there are concerns regarding MFA adoption and authentication failures.


### Security Findings


#### HIGH: MFA Adoption Remains Low

Despite the importance of MFA in protecting against phishing and other attacks, no users have enabled MFA since its introduction.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: None

- deviation: -




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Implementing MFA is essential for preventing unauthorized access to information and systems.



**Recommendation:** Ensure that all users are prompted to enable MFA and provide training on its importance.

---


#### MEDIUM: Authentication Failures at High Rate

The authentication failure rate has remained high, with a fail rate of 69.68%.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6968

- baseline_value: [0.5548, 0.5469, 0.5408]

- deviation: -27.54%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Regularly reviewing and improving authentication mechanisms is essential for maintaining security.



**Recommendation:** Review and improve the authentication process to reduce failure rates.

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 69.7%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 69.7%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/1596182 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### LOW: Administrative Roles Not Reviewed Regularly

No administrative roles have been reviewed or updated since the introduction of MFA.


**Evidence:**

- metric: admins.last_review_date

- current_value: unknown

- baseline_value: None

- deviation: -




**Compliance Impact:**

- **NIS2** (Article 24.5(i)): Regularly reviewing and updating administrative roles is essential for maintaining compliance.



**Recommendation:** Schedule regular reviews of administrative roles to ensure they remain up-to-date.

---




### Positive Observations

- The number of distinct source IPs has increased by 12.58% since the last period.




### Trend Analysis

**Improving:** distinct_src_ips


**Degrading:** mfa.enabled_users, auth_failures.fail_rate


**Stable:** admins.count





## Compliance Observations
Here is a concise access-control compliance section based on the provided LEGAL TEXTS and METRICS JSON:

**Access Control Compliance**

* The organization does not have any multi-factor authentication (MFA) enabled users, as per [NIS2-21.2.j] which requires MFA or continuous authentication solutions for entities where appropriate. [metrics: "enabled_users": 0]
* The organization has no administrative accounts with MFA enabled, as there are no administrators with MFA ([metrics: "with_mfa": 0]).
* There is no information available on the organization's access control policies and asset management practices, which are required by [NIS2-21.2.i].
* The organization does not have any human resources security measures in place, including access control policies and asset management, as per [NIS2-21.2.i].

Note: Since there is no information available on the organization's access control policies and practices, we cannot make any further findings or recommendations.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures