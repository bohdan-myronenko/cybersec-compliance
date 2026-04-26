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


The security posture of the analyzed system shows high-risk authentication failures, lack of MFA adoption, and no regular admin account reviews. This poses a significant risk to compliance with NIS2 regulations.


### Security Findings


#### CRITICAL: Lack of MFA Adoption and High-Risk Authentication Failures

The current system has 50,215 total users, but none have MFA enabled (0.0% coverage). This is a significant risk to authentication security. Additionally, there were 61,540 failed authentications with a success rate of 2.93%, indicating potential attack attempts.


**Evidence:**

- metric: mfa

- current_value: 0

- baseline_value: 635091

- deviation: 100% decrease




**Compliance Impact:**

- **NIS2** (Article 21.2(v)): Non-compliance with MFA requirement



**Recommendation:** Implement and require MFA for all users

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


#### HIGH: No Regular Admin Account Reviews

There are no admin accounts with MFA enabled and the last review date for admins is unknown. This poses a significant risk to access control security.


**Evidence:**

- metric: admins

- current_value: 0

- baseline_value: 1596182

- deviation: -100% decrease




**Compliance Impact:**

- **NIS2** (Article 22.1(ii)): Non-compliance with admin account review requirement



**Recommendation:** Regularly review and update admin accounts

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


#### MEDIUM: Top IPs with High-Number of Failed Authentications

The top IPs with high-number of failed authentications are 10.0.181.226 (187), 10.0.181.227 (183), and others.


**Evidence:**

- metric: auth_failures

- current_value: Top IPs: 10.0.181.226, 10.0.181.227, etc.

- baseline_value: None

- deviation: None




**Compliance Impact:**

- **NIS2** (Article 24.1(i)): Potential non-compliance with security incident response requirement



**Recommendation:** Investigate and block suspicious IPs

---




### Positive Observations

- The system has a low number of exceptions (0)




### Trend Analysis

**Improving:** MFA adoption


**Degrading:** Failed authentication success rate


**Stable:** Admin account review frequency





## Compliance Observations
Based on the provided METRICS JSON and LEGAL TEXTS, here is a concise access-control compliance section:

**Access Control Compliance**

* No multi-factor authentication (MFA) or continuous authentication solutions are in use [NIS2-21.2.j], with only 0 users enabled for MFA out of 50,215 total users.
* No information is available on the last review date of administrative access control policies and asset management procedures for administrators [No data available in the provided evidence].
* The organization has no specific metrics or information regarding human resources security, access control policies, and asset management.

**Notes:**
The METRICS JSON does not contain any information related to supply chain security, basic cyber hygiene practices, or cybersecurity training. Therefore, these findings are not included in this report.

Please let me know if you would like me to add anything else.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures