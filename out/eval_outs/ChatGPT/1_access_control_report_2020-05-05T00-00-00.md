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


For the 90-day window ending 2020-05-05, the environment shows a severe NIS2-relevant authentication control gap: MFA is effectively not deployed (0% coverage for 1,510,016 users), and there is a very high authentication failure rate (54.69% failures: 3,500,337 total failures vs 2,899,642 successes). While no account takeovers or “attack IP attempts” are flagged by the metric set, the combination of zero MFA and elevated failure activity represents a critical compliance and operational risk under NIS2. Additionally, there are no recorded admins (0) and no last review date, indicating missing governance/visibility for privileged access controls.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication is not enabled for any user accounts. With 1,510,016 distinct users and 0 enabled users, the organization is not meeting baseline expectations for strong authentication controls. This materially increases the likelihood and impact of credential compromise and unauthorized access, and it undermines NIS2 requirements for risk management and security measures for network and information systems.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0%

- deviation: No improvement; remains at 0% (current: 0 enabled of 1,510,016 users)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate security measures (e.g., strong authentication such as MFA) increases risk of unauthorized access and does not adequately address security of network and information systems.



**Recommendation:** Immediately enable MFA for all users, starting with privileged roles and high-risk populations. Implement a phased rollout with enforced enrollment (no exceptions) and require MFA for all interactive logins. Provide compensating controls only if formally risk-assessed and time-bound, and document exceptions (none are currently present in the dataset).

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


#### HIGH: High authentication failure rate (~54.7%) indicates persistent login issues and/or brute-force attempts

Authentication failures are extremely frequent: 3,500,337 total failures with 2,899,642 successes, yielding a fail rate of 54.69%. This level of failure can indicate brute-force activity, credential stuffing, misconfiguration (e.g., incorrect password policies or identity provider issues), or widespread user authentication errors. Even though the metric set reports 0 attack IP attempts and 0 account takeovers, the failure volume is high enough to warrant investigation and tighter detection/response.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5469 (54.69%)

- baseline_value: 0.5408 (54.08%)

- deviation: +0.09 percentage points (slight increase vs baseline period)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent authentication failures reflect inadequate control effectiveness and/or insufficient monitoring and response to security events affecting access to network and information systems.



**Recommendation:** Investigate top failure sources and authentication flows: (1) review the top IPs generating failures (e.g., 23.137.225.33: 63,681; 158.149.114.95: 21,443; 10.0.181.232: 14,249) for malicious patterns and NAT/proxy behavior, (2) validate rate limiting, lockout/throttling, and bot protections, (3) ensure alerting on abnormal failure rates and credential-stuffing indicators, and (4) check for identity provider misconfiguration causing legitimate failures. Produce a remediation plan with measurable targets (e.g., reduce fail rate by X% within Y days).

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


#### HIGH: Privileged access governance data missing: 0 admins recorded and no last review date

The dataset reports 0 admins and 0 admins with MFA, with last_review_date marked as 'unknown'. This suggests either (a) privileged accounts are not being tracked in the telemetry used for compliance reporting, or (b) privileged access is not properly governed. Under NIS2, organizations must ensure appropriate security measures and governance for access to systems, especially for privileged roles.


**Evidence:**

- metric: admins.count

- current_value: 0

- baseline_value: 0

- deviation: No change; however, last_review_date is 'unknown' and admin population is not verifiable




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of verifiable privileged access governance and review evidence undermines the ability to demonstrate appropriate security measures for access control.



**Recommendation:** Reconcile privileged account inventory: ensure all admin/privileged roles are correctly identified in the reporting source of truth. Establish and record a recurring privileged access review cadence (e.g., monthly/quarterly) and populate last_review_date. Enforce MFA for all privileged accounts (and verify via telemetry).

---


#### MEDIUM: Large scale of authentication events with no detected takeovers may indicate detection blind spots

Despite very high authentication failure volume (3,500,337 failures), the dataset reports 0 account takeovers and 0 users with takeover, and 0 attack IP attempts. This could be accurate, but it also may indicate that takeover detection logic is not aligned with the observed authentication patterns or that relevant signals are not being ingested. This is important because compliance requires not only prevention but also detection and response capability.


**Evidence:**

- metric: auth_failures.account_takeovers

- current_value: 0

- baseline_value: 0

- deviation: No change; potential mismatch with high failure volume (54.69% fail rate)




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): If detection is ineffective or incomplete, the organization may not adequately identify and respond to security incidents affecting access to network and information systems.



**Recommendation:** Validate and test detection coverage: run tabletop exercises and/or controlled simulations to confirm that credential-stuffing and takeover scenarios generate the expected alerts/metrics. Review detection rules, data sources, and thresholds used to populate 'attack_ip_attempts' and 'account_takeovers'. Ensure correlation between authentication failures, successful logins, and anomalous account behavior.

---




### Positive Observations

- Authentication activity is being measured at scale (6,399,979 frame rows; 1,510,016 distinct users; 1,251,718 distinct source IPs), providing a basis for investigation and monitoring.

- No account takeovers are currently flagged (0 users with takeover), suggesting either limited successful compromise or (more likely) detection/telemetry gaps that should be validated.




### Trend Analysis


**Degrading:** Authentication failure rate slightly increased from 54.08% (baseline 2020-02-05) to 54.69% (current 2020-05-05 window), indicating worsening or persistent authentication friction.


**Stable:** MFA coverage remains at 0.0% (enabled_users = 0) across current and baseline periods., No account takeovers and no attack IP attempts are recorded (0/0) in both current and baseline periods.





## Compliance Observations
## Access-control compliance (Article 21)

- The entity shall implement access control policies as part of human resources security and asset management measures. [NIS2 Art. 21(2)(i)]

- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [NIS2 Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1510016). [METRICS mfa]

- Administrators count is 0; administrators with MFA is 0; last_review_date is “unknown”. [METRICS admins]

- Authentication failures total 3,500,337 with success_total 2,899,642 (fail_rate 0.5469). [METRICS auth_failures]

- No data indicates account takeovers (account_takeovers: 0; users_with_takeover: 0). [METRICS auth_failures]

- No data indicates attack IP attempts or distinct attack IPs (attack_ip_attempts: 0; attack_ip_distinct_ips: 0). [METRICS auth_failures]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures