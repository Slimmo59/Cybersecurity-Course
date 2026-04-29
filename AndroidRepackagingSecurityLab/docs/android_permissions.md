# 🔐 Android Permission Model

Android uses a permission-based security model to control access to sensitive resources.

---

## 📌 Common Permissions

### 🌐 INTERNET

Allows the application to open network sockets.

```xml
<uses-permission android:name="android.permission.INTERNET"/>
```

---

### 📡 ACCESS_NETWORK_STATE

Allows the app to check network connectivity status.

```xml
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
```

---

## 🔍 Why Permissions Matter

Permissions define what an application is allowed to do.

When modifying an APK, changing permissions can:

* Enable network communication
* Allow data exfiltration
* Expand attack surface

---

## 🛡️ Security Risks

* Over-permissioned apps increase risk
* Users often ignore permission prompts
* Malicious apps may request unnecessary permissions

---

## 📱 Android 12 Considerations

* Stricter permission controls
* Runtime permission enforcement
* Increased visibility for users

---

## 🔐 Defensive Perspective

To reduce risk:

* Install apps only from trusted sources
* Review requested permissions carefully
* Use security tools (Play Protect, MDM solutions)

---

## 🧠 Key Takeaway

Permissions are a critical part of Android security.

Understanding them helps:

* Detect suspicious behavior
* Analyze modified applications
* Improve mobile security awareness
