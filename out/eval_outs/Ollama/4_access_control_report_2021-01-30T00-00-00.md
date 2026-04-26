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


The security posture of the organization has shown significant improvement in authentication failures, but remains critically vulnerable to MFA enforcement. The top IPs for authentication failures have shifted, indicating potential lateral movement by attackers.


### Security Findings


#### CRITICAL: MFA Enforcement Critical Vulnerability

No MFA enforcement is in place for any users, making the organization critically vulnerable to authentication attacks.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: 0

- deviation: 0% (no change)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inadequate MFA enforcement may lead to unauthorized access and breach of confidentiality.



**Recommendation:** Enable MFA for all users with a coverage goal of at least 95%.

---


#### HIGH: Increased Authentication Failures from Untrusted IPs

A high number of authentication failures are coming from untrusted IP addresses, indicating potential brute-force attacks.


**Evidence:**

- metric: auth_failures.total

- current_value: 1511918

- baseline_value: 6487620

- deviation: -76.6% (improvement)




**Compliance Impact:**

- **NIS2** (Article 21.2(ii)): Inadequate access controls may lead to unauthorized access and breach of confidentiality.



**Recommendation:** Implement IP-based rate limiting for authentication attempts, with a focus on high-risk IPs.

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


#### MEDIUM: Shift in Top IPs for Authentication Failures

The top IPs for authentication failures have shifted, indicating potential lateral movement by attackers.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: ['170.39.78.106', '10.0.77.230']

- baseline_value: ['10.3.205.197', '10.3.205.196']

- deviation: IPs changed by 100%





**Recommendation:** Monitor top IPs for authentication failures and consider implementing IP-based rate limiting.

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

- MFA enforcement has improved significantly, with a 76.6% reduction in authentication failures compared to the previous period.




### Trend Analysis

**Improving:** mfa.enabled_users, auth_failures.total







## Compliance Observations
Based on the provided METRICS JSON and LEGAL TEXTS, here is a concise access-control compliance section:

**Access Control Compliance**

The organization has not implemented Multi-Factor Authentication (MFA) as no users have MFA enabled ([NIS2-21.2.j]). This may pose a risk to network and information systems security.

* Total Users: 635091
* Enabled Users with MFA: 0

**Administrators Compliance**

No administrators were found, which may indicate an incomplete implementation of access control policies ([NIS2-21.2.i]).

* Count of Administrators: 0
* Administrators with MFA: 0

Note that no other relevant metrics or data points are available in the provided METRICS JSON to assess access-control compliance further.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures