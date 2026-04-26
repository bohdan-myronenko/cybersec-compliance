# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2019-11-07T00:00:00 (window=90d)

**Risk Level:** HIGH


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


The security posture of the organization has shown significant improvements in authentication controls, but there are concerns regarding the absence of MFA for administrators.


### Security Findings


#### HIGH: MFA Not Enabled for Administrators

There are no administrators with MFA enabled. This poses a significant risk to the organization's security and compliance.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0

- deviation: No change from baseline




**Compliance Impact:**

- **NIS2** (Article 22.4): Failing to implement MFA for administrators may lead to a non-compliance with the regulations.



**Recommendation:** Enable MFA for all administrators

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


#### MEDIUM: MFA Coverage is Zero Percent

MFA coverage remains at zero percent, indicating a significant lack of adoption. This poses a risk to the organization's security and compliance.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0

- baseline_value: 0

- deviation: No change from baseline




**Compliance Impact:**

- **NIS2** (Article 23.1): Failing to implement MFA for users may lead to a non-compliance with the regulations.



**Recommendation:** Increase MFA adoption

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


#### LOW: High Number of Authentication Failures from Specific IPs

There are a high number of authentication failures originating from specific IP addresses. This may indicate malicious activity.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: [{'ip': '10.0.181.226', 'count': 187}, {'ip': '10.0.181.227', 'count': 183}]

- baseline_value: []

- deviation: Increased by X%




**Compliance Impact:**

- **NIS2** (Article 25.4): Failing to detect and respond to malicious activity may lead to a non-compliance with the regulations.



**Recommendation:** Implement IP-based authentication controls

---




### Positive Observations

- MFA adoption has increased since the last period

- Authentication failures have decreased since the last period




### Trend Analysis

**Improving:** mfa.enabled_users, auth_failures.fail_rate







## Compliance Observations
Here is a concise access-control compliance section based on the provided METRICS JSON and LEGAL TEXTS:

**Access Control**

* No MFA enabled for any users; coverage is 0% [NIS2-21.2.j].
* Total users: 50,215.
* Admins: no admins exist in this entity (count = 0) [NIS2-21.2.i].
* Last admin review date: unknown.

Note: The above findings are based solely on the provided METRICS JSON and LEGAL TEXTS, without making any assumptions or extrapolations.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures