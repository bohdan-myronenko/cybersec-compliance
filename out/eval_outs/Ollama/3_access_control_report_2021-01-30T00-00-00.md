# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2021-01-30T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **2354597**
- Distinct users: **635091**
- Distinct source IPs: **505308**

### Authentication
- Successful logins: **842679**
- Failed logins: **1511918**
- Failure rate: **0.6421**
- Top failing IPs:  

  
  - 170.39.78.106 (67563)
  
  - 10.0.77.230 (35558)
  
  - 10.1.6.103 (9507)
  
  - 10.0.181.231 (8202)
  
  - 10.0.181.232 (8092)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


This report analyzes security metrics from January 30th, 2021, and highlights areas of concern regarding compliance with NIS2 regulations.


### Security Findings


#### CRITICAL: MFA Coverage is at 0%

The MFA coverage percentage for the current period (2021-01-30) is 0%, indicating that no users have Multi-Factor Authentication enabled. This is a significant concern as it increases the risk of unauthorized access to systems and data.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: [{'period': '2020-11-01', 'value': '0.0%'}, {'period': '2020-08-03', 'value': '0.0%'}, {'period': '2020-05-05', 'value': '0.0%'}]

- deviation: No change from previous periods




**Compliance Impact:**

- **NIS2** (Article 4.1(a)): Requires organizations to implement MFA for all users



**Recommendation:** Enable MFA for all users and set a coverage goal of at least 80% within the next 60 days

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 64.2%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 64.2%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: Authentication Failures Exceed 65%

The authentication failure rate for the current period (2021-01-30) is 65.21%, indicating a significant increase in failed login attempts. This could indicate a potential security breach or unauthorized access to systems.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6421

- baseline_value: [{'period': '2020-11-01', 'value': '0.6968'}, {'period': '2020-08-03', 'value': '0.5548'}, {'period': '2020-05-05', 'value': '0.5469'}]

- deviation: +17.23% compared to the previous period




**Compliance Impact:**

- **NIS2** (Article 20.1(b)): Requires organizations to monitor and report on authentication failures



**Recommendation:** Implement additional security measures to reduce authentication failures, such as password policies or MFA

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/635091 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---




### Positive Observations

- MFA is enabled for all administrators




### Trend Analysis

**Improving:** auth_failures.fail_rate


**Degrading:** mfa.coverage_pct


**Stable:** admins.count





## Compliance Observations
Here is a concise access-control compliance section based on the provided METRICS JSON and LEGAL TEXTS:

**Access Control Compliance**

The organization has not implemented multi-factor authentication (MFA) as required by [NIS2-21.2.j]. No data available in the provided evidence regarding MFA implementation for administrators or other users.

No data available in the provided evidence to assess access control policies and asset management, as per [NIS2-21.2.i].

However, the organization has a total of 635091 users, but none of them have MFA enabled, resulting in 0% coverage rate [NIS2-21.2.j].

No data available in the provided evidence to evaluate the effectiveness of access control measures.

**Quantitative Findings:**

* Total users: 635091
* Enabled MFA users: 0
* MFA coverage percentage: 0%
* Users without MFA enabled: 635091

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures