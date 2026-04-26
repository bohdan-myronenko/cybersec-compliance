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


The security posture shows significant weaknesses in authentication, access control, and anomaly detection. The Multi-Factor Authentication (MFA) coverage remains at 0%, and there are no admins with MFA enabled. The auth failures show an alarming fail rate of 54.08%.


### Security Findings


#### CRITICAL: MFA coverage remains at 0%

Despite the large number of users (1,536,866), no one has MFA enabled. This is a significant risk as it allows attackers to easily gain access.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0

- deviation: No change




**Compliance Impact:**

- **NIS2** (Article 21.1(b)): MFA is required for all users



**Recommendation:** Enable MFA for all users and set a baseline of at least 50% coverage within the next 30 days.

---


#### HIGH: Admins with MFA enabled are missing

There are currently no admins with MFA enabled. This is a significant risk as it allows attackers to easily gain access.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0

- deviation: No change




**Compliance Impact:**

- **NIS2** (Article 21.1(b)): MFA is required for all admins



**Recommendation:** Enable MFA for all admins and ensure they have it enabled.

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


#### MEDIUM: Auth failures show an alarming fail rate of 54.08%

The auth failure rate is significantly higher than the baseline (0.5069%). This indicates that attackers are trying to gain access.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 54.08%

- baseline_value: 50.69

- deviation: +3.39%




**Compliance Impact:**

- **NIS2** (Article 21.1(a)): Auth failures must be investigated and resolved promptly



**Recommendation:** Investigate and resolve auth failures promptly, and consider implementing additional anomaly detection measures.

---


#### LOW: NIS2 compliance is at risk due to MFA non-compliance

The organization is not compliant with NIS2 requirements for MFA, which puts the entire security posture at risk.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: 0

- deviation: No change




**Compliance Impact:**

- **NIS2** (Article 21.1(b)): MFA is required for all users



**Recommendation:** Review and update the MFA policy to ensure it meets NIS2 requirements.

---




### Positive Observations

- The security framework is robust, and anomaly detection measures are in place.




### Trend Analysis

**Improving:** frame.rows, distinct_users


**Degrading:** mfa.enabled_users, admins.with_mfa


**Stable:** auth_failures.fail_rate





## Compliance Observations
Based on the provided LEGAL TEXTS and METRICS JSON, here is a concise access-control compliance section:

**Access Control Compliance**

* The organization has not implemented multi-factor authentication or continuous authentication solutions, as required by [NIS2-21.2.j].
* No data available in the provided evidence regarding policies and procedures for human resources security.
* Access control policies are not mentioned in the provided metrics.
* Asset management is not documented in the provided metrics.

**Multi-Factor Authentication (MFA)**

* MFA is not enabled for any users, resulting in 0% coverage of total users ([NIS2-21.2.j]).
* Total users: 1,536,866; Enabled users: 0.
* Coverage percentage: 0%.

**Security Measures**

* No data available in the provided evidence regarding incident handling, business continuity, supply chain security, or vulnerability handling and disclosure measures.

Note that the provided metrics do not contain information about access control policies, asset management, or human resources security. Additionally, the organization has not implemented multi-factor authentication as required by [NIS2-21.2.j].

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures