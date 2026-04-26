# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-02-05T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **6552134**
- Distinct users: **1536866**
- Distinct source IPs: **1328745**

### Authentication
- Successful logins: **3008918**
- Failed logins: **3543216**
- Failure rate: **0.5408**
- Top failing IPs:  

  
  - 158.149.114.95 (12584)
  
  - 10.0.181.227 (10967)
  
  - 10.0.181.226 (10254)
  
  - 10.0.181.221 (7558)
  
  - 10.0.181.200 (7256)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


Security posture is at a high risk due to low MFA adoption, significant auth failures, and potential attack IP attempts.


### Security Findings


#### CRITICAL: MFA Adoption Rate is Critically Low

The current MFA adoption rate is 0%, which poses a significant risk to the security posture. This is a critical finding that requires immediate attention.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: 635091

- deviation: -100% deviation from baseline




**Compliance Impact:**

- **NIS2** (Article 4.1): Low MFA adoption rate may impact compliance with NIS2 Article 4.1



**Recommendation:** Enable MFA for all users and set a minimum password strength of 12 characters

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 54.1%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 54.1%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: Significant Auth Failures Detected

The current auth failure rate is 54.09%, which is significantly higher than the baseline of 50.69%. This indicates a potential security risk.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5408

- baseline_value: 0.5069

- deviation: +6.40% deviation from baseline




**Compliance Impact:**

- **NIS2** (Article 17.1): High auth failure rate may impact compliance with NIS2 Article 17.1



**Recommendation:** Review and update password policies to include multi-factor authentication

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/1536866 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### MEDIUM: Potential Attack IP Attempts Detected

There are several IP addresses that have attempted to access the system multiple times. This may indicate a potential security threat.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: [{'ip': '158.149.114.95', 'count': 12584}, {'ip': '10.0.181.227', 'count': 10967}]

- baseline_value: []

- deviation: New IP addresses detected




**Compliance Impact:**

- **NIS2** (Article 15.1): Potential attack IP attempts may impact compliance with NIS2 Article 15.1



**Recommendation:** Review and block suspicious IP addresses

---




### Positive Observations

- Password strength is high (>12 characters)




### Trend Analysis

**Improving:** password strength


**Degrading:** MFA adoption rate, auth failure rate


**Stable:** distinct users, distinct source IPs





## Compliance Observations
**Access Control Compliance Section**

* The organization has not implemented Multi-Factor Authentication (MFA) for users, as no MFA-enabled users are reported ([NIS2-21.2.j]).

**Metrics**

* Total Users: 1,536,866
* MFA-enabled Users: 0

Note: This report only covers the access control requirements and does not include other aspects of cybersecurity compliance.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures