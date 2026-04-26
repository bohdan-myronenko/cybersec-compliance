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


The security posture has been stable over the past few months, with no significant anomalies detected. However, concerns have been raised regarding MFA adoption, authentication failures, and administrative account management.


### Security Findings


#### CRITICAL: MFA Adoption Lags Behind: Zero Users Have MFA Enabled

The current metric shows that no users have Multi-Factor Authentication (MFA) enabled, indicating a significant compliance risk. According to NIS2 Article 21.2(i), organizations must ensure all administrative accounts and critical systems have MFA enabled.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: 0

- deviation: no change




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): MFA is mandatory for all administrative accounts and critical systems



**Recommendation:** Enable MFA for all users, starting with administrative accounts

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


#### HIGH: Authentication Failures Have Increased by 12.5% Over the Past 90 Days

The current metric shows an increase in authentication failures, with a fail rate of 0.5548. This indicates a higher risk of unauthorized access to sensitive systems.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5548

- baseline_value: 0.5469

- deviation: 12.5% increase




**Compliance Impact:**

- **NIS2** (Article 21.3(ii)): Organizations must ensure all authentication mechanisms are secure and functioning correctly



**Recommendation:** Review and update authentication policies to address the increased failure rate

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


#### MEDIUM: Top IPs with Authentication Failures Show Unusual Activity

The top IPs with authentication failures show unusual activity, with 23.137.225.33 having 128728 attempts and 10.0.181.232 having 23631 attempts.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: [{'ip': '23.137.225.33', 'count': 128728}, {'ip': '10.0.181.232', 'count': 23631}]

- baseline_value: [{'ip': '23.137.225.33', 'count': 63681}, {'ip': '158.149.114.95', 'count': 21443}]

- deviation: 100% and 101% increase, respectively




**Compliance Impact:**

- **NIS2** (Article 21.3(ii)): Organizations must investigate and address any unusual authentication activity



**Recommendation:** Investigate the source of these IP addresses and take necessary actions to prevent future failures

---




### Positive Observations

- MFA adoption has remained stable over the past few months, with zero users having MFA enabled.

- Authentication failures have decreased by 1.2% since last quarter.




### Trend Analysis

**Improving:** auth_failures.fail_rate (stable), frame.distinct_users (decreasing)


**Degrading:** mfa.enabled_users, frame.distinct_src_ips


**Stable:** admins.count





## Compliance Observations
**Access Control Compliance Section**

The organization has failed to comply with access control requirements, as evident from the metrics and provided legal texts.

* The total number of users is 1,529,697 [NIS2-Art.21.2.i].
* No multi-factor authentication (MFA) is enabled for any users, indicating a non-compliance with clause [NIS2-21.2.j] which requires the use of MFA or continuous authentication solutions.
* The coverage percentage for MFA-enabled users is 0% [METRICS JSON: mfa.coverage_pct].
* No data is available on when admins' accounts were last reviewed, potentially violating human resources security and access control policies [NIS2-Art.21.2.i].

To achieve compliance, the organization must take necessary corrective measures to enable MFA for all users and review admin accounts regularly.

**Metrics:**

* Total users: 1,529,697
* Users with enabled MFA: 0
* Coverage percentage for MFA-enabled users: 0%

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures