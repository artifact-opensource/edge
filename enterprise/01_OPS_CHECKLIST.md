# 🧪 OPERATIONS TEST CHECKLIST

**Artifact Virtual Studio - Quality & Operations Testing**

Version: 1.0.0  
Last Updated: 2026-02-02  
Status: Ready for Testing

---

## 📋 PRE-FLIGHT CHECKS

### Environment Setup
- [ ] PostgreSQL database running and accessible
- [ ] Backend `.env` configured with valid `DATABASE_URL`
- [ ] Prisma migrations applied (`npx prisma migrate dev`)
- [ ] Backend server running on port 3000
- [ ] Frontend server running on port 5173
- [ ] No console errors in browser developer tools

### Quick Start Commands
```bash
# Terminal 1: Backend
cd backend
npm install
cp .env.example .env
# Edit .env with DATABASE_URL
npx prisma migrate dev
npm run dev

# Terminal 2: Frontend
cd studio/app
npm install
npm run dev
```

---

## 🔐 AUTHENTICATION TESTS

### 1. User Registration
- [ ] Navigate to `/register` page
- [ ] Fill in registration form:
  - Email: test@example.com
  - Password: TestPassword123!
  - First Name: Test
  - Last Name: User
- [ ] Submit form
- [ ] Verify redirect to dashboard
- [ ] Verify user name appears in header

### 2. User Login
- [ ] Log out if authenticated
- [ ] Navigate to `/login` page
- [ ] Enter credentials from registration
- [ ] Submit form
- [ ] Verify successful login
- [ ] Verify JWT token stored in localStorage

### 3. Session Persistence
- [ ] Log in successfully
- [ ] Refresh browser
- [ ] Verify still authenticated
- [ ] Verify user data still available

### 4. Logout
- [ ] Click logout button
- [ ] Verify redirect to login page
- [ ] Verify token removed from localStorage
- [ ] Verify cannot access protected routes

---

## 👥 CRM MODULE TESTS

### 5. Contacts - List
- [ ] Navigate to CRM > Contacts
- [ ] Verify contacts list loads from API
- [ ] Verify no mock/demo data shown
- [ ] Check loading state appears briefly

### 6. Contacts - Create
- [ ] Click "Add Contact" button
- [ ] Fill in contact form:
  - First Name: John
  - Last Name: Smith
  - Email: john.smith@company.com
  - Phone: +1-555-0123
  - Company: Acme Corp
  - Status: Lead
- [ ] Submit form
- [ ] Verify contact appears in list
- [ ] Verify success notification

### 7. Contacts - Edit
- [ ] Click on contact to view details
- [ ] Click edit button
- [ ] Change status from Lead to Customer
- [ ] Save changes
- [ ] Verify changes persisted

### 8. Contacts - Delete
- [ ] Select a contact
- [ ] Click delete button
- [ ] Confirm deletion
- [ ] Verify contact removed from list
- [ ] Refresh page - verify still deleted

### 9. Deals - List
- [ ] Navigate to CRM > Deals
- [ ] Verify deals list loads from API
- [ ] Verify pipeline stats shown

### 10. Deals - Create
- [ ] Click "Add Deal"
- [ ] Fill in deal form:
  - Title: Enterprise License
  - Value: 50000
  - Stage: Qualified
  - Contact: (select existing)
- [ ] Submit form
- [ ] Verify deal appears in list

### 11. Deals - Pipeline View
- [ ] Switch to Kanban/Pipeline view
- [ ] Verify deals grouped by stage
- [ ] Verify drag-and-drop (if implemented)

---

## 👤 HRM MODULE TESTS

### 12. Employees - List
- [ ] Navigate to HRM > Employees
- [ ] Verify employee list loads from API
- [ ] Verify department filter works

### 13. Employees - Create
- [ ] Click "Add Employee"
- [ ] Fill in employee form:
  - First Name: Jane
  - Last Name: Doe
  - Email: jane.doe@artifactvirtual.com
  - Department: Engineering
  - Position: Software Engineer
  - Hire Date: Today
- [ ] Submit form
- [ ] Verify employee appears in list

### 14. Employees - Status Update
- [ ] Select an employee
- [ ] Change status (Active → On Leave)
- [ ] Verify status updated
- [ ] Verify reflected in list

---

## $ FINANCE MODULE TESTS

### 15. Invoices - List
- [ ] Navigate to Finance > Invoices
- [ ] Verify invoices load from API
- [ ] Verify totals calculated correctly

### 16. Invoices - Create
- [ ] Click "Create Invoice"
- [ ] Fill in invoice form:
  - Title: Consulting Services
  - Client: Test Client
  - Amount: 5000
  - Due Date: 30 days from now
- [ ] Add line items
- [ ] Submit form
- [ ] Verify invoice number generated

### 17. Invoices - Record Payment
- [ ] Select an invoice
- [ ] Click "Record Payment"
- [ ] Enter payment details
- [ ] Submit
- [ ] Verify status changes to Paid

---

## → DEVELOPMENT MODULE TESTS

### 18. Projects - List
- [ ] Navigate to Development > Projects
- [ ] Verify projects load from API
- [ ] Verify status badges shown

### 19. Projects - Create
- [ ] Click "New Project"
- [ ] Fill in project form:
  - Name: New Feature Development
  - Description: Building new features
  - Priority: High
  - Start Date: Today
- [ ] Submit form
- [ ] Verify project created

### 20. Projects - Progress Update
- [ ] Select a project
- [ ] Update progress slider to 50%
- [ ] Verify progress saved
- [ ] Refresh page - verify progress persisted

---

## ■ ANALYTICS/DASHBOARD TESTS

### 21. Dashboard Load
- [ ] Navigate to Dashboard
- [ ] Verify KPIs load correctly
- [ ] Verify charts render
- [ ] Verify recent activity shows

### 22. Data Accuracy
- [ ] Verify revenue total matches invoices
- [ ] Verify deal pipeline values correct
- [ ] Verify employee counts correct

---

## ↻ API INTEGRATION TESTS

### 23. Health Check
```bash
curl http://localhost:3000/health
```
- [ ] Returns `{"status":"ok"}`

### 24. API Documentation
- [ ] Navigate to http://localhost:3000/docs
- [ ] Swagger UI loads
- [ ] All endpoints documented

### 25. Error Handling
- [ ] Try to access invalid endpoint
- [ ] Verify proper error response
- [ ] Frontend shows error message gracefully

### 26. Rate Limiting
- [ ] Make rapid requests (>100 in 1 minute)
- [ ] Verify rate limit error returned
- [ ] Verify UI shows appropriate message

---

## 🔒 SECURITY TESTS

### 27. Protected Routes
- [ ] Log out
- [ ] Try to access `/dashboard` directly
- [ ] Verify redirect to login

### 28. Invalid Token
- [ ] Manually corrupt localStorage token
- [ ] Refresh page
- [ ] Verify forced logout

### 29. CORS
- [ ] Check browser console for CORS errors
- [ ] Verify API accessible from frontend origin

---

## 📱 UI/UX TESTS

### 30. Responsive Design
- [ ] Test on desktop (1920x1080)
- [ ] Test on tablet (768px width)
- [ ] Test on mobile (375px width)

### 31. Theme Switching
- [ ] Toggle dark/light mode
- [ ] Verify theme persists on refresh
- [ ] Verify all components themed correctly

### 32. Loading States
- [ ] Verify loading spinners show during API calls
- [ ] Verify skeleton loaders where appropriate

### 33. Error States
- [ ] Disconnect network
- [ ] Verify error messages displayed
- [ ] Reconnect - verify recovery

---

## 🐛 REGRESSION TESTS

### 34. Data Persistence
- [ ] Create new contact
- [ ] Refresh page
- [ ] Verify contact still exists
- [ ] Restart backend server
- [ ] Verify data still persisted

### 35. Navigation
- [ ] Test all sidebar navigation links
- [ ] Verify browser back/forward works
- [ ] Verify no broken links

### 36. Form Validation
- [ ] Submit empty forms
- [ ] Verify validation errors shown
- [ ] Test invalid email formats
- [ ] Test required fields

---

## 📋 TEST RESULTS

### Summary
| Category | Passed | Failed | Skipped |
|----------|--------|--------|---------|
| Authentication | /4 | | |
| CRM | /7 | | |
| HRM | /3 | | |
| Finance | /3 | | |
| Development | /3 | | |
| Analytics | /2 | | |
| API | /4 | | |
| Security | /3 | | |
| UI/UX | /4 | | |
| Regression | /3 | | |
| **TOTAL** | /36 | | |

### Issues Found
| ID | Description | Severity | Status |
|----|-------------|----------|--------|
| | | | |

### Notes
```
Test Date: 
Tester: 
Environment: 
Browser: 
```

---

## ✓ GO-LIVE CHECKLIST

### Pre-Deployment
- [ ] All critical tests passed
- [ ] No high-severity issues open
- [ ] Database backed up
- [ ] Environment variables configured for production
- [ ] SSL certificates valid
- [ ] DNS configured

### Deployment
- [ ] Deploy backend to production
- [ ] Run database migrations
- [ ] Deploy frontend to production
- [ ] Verify health check endpoint

### Post-Deployment
- [ ] Smoke test all major features
- [ ] Monitor error logs
- [ ] Verify analytics tracking
- [ ] Notify stakeholders

---

**Document Owner:** Development Team  
**Last Review:** 2026-02-02  
**Next Review:** After each release
