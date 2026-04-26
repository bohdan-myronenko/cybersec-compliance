# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2019-11-07T00:00:00 (window=90d)

**Risk Level:** HIGH


## Key Metrics

- Total login attempts: **121411**
- Distinct users: **50215**
- Distinct source IPs: **55426**

### Authentication
- Successful logins: **59871**
- Failed logins: **61540**
- Failure rate: **0.5069**
- Top failing IPs:  

  
  - 10.0.181.226 (187)
  
  - 10.0.181.227 (183)
  
  - 10.0.77.228 (108)
  
  - 10.0.77.226 (104)
  
  - 10.0.77.229 (94)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


Analysis could not be completed due to an error.


### Security Findings


#### INFO: Analysis Error

Failed to parse JSON: Expecting ',' delimiter: line 14 column 35 (char 634)





**Recommendation:** Retry the analysis or review metrics manually.

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 50.7%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 50.7%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/50215 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---






### Trend Analysis







## Compliance Observations
Here is a concise access-control compliance section based on the provided metrics and legal texts:

**Access Control Compliance**

The organization has not implemented multi-factor authentication or continuous authentication solutions as required by [NIS2-21.2.j].

* No users have MFA enabled ([metrics]: "mfa": {"enabled_users": 0}).
* No data available in the provided evidence on access control policies and asset management.
* The number of distinct source IPs accessing the network is 55426 ([metrics]: "frame": {"distinct_src_ips": 55426}).

The organization has not taken into account the vulnerabilities specific to each direct supplier or service provider, as required by [NIS2-21.3].

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures