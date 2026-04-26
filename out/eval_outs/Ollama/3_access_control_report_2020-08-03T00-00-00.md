# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-08-03T00:00:00 (window=90d)

**Risk Level:** HIGH


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


The security posture of our organization has shown significant degradation in authentication failures, with an increase in failed attempts from 0.5469 to 0.5548. Additionally, Multi-Factor Authentication (MFA) remains disabled for all users.


### Security Findings


#### HIGH: Multi-Factor Authentication (MFA) not enabled for any user

Despite the importance of MFA in securing user accounts, it remains disabled for all users. This increases the risk of unauthorized access to sensitive data and systems.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: 0

- deviation: 0% (no change from baseline)




**Compliance Impact:**

- **NIS2** (Article 13.1(b)): MFA is a requirement for all users accessing sensitive data and systems



**Recommendation:** Enable MFA for all users, with the exception of those who have valid business reasons for exemption

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


#### MEDIUM: Increased authentication failures from suspicious IP addresses

We observed a significant increase in failed login attempts originating from suspicious IP addresses, including 23.137.225.33 with 128728 attempts and 10.0.181.232 with 23631 attempts.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: [{'ip': '23.137.225.33', 'count': 128728}, {'ip': '10.0.181.232', 'count': 23631}]

- baseline_value: [{'ip': '158.149.114.95', 'count': 21443}, {'ip': '10.0.181.232', 'count': 14249}]

- deviation: 498% increase in failed attempts from suspicious IP addresses




**Compliance Impact:**

- **NIS2** (Article 17.3(a)): Regular monitoring and analysis of authentication failures is required



**Recommendation:** Implement additional security measures to detect and prevent malicious login attempts, such as IP blocking or rate limiting

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

- Authentication failure rates remain relatively stable compared to historical baselines




### Trend Analysis

**Improving:** distinct_src_ips


**Degrading:** mfa.coverage_pct, auth_failures.fail_rate


**Stable:** frame.rows





## Compliance Observations
Here is a concise access-control compliance section based on the METRICS JSON and LEGAL TEXTS:

**Access Control Compliance**

The organization does not implement multi-factor authentication or continuous authentication solutions, as required by [NIS2-21.2.j]. This results in a coverage rate of 0% (mfa.coverage_pct).

No data is available to assess the effectiveness of human resources security, access control policies, and asset management ([NIS2-21.2.i]).

The organization has no administrators with MFA enabled (admins.with_mfa).

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures