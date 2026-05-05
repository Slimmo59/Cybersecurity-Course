# ⚠️ Limitations

## Visibility Constraints

- Full detection requires root privileges
- Some processes may restrict access to their file descriptors

---

## Kernel-Level Threats

- Advanced rootkits may hide from `/proc/modules`
- Kernel manipulation can bypass user-space detection

---

## False Positives

- Legitimate processes (e.g. input drivers, desktop services) may access `/dev/input/`
- Keyword-based detection may flag benign processes

---

## Detection Scope

This tool focuses on:

- Behavioral indicators
- Basic anomaly detection

It does NOT provide:

- Signature-based detection
- Memory analysis
- Network correlation

---

## Conclusion

This script is intended as a learning tool and a baseline for understanding input monitoring detection, not as a production-grade security solution.
