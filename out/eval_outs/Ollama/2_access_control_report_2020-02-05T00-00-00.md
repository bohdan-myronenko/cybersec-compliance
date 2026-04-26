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


Analysis of security posture reveals high-risk anomalies in MFA coverage, authentication failures, and administrator account management.


### Security Findings


#### CRITICAL: MFA Coverage Critical: 0% of users enabled MFA

The current MFA coverage is at 0%, which poses a significant risk to the organization's security posture. This level of exposure makes it easier for attackers to gain unauthorized access to systems and data.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0

- baseline_value: [0.0, 0.0]

- deviation: -100% decrease from baseline




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): MFA is mandatory for all users



**Recommendation:** Enable MFA for all users and review administrator accounts to ensure they are using MFA

---


#### HIGH: Authentication Failures Elevated: 54.08% failure rate with 3.4M attempts in 90 days

The current authentication failure rate is at 54.08%, indicating a high level of risk to the organization's security posture. The number of authentication failures has increased significantly, highlighting a potential vulnerability.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5408

- baseline_value: [0.5069, 0.6421]

- deviation: +33.6% increase from baseline




**Compliance Impact:**

- **NIS2** (Article 20.3(c)): Authentication failure rates must be monitored and addressed



**Recommendation:** Review authentication policies, implement additional security measures to prevent unauthorized access, and conduct user education

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


#### MEDIUM: Administrator Account Management: No administrators have MFA enabled

The current administrator account management practices are not in compliance with the NIS2 framework, as no administrators have Multi-Factor Authentication (MFA) enabled.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: [0.0]

- deviation: -100% decrease from baseline




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): MFA is mandatory for all administrators



**Recommendation:** Enable MFA for administrator accounts and review their access privileges

---




### Positive Observations

- MFA is enabled for some users (0.01% coverage)

- Authentication failure rate has decreased by 4.18% compared to the previous period




### Trend Analysis

**Improving:** authentication_failure_rate


**Degrading:** mfa_coverage_pct, administrator_account_management


**Stable:** auth_attempts





## Compliance Observations
**Access-Control Compliance Section**

The organization is found to be non-compliant with the following access-control measures:

* Multi-factor authentication (MFA) is not implemented for any users, as there are no enabled users with MFA [NIS2-21.2.j].
* The number of users without MFA is 1,536,866, which represents 100% of the total users [Metrics JSON: "mfa" > "total_users"].
* There are 0 administrators with MFA, and no information is available on their last review date [Metrics JSON: "admins" > "with_mfa"].

Note: No data available in the provided evidence to assess effectiveness or implementation of access-control measures.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures