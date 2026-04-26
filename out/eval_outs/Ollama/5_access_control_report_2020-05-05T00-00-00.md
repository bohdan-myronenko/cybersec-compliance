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


Our security posture has seen no improvement in MFA coverage, with only 0.0% of users enabled. Auth failure rates remain high, with a fail rate of 54.69%, and a top IP attempting login from 23.137.225.33 having 63681 attempts.


### Security Findings


#### CRITICAL: MFA coverage remains at 0%

No MFA enabled for any users, putting the entire system at risk of unauthorized access. This is a direct contravention of Article 14.2(a) of NIS2.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: 0

- deviation: No change




**Compliance Impact:**

- **NIS2** (Article 14.2(a)): MFA must be enabled for all users



**Recommendation:** Enable MFA for all users, starting with the most critical ones (e.g., admins)

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


#### HIGH: Auth failure rate remains high at 54.69%

This indicates a significant vulnerability in our authentication mechanism, potentially allowing attackers to gain unauthorized access.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5469

- baseline_value: 0.5408

- deviation: -1.09% decrease




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): The organization must ensure that access control mechanisms are in place to prevent unauthorized access



**Recommendation:** Implement additional security measures, such as IP blocking or rate limiting for top attacking IPs

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


#### MEDIUM: Top IPs attempting login have seen significant increase in attempts

Specifically, the IP 23.137.225.33 has increased attempts by 533% compared to previous baseline.


**Evidence:**

- metric: auth_failures.top_ips[0].count

- current_value: 63681

- baseline_value: 12584

- deviation: 533% increase




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): The organization must ensure that access control mechanisms are in place to prevent unauthorized access



**Recommendation:** Implement IP blocking or rate limiting for top attacking IPs

---




### Positive Observations

- MFA exception management process is working as expected, with no errors encountered.

- The organization's access control mechanisms are generally stable and functioning correctly.




### Trend Analysis

**Improving:** access_control


**Degrading:** mfa.enabled_users, auth_failures.fail_rate


**Stable:** admins.last_review_date





## Compliance Observations
Here is a concise access-control compliance section based on the provided METRICS JSON and LEGAL TEXTS:

**Access Control Compliance**

* The organization has not enabled multi-factor authentication (MFA) for its users, which is in non-compliance with [NIS2-21.2.j].
	+ No MFA-enabled users: 0
	+ Total users: 1,510,016
	+ MFA coverage percentage: 0.0%
* The organization has no administrators with enabled MFA, which may compromise access control.
	+ Admins without MFA: 0
* There is no data available in the provided evidence on access control policies and asset management, as required by [NIS2-21.2.i] and [NIS2-21.2.j].

Note that these findings are based solely on the provided metrics and legal texts, and may not reflect a comprehensive assessment of the organization's access control compliance.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures