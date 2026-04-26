# Access Control Compliance Summary

**Scope:** Access control (authentication, anomalous login attempts, privileged risks)  
**Period:** 2020-11-01T00:00:00 (window=90d)

**Risk Level:** CRITICAL


## Key Metrics

- Total login attempts: **9309939**
- Distinct users: **1596182**
- Distinct source IPs: **1237098**

### Authentication
- Successful logins: **2822319**
- Failed logins: **6487620**
- Failure rate: **0.6968**
- Top failing IPs:  

  
  - 10.3.205.197 (443523)
  
  - 10.3.205.196 (257018)
  
  - 10.3.205.195 (236489)
  
  - 10.3.205.194 (177160)
  
  - 10.3.205.193 (152239)
  


### Attack Surface Indicators
- Known attack IP attempts: **0**
- Unique attack IPs: **0**
- Confirmed account takeover events: **0**
- Users impacted by takeovers: **0**

## Notable Exceptions

_No exceptions reported._



## AI-Generated Insights


For the 90-day window ending 2020-11-01, the organization shows a severe NIS2 compliance gap in authentication hardening: MFA coverage is 0% (0 of 1,596,182 users enabled), including zero MFA for admins (admins count also reported as 0, indicating missing/incorrect privileged account inventory). In parallel, authentication activity is heavily skewed toward failures: the overall authentication fail rate is 69.68% (6,487,620 total failures vs 2,822,319 successes), which is a material deterioration versus the historical baseline (fail rate ~54–55% in earlier periods). While no account takeovers and no “attack IP attempts” are detected by the current metrics, the high failure volume and concentration in a small set of source IPs (top IPs in the 10.3.205.193–197 range) indicate likely brute-force/credential-stuffing attempts or misconfiguration, requiring immediate investigation and remediation.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any user accounts. This represents a direct failure to implement baseline authentication controls expected for network and information security risk management under NIS2. The issue persists across historical periods (MFA coverage has been 0% in all provided baselines), indicating a systemic control gap rather than a transient outage.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement across historical periods; control remains fully absent.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate technical and organizational measures for securing network and information systems, including access control and authentication hardening (MFA).



**Recommendation:** Implement MFA for all users with a phased rollout (start with privileged/admin accounts and high-risk roles), enforce MFA at authentication entry points, and block sign-in for accounts that cannot enroll within a defined deadline. Provide evidence of enforcement (policy + telemetry showing enabled users >0).

---


#### CRITICAL: Authentication failure rate is extremely high and worsening

The system experiences a very high authentication failure rate (69.68%), indicating either widespread incorrect credentials, automated brute-force/credential-stuffing, or an authentication/identity integration issue. Compared to historical baselines, the fail rate has increased materially (from ~54.68% on 2020-08-03 and ~54.69% on 2020-05-05 to 69.68% currently). This elevates the likelihood of ongoing attack attempts and/or account lockout/availability impacts.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.6968 (69.68%)

- baseline_value: 0.5548 (55.48%)

- deviation: +14.20 percentage points (~+25.6% relative increase)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inadequate detection/response and insufficient access control resilience when authentication attempts fail at very high rates, potentially indicating active compromise attempts or misconfiguration.



**Recommendation:** Triage authentication failures immediately: (1) identify whether failures correlate with specific apps/tenants/identity providers, (2) enable/verify rate limiting, lockout/backoff, and bot/credential-stuffing protections, (3) review authentication logs for error codes and user/account patterns, and (4) validate that MFA enforcement is active at the identity layer (since MFA coverage is currently 0%).

---


#### HIGH: High Authentication Failure Rate

Authentication failure rate is 69.7%, which exceeds the 25% critical threshold.


**Evidence:**

- metric: fail_rate

- current_value: 69.7%

- threshold: 25%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): High failure rates may indicate inadequate access control measures.



**Recommendation:** Investigate sources of failed authentications. Consider implementing rate limiting and account lockout policies.

---


#### HIGH: Failure attempts concentrated in a small set of source IPs

Top source IPs account for a large share of failures, suggesting targeted automated attempts or a misrouted internal service. The current top IPs are 10.3.205.193–197 with counts ranging from 152,239 to 443,523. This concentration is inconsistent with a normal distribution of user-driven failures and warrants investigation for compromised hosts, misconfigured clients, or internal scanning.


**Evidence:**

- metric: auth_failures.top_ips

- current_value: Top IP 10.3.205.197: 443,523; 10.3.205.196: 257,018; 10.3.205.195: 236,489; 10.3.205.194: 177,160; 10.3.205.193: 152,239

- baseline_value: Top IPs previously included 23.137.225.33 (128,728) and 10.0.181.x ranges (e.g., 23,631; 19,053; 16,826; 16,411)

- deviation: Shift in top talkers to 10.3.205.193–197 and continued high failure volume.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Insufficient monitoring and response to anomalous authentication behavior can undermine the effectiveness of access control measures.



**Recommendation:** Investigate the listed source IPs: confirm ownership (internal vs external), validate whether they correspond to known NAT/proxies, and check for compromise indicators on those hosts. Apply targeted controls (temporary blocking/allowlisting, stricter rate limits) for offending IPs while ensuring legitimate services are not disrupted.

---


#### HIGH: Privileged account inventory and MFA status are missing/invalid (admins count = 0)

The metrics report admins count as 0 and with_mfa as 0, with last_review_date = 'unknown'. This is likely an instrumentation/data quality issue or indicates that privileged accounts are not being inventoried. For NIS2-aligned security governance, privileged access must be identified, reviewed, and protected with strong authentication.


**Evidence:**

- metric: admins.count / admins.with_mfa / admins.last_review_date

- current_value: admins.count=0; with_mfa=0; last_review_date='unknown'

- baseline_value: admins.count=0; with_mfa=0; last_review_date='unknown'

- deviation: No improvement; privileged account governance evidence is absent.




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of demonstrable privileged access management and review undermines the ability to show appropriate security measures for access control.



**Recommendation:** Fix privileged account inventory: integrate identity provider/HR/role systems to enumerate admin/privileged roles, record last review dates, and require MFA for all privileged accounts. Produce audit-ready evidence (role list, MFA enforcement policy, and compliance reporting).

---


#### HIGH: Incomplete MFA Coverage

MFA is enabled for 0/1596182 users (0.0%).


**Evidence:**

- metric: mfa_coverage

- current_value: 0.0%

- target: 100%




**Compliance Impact:**

- **NIS2** (Article 21.2(j)): Multi-factor authentication is explicitly required.



**Recommendation:** Enforce MFA for all user accounts, prioritizing privileged accounts.

---


#### MEDIUM: Authentication volume increased (more rows and distinct users)

The dataset shows growth in observed authentication-related events: frame rows increased from 6,531,204 (2020-08-03) to 9,309,939 currently, and distinct users increased from 1,529,697 to 1,596,182. This may reflect increased activity, but combined with the higher fail rate it suggests worsening authentication conditions that should be correlated with incidents and identity changes.


**Evidence:**

- metric: frame.rows / frame.distinct_users

- current_value: rows=9,309,939; distinct_users=1,596,182

- baseline_value: rows=6,531,204; distinct_users=1,529,697

- deviation: rows +42.5%; distinct_users +4.3%




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Rising authentication anomalies without corresponding compensating controls (e.g., MFA, rate limiting) indicates inadequate risk management.



**Recommendation:** Correlate the increase with change management: identity provider upgrades, new client apps, password policy changes, and network routing/proxy changes. Segment failures by application/tenant and by user cohort to determine whether the increase is attack-driven or operational.

---




### Positive Observations

- No account takeovers detected by current metrics (account_takeovers=0; users_with_takeover=0), suggesting the current detection logic is not flagging successful compromises.

- No 'attack_ip_attempts' and no 'attack_ip_distinct_ips' are recorded (both 0), which may indicate either effective blocking for successful attack patterns or limitations in the current detection criteria.




### Trend Analysis


**Degrading:** Authentication fail rate increased to 69.68% from 55.48% (2020-08-03 baseline), a +14.20 percentage point deterioration., Authentication event volume increased (frame rows +42.5% vs 2020-08-03), coinciding with higher failure rates.


**Stable:** MFA coverage remains at 0.0% across all provided periods (no improvement)., Account takeover indicators remain at 0 across current and historical baselines.





## Compliance Observations
### Access-control compliance (Article 21)

- The entity shall implement access control policies as part of human resources security and asset management measures. [NIS2 Art. 21(2)(i)]

- The entity shall use multi-factor authentication or continuous authentication solutions as an access-control measure. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1596182). [METRICS mfa]

- No administrators are recorded (admins.count: 0) and no administrators have MFA (admins.with_mfa: 0). [METRICS admins]

- Authentication failures total 6,487,620 with success_total 2,822,319 (fail_rate 0.6968). [METRICS auth_failures]

- No attack IP attempts or distinct attack IPs are recorded (attack_ip_attempts: 0; attack_ip_distinct_ips: 0). [METRICS auth_failures]

- No account takeovers are recorded (account_takeovers: 0; users_with_takeover: 0). [METRICS auth_failures]

- The access-control measures must be appropriate and proportionate to the risks posed, considering exposure, size, and incident likelihood/severity. [NIS2 Art. 21(1)]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures