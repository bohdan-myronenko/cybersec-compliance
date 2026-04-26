# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-11-01T00:00:00 (window=90d)

**Risk Level:** CRITICAL


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


The security posture of the system has significant anomalies and compliance concerns. Authentication failures are high, and MFA is not enabled for any users.


### Security Findings


#### CRITICAL: MFA is not enabled for any users

No users have Multi-Factor Authentication (MFA) enabled, which is a significant security risk. MFA coverage percentage is 0.0%.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: None

- deviation: No change from baseline




**Compliance Impact:**

- **NIS2** (Article 21.1(i)): Lack of MFA increases the risk of unauthorized access.



**Recommendation:** Enable MFA for all users as soon as possible.

---


#### HIGH: High authentication failure rate and IP addresses

The authentication failure rate is high at 69.68%, and there are several IP addresses with a large number of failed attempts.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6968

- baseline_value: None

- deviation: Significantly higher than baseline




**Compliance Impact:**

- **NIS2** (Article 21.3(i)): High authentication failure rate increases the risk of unauthorized access.



**Recommendation:** Review and investigate the cause of high authentication failures, and implement measures to reduce failed attempts.

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


#### MEDIUM: No MFA enabled for admins

MFA is not enabled for any admin users, which is a compliance concern.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: None

- deviation: No change from baseline




**Compliance Impact:**

- **NIS2** (Article 21.1(ii)): Lack of MFA for admins increases the risk of unauthorized access.



**Recommendation:** Enable MFA for all admin users as soon as possible.

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




### Positive Observations

- The system has a stable number of distinct source IP addresses.




### Trend Analysis


**Degrading:** auth_failures.fail_rate


**Stable:** admins.with_mfa





## Compliance Observations
**Access Control Compliance Section**

The organization has not implemented Multi-Factor Authentication (MFA) to protect its users, as per Article [NIS2-21.2.j], which recommends the use of MFA or continuous authentication solutions.

* Total Users: 1,596,182
* Enabled Users for MFA: 0

No data available in the provided evidence regarding the implementation of human resources security, access control policies, and asset management as per Article [NIS2-21.2.i].

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures