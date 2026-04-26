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


The security posture remains concerning due to a lack of MFA enforcement, high auth failure rates, and unreviewed admin accounts.


### Security Findings


#### CRITICAL: MFA Enforcement Lacking

There are no users with MFA enabled, despite a total of 1,510,016 users.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: None

- deviation: 100% decrease from baseline




**Compliance Impact:**

- **NIS2** (Article 7.1): Lack of MFA enforcement violates NIS2 requirements



**Recommendation:** Implement MFA for all users, following the guidelines in NIS2 Article 7.

---


#### HIGH: High Auth Failure Rates

The auth failure rate is 54.69%, with a total of 3,500,337 failures.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5469

- baseline_value: 0.5408

- deviation: 1% increase from baseline




**Compliance Impact:**

- **NIS2** (Article 16.3): High auth failure rates may indicate a security breach



**Recommendation:** Implement additional authentication mechanisms to reduce auth failures.

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


#### MEDIUM: Unreviewed Admin Accounts

There are no admin accounts with MFA enabled, and the last review date is unknown.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: None

- deviation: 100% decrease from baseline




**Compliance Impact:**

- **NIS2** (Article 14.1): Unreviewed admin accounts violate NIS2 requirements



**Recommendation:** Review and update admin accounts, ensuring MFA enforcement and timely reviews.

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

- The number of distinct source IPs has increased by 7.4% compared to the previous period.




### Trend Analysis

**Improving:** distinct_src_ips


**Degrading:** mfa.enabled_users, auth_failures.fail_rate


**Stable:** admins.count





## Compliance Observations
Here is the compliance section:

**Access Control Compliance**

• The organization does not enable Multi-Factor Authentication (MFA) for its users, as per METRICS JSON: {"mfa": {"enabled_users": 0}} [NIS2-21.2.j]

• There are no administrators with enabled MFA on record, as per METRICS JSON: {"admins": {"with_mfa": 0}} [NIS2-21.2.i]

• The organization has not reviewed its administrative accounts' access control policies in the last known review date, which is 'unknown', as per METRICS JSON: {"admins": {"last_review_date": "unknown"}} [NIS2-21.2.i]

Note: Since no data is available regarding the organization's risk assessment, incident handling procedures, or business continuity planning related to access control, these areas are not addressed in this report.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures