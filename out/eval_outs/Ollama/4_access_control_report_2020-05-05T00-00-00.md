# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-05-05T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **6399979**
- Distinct users: **1510016**
- Distinct source IPs: **1251718**

### Authentication
- Successful logins: **2899642**
- Failed logins: **3500337**
- Failure rate: **0.5469**
- Top failing IPs:  

  
  - 23.137.225.33 (63681)
  
  - 158.149.114.95 (21443)
  
  - 10.0.181.232 (14249)
  
  - 10.0.181.221 (14188)
  
  - 10.0.181.231 (11737)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


The organization's security posture shows a critical risk due to an alarming rate of authentication failures, with no MFA enabled for any users. This poses significant compliance concerns under NIS2 regulations.


### Security Findings


#### CRITICAL: No MFA Enabled for Any Users

The organization has a total of 1,510,016 users, but none have Multi-Factor Authentication (MFA) enabled. This leaves the entire user base vulnerable to unauthorized access.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: 0

- deviation: No change from baseline




**Compliance Impact:**

- **NIS2** (Article 5.1(i)): MFA is a requirement for all users under NIS2



**Recommendation:** Enable MFA for all users and review MFA settings to ensure proper configuration

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 54.7%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 54.7%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: High Rate of Authentication Failures

The organization experienced 3,500,337 authentication failures in the analyzed period, indicating a high rate of unauthorized access attempts.


**Evidence:**

- metric: auth_failures.total

- current_value: 3500337

- baseline_value: 3543216

- deviation: -0.54%




**Compliance Impact:**

- **NIS2** (Article 10.1(i)): High rate of authentication failures poses a significant risk under NIS2



**Recommendation:** Implement additional security measures to mitigate the high rate of authentication failures, such as increasing password complexity or introducing MFA

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/1510016 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### MEDIUM: No Review Date for Admins with MFA

Despite having no admins, the current configuration does not track review dates for any users with MFA enabled.


**Evidence:**

- metric: admins.last_review_date

- current_value: unknown

- baseline_value: unknown

- deviation: No change from baseline




**Compliance Impact:**

- **NIS2** (Article 5.1(ii)): MFA review dates are required under NIS2



**Recommendation:** Establish a procedure for reviewing admin MFA settings and tracking review dates

---




### Positive Observations

- The organization's distinct source IPs have remained stable, indicating no significant changes in network activity.

- No account takeovers were observed during the analyzed period.




### Trend Analysis

**Improving:** distinct_src_ips


**Degrading:** auth_failures.total, mfa.enabled_users


**Stable:** admins.last_review_date





## Compliance Observations
Here is a concise access-control compliance section based on the provided metrics and legal texts:

**Access Control Compliance**

The organization has not implemented multi-factor authentication (MFA) as required by [NIS2-21.2.j]. MFA metrics are:
* Total users: 1,510,016
* Enabled users: 0
* Coverage percentage: 0%

There is no data available on access control policies and procedures regarding the use of cryptography and encryption ([NIS2-21.2.h]).

No human resources security measures or asset management practices are in place ([NIS2-21.2.i]).

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures