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


The organization's security posture has shown a significant increase in authentication failures, with a fail rate of 69.68% compared to previous periods.


### Security Findings


#### CRITICAL: High Authentication Failure Rate

The current authentication failure rate is significantly higher than previous periods, indicating a potential security vulnerability.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6968

- baseline_value: 0.5548

- deviation: 26% increase in fail rate




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High authentication failure rates can impact the effectiveness of access controls



**Recommendation:** Implement MFA for all users and review access control policies to prevent excessive login attempts.

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


#### HIGH: MFA Not Implemented for Admins

Despite a high fail rate, MFA is not enabled for admin users, leaving them vulnerable to account takeovers.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0

- deviation: no change




**Compliance Impact:**

- **NIS2** (Article 23.1(i)): Admin accounts must have MFA enabled



**Recommendation:** Enable MFA for admin users and review last review date to ensure it is up-to-date.

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


#### MEDIUM: Top IP Addresses with High Authentication Failures

The top IP addresses with high authentication failures are largely internal, indicating potential insider threats.


**Evidence:**

- metric: auth_failures.top_ips[0].count

- current_value: 443523

- baseline_value: None

- deviation: new IP address with high failure rate




**Compliance Impact:**

- **NIS2** (Article 22.1(i)): Internal threats can impact the effectiveness of access controls



**Recommendation:** Review logs to identify potential insider threats and implement additional security measures.

---




### Positive Observations

- The organization has a high number of distinct source IP addresses, indicating low risk for network-based attacks.




### Trend Analysis

**Improving:** distinct_users


**Degrading:** auth_failures.fail_rate, admins.with_mfa


**Stable:** frame.rows





## Compliance Observations
**Access-Control Compliance Section**

Based on the provided METRICS JSON and LEGAL TEXTS, the following access-control compliance findings are reported:

• The use of multi-factor authentication (MFA) is not enabled for any users [NIS2-21.2.j].
• No data available in the provided evidence regarding the implementation of continuous authentication solutions.
• No data available in the provided evidence regarding secured voice, video, and text communications.
• No data available in the provided evidence regarding secured emergency communication systems.

It is noted that essential and important entities are required to implement multi-factor authentication or continuous authentication solutions [NIS2-21.2.j].

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures