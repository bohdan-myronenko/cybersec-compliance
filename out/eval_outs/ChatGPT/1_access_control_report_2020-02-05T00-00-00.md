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


During the 90-day window ending 2020-02-05, the environment shows a severe NIS2-relevant authentication control gap: MFA is not enabled for any of 1,536,866 users (0% coverage), including zero MFA-protected administrators. At the same time, authentication failures are extremely high (3,543,216 total failures with a 54.08% failure rate), indicating persistent unsuccessful authentication attempts across 1,328,745 distinct source IPs. While no account takeovers or “attack IP attempts” are detected in the computed metrics, the combination of zero MFA coverage and high failure volume represents a critical compliance and risk posture under NIS2’s requirements for appropriate technical and organizational measures to secure network and information systems.


### Security Findings


#### CRITICAL: MFA not enabled for any users (0% coverage)

Multi-factor authentication (MFA) is completely disabled across the user base. This is a direct control failure for protecting access to network and information systems, especially for remote or privileged access. The issue is systemic (0 enabled users) and therefore likely to affect both confidentiality and integrity by increasing the likelihood and impact of credential compromise.


**Evidence:**

- metric: mfa.coverage_pct

- current_value: 0.0%

- baseline_value: 0.0% (2019-11-07), 0.0% (2021-01-30)

- deviation: No improvement; remains at 0% across observed periods




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Failure to implement appropriate measures to secure access (e.g., MFA) undermines the obligation to ensure security of network and information systems and access control.



**Recommendation:** Implement MFA enforcement immediately: (1) enable MFA for all users, starting with administrators and high-risk roles; (2) require MFA for all interactive logins and privileged actions; (3) add a monitoring rule to alert on any account without MFA; (4) document rollout timeline and exceptions process (with approval and compensating controls).

---


#### CRITICAL: No MFA for administrators (privileged access not protected)

The computed metrics indicate there are 0 administrators with MFA enabled (admins.count=0, with_mfa=0). Even if the admin count is mis-modeled, the effective outcome is that privileged access is not demonstrably protected by MFA, which is a high-impact access control weakness.


**Evidence:**

- metric: admins.with_mfa

- current_value: 0

- baseline_value: 0 (2019-11-07), 0 (2021-01-30)

- deviation: No improvement; privileged MFA coverage remains absent




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Lack of strong authentication for privileged access fails to meet expectations for appropriate access security measures.



**Recommendation:** Verify admin inventory and enforce MFA for all privileged accounts: (1) reconcile the source of truth for admin accounts (admins.count=0 may indicate telemetry/config issue); (2) ensure every privileged account is included in MFA coverage reporting; (3) enforce MFA for admin roles and break-glass accounts with additional controls (IP allowlisting, hardware-backed MFA, and separate monitoring).

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


#### HIGH: High authentication failure rate across large source-IP footprint

Authentication failures are very high: 3,543,216 total failures with 3,008,918 successful authentications, yielding a 54.08% failure rate. Failures are distributed across 1,328,745 distinct source IPs, suggesting widespread unsuccessful login attempts (e.g., credential stuffing, misconfiguration, or brute-force attempts). Although computed metrics show no detected account takeovers, the failure volume combined with zero MFA coverage materially increases the probability of successful credential compromise.


**Evidence:**

- metric: auth_failures.fail_rate

- current_value: 0.5408 (54.08%)

- baseline_value: 0.5069 (50.69%) on 2019-11-07; 0.6421 (64.21%) on 2021-01-30

- deviation: Current failure rate is higher than 2019-11-07 by ~3.39 percentage points; lower than 2021-01-30 by ~10.13 percentage points




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Persistent authentication failures indicate insufficient protective measures and may reflect inadequate detection/response and access security controls.



**Recommendation:** Triage and reduce failed authentication attempts: (1) identify top offending IPs and correlate with user accounts targeted; top IPs include 158.149.114.95 (12,584 attempts) and 10.0.181.227 (10,967 attempts); (2) implement rate limiting, progressive delays, and lockout/step-up controls for repeated failures; (3) deploy credential-stuffing protections (e.g., bot detection, impossible travel checks, and MFA step-up on risk); (4) ensure incident detection rules are in place for spikes in failure rate and distributed sources.

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


#### MEDIUM: Potential telemetry/logic gap: no detected attack IP attempts or account takeovers despite high failure volume

The metrics report attack_ip_attempts=0 and account_takeovers=0, users_with_takeover=0. Given the extremely high failure volume and broad source-IP distribution, this may indicate that the detection logic for attacks and takeovers is not capturing relevant events, or that the environment is experiencing unsuccessful attempts without successful compromise. Either way, the lack of detected outcomes reduces confidence in monitoring coverage.


**Evidence:**

- metric: auth_failures.attack_ip_attempts / account_takeovers

- current_value: 0 / 0

- baseline_value: 0 / 0 (2019-11-07), 0 / 0 (2021-01-30)

- deviation: No change; detection signals remain absent across periods




**Compliance Impact:**

- **NIS2** (Article 21.2(i)): Inadequate detection/monitoring of security events can undermine the effectiveness of security measures required for NIS2.



**Recommendation:** Validate and improve detection logic: (1) review how “attack_ip_attempts” and “account_takeovers” are defined; (2) run a backtest using known indicators (e.g., high-velocity failures, anomalous geo/IP changes, session anomalies) to confirm the pipeline can detect takeovers; (3) ensure correlation between failed logins, successful logins, and sensitive actions is implemented; (4) document monitoring coverage and limitations for compliance evidence.

---




### Positive Observations

- No account takeovers are detected in the computed metrics (account_takeovers=0; users_with_takeover=0), which may indicate that despite high failure rates, successful compromise is not being observed by current detection logic.

- Failure rate is not at the highest historical level: current fail_rate=54.08% is lower than 2021-01-30 (64.21%), suggesting some improvement versus that later baseline point.




### Trend Analysis

**Improving:** Authentication failure rate is lower than the 2021-01-30 baseline (54.08% vs 64.21%), indicating fewer failures relative to successes than in that later period.


**Degrading:** Authentication failure rate is higher than the 2019-11-07 baseline (54.08% vs 50.69%), indicating increased unsuccessful authentication activity compared to that earlier period.


**Stable:** MFA coverage remains at 0.0% across observed periods (2019-11-07, current window, and 2021-01-30)., No detected attack IP attempts or account takeovers across observed periods (all reported as 0).





## Compliance Observations
### Access-control compliance (Article 21)

- The entity shall implement access control policies and asset management as part of cybersecurity risk-management measures. [article_21_cybersecurity_risk-management_measures Art. 21(2)(i)]

- The entity shall use multi-factor authentication or continuous authentication solutions, where appropriate. [article_21_cybersecurity_risk-management_measures Art. 21(2)(j)]

- MFA coverage is 0.0% (enabled_users: 0 of total_users: 1536866). [METRICS JSON mfa]

- Administrators count is 0; administrators with MFA is 0; last_review_date is “unknown”. [METRICS JSON admins]

- Authentication failures total 3,543,216 with success_total 3,008,918; fail_rate is 0.5408. [METRICS JSON auth_failures]

- Top IPs with authentication failures include 158.149.114.95 (12,584) and 10.0.181.227 (10,967). [METRICS JSON auth_failures.top_ips]

- No data indicates account takeovers (account_takeovers: 0; users_with_takeover: 0). [METRICS JSON auth_failures]

## Legal Context Provided
- article_21_cybersecurity_risk-management_measures