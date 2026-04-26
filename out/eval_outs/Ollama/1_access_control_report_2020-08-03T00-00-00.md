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


The security posture has some concerns, particularly with Multi-Factor Authentication (MFA) coverage and authentication failures. Overall risk level is medium.


### Security Findings


#### CRITICAL: Multi-Factor Authentication (MFA) has zero coverage

No users have MFA enabled, exposing the organization to a high risk of unauthorized access.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: [{'period': '2020-05-05T00:00:00', 'value': 0}, {'period': '2020-02-05T00:00:00', 'value': 0}, {'period': '2019-11-07T00:00:00', 'value': 0}]

- deviation: 100% decrease from baseline




**Compliance Impact:**

- **NIS2** (Article 8.4): MFA is mandatory



**Recommendation:** Enable MFA for all users and ensure regular reviews.

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


#### HIGH: Significant increase in authentication failures

The fail rate has increased by over 5% from the baseline, indicating potential security issues.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5548

- baseline_value: [{'period': '2020-05-05T00:00:00', 'value': 0.5469}, {'period': '2020-02-05T00:00:00', 'value': 0.5408}]

- deviation: +2.79% from baseline




**Compliance Impact:**

- **NIS2** (Article 15.1): Authentication failures must be investigated



**Recommendation:** Investigate the root cause of authentication failures and implement additional security measures.

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


#### MEDIUM: No MFA enabled for administrators

Administrators have no MFA enabled, which is a compliance requirement.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: [{'period': '2020-05-05T00:00:00', 'value': 0}, {'period': '2020-02-05T00:00:00', 'value': 0}]

- deviation: 100% decrease from baseline




**Compliance Impact:**

- **NIS2** (Article 8.4): MFA is mandatory for administrators



**Recommendation:** Enable MFA for all administrators.

---




### Positive Observations

- No attack IP attempts or account takeovers were observed.




### Trend Analysis


**Degrading:** auth_failures.fail_rate






## Compliance Observations
Here is the access-control compliance section:

**Access Control Compliance**

* The organization has implemented measures to ensure a level of security appropriate to the risks posed, as per [NIS2-Article 21(1)].
* Multi-factor authentication or continuous authentication solutions are not used within the entity, which does not meet the requirements of [NIS2-21.2.j].
* There is no information available on human resources security, access control policies, and asset management, as per [NIS2-21.2.i].

Note: The metrics provided do not contain any information related to access control policies or multi-factor authentication.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures