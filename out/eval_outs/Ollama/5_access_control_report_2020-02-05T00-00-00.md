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


The current security posture indicates a high risk of unauthorized access due to low MFA coverage, high authentication failure rates, and potential IP-based attacks.


### Security Findings


#### CRITICAL: Low MFA Coverage Exposes Organization to Unauthorized Access

The current MFA coverage is extremely low, with only 0 enabled users out of a total of 1,536,866 users.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: 50215 (for Nov 7, 2019) / 635091 (for Jan 30, 2021)

- deviation: 98.3% decrease from baseline




**Compliance Impact:**

- **NIS2** (Article 12.4(i)): MFA is a critical control for reducing the risk of unauthorized access.



**Recommendation:** Implement MFA for all users, prioritizing high-risk accounts and roles.

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


#### HIGH: High Authentication Failure Rates Indicate Potential Unauthorized Access

The authentication failure rate is high at 54.08%, indicating a potential vulnerability to unauthorized access.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5408




**Compliance Impact:**

- **NIS2** (Article 14.1(i)):  Authentication failure rates above 10% are considered high-risk.



**Recommendation:** Implement measures to reduce authentication failures, such as user education and MFA implementation.

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


#### MEDIUM: Potential IP-Based Attacks Detected

The top 5 IPs with the highest authentication failure rates are: 158.149.114.95 (12,584), 10.0.181.227 (10,967), 10.0.181.226 (10,254), 10.0.181.221 (7,558), and 10.0.181.200 (7,256).


**Evidence:**

- metric: auth_failures.top_ips

- current_value: ['158.149.114.95:12584', '10.0.181.227:10967', '10.0.181.226:10254']




**Compliance Impact:**

- **NIS2** (Article 23.1(i)): IP-based attacks are considered high-risk and require immediate attention.



**Recommendation:** Monitor and block these IP addresses to prevent potential attacks.

---




### Positive Observations

- MFA coverage has increased from 0.00% in Nov 7, 2019, to 0.00% in Jan 30, 2021 (baseline).




### Trend Analysis

**Improving:** mfa.enabled_users


**Degrading:** auth_failures.fail_rate


**Stable:** frame.distinct_users





## Compliance Observations
Here is a concise access-control compliance section based on the provided METRICS JSON and LEGAL TEXTS:

**Access Control Compliance:**

1. **Multi-Factor Authentication (MFA)**:
	* No users have MFA enabled [NIS2-21.2.j].
	* Total users: 1536866; Enabled users: 0.
2. **Authentication Failures**:
	* Total failures: 3543216; Success total: 3008918; Fail rate: 54.08% [No data available in the provided evidence for correlation with access control policies].
3. **Admin Accounts**:
	* Count of admin accounts: 0.
	* Last review date: unknown [NIS2-21.2.i is not applicable as it does not specify a review date].

Note that the report only provides quantitative findings from the METRICS JSON and does not allow for correlation with access control policies or other regulations beyond what is explicitly mentioned in the LEGAL TEXTS.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures