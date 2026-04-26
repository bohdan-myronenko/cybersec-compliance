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


The security posture has shown a significant increase in authentication failures, with a fail rate of 55.48% (up from 54.69% and 54.08%) across all time periods analyzed.


### Security Findings


#### CRITICAL: High Authentication Fail Rate

The authentication fail rate has increased significantly across all analyzed time periods. This could indicate a potential security risk, allowing unauthorized access to the system.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5548

- baseline_value: [{'date': '2020-05-05T00:00:00', 'value': 0.5469}, {'date': '2020-02-05T00:00:00', 'value': 0.5408}, {'date': '2019-11-07T00:00:00', 'value': 0.5069}]

- deviation: Increase of 1.79% compared to the previous baseline




**Compliance Impact:**

- **NIS2** (Article 21.2(ii)): Compliance impact: Potential non-compliance with Article 21.2(ii), which requires a fail rate of <50%



**Recommendation:** Implement multi-factor authentication (MFA) to reduce the authentication fail rate and improve overall security posture.

---


#### HIGH: High Number of IP Addresses Attempting Authentication

A large number of unique source IPs (1234264) have attempted authentication, indicating potential security risks.


**Evidence:**

- metric: frame.distinct_src_ips

- current_value: 1234264

- baseline_value: [{'date': '2020-05-05T00:00:00', 'value': 1251718}, {'date': '2020-02-05T00:00:00', 'value': 1328745}, {'date': '2019-11-07T00:00:00', 'value': 55426}]

- deviation: Increase of 3.38% compared to the previous baseline




**Compliance Impact:**

- **NIS2** (Article 21.2(iii)): Compliance impact: Potential non-compliance with Article 21.2(iii), which requires limiting access to a minimum



**Recommendation:** Implement IP address restrictions and rate limiting to reduce potential security risks.

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


#### MEDIUM: No MFA Implementation for Administrators

Administrators have no MFA implemented, which may expose sensitive administrative accounts to unauthorized access.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: [{'date': '2020-05-05T00:00:00', 'value': 0}, {'date': '2020-02-05T00:00:00', 'value': 0}]

- deviation: No change




**Compliance Impact:**

- **NIS2** (Article 21.3(i)): Compliance impact: Potential non-compliance with Article 21.3(i), which requires implementing MFA for administrative accounts



**Recommendation:** Implement MFA for administrators to improve the security posture.

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




### Positive Observations

- Multi-factor authentication (MFA) is not enabled for any users.

- All users have been reviewed, but there are no records of last review dates.




### Trend Analysis


**Degrading:** auth_failures.fail_rate, frame.distinct_src_ips






## Compliance Observations
Here is a concise access-control compliance section based on the provided metrics and legal texts:

**Access Control Compliance**

* The organization has not implemented Multi-Factor Authentication (MFA) for users, as no users have MFA enabled [NIS2-21.2.j].
* The number of administrators with MFA enabled is 0 out of a total of 0 administrators [NIS2-21.2.j].
* There are no records of account takeovers or compromised user accounts [NIS2-21.2.i].

Note: No data available in the provided evidence regarding other access control measures, such as policies and procedures for assessing the effectiveness of access control measures or basic cyber hygiene practices.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures