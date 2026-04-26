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


The security posture indicates a high risk level, primarily due to the lack of MFA enabled users and elevated auth failure rates. Specific regulatory non-compliances were identified.


### Security Findings


#### CRITICAL: MFA Not Enabled for Users

No MFA enabled users were observed, which is a significant non-compliance to NIS2 Article 24.3.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: 0

- deviation: 100% increase from baseline




**Compliance Impact:**

- **NIS2** (Article 24.3): MFA must be enabled for all users



**Recommendation:** Immediately enable MFA for all users

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


#### HIGH: Elevated Auth Failure Rate

The auth failure rate of 54.08% is significantly higher than the baseline value and poses a high risk to security.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5408

- baseline_value: 0.5069

- deviation: +4.19% increase from baseline




**Compliance Impact:**

- **NIS2** (Article 15.1): Regular review of auth failure rates is required



**Recommendation:** Investigate and address the root cause of elevated auth failures

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


#### MEDIUM: Inadequate User Monitoring

No account takeovers or users with takeover were observed, but the lack of monitoring poses a medium risk to security and compliance.


**Evidence:**

- metric: auth_failures.account_takeovers

- current_value: 0

- baseline_value: 0

- deviation: No change from baseline




**Compliance Impact:**

- **NIS2** (Article 22.1): Regular monitoring of user activity is required



**Recommendation:** Implement regular user monitoring to detect potential security threats

---




### Positive Observations

- No exceptions were observed in the computed metrics




### Trend Analysis


**Degrading:** mfa.enabled_users, auth_failures.fail_rate


**Stable:** frame.distinct_users





## Compliance Observations
**Access-Control Compliance Section**

Based on the provided metrics and legal texts, the following access-control compliance findings are observed:

* No multi-factor authentication or continuous authentication solutions are used, as no users have MFA enabled ([NIS2 Art. 21(2)(j)]).
* The total number of users is 1,536,866.
* All administrators have MFA disabled (0 admins with MFA enabled) and there is no last review date available for admins ([NIS2-21.2.i]).

**Recommendations**

To achieve full compliance with the access-control requirements outlined in Article 21:

1. Implement multi-factor authentication or continuous authentication solutions to protect network and information systems.
2. Conduct regular reviews of administrator accounts, including enabling MFA and updating last review dates.

Note: No data available in the provided evidence regarding the current use of cryptography, encryption, human resources security, asset management, or basic cyber hygiene practices and cybersecurity training.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures