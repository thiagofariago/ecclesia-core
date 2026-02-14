# Ecclesia Core - Product Backlog

**Last Updated:** 2026-02-14
**Version:** 0.1.0 (MVP Complete)

---

## Introduction

This backlog contains planned features and enhancements for future iterations of Ecclesia Core. Items are prioritized by business value and organized by theme.

**Prioritization:**
- **P0 (Critical):** Blocks production use or serious security risk
- **P1 (High):** High business value, should do next
- **P2 (Medium):** Nice to have, moderate value
- **P3 (Low):** Future consideration, low urgency

**Effort Estimates:**
- **S (Small):** 1-2 days
- **M (Medium):** 3-5 days
- **L (Large):** 1-2 weeks
- **XL (Extra Large):** 2+ weeks

---

## Security & Compliance

### P1 - LGPD Consent Mechanism
**Priority:** P1 (High)
**Effort:** M
**Description:** Implement explicit consent collection when registering dizimistas.

**Acceptance Criteria:**
- [ ] Consent checkbox on dizimista registration form
- [ ] Consent status stored in database (consented_at timestamp)
- [ ] Consent text displays privacy policy link
- [ ] Backend validation ensures consent is given before data processing
- [ ] Audit log of consent events

**Technical Notes:**
- Add `lgpd_consent` and `lgpd_consented_at` fields to Dizimista model
- Create migration
- Update frontend form
- Create privacy policy page (separate P2 task)

---

### P1 - Data Export (LGPD Portability)
**Priority:** P1 (High)
**Effort:** M
**Description:** Allow dizimistas to export their personal data.

**Acceptance Criteria:**
- [ ] API endpoint: GET /api/dizimistas/{id}/export (admin or self)
- [ ] Export format: JSON or CSV
- [ ] Includes: personal info, contribution history, audit logs
- [ ] Frontend button: "Exportar Meus Dados"
- [ ] Admin can export any dizimista data
- [ ] Dizimista can request own data (future: self-service portal)

**Technical Notes:**
- Create export service in backend
- Generate CSV/JSON with all personal data
- Add route and permission checks
- Frontend download button

---

### P1 - Complete Data Deletion (LGPD Right to Erasure)
**Priority:** P1 (High)
**Effort:** M
**Description:** Implement hard delete option for dizimistas upon request.

**Acceptance Criteria:**
- [ ] API endpoint: DELETE /api/dizimistas/{id}/hard-delete (admin only)
- [ ] Anonymize instead of delete if contributions exist (preserve financial records)
- [ ] Option to anonymize: replace name with "Anônimo [ID]", clear CPF, email, phone
- [ ] Confirmation modal with warning
- [ ] Audit log entry for deletion/anonymization

**Technical Notes:**
- Current DELETE does soft delete (ativo=false)
- Add hard-delete endpoint
- Implement anonymization logic
- Update frontend with confirmation dialog

---

### P2 - Privacy Policy and Terms
**Priority:** P2 (Medium)
**Effort:** S
**Description:** Create privacy policy and terms of use pages.

**Acceptance Criteria:**
- [ ] Privacy policy page in Portuguese
- [ ] Terms of use page
- [ ] Accessible from footer and consent form
- [ ] Includes: data collection, usage, retention, user rights (LGPD)
- [ ] Version tracking (v1.0, last updated date)

**Technical Notes:**
- Create static pages or CMS integration
- Link from footer
- Reference in consent text

---

### P2 - CPF Validation Enhancement
**Priority:** P2 (Medium)
**Effort:** S
**Description:** Add CPF checksum validation (currently only format validation).

**Acceptance Criteria:**
- [ ] Backend validates CPF checksum algorithm
- [ ] Frontend provides real-time validation feedback
- [ ] Existing invalid CPFs handled gracefully (warning, not error)
- [ ] Duplicate CPF detection (warn if CPF already registered)

**Technical Notes:**
- Implement CPF validation algorithm in backend
- Add validator to Dizimista schema
- Update frontend validation
- Handle edge case: multiple people might share CPF (rare but possible)

---

### P2 - Password Policy Enhancement
**Priority:** P2 (Medium)
**Effort:** S
**Description:** Strengthen password requirements.

**Acceptance Criteria:**
- [ ] Minimum 12 characters (currently 8)
- [ ] Require: uppercase, lowercase, number, special character
- [ ] Password strength meter on frontend
- [ ] Prevent common passwords (list of 1000 most common)
- [ ] Password expiry policy (optional: 90 days)

**Technical Notes:**
- Add password validator to backend
- Integrate strength meter on frontend (e.g., zxcvbn)
- Update user documentation

---

### P3 - Two-Factor Authentication (2FA)
**Priority:** P3 (Low)
**Effort:** L
**Description:** Optional 2FA for admin users.

**Acceptance Criteria:**
- [ ] Support TOTP (Google Authenticator, Authy)
- [ ] QR code generation for setup
- [ ] Backup codes (10 single-use codes)
- [ ] Enforce 2FA for admin role (optional)
- [ ] Frontend setup wizard

**Technical Notes:**
- Use pyotp library for backend
- Add `totp_secret` and `totp_enabled` to Usuario model
- Create 2FA setup and verification endpoints
- Update login flow

---

## Reporting & Analytics

### P1 - PDF Receipt Generation
**Priority:** P1 (High)
**Effort:** M
**Description:** Generate PDF receipts for contributions.

**Acceptance Criteria:**
- [ ] API endpoint: GET /api/contribuicoes/{id}/receipt (returns PDF)
- [ ] Receipt includes: church info, dizimista info, contribution details, date
- [ ] Church logo support (upload logo in settings)
- [ ] Complies with Brazilian receipt standards (optional: fiscal note format)
- [ ] Frontend button: "Gerar Recibo" on contribution detail
- [ ] Email receipt option (future: send via email)

**Technical Notes:**
- Use ReportLab or WeasyPrint for PDF generation
- Create PDF template
- Add endpoint to router
- Frontend download button

---

### P1 - Dashboard Charts and Graphs
**Priority:** P1 (High)
**Effort:** M
**Description:** Visual charts on dashboard for better insights.

**Acceptance Criteria:**
- [ ] Chart: Monthly contributions trend (line chart)
- [ ] Chart: Dízimo vs Oferta (pie chart)
- [ ] Chart: Contributions by comunidade (bar chart)
- [ ] Chart: Active vs inactive dizimistas (donut chart)
- [ ] Time range selector (last 30/60/90 days, YTD)
- [ ] Responsive charts (mobile-friendly)

**Technical Notes:**
- Use Chart.js or Recharts for frontend
- Create backend endpoints for chart data
- Add to DashboardPage

---

### P1 - Excel/CSV Export for Reports
**Priority:** P1 (High)
**Effort:** S
**Description:** Export reports to Excel or CSV.

**Acceptance Criteria:**
- [ ] Export dizimistas list to CSV/Excel
- [ ] Export contributions list to CSV/Excel
- [ ] Export aniversariantes to CSV/Excel
- [ ] Export financial reports to CSV/Excel
- [ ] Include filters applied (e.g., date range, comunidade)
- [ ] Frontend button: "Exportar para Excel"

**Technical Notes:**
- Backend: generate CSV with Python csv module or pandas
- Frontend: download blob
- Consider using xlsx library for proper Excel format

---

### P2 - Advanced Financial Reports
**Priority:** P2 (Medium)
**Effort:** M
**Description:** More detailed financial reporting.

**Acceptance Criteria:**
- [ ] Monthly comparison (current month vs last month)
- [ ] Year-over-year comparison
- [ ] Contribution trends by dizimista (top contributors)
- [ ] Contribution distribution (histogram of amounts)
- [ ] Forecast based on trends (optional)
- [ ] Export to PDF report

**Technical Notes:**
- Create report service methods
- Add endpoints
- Create frontend report pages

---

### P2 - Family Grouping
**Priority:** P2 (Medium)
**Effort:** M
**Description:** Group dizimistas by family and track family contributions.

**Acceptance Criteria:**
- [ ] Family model (id, nome, endereco)
- [ ] Link dizimistas to family (optional FK)
- [ ] Family contribution view (total by family)
- [ ] Family birthday list (all members)
- [ ] Family contact person (primary dizimista)

**Technical Notes:**
- Add Familia model
- Migration: dizimista.familia_id nullable FK
- Update schemas and routers
- Frontend family management page

---

## User Experience

### P1 - Email Notifications
**Priority:** P1 (High)
**Effort:** M
**Description:** Automated email notifications.

**Acceptance Criteria:**
- [ ] Contribution confirmation email to dizimista (if email provided)
- [ ] Birthday email (optional, configurable)
- [ ] Monthly summary email to admins
- [ ] Email templates in Portuguese
- [ ] SMTP configuration via environment variables
- [ ] Opt-out mechanism (user can disable emails)

**Technical Notes:**
- Use FastAPI-Mail or python-sendgrid
- Create email templates (HTML + plain text)
- Add background task for sending emails
- Frontend: user email preferences

---

### P2 - Bulk Import Dizimistas
**Priority:** P2 (Medium)
**Effort:** M
**Description:** Import dizimistas from spreadsheet (Excel/CSV).

**Acceptance Criteria:**
- [ ] Upload Excel or CSV file
- [ ] Preview import (show first 10 rows)
- [ ] Validation: required fields, formats (CPF, email, phone)
- [ ] Duplicate detection (warn if name or CPF exists)
- [ ] Dry-run mode (validate without committing)
- [ ] Import summary (success, errors, duplicates)

**Technical Notes:**
- Backend: parse CSV/Excel with pandas
- Validate rows
- Create bulk insert endpoint
- Frontend: file upload with preview

---

### P2 - SMS Notifications
**Priority:** P2 (Medium)
**Effort:** L
**Description:** Send SMS notifications for important events.

**Acceptance Criteria:**
- [ ] Birthday SMS (optional, configurable)
- [ ] Contribution confirmation SMS
- [ ] SMS for special events (campaigns, holidays)
- [ ] Integration with SMS provider (Twilio, Zenvia, etc.)
- [ ] Cost tracking (SMS are paid)
- [ ] User opt-in required

**Technical Notes:**
- Integrate with SMS API
- Add SMS service
- Frontend: user SMS preferences
- Consider cost implications (charge per SMS)

---

### P2 - Search Autocomplete
**Priority:** P2 (Medium)
**Effort:** S
**Description:** Autocomplete for dizimista search.

**Acceptance Criteria:**
- [ ] Type-ahead search for dizimista names
- [ ] Search by name, CPF, or phone
- [ ] Show top 10 results as you type
- [ ] Debounce (wait 300ms before searching)
- [ ] Keyboard navigation (arrow keys, enter to select)

**Technical Notes:**
- Backend: optimize search query
- Frontend: use react-select or custom autocomplete
- Add debounce hook

---

### P3 - Mobile App (React Native)
**Priority:** P3 (Low)
**Effort:** XL
**Description:** Native mobile app for iOS and Android.

**Acceptance Criteria:**
- [ ] Login and authentication
- [ ] View dizimistas (list, search, detail)
- [ ] Register contributions (simplified form)
- [ ] View reports (read-only)
- [ ] Push notifications (birthdays, important events)
- [ ] Offline mode (cache data for viewing)
- [ ] iOS and Android builds

**Technical Notes:**
- Use React Native or Expo
- Reuse TypeScript types and API clients
- Implement secure token storage (AsyncStorage + encryption)
- Publish to App Store and Google Play

---

## Multi-Tenant & Scalability

### P1 - Multi-Parish Support
**Priority:** P1 (High)
**Effort:** L
**Description:** Support multiple parishes in a single instance.

**Acceptance Criteria:**
- [ ] Each user belongs to one parish (or multiple with role per parish)
- [ ] Data isolation: users only see their parish data
- [ ] Super admin role (can manage all parishes)
- [ ] Parish settings (name, logo, contact info)
- [ ] Parish-specific reports
- [ ] Domain-based routing (optional: parish.ecclesia.com)

**Technical Notes:**
- Major refactor: add parish_id to all entities
- Row-level security or query filters
- Update all services to filter by parish
- Migration strategy for existing data

---

### P2 - API Rate Limiting Configuration
**Priority:** P2 (Medium)
**Effort:** S
**Description:** Make rate limits configurable via environment.

**Acceptance Criteria:**
- [ ] Environment variables for rate limits (login, global)
- [ ] Different limits for different roles (admin = higher limit)
- [ ] Rate limit info in response headers (X-RateLimit-Remaining)
- [ ] Admin dashboard to view rate limit status

**Technical Notes:**
- Update slowapi configuration
- Add env vars: RATE_LIMIT_LOGIN, RATE_LIMIT_GLOBAL
- Implement role-based limits

---

### P3 - Caching Layer
**Priority:** P3 (Low)
**Effort:** M
**Description:** Implement caching for frequently accessed data.

**Acceptance Criteria:**
- [ ] Redis integration
- [ ] Cache report results (TTL: 5 minutes)
- [ ] Cache dizimista list (invalidate on create/update)
- [ ] Cache comunidade/paroquia lists
- [ ] Cache-Control headers on frontend

**Technical Notes:**
- Add Redis to docker-compose
- Use redis-py for backend
- Implement cache decorators
- Consider cache invalidation strategy

---

## Payments & Integrations

### P2 - Payment Gateway Integration
**Priority:** P2 (Medium)
**Effort:** L
**Description:** Accept online payments (credit card, Pix, boleto).

**Acceptance Criteria:**
- [ ] Integration with Brazilian payment gateway (e.g., Stripe, Mercado Pago, PagSeguro)
- [ ] Support Pix, credit card, boleto
- [ ] Payment form on frontend
- [ ] Automatic contribution creation on successful payment
- [ ] Payment status tracking (pending, completed, failed)
- [ ] Webhook handling for payment confirmations
- [ ] Refund support (admin only)

**Technical Notes:**
- Choose payment provider (consider fees)
- Implement webhook handling
- Add payment_id to Contribuicao model
- PCI compliance considerations

---

### P2 - Recurring Contributions
**Priority:** P2 (Medium)
**Effort:** M
**Description:** Set up recurring monthly contributions.

**Acceptance Criteria:**
- [ ] Dizimista can opt-in to recurring payments
- [ ] Frequency: monthly, quarterly, yearly
- [ ] Amount and payment method configuration
- [ ] Automatic charge on schedule
- [ ] Email confirmation after each charge
- [ ] Pause or cancel subscription
- [ ] Admin view: active subscriptions

**Technical Notes:**
- Requires payment gateway integration (see above)
- Add Subscription model
- Cron job or background task for processing
- Use payment gateway's subscription features

---

### P3 - Accounting Software Integration
**Priority:** P3 (Low)
**Effort:** L
**Description:** Export data to accounting software.

**Acceptance Criteria:**
- [ ] Export to standard accounting format (OFX, CSV for accounting)
- [ ] Integration with popular Brazilian accounting tools
- [ ] Chart of accounts mapping (dízimo, oferta categories)
- [ ] Periodic export (monthly)
- [ ] Audit trail for exports

**Technical Notes:**
- Research Brazilian accounting software APIs
- Create export formats
- Consider scheduled exports

---

## Administration

### P1 - User Management
**Priority:** P1 (High)
**Effort:** S
**Description:** Admin UI for user management.

**Acceptance Criteria:**
- [ ] Admin page: list users
- [ ] Create new user (currently only via seed or API)
- [ ] Edit user (change role, name, email)
- [ ] Deactivate/activate user
- [ ] Password reset (admin initiated)
- [ ] Audit log of user changes

**Technical Notes:**
- Frontend: UsersPage with CRUD
- Backend: user management endpoints already exist (POST /api/auth/register)
- Add user list endpoint

---

### P2 - Activity Audit Log
**Priority:** P2 (Medium)
**Effort:** M
**Description:** Comprehensive audit log of all actions.

**Acceptance Criteria:**
- [ ] Log all create/update/delete actions
- [ ] Store: user, action, entity type, entity ID, timestamp, old/new values
- [ ] Admin view: audit log table with filters (user, date, action type)
- [ ] Export audit log to CSV
- [ ] Retention policy (keep 2 years)

**Technical Notes:**
- Create AuditLog model
- Middleware or service decorator to capture actions
- Frontend audit log page (admin only)

---

### P2 - Backup Automation
**Priority:** P2 (Medium)
**Effort:** S
**Description:** Automate database backups.

**Acceptance Criteria:**
- [ ] Automated daily backups (cron job or platform feature)
- [ ] Backup stored in S3-compatible storage (AWS S3, DigitalOcean Spaces)
- [ ] Retention: 7 daily, 4 weekly, 12 monthly
- [ ] Backup verification (test restore quarterly)
- [ ] Notification on backup failure

**Technical Notes:**
- Use infra/backup.sh script
- Schedule with cron or platform scheduler
- Upload to cloud storage
- Monitor backup success

---

### P3 - Settings Management
**Priority:** P3 (Low)
**Effort:** M
**Description:** Admin UI for system settings.

**Acceptance Criteria:**
- [ ] Church info: name, logo, address, contact
- [ ] Email settings: SMTP config, email templates
- [ ] Notification preferences: enable/disable email, SMS
- [ ] System settings: rate limits, token expiry
- [ ] UI stored in database (not just env vars)

**Technical Notes:**
- Create Settings model
- Settings service
- Frontend settings page (admin only)
- Override env vars with database settings

---

## Localization & Accessibility

### P2 - English Localization
**Priority:** P2 (Medium)
**Effort:** M
**Description:** Add English language support.

**Acceptance Criteria:**
- [ ] i18n library integration (react-i18next)
- [ ] All UI text in translation files (pt-BR, en-US)
- [ ] Language switcher in UI
- [ ] Backend error messages in selected language
- [ ] Default: Portuguese (current behavior)

**Technical Notes:**
- Add i18next to frontend
- Extract all strings to translation files
- Backend: accept Accept-Language header

---

### P2 - Accessibility Improvements
**Priority:** P2 (Medium)
**Effort:** S
**Description:** Enhance accessibility (WCAG 2.1 AA compliance).

**Acceptance Criteria:**
- [ ] All images have alt text
- [ ] Form inputs have associated labels
- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] Keyboard navigation for all interactive elements
- [ ] Color contrast meets WCAG AA standards
- [ ] Screen reader testing (NVDA, JAWS)
- [ ] Skip to main content link

**Technical Notes:**
- Use axe-core for automated testing
- Manual testing with screen readers
- Update components with ARIA attributes

---

### P3 - Dark Mode
**Priority:** P3 (Low)
**Effort:** S
**Description:** Add dark mode theme.

**Acceptance Criteria:**
- [ ] Dark theme colors (Tailwind dark mode classes)
- [ ] Theme toggle in header
- [ ] Persist preference in localStorage
- [ ] Smooth transition between themes
- [ ] Respect system preference (prefers-color-scheme)

**Technical Notes:**
- Configure Tailwind dark mode
- Add theme context
- Update all components with dark: classes

---

## Technical Debt

### P2 - Frontend Testing
**Priority:** P2 (Medium)
**Effort:** M
**Description:** Add comprehensive frontend tests.

**Acceptance Criteria:**
- [ ] Component tests (React Testing Library)
- [ ] Integration tests for user flows
- [ ] E2E tests for critical paths (Playwright or Cypress)
- [ ] Coverage: >70% for components
- [ ] Run tests in CI

**Technical Notes:**
- Set up Jest + React Testing Library
- Write tests for key components (DizimistaForm, ContribuicaoForm)
- Add E2E tests for login, create dizimista, create contribution

---

### P2 - API Versioning
**Priority:** P2 (Medium)
**Effort:** S
**Description:** Implement API versioning.

**Acceptance Criteria:**
- [ ] Current API: /api/v1/...
- [ ] Version in URL (not header for simplicity)
- [ ] Support for multiple versions (v1, v2)
- [ ] Deprecation notices for old versions
- [ ] Documentation for each version

**Technical Notes:**
- Update router prefixes to /api/v1
- Create v2 routers when breaking changes needed
- Document versioning policy

---

### P3 - Database Connection Pooling Optimization
**Priority:** P3 (Low)
**Effort:** S
**Description:** Optimize database connection pool settings.

**Acceptance Criteria:**
- [ ] Tune pool size based on load testing
- [ ] Connection timeout settings
- [ ] Pool overflow settings
- [ ] Monitor connection usage
- [ ] Document optimal settings

**Technical Notes:**
- Adjust SQLAlchemy engine settings
- Load test to find optimal pool size
- Monitor with pg_stat_activity

---

### P3 - Performance Optimization
**Priority:** P3 (Low)
**Effort:** M
**Description:** General performance improvements.

**Acceptance Criteria:**
- [ ] Add database indexes on slow queries
- [ ] Optimize N+1 query problems (use joinedload)
- [ ] Frontend code splitting (lazy load routes)
- [ ] Image optimization (compress, lazy load)
- [ ] Backend query optimization (EXPLAIN ANALYZE)
- [ ] Frontend bundle size reduction

**Technical Notes:**
- Profile with Django Debug Toolbar or logging
- Use React.lazy for code splitting
- Optimize images with next/image or similar

---

## Future Ideas (Not Prioritized)

- **Campaigns:** Create fundraising campaigns with goals and progress tracking
- **Events:** Event management (masses, festivals) with attendance tracking
- **Volunteer Management:** Track volunteers and their activities
- **Inventory:** Manage church inventory (bibles, hymnals, supplies)
- **Communication:** Built-in messaging system for parishioners
- **Pledges:** Track pledges and fulfillment
- **Sacraments:** Track baptisms, confirmations, marriages
- **Cemetery Management:** If parish manages a cemetery
- **WhatsApp Integration:** Send notifications via WhatsApp Business API
- **AI Chatbot:** Answer common questions from parishioners

---

## How to Use This Backlog

1. **Review regularly:** Revisit priorities every sprint or month
2. **User feedback:** Gather feedback from actual church users to reprioritize
3. **Estimate:** Refine effort estimates as you learn more
4. **Dependencies:** Some items depend on others (e.g., recurring payments require payment gateway)
5. **MVP+:** Start with P1 items to build MVP+, then P2, then P3

---

**Version:** 1.0
**Maintained by:** Development Team
**Next Review:** After MVP deployment and user feedback
