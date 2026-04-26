# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-05-05T00:00:00 (window=90d)

**Risk Level:** HIGH


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


Analysis could not be completed due to an error.


### Security Findings


#### INFO: Analysis Error

Failed to parse JSON: Expecting ',' delimiter: line 14 column 29 (char 718)





**Recommendation:** Retry the analysis or review metrics manually.

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






### Trend Analysis







## Compliance Observations
**Access-Control Compliance**

1. **Multi-Factor Authentication (MFA)**: No MFA is enabled, and no users have multi-factor authentication set up ([NIS2-21.2.j]). Total users without MFA: 1510016.
2. **Admins**: No admins are present, with or without MFA ([NIS2-21.2.i]).
3. **Account Takeovers**: No account takeovers detected, and no users have been compromised ([NIS2-21.2.j]). Total account takeovers: 0.
4. **Attack IP Attempts**: No attack IP attempts were made ([NIS2-21.2.j]). Distinct attack IPs: 0.

Note: The metrics provided do not include any information on access-control policies or procedures, human resources security, asset management, or other related measures mentioned in the legal texts. Therefore, no further findings can be reported for these areas.

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures