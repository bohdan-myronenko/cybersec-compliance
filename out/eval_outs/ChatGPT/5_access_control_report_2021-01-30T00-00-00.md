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


Across the last 90 days (ending 2021-01-30), the environment shows a severe NIS2 compliance gap: MFA is not enabled for any users (0% coverage), including administrators (0 admins identified with MFA). Authentication activity also shows a high overall failure rate (64.21% failures), with a large volume of failed attempts (1,511,918 total failures) and concentration in a small set of source IPs. While no account takeovers or “attack IP attempts” were detected by the computed metrics, the combination of zero MFA coverage and elevated authentication failures represents a critical risk to account compromise and violates NIS2 expectations for risk-based access control and security of network and information systems.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any of the 635,091 distinct users in the analyzed period. This creates a single-factor authentication exposure and materially increases the likelihood and impact of credential theft, phishing, and brute-force attempts. From a compliance perspective, this indicates a failure to implement appropriate authentication hardening measures expected under NIS2 security requirements.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement; consistently 0% across historical periods (2020-05-05, 2020-08-03, 2020-11-01).




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of MFA undermines access control measures and increases risk of unauthorized access to network and information systems.



**Recommendation:** Implement MFA for all users with a phased rollout (start with privileged/admin accounts and high-risk user groups). Enforce MFA at authentication policy level (IdP/SSO) and block sign-in for accounts that do not meet MFA requirements. Provide an exception process with time-bound approvals and compensating controls (e.g., step-up auth, device trust) until full coverage is achieved.

---


#### CRITICAL: No administrators identified with MFA (privileged access not hardened)

The computed metrics report 0 administrators and 0 admins with MFA, with last_review_date marked as 'unknown'. This prevents validation that privileged accounts are protected with MFA and suggests either missing inventory/role mapping or a lack of privileged access governance. Under NIS2, privileged access must be controlled and secured with appropriate measures.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0

- deviation: No improvement; also indicates potential gaps in admin inventory/controls (last_review_date='unknown').




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inadequate privileged access controls (or inability to demonstrate them) increases the risk of unauthorized administrative actions.



**Recommendation:** Fix privileged account inventory: ensure all admin/privileged roles are correctly mapped and counted. Establish a recurring review cadence (set last_review_date to a real value and automate evidence capture). Require MFA for all privileged roles immediately and verify via reporting that privileged accounts have MFA enforced at the IdP.

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


#### HIGH: High authentication failure rate (64.21%) indicating potential brute-force/credential issues

Authentication failures are extremely high: 1,511,918 total failures vs 842,679 successful authentications, resulting in a fail rate of 64.21%. This level of failure can indicate brute-force attempts, misconfigured clients, or widespread credential errors. Even though computed metrics show 0 account takeovers and 0 attack IP attempts, the failure volume combined with zero MFA coverage increases the probability of eventual compromise.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6421 (64.21%)

- baseline_value: 0.6968 (69.68%) on 2020-11-01; 0.5548 (55.48%) on 2020-08-03; 0.5469 (54.69%) on 2020-05-05

- deviation: Compared to 2020-11-01: improvement of ~5.47 percentage points; compared to 2020-08-03 and 2020-05-05: degradation of ~8.73 and ~9.52 percentage points respectively.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent authentication failures reflect weaknesses in access security controls and increase exposure to unauthorized access attempts.



**Recommendation:** Triage the failure sources: (1) identify whether failures are concentrated by user, application, or client; (2) implement/verify rate limiting, lockout/step-up policies, and bot detection for repeated failures; (3) review top failing IPs and associated accounts for suspicious patterns; (4) validate client configuration to reduce legitimate mis-authentications. Produce an evidence report showing controls are active and effective (e.g., reduced fail rate and blocked abusive patterns).

---


#### HIGH: Authentication failures concentrated in a small set of source IPs

Failed authentication attempts are heavily concentrated in top source IPs, suggesting automated activity or targeted attempts. The top IP 170.39.78.106 accounts for 67,563 failures, followed by 10.0.77.230 (35,558), and multiple internal 10.x addresses with thousands of failures each. This concentration warrants investigation for compromised hosts, misconfigured services, or abusive automation.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IPs: 170.39.78.106=67563; 10.0.77.230=35558; 10.1.6.103=9507; 10.0.181.231=8202; 10.0.181.232=8092

- baseline_value: Historical top IPs differed (e.g., 10.3.205.197=443523 on 2020-11-01; 23.137.225.33=128728 on 2020-08-03)

- deviation: Concentration persists, but the specific top IPs change across periods.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Concentrated failed authentication attempts indicate potential security events and insufficient preventive/detective controls.



**Recommendation:** Investigate each top IP: determine whether it belongs to known NAT/proxies, legitimate services, or external clients. If external/unknown, block or challenge at the edge (WAF/IdP) and add IP reputation/rate limits. If internal, check for compromised endpoints or misconfigured authentication clients. Document findings and remediation actions.

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


#### MEDIUM: No detected account takeovers despite very high failure volume (detection gap risk)

The metrics report 0 account_takeovers and 0 users_with_takeover, even while failures are extremely high (1,511,918). This could mean attacks are not succeeding, or it could indicate that takeover detection logic is incomplete or not aligned with actual threat patterns. Either way, the lack of detected takeovers should be validated against detection coverage.


**Evidence:**

- metric: auth_failures.account_takeovers

- current_value: 0

- baseline_value: 0

- deviation: No change across historical periods; detection may be consistently non-functional or overly conservative.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient detection/response evidence can undermine the effectiveness of access security controls.



**Recommendation:** Validate takeover detection: review detection rules, telemetry sources, and thresholds (e.g., impossible travel, new device, password reset + login sequence, MFA bypass attempts). Run a tabletop exercise using simulated compromised credentials to confirm alerts trigger. Ensure evidence is captured for compliance reporting.

---




### Positive Observations

- No account takeovers were detected by the computed metrics (account_takeovers=0; users_with_takeover=0), suggesting either limited successful compromise or conservative detection.

- Authentication failure rate shows some improvement versus 2020-11-01 (fail_rate 64.21% current vs 69.68% baseline), indicating partial reduction in failure intensity.




### Trend Analysis

**Improving:** Authentication fail rate improved compared to 2020-11-01 (69.68% -> 64.21%, ~-5.47 percentage points).


**Degrading:** Authentication fail rate is worse than 2020-08-03 and 2020-05-05 baselines (55.48% -> 64.21% and 54.69% -> 64.21%, ~+8.73 and +9.52 percentage points).


**Stable:** MFA coverage remains at 0.0% across all compared periods (no progress on MFA enablement)., Account takeover indicators remain at 0 across periods (account_takeovers=0).





## Compliance Observations
## Access-Control Compliance (Concise)

- The entity shall implement human resources security, access control policies, and asset management as cybersecurity risk-management measures. [NIS2 Art. 21(2)(i)]

- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]

- MFA coverage is reported as 0.0% (enabled_users: 0 of total_users: 635091). [METRICS mfa]

- Administrators are reported as count: 0, with_mfa: 0, and last_review_date: “unknown”. [METRICS admins]

- Authentication failures are reported: total 1511918, success_total 842679, fail_rate 0.6421. [METRICS auth_failures]

- Top source IPs for authentication failures include 170.39.78.106 (67563) and 10.0.77.230 (35558). [METRICS auth_failures.top_ips]

- No data available in the provided evidence for account takeovers or users_with_takeover. [METRICS auth_failures]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures