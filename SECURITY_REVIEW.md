# Security & Quality Review - Ecclesia Core

**Date:** 2026-02-14
**Reviewer:** Security Review Agent
**Version:** 0.1.0 (MVP)
**Environment:** Development → Production Readiness Assessment

---

## Executive Summary

### Overall Assessment: **MEDIUM RISK** ⚠️

The Ecclesia Core system demonstrates **good security fundamentals** with proper authentication, password hashing, and basic access controls. However, several **critical and high-priority issues** must be addressed before production deployment, particularly around:

- Missing input validation for CPF format
- Lack of rate limiting protection
- CORS configuration set to allow all origins
- Missing security headers
- Incomplete LGPD compliance mechanisms
- Authentication endpoint mismatch (login expects JSON but receives form data)

### Issue Count Summary

| Severity | Count | Status |
|----------|-------|--------|
| **Critical** | 3 | Must fix before production |
| **High** | 8 | Should fix before production |
| **Medium** | 12 | Consider fixing |
| **Low** | 6 | Nice to have |

---

## Critical Findings (Must Fix Before Production)

### 1. ⚠️ CORS Policy Too Permissive
**Severity:** Critical
**File:** `/home/th_faria/ecclesia-core/backend/app/main.py:20-26`

**Issue:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← Accepts requests from ANY domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Risk:** This allows any website to make authenticated requests to your API, enabling Cross-Site Request Forgery (CSRF) and data theft attacks.

**Recommendation:**
```python
# For production
allow_origins=[
    "https://ecclesia.suaparoquia.com.br",  # Production domain
    "https://admin.ecclesia.suaparoquia.com.br"  # Admin domain if separate
]

# Or use environment variable
allow_origins=settings.ALLOWED_ORIGINS.split(",")
```

### 2. ⚠️ Default SECRET_KEY in Code
**Severity:** Critical
**File:** `/home/th_faria/ecclesia-core/backend/app/config.py:15`

**Issue:**
```python
SECRET_KEY: str = "your-secret-key-change-in-production"
```

**Risk:** If the `.env` file is missing, the application falls back to this hardcoded weak secret, compromising all JWT tokens.

**Recommendation:**
- Remove default value
- Make SECRET_KEY required at startup
- Add validation to ensure it's changed from default
```python
SECRET_KEY: str  # No default - will fail if not set

def __init__(self, **kwargs):
    super().__init__(**kwargs)
    if self.SECRET_KEY == "your-secret-key-change-in-production":
        raise ValueError("SECRET_KEY must be changed from default value!")
    if len(self.SECRET_KEY) < 32:
        raise ValueError("SECRET_KEY must be at least 32 characters!")
```

### 3. ⚠️ No Rate Limiting Protection
**Severity:** Critical
**File:** All API endpoints

**Issue:** No rate limiting implemented on authentication or any other endpoints.

**Risk:**
- Brute-force password attacks on `/api/auth/login`
- API abuse and DoS attacks
- Resource exhaustion

**Recommendation:**
Implement rate limiting using `slowapi` or similar:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# On login endpoint
@limiter.limit("5/minute")
@router.post("/login")
async def login(...):
```

---

## High Priority Findings (Should Fix Before Production)

### 4. Missing CPF Validation
**Severity:** High
**File:** `/home/th_faria/ecclesia-core/backend/app/schemas/dizimista.py:13,31`

**Issue:** CPF field accepts any string up to 14 characters without format or checksum validation.

**Risk:**
- Invalid CPF data in database
- Duplicate members with typos in CPF
- Difficulty in data analysis and reporting

**Recommendation:**
Add CPF validation with checksum algorithm:
```python
from pydantic import field_validator
import re

@field_validator("cpf")
@classmethod
def validate_cpf(cls, v: Optional[str]) -> Optional[str]:
    if v is None or v == "":
        return None

    # Remove formatting
    cpf = re.sub(r'[^0-9]', '', v)

    # Check length
    if len(cpf) != 11:
        raise ValueError("CPF deve ter 11 dígitos")

    # Check for repeated digits
    if cpf == cpf[0] * 11:
        raise ValueError("CPF inválido")

    # Validate checksum (implement CPF algorithm)
    # ... validation logic ...

    return v  # Return formatted version
```

### 5. Missing Email Validation on Backend
**Severity:** High
**File:** `/home/th_faria/ecclesia-core/backend/app/schemas/dizimista.py:15`

**Issue:** Email field uses `Optional[str]` instead of `Optional[EmailStr]`.

**Risk:** Invalid email addresses stored in database.

**Recommendation:**
```python
email: Optional[EmailStr] = Field(None, description="Email do dizimista")
```

### 6. SQL Injection Risk in Search Queries
**Severity:** High
**File:** `/home/th_faria/ecclesia-core/backend/app/services/dizimista_service.py:52-60`

**Issue:** While using SQLAlchemy ORM (which is generally safe), the `ilike()` function with user input needs verification.

**Current Code:**
```python
search_term = f"%{search}%"
query = query.filter(
    or_(
        Dizimista.nome.ilike(search_term),
        Dizimista.telefone.ilike(search_term),
        Dizimista.email.ilike(search_term),
    )
)
```

**Assessment:** Actually **SAFE** - SQLAlchemy properly parameterizes queries.

**Recommendation:** Add input sanitization as defense-in-depth:
```python
# Limit search term length
if len(search) > 100:
    raise ValueError("Termo de busca muito longo")

# Remove SQL wildcards from user input to prevent wildcard injection
search = search.replace('%', '').replace('_', '')
search_term = f"%{search}%"
```

### 7. Missing HTTPS Enforcement
**Severity:** High
**File:** Configuration/Infrastructure

**Issue:** No explicit HTTPS redirect or enforcement in application.

**Risk:**
- Credentials transmitted in clear text
- Man-in-the-middle attacks
- Session hijacking

**Recommendation:**
Add middleware for HTTPS redirect in production:
```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if settings.ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
```

### 8. Weak Password Policy
**Severity:** High
**File:** `/home/th_faria/ecclesia-core/backend/app/schemas/usuario.py:21`

**Issue:** Minimum password length is only 8 characters with no complexity requirements.

**Risk:** Weak passwords vulnerable to brute-force attacks.

**Recommendation:**
```python
from pydantic import field_validator

@field_validator("senha")
@classmethod
def validate_senha(cls, v: str) -> str:
    if len(v) < 12:
        raise ValueError("Senha deve ter no mínimo 12 caracteres")

    if not re.search(r'[A-Z]', v):
        raise ValueError("Senha deve conter ao menos uma letra maiúscula")

    if not re.search(r'[a-z]', v):
        raise ValueError("Senha deve conter ao menos uma letra minúscula")

    if not re.search(r'[0-9]', v):
        raise ValueError("Senha deve conter ao menos um número")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
        raise ValueError("Senha deve conter ao menos um caractere especial")

    return v
```

### 9. Token Expiration Too Long
**Severity:** High
**File:** `/home/th_faria/ecclesia-core/backend/.env.example:7`

**Issue:** Default token expiration is 30 minutes, which may be too long for a financial system.

**Recommendation:**
- Reduce to 15 minutes for standard tokens
- Implement refresh tokens for longer sessions
- Add token revocation list for logout

### 10. Missing Security Headers
**Severity:** High
**File:** `/home/th_faria/ecclesia-core/backend/app/main.py`

**Issue:** No security headers configured (X-Frame-Options, X-Content-Type-Options, CSP, etc.).

**Risk:**
- Clickjacking attacks
- MIME-sniffing attacks
- XSS vulnerabilities

**Recommendation:**
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# Add trusted host middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["ecclesia.suaparoquia.com.br"])
```

### 11. Frontend Token Storage in localStorage
**Severity:** High
**File:** `/home/th_faria/ecclesia-core/frontend/src/services/api.ts:14,30-31`

**Issue:** JWT tokens stored in localStorage are vulnerable to XSS attacks.

**Risk:** If an XSS vulnerability exists anywhere in the app, attackers can steal authentication tokens.

**Recommendation:**
- Use httpOnly cookies for token storage (requires backend changes)
- If localStorage is necessary, implement additional XSS protections
- Add Content Security Policy headers
- Sanitize all user inputs displayed in UI

---

## Medium Priority Findings (Consider Fixing)

### 12. Missing Audit Trail
**Severity:** Medium
**File:** All models

**Issue:** No audit logging for sensitive operations (who created/modified financial records).

**Risk:** Lack of accountability and forensics capability.

**Recommendation:**
Add audit fields to critical models:
```python
criado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
atualizado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
```

### 13. No Email Verification
**Severity:** Medium
**File:** User registration flow

**Issue:** Email addresses are not verified.

**Risk:** Invalid contact information, potential for account takeover.

**Recommendation:** Implement email verification flow for user registration.

### 14. Missing Input Length Validation
**Severity:** Medium
**File:** Multiple schema files

**Issue:** Text fields like `observacoes` and `endereco` have no maximum length.

**Risk:**
- Database storage abuse
- DoS through large payloads

**Recommendation:**
```python
observacoes: Optional[str] = Field(None, max_length=1000, description="...")
endereco: Optional[str] = Field(None, max_length=500, description="...")
```

### 15. Timestamp Uses `datetime.utcnow()` (Deprecated)
**Severity:** Medium
**File:** `/home/th_faria/ecclesia-core/backend/app/auth/utils.py:57,59`

**Issue:** Using deprecated `datetime.utcnow()` instead of timezone-aware datetime.

**Recommendation:**
```python
from datetime import datetime, timezone

expire = datetime.now(timezone.utc) + expires_delta
```

### 16. No Database Connection Pooling Configuration
**Severity:** Medium
**File:** `/home/th_faria/ecclesia-core/backend/app/database.py:11-15`

**Issue:** No explicit pool size configuration.

**Recommendation:**
```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,          # Maximum connections
    max_overflow=20,        # Additional connections when pool is full
    pool_recycle=3600,      # Recycle connections after 1 hour
    echo=settings.DEBUG
)
```

### 17. Missing Transaction Rollback in Error Cases
**Severity:** Medium
**File:** Service layer functions

**Issue:** Some service functions don't explicitly handle transaction rollback on errors.

**Current:** Relying on FastAPI's dependency cleanup.

**Recommendation:** Add explicit error handling:
```python
try:
    # operations
    db.commit()
except Exception as e:
    db.rollback()
    raise
```

### 18. No Soft Delete Verification Before Hard Operations
**Severity:** Medium
**File:** Contribution deletion

**Issue:** Contributions can be permanently deleted without soft delete option.

**Risk:** Accidental data loss.

**Recommendation:** Implement soft delete for contributions similar to dizimistas.

### 19. Missing Password Change Endpoint
**Severity:** Medium
**File:** Auth router

**Issue:** No endpoint for users to change their own password.

**Risk:** Security best practice violation.

**Recommendation:** Add password change endpoint with old password verification.

### 20. Date Range Validation Missing Upper Bound
**Severity:** Medium
**File:** `/home/th_faria/ecclesia-core/backend/app/routers/reports.py:71-75`

**Issue:** Only validates start_date < end_date, but allows future dates.

**Risk:** Confusing reports with invalid date ranges.

**Recommendation:**
```python
from datetime import date

if start_date > date.today():
    raise HTTPException(400, "Data de início não pode ser futura")

if (end_date - start_date).days > 365:
    raise HTTPException(400, "Período máximo é de 1 ano")
```

### 21. No Request Size Limit
**Severity:** Medium
**File:** FastAPI configuration

**Issue:** No explicit request body size limit.

**Risk:** DoS attacks with large payloads.

**Recommendation:**
```python
from fastapi import Request

app = FastAPI(
    title=settings.APP_NAME,
    # ... other config
)

@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 10_000_000:  # 10MB
        return JSONResponse(
            status_code=413,
            content={"detail": "Request too large"}
        )
    return await call_next(request)
```

### 22. Frontend API URL Hardcoded
**Severity:** Medium
**File:** `/home/th_faria/ecclesia-core/frontend/.env:1`

**Issue:** Production builds might use localhost URL if not properly configured.

**Risk:** Application won't work in production.

**Recommendation:** Ensure build process validates API URL configuration.

### 23. Error Messages May Leak Information
**Severity:** Medium
**File:** Various routers

**Issue:** Some error messages might be too detailed for production.

**Example:** Database integrity errors expose schema information.

**Recommendation:**
- Use generic error messages in production
- Log detailed errors server-side only
- Implement error monitoring (Sentry, etc.)

---

## Low Priority Findings (Nice to Have)

### 24. No API Versioning
**Severity:** Low
**File:** API routing

**Issue:** No version prefix on API routes.

**Recommendation:** Use `/api/v1/` prefix for future-proofing.

### 25. Missing Request ID Tracking
**Severity:** Low
**File:** Logging infrastructure

**Issue:** No correlation ID for request tracing.

**Recommendation:** Add request ID middleware for better debugging.

### 26. No Health Check Details
**Severity:** Low
**File:** `/home/th_faria/ecclesia-core/backend/app/main.py:29-38`

**Issue:** Health check doesn't verify database connectivity.

**Recommendation:**
```python
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test DB connection
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    return {
        "status": "ok" if db_status == "healthy" else "degraded",
        "database": db_status,
        "version": settings.APP_VERSION
    }
```

### 27. No Pagination Limit Enforcement
**Severity:** Low
**File:** Pagination endpoints

**Issue:** While page_size has max of 100, this could still be optimized.

**Recommendation:** Consider reducing max page size to 50 for better performance.

### 28. Missing Index on Foreign Keys
**Severity:** Low
**File:** Database models

**Assessment:** Most foreign keys already have indexes.

**Recommendation:** Verify with `EXPLAIN ANALYZE` on common queries.

### 29. No Database Backup Strategy Documented
**Severity:** Low
**File:** Documentation

**Issue:** No documented backup/restore procedures.

**Recommendation:** Add backup strategy to operations documentation.

---

## LGPD (Brazilian Data Protection Law) Compliance

### Status: **PARTIALLY COMPLIANT** ⚠️

| Requirement | Status | Notes |
|------------|--------|-------|
| **Data Minimization** | ✅ Good | Only essential data collected |
| **Purpose Limitation** | ✅ Good | Data used only for tithing management |
| **Consent** | ❌ Missing | No explicit consent mechanism |
| **Right to Access** | ⚠️ Partial | Users can view their data, but no export feature |
| **Right to Deletion** | ⚠️ Partial | Soft delete exists, but no complete erasure process |
| **Right to Rectification** | ✅ Good | Update functionality exists |
| **Data Portability** | ❌ Missing | No data export in structured format |
| **Security Measures** | ⚠️ Partial | Basic security, needs improvements per this review |
| **Data Breach Protocol** | ❌ Missing | No documented incident response |
| **Privacy Policy** | ❌ Missing | No privacy policy or terms |
| **Data Retention Policy** | ❌ Missing | No defined retention periods |
| **DPO Designation** | N/A | Required only if high-risk processing |

### LGPD Recommendations

#### Must Implement:
1. **Consent Mechanism**
   - Add terms acceptance on dizimista registration
   - Log consent timestamp and purpose
   - Allow consent withdrawal

2. **Data Export (Portability)**
   ```python
   @router.get("/dizimista/{id}/export")
   async def export_dizimista_data(id: int, ...):
       # Return JSON/CSV with all dizimista data
       # Include contributions, personal info
   ```

3. **Complete Data Deletion**
   ```python
   @router.delete("/dizimista/{id}/gdpr-delete")
   async def complete_deletion(id: int, ...):
       # Anonymize or completely remove PII
       # Keep financial records but anonymize
       # Log deletion for audit
   ```

4. **Privacy Policy & Terms**
   - Create privacy policy document
   - Add acceptance checkbox on registration
   - Store acceptance records

5. **Data Breach Response Plan**
   - Document notification procedures
   - Define incident response team
   - Prepare communication templates

6. **Data Retention Policy**
   - Define how long to keep dizimista records
   - Implement automated archival/deletion
   - Balance with financial record-keeping requirements

#### Good to Have:
- Data access logging (who accessed whose data when)
- Enhanced encryption for sensitive fields (CPF)
- Regular privacy impact assessments
- Staff training on data protection

---

## Positive Findings (Good Practices) ✅

The following security practices are **well implemented**:

1. **Strong Password Hashing** - Using bcrypt with proper salt
2. **JWT Token Authentication** - Proper implementation with expiration
3. **Role-Based Access Control** - Admin and Operator roles properly enforced
4. **SQL Injection Protection** - Using SQLAlchemy ORM (parameterized queries)
5. **Soft Delete Pattern** - Prevents accidental data loss for dizimistas
6. **Input Validation** - Pydantic schemas provide good type safety
7. **Environment Variables** - Secrets managed via .env (not committed)
8. **Database Constraints** - Proper foreign keys and unique constraints
9. **Timestamps** - Audit trail via created_at/updated_at
10. **Error Handling** - Consistent HTTP status codes and error messages
11. **API Documentation** - Swagger/OpenAPI auto-generated
12. **Test Coverage** - Comprehensive test suite for core functionality
13. **Docker Containerization** - Reproducible development environment
14. **Database Migrations** - Alembic for version-controlled schema changes
15. **Inactive User Check** - Authentication validates user is active

---

## Production Readiness Checklist

### Security (Must Complete Before Production)

- [ ] **Critical #1:** Configure CORS to specific domain(s)
- [ ] **Critical #2:** Enforce non-default SECRET_KEY with validation
- [ ] **Critical #3:** Implement rate limiting on auth endpoints
- [ ] **High #4:** Add CPF format and checksum validation
- [ ] **High #5:** Fix email validation in dizimista schema
- [ ] **High #7:** Enable HTTPS enforcement
- [ ] **High #8:** Strengthen password policy
- [ ] **High #9:** Reduce token expiration time
- [ ] **High #10:** Add security headers middleware
- [ ] **High #11:** Review token storage strategy (consider httpOnly cookies)

### LGPD Compliance (Must Complete Before Production)

- [ ] Create and publish Privacy Policy
- [ ] Implement consent mechanism for data collection
- [ ] Add data export endpoint (portability)
- [ ] Implement complete data deletion workflow
- [ ] Document data breach response plan
- [ ] Define and implement data retention policy

### Operations (Recommended Before Production)

- [ ] Set up monitoring and alerting
- [ ] Configure automated backups
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Implement logging aggregation
- [ ] Create runbook for common operations
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Implement database connection pooling
- [ ] Add health check with DB verification
- [ ] Set up CI/CD pipeline
- [ ] Performance testing and optimization
- [ ] Load testing

### Documentation (Recommended)

- [ ] API documentation review and updates
- [ ] User manual in Portuguese
- [ ] Administrator guide
- [ ] Disaster recovery procedures
- [ ] Security incident response plan

---

## Testing Recommendations

### Security Testing Needed:

1. **Penetration Testing**
   - Authentication bypass attempts
   - SQL injection testing
   - XSS vulnerability scanning
   - CSRF testing

2. **Password Security**
   - Brute force resistance
   - Password reset flow security
   - Session management testing

3. **Authorization Testing**
   - Privilege escalation attempts
   - Cross-user data access attempts
   - API endpoint authorization checks

4. **Input Validation**
   - Fuzzing with malformed inputs
   - Boundary value testing
   - SQL/XSS injection attempts

5. **Infrastructure**
   - Port scanning
   - SSL/TLS configuration review
   - Docker security audit

---

## Risk Matrix

| Finding | Severity | Exploitability | Impact | Priority |
|---------|----------|----------------|--------|----------|
| CORS Allow All | Critical | High | High | P0 |
| Default SECRET_KEY | Critical | Medium | Critical | P0 |
| No Rate Limiting | Critical | High | High | P0 |
| CPF Validation | High | Low | Medium | P1 |
| HTTPS Enforcement | High | Medium | High | P1 |
| Weak Password Policy | High | Medium | High | P1 |
| Security Headers | High | Low | Medium | P1 |
| Token in localStorage | High | Medium | High | P1 |
| Audit Trail | Medium | Low | Medium | P2 |
| LGPD Consent | Medium | Low | High | P2 |

**Priority Levels:**
- **P0 (Critical):** Must fix before any production deployment
- **P1 (High):** Should fix before production, acceptable for staging
- **P2 (Medium):** Plan to fix within first month of production
- **P3 (Low):** Consider for future iterations

---

## Summary & Recommendations

### Overall Security Posture: **MEDIUM** ⚠️

The Ecclesia Core system has a **solid foundation** with proper authentication, authorization, and input validation through Pydantic schemas. The use of modern frameworks (FastAPI, React) and best practices (JWT, bcrypt, ORM) demonstrates good security awareness.

However, **critical production-readiness gaps** exist:

### Immediate Actions Required (Before Production):

1. **Fix CORS configuration** - This is a critical security flaw
2. **Enforce strong SECRET_KEY** - Add validation to prevent default key
3. **Implement rate limiting** - Protect against brute force attacks
4. **Add security headers** - Basic web security hygiene
5. **Enable HTTPS** - Essential for financial data protection
6. **Implement LGPD compliance** - Legal requirement in Brazil

### Recommended Timeline:

- **Week 1:** Address all Critical findings (#1-3)
- **Week 2:** Address High Priority security findings (#4-11)
- **Week 3:** Implement LGPD compliance mechanisms
- **Week 4:** Address Medium Priority findings and testing
- **Ongoing:** Low priority improvements and monitoring

### Investment vs. Risk:

The fixes required are **relatively straightforward** and mostly involve:
- Configuration changes (CORS, headers)
- Adding middleware (rate limiting, security headers)
- Schema validation enhancements (CPF, password)
- LGPD compliance workflows (consent, export, deletion)

**Estimated effort:** 2-3 weeks of development for all Critical and High priority items.

**Risk of not fixing:** Potential data breaches, legal non-compliance (LGPD fines up to 2% of revenue), reputational damage to church.

### Final Verdict:

**DO NOT DEPLOY TO PRODUCTION** until Critical and High Priority security issues are resolved and LGPD compliance mechanisms are in place.

---

## Contact & Support

For questions about this security review:
- Review Date: 2026-02-14
- Version Reviewed: 0.1.0 (MVP)
- Next Review Recommended: After implementing fixes, before production deployment

---

**Document Classification:** Internal Use
**Last Updated:** 2026-02-14
