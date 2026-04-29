# 🔧 Smali Basics

Smali is a human-readable representation of Android's Dalvik bytecode.

It is used during reverse engineering to inspect and modify application logic.

---

## 📌 Example

```smali
invoke-virtual {p0}, Ljava/lang/String;->length()I
```

### Explanation:

* `invoke-virtual` → method call
* `{p0}` → register (parameter reference)
* `Ljava/lang/String;` → class reference
* `length()` → method
* `I` → return type (integer)

---

## 🧠 Key Concepts

### Registers

* Used instead of variables
* Example: `p0`, `v0`, `v1`

---

### Methods

Defined using:

```smali
.method public exampleMethod()V
```

---

### Return Types

* `V` → void
* `I` → integer
* `Z` → boolean
* `Ljava/lang/String;` → string

---

## 🔍 Why It Matters

Understanding Smali allows:

* Analysis of application logic
* Identification of execution flow
* Detection of injected or modified code

---

## ⚠️ Security Insight

Smali modification is commonly used in:

* Application repackaging
* Code injection
* Mobile malware development

This makes reverse engineering a key skill in mobile security.
