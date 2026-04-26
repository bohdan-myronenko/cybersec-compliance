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


The organization's security posture has shown a significant increase in authentication failures with a fail rate of 54.69% (up from 50.69% in 2019) and a high number of IP addresses attempting authentication failures.


### Security Findings


#### CRITICAL: High Authentication Failure Rate and Unsecured IPs Attempting Access

The current authentication failure rate has increased to 54.69%, indicating potential security breaches. Further, multiple IP addresses are attempting access with high frequency.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5469

- baseline_value: 0.5069 (2019-11-07)

- deviation: +8.4% increase in 90 days




**Compliance Impact:**

- **NIS2** (Article 5.1): Ensure secure authentication procedures are implemented to prevent unauthorized access



**Recommendation:** Implement Multi-Factor Authentication (MFA) for all users and monitor IP addresses attempting high-frequency login attempts.

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


#### HIGH: No MFA Implemented for Administrators

The organization has no Multi-Factor Authentication (MFA) implemented for administrators, making them vulnerable to account takeovers.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0 (unknown)

- deviation: N/A




**Compliance Impact:**

- **NIS2** (Article 17.1): Implement MFA for all administrators to prevent unauthorized access



**Recommendation:** Enable MFA for all administrator accounts.

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


#### MEDIUM: High Number of IP Addresses Attempting Access with High Frequency

Multiple IP addresses are attempting access with high frequency, potentially indicating malicious activity.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: [...]

- baseline_value: [...]

- deviation: +100-500% increase in 90 days




**Compliance Impact:**

- **NIS2** (Article 22.1): Implement IP blocking and access controls to prevent unauthorized access



**Recommendation:** Monitor and block suspicious IP addresses attempting high-frequency login attempts.

---




### Positive Observations

- MFA is enabled for all users (total_users: 1510016)




### Trend Analysis

**Improving:** distinct_src_ips, distinct_users


**Degrading:** auth_failures.fail_rate


**Stable:** admins.count





## Compliance Observations
**Access Control Compliance Section**

Based on the provided metrics and legal texts, the following access control compliance findings are noted:

* The organization has not implemented multi-factor authentication ([NIS2 Art. 21(2)(j)]), with only 0 users enabled for MFA out of a total of 1,510,016 users.
* No accounts have been taken over, and no users have takeover attributes ([NIS2 Art. 21(2)(i) not applicable as there are no account takeovers]).
* The organization has not conducted any coordinated security risk assessments of critical supply chains as per Article 22(1).

**Metrics:**

* Total Users: 1,510,016
* Enabled MFA Users: 0

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures