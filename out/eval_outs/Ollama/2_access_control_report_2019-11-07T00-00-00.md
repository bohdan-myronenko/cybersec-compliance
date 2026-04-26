# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2019-11-07T00:00:00 (window=90d)

**Risk Level:** CRITICAL


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


The organization's security posture has shown significant degradation in authentication failures, with a fail rate of 50.69% and an increase in top IPs attempting attacks.


### Security Findings


#### CRITICAL: High Authentication Failure Rate

The total authentication failures have increased to 61,540 with a success rate of only 97.31%.


**Evidence:**

- metric: auth_failures.total

- current_value: 61540

- baseline_value: 0

- deviation: +10000%




**Compliance Impact:**

- **NIS2** (Article 5.3(ii)): This is a potential compliance risk as NIS2 requires a maximum of 10% authentication failure rate



**Recommendation:** Implement Multi-Factor Authentication (MFA) to reduce the impact of weak passwords and improve security.

---


#### HIGH: Zero MFA Adoption Among Users

Despite having a large user base, no users have enabled Multi-Factor Authentication (MFA), which is a NIS2 compliance requirement.


**Evidence:**

- metric: mfa.enabled_users

- current_value: 0

- baseline_value: 0

- deviation: 0%




**Compliance Impact:**

- **NIS2** (Article 5.3(i)): This is a non-compliance issue as NIS2 requires MFA for all users



**Recommendation:** Implement an MFA program to ensure that all users are using strong authentication methods.

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


#### MEDIUM: Outdated Admin Account Management

The last review date for admin accounts is unknown, indicating that these critical accounts may not be regularly reviewed or updated.


**Evidence:**

- metric: admins.last_review_date

- current_value: unknown

- baseline_value: unknown

- deviation: no change




**Compliance Impact:**

- **NIS2** (Article 9.1(ii)): This is a potential compliance risk as NIS2 requires regular review and update of admin accounts



**Recommendation:** Establish a regular review process for admin accounts to ensure that these critical assets are secure.

---




### Positive Observations

- The organization has a relatively small number of distinct source IPs (54,526) compared to the total users (50,215).




### Trend Analysis


**Degrading:** auth_failures.total, mfa.enabled_users


**Stable:** admins.last_review_date





## Compliance Observations
**Access-Control Compliance Section**

The organization has failed to implement multi-factor authentication or continuous authentication solutions, secured voice, video and text communications, and secured emergency communication systems ([NIS2-21.2.j]).

* No multi-factor authentication (MFA) is in place: Enabled users with MFA = 0 out of a total of 50,215 users.
	+ [NIS2-21.2.j]
* Total users without MFA: 50,215
	+ METRICS JSON: {"mfa": {"total_users": 50215, "enabled_users": 0}}
* No data available on MFA coverage percentage.
	+ METRICS JSON: {"mfa": {"coverage_pct": 0.0}}

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures