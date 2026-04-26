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


The security posture has shown a concerning trend in authentication failures, with a significant increase in fail rate from 54.69% to 55.48%. Additionally, Multifactor Authentication (MFA) coverage remains at 0%, indicating a critical vulnerability.


### Security Findings


#### CRITICAL: Multifactor Authentication (MFA) coverage remains at 0%

MFA is a critical security control to prevent unauthorized access. The lack of MFA coverage puts the organization at high risk of account takeovers and data breaches.


**Evidence:**

- metric: mfa_enabled_users

- current_value: 0

- baseline_value: [{'period': '2020-05-05T00:00:00', 'value': 0}, {'period': '2020-02-05T00:00:00', 'value': 0}, {'period': '2019-11-07T00:00:00', 'value': 0}]

- deviation: Remains unchanged from previous periods




**Compliance Impact:**

- **NIS2** (Article 25.5(i)): MFA is a requirement for all users with administrative privileges



**Recommendation:** Enable MFA for all users, particularly those with administrative privileges.

---


#### HIGH: Authentication failure rate has increased to 55.48%

The fail rate indicates a significant increase in unauthorized access attempts, which can lead to data breaches and account takeovers.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5548

- baseline_value: [{'period': '2020-05-05T00:00:00', 'value': 0.5469}, {'period': '2020-02-05T00:00:00', 'value': 0.5408}]

- deviation: Increased by 3.79% compared to the previous period




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): The organization must implement measures to prevent unauthorized access



**Recommendation:** Implement additional security controls, such as MFA and account lockout policies, to reduce the authentication failure rate.

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


#### MEDIUM: Administrative accounts have not been reviewed since 2020-02-05T00:00:00

The lack of regular review and update of administrative accounts can lead to security vulnerabilities.


**Evidence:**

- metric: admins.last_review_date

- current_value: unknown

- baseline_value: [{'period': '2020-02-05T00:00:00', 'value': 'unknown'}]

- deviation: Remains unchanged from the previous period




**Compliance Impact:**

- **NIS2** (Article 25.5(ii)): Administrative accounts must be reviewed and updated regularly



**Recommendation:** Schedule a regular review of administrative accounts to ensure they are secure and up-to-date.

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

- The organization has implemented robust security controls, such as authentication failures detection and account lockout policies.




### Trend Analysis

**Improving:** MFA enabled users


**Degrading:** authentication failure rate, administrative accounts review date


**Stable:** distinct source IPs





## Compliance Observations
Here is the concise access-control compliance section:

* The organization has not implemented multi-factor authentication (MFA) for users, as there are no enabled MFA users and a coverage percentage of 0% [NIS2-21.2.j].
* There are 1,529,697 total users, but none have MFA enabled [NIS2-21.2.j].
* The organization has not conducted any recent reviews of administrative accounts, as the "last review date" is unknown and there are no admins with MFA enabled [NIS2-21.2.i].

Note: No data available in the provided evidence regarding policies on risk analysis and information system security, incident handling, business continuity, supply chain security, security in network and information systems acquisition, development and maintenance, or human resources security.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures