# Ecommerce-website Architecture Documentation

## Project Overview

**Project Name:** Ecommerce Website - Full-Featured E-Commerce Platform  
**Purpose:** Complete e-commerce solution with user authentication, product catalog, shopping cart, and payment processing  
**Target Users:** Customers, Administrators, Payment processors  
**Primary Language:** Python (Backend), HTML/CSS/JavaScript (Frontend)  
**Framework:** Flask/Django (Backend), Bootstrap (Frontend)  
**Repository Type:** Full-Stack Web Application  

This repository implements a production-grade e-commerce platform with secure payment processing, user management, and comprehensive order handling.

---

## Domain Knowledge & Business Context

### Core Business Objectives

1. **Customer Experience**
   - Easy product discovery and browsing
   - Secure account management
   - Seamless checkout process
   - Order tracking and history

2. **Security & Compliance**
   - PCI DSS compliance for payment processing
   - Protect customer data (PII)
   - Prevent SQL injection and XSS attacks
   - Secure password storage with bcrypt

3. **Business Operations**
   - Inventory management
   - Order fulfillment tracking
   - Revenue reporting and analytics
   - Customer relationship management

4. **Scalability & Performance**
   - Handle thousands of concurrent users
   - Fast product search and filtering
   - Efficient database queries
   - Caching for frequently accessed data

### Key Entities

#### 1. **User**
- **Definition:** Customer account in the system
- **Properties:**
  - User ID (unique identifier)
  - Email (unique, used for login)
  - Password (hashed with bcrypt)
  - Full name
  - Phone number
  - Account status (active, suspended, deleted)
  - Created date
  - Last login date
  - Preferences (newsletter, notifications)

#### 2. **Product**
- **Definition:** Item available for purchase
- **Properties:**
  - Product ID
  - Name
  - Description
  - Price (USD)
  - Stock quantity
  - Category
  - Images
  - Ratings and reviews
  - SKU (stock keeping unit)
  - Created date
  - Last updated date

#### 3. **Cart**
- **Definition:** Temporary collection of items for purchase
- **Properties:**
  - Cart ID
  - User ID (owner)
  - Items (product_id, quantity, price)
  - Subtotal
  - Created date
  - Last updated date
  - Expiration (30 days)

#### 4. **Order**
- **Definition:** Completed purchase transaction
- **Properties:**
  - Order ID
  - User ID (buyer)
  - Items (product details, quantity, price)
  - Subtotal
  - Tax amount
  - Shipping cost
  - Total amount
  - Status (pending, processing, shipped, delivered)
  - Shipping address
  - Billing address
  - Payment method
  - Payment status
  - Created date
  - Shipped date
  - Delivered date

#### 5. **Payment**
- **Definition:** Financial transaction record
- **Properties:**
  - Payment ID
  - Order ID
  - Amount
  - Currency (USD)
  - Payment method (credit card, debit card)
  - Status (pending, completed, failed, refunded)
  - Transaction ID (from payment gateway)
  - Last 4 digits of card
  - Timestamp
  - Receipt

#### 6. **Address**
- **Definition:** Shipping or billing location
- **Properties:**
  - Address ID
  - User ID
  - Type (shipping, billing)
  - Street address
  - City
  - State/Province
  - ZIP/Postal code
  - Country
  - Phone number
  - Default flag

#### 7. **Review**
- **Definition:** Customer feedback on product
- **Properties:**
  - Review ID
  - Product ID
  - User ID (reviewer)
  - Rating (1-5 stars)
  - Title
  - Content
  - Created date
  - Helpful count

### Business Rules & Constraints

1. **User Management Rules**
   - Email must be unique
   - Password minimum 8 characters
   - Account lockout after 5 failed login attempts
   - Password reset link expires in 24 hours
   - Email verification required for new accounts

2. **Product Rules**
   - Price must be > 0
   - Stock cannot be negative
   - Product must have at least one image
   - Description required (minimum 50 characters)
   - Category required

3. **Cart Rules**
   - Cart expires after 30 days of inactivity
   - Maximum 100 items per cart
   - Quantity must be > 0 and <= stock
   - Cart cleared after successful checkout
   - Cannot add out-of-stock items

4. **Order Rules**
   - Order total = subtotal + tax + shipping
   - Tax calculated based on shipping address
   - Shipping cost based on destination and weight
   - Minimum order value: $10
   - Maximum order value: $100,000
   - Order cancellation allowed within 24 hours

5. **Payment Rules**
   - Only valid credit/debit cards accepted
   - Card validation: Luhn algorithm
   - CVV required for all transactions
   - PCI DSS compliance mandatory
   - Payment timeout: 10 minutes
   - Automatic refund for failed orders

6. **Security Rules**
   - All passwords hashed with bcrypt (min 10 rounds)
   - SQL injection prevention: parameterized queries
   - XSS prevention: input sanitization
   - CSRF protection: token validation
   - Rate limiting: 10 requests per minute per IP
   - HTTPS enforced for all pages
   - Session timeout: 30 minutes of inactivity

### User Journey Workflows

#### Registration Workflow
```
User Visits Website
    ↓
┌──────────────────────────────────┐
│ 1. Registration Form             │
│    - Email, password, name       │
│    - Phone number (optional)     │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 2. Input Validation              │
│    - Email format & uniqueness   │
│    - Password strength           │
│    - Required fields             │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 3. Hash Password                 │
│    - bcrypt with 10+ rounds      │
│    - Store securely              │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 4. Create User Account           │
│    - Store in database           │
│    - Generate verification token │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 5. Send Verification Email       │
│    - Include verification link   │
│    - Link expires in 24 hours    │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 6. User Clicks Link              │
│    - Verify email address        │
│    - Activate account            │
│    - Redirect to login           │
└──────────────────────────────────┘
    ↓
Account Created & Verified
```

#### Checkout Workflow
```
User Views Cart
    ↓
┌──────────────────────────────────┐
│ 1. Review Items                  │
│    - Verify quantities           │
│    - Check prices                │
│    - Confirm stock availability  │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 2. Enter Shipping Address        │
│    - Validate address format     │
│    - Check address completeness  │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 3. Calculate Shipping            │
│    - Based on destination        │
│    - Based on weight             │
│    - Display options             │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 4. Calculate Tax                 │
│    - Based on shipping address   │
│    - Apply tax rate              │
│    - Display breakdown           │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 5. Review Order Summary          │
│    - Items, subtotal             │
│    - Tax, shipping, total        │
│    - Confirm before payment      │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 6. Enter Payment Details         │
│    - Card number, expiry, CVV    │
│    - Billing address             │
│    - Validate card format        │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 7. Process Payment               │
│    - Send to payment gateway     │
│    - Verify authorization        │
│    - Capture payment             │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 8. Create Order                  │
│    - Store order details         │
│    - Reduce stock                │
│    - Clear cart                  │
└──────────────────────────────────┘
    ↓
┌──────────────────────────────────┐
│ 9. Send Confirmation             │
│    - Email receipt               │
│    - Order number                │
│    - Tracking info               │
└──────────────────────────────────┘
    ↓
Order Complete
```

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│         E-Commerce Platform - Complete Architecture         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Frontend Layer (HTML/CSS/JS)                 │  │
│  │  - Product browsing & search                        │  │
│  │  - Shopping cart interface                          │  │
│  │  - User account management                          │  │
│  │  - Checkout & payment form                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Web Server & Request Handler                 │  │
│  │  - Route requests to controllers                    │  │
│  │  - Session management                              │  │
│  │  - CSRF token validation                           │  │
│  │  - Rate limiting                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    Application Layer (Flask/Django)                  │  │
│  │  - User authentication & authorization             │  │
│  │  - Product management                              │  │
│  │  - Cart operations                                 │  │
│  │  - Order processing                                │  │
│  │  - Payment handling                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    Business Logic Layer                              │  │
│  │  - Inventory management                            │  │
│  │  - Pricing & discounts                             │  │
│  │  - Tax calculation                                 │  │
│  │  - Shipping calculation                            │  │
│  │  - Payment validation                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    Data Access Layer (ORM)                           │  │
│  │  - Database queries                                │  │
│  │  - Transaction management                          │  │
│  │  - Data validation                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    Database Layer (PostgreSQL)                       │  │
│  │  - Users, Products, Orders                         │  │
│  │  - Payments, Addresses, Reviews                    │  │
│  │  - Transactions & ACID compliance                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    External Services                                 │  │
│  │  - Payment Gateway (Stripe/PayPal)                 │  │
│  │  - Email Service (SendGrid)                        │  │
│  │  - SMS Service (Twilio)                            │  │
│  │  - Analytics (Google Analytics)                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    Caching Layer (Redis)                             │  │
│  │  - Session storage                                 │  │
│  │  - Product cache                                   │  │
│  │  - Rate limit tracking                             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
Ecommerce-website/
├── README.md                          # Project overview and setup
├── Ecommerce-website_architecture.md  # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
│
├── app/                               # Flask/Django application
│   ├── __init__.py
│   ├── config.py                      # Configuration management
│   ├── models.py                      # Database models
│   ├── extensions.py                  # Extensions (SQLAlchemy, etc.)
│   │
│   ├── auth/                          # Authentication module
│   │   ├── __init__.py
│   │   ├── routes.py                  # Login, register, logout
│   │   ├── forms.py                   # Auth forms
│   │   ├── utils.py                   # Password hashing, JWT
│   │   └── decorators.py              # Auth decorators
│   │
│   ├── products/                      # Product management
│   │   ├── __init__.py
│   │   ├── routes.py                  # Product listing, search
│   │   ├── models.py                  # Product model
│   │   ├── services.py                # Product business logic
│   │   └── utils.py                   # Search, filtering
│   │
│   ├── cart/                          # Shopping cart
│   │   ├── __init__.py
│   │   ├── routes.py                  # Add, remove, update cart
│   │   ├── models.py                  # Cart model
│   │   └── services.py                # Cart operations
│   │
│   ├── orders/                        # Order management
│   │   ├── __init__.py
│   │   ├── routes.py                  # Order creation, tracking
│   │   ├── models.py                  # Order model
│   │   ├── services.py                # Order processing
│   │   └── status.py                  # Order status management
│   │
│   ├── payments/                      # Payment processing
│   │   ├── __init__.py
│   │   ├── routes.py                  # Payment endpoints
│   │   ├── gateway.py                 # Payment gateway integration
│   │   ├── validation.py              # Card validation
│   │   ├── security.py                # PCI compliance
│   │   └── handlers.py                # Payment event handlers
│   │
│   ├── users/                         # User management
│   │   ├── __init__.py
│   │   ├── routes.py                  # Profile, settings
│   │   ├── models.py                  # User model
│   │   ├── services.py                # User operations
│   │   └── validators.py              # Input validation
│   │
│   ├── admin/                         # Admin panel
│   │   ├── __init__.py
│   │   ├── routes.py                  # Admin pages
│   │   ├── decorators.py              # Admin-only access
│   │   └── services.py                # Admin operations
│   │
│   ├── api/                           # REST API
│   │   ├── __init__.py
│   │   ├── v1/                        # API version 1
│   │   │   ├── products.py
│   │   │   ├── orders.py
│   │   │   ├── payments.py
│   │   │   └── users.py
│   │   └── middleware.py              # API middleware
│   │
│   ├── static/                        # Static files
│   │   ├── css/
│   │   │   ├── bootstrap.min.css
│   │   │   ├── style.css
│   │   │   └── responsive.css
│   │   ├── js/
│   │   │   ├── jquery.min.js
│   │   │   ├── bootstrap.min.js
│   │   │   ├── cart.js
│   │   │   ├── checkout.js
│   │   │   └── validation.js
│   │   └── images/
│   │       ├── logo.png
│   │       └── products/
│   │
│   ├── templates/                     # HTML templates
│   │   ├── base.html                  # Base template
│   │   ├── navbar.html                # Navigation bar
│   │   ├── footer.html                # Footer
│   │   ├── home.html                  # Homepage
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   └── reset_password.html
│   │   ├── products/
│   │   │   ├── list.html              # Product listing
│   │   │   ├── detail.html            # Product details
│   │   │   └── search.html            # Search results
│   │   ├── cart/
│   │   │   └── view.html              # Shopping cart
│   │   ├── checkout/
│   │   │   ├── shipping.html
│   │   │   ├── payment.html
│   │   │   └── confirmation.html
│   │   ├── orders/
│   │   │   ├── list.html              # Order history
│   │   │   └── detail.html            # Order details
│   │   ├── user/
│   │   │   ├── profile.html
│   │   │   ├── settings.html
│   │   │   └── addresses.html
│   │   └── admin/
│   │       ├── dashboard.html
│   │       ├── products.html
│   │       └── orders.html
│   │
│   └── utils/                         # Utility functions
│       ├── __init__.py
│       ├── security.py                # Security utilities
│       ├── validators.py              # Input validators
│       ├── decorators.py              # Custom decorators
│       ├── helpers.py                 # Helper functions
│       └── constants.py               # Constants
│
├── migrations/                        # Database migrations
│   └── versions/
│       ├── 001_initial_schema.py
│       ├── 002_add_reviews.py
│       └── ...
│
├── tests/                             # Test suite
│   ├── __init__.py
│   ├── test_auth.py                   # Authentication tests
│   ├── test_products.py               # Product tests
│   ├── test_cart.py                   # Cart tests
│   ├── test_orders.py                 # Order tests
│   ├── test_payments.py               # Payment tests
│   ├── test_security.py               # Security tests
│   ├── conftest.py                    # Pytest fixtures
│   └── fixtures/
│       ├── users.json
│       ├── products.json
│       └── orders.json
│
├── scripts/                           # Utility scripts
│   ├── init_db.py                     # Initialize database
│   ├── seed_data.py                   # Seed test data
│   ├── backup_db.py                   # Database backup
│   └── cleanup.py                     # Cleanup script
│
├── docker/                            # Docker configuration
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
│
├── docs/                              # Documentation
│   ├── API.md                         # API documentation
│   ├── DATABASE.md                    # Database schema
│   ├── SECURITY.md                    # Security guidelines
│   ├── DEPLOYMENT.md                  # Deployment guide
│   └── TROUBLESHOOTING.md             # Troubleshooting
│
└── run.py                             # Application entry point
```

### Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Backend** | Flask/Django | 2.0+ | Web framework |
| **Database** | PostgreSQL | 12+ | Data persistence |
| **ORM** | SQLAlchemy/Django ORM | Latest | Database abstraction |
| **Frontend** | HTML5, CSS3, JavaScript | Latest | User interface |
| **CSS Framework** | Bootstrap | 5.0+ | Responsive design |
| **Caching** | Redis | 7.0+ | Session & cache |
| **Payment** | Stripe/PayPal API | Latest | Payment processing |
| **Email** | SendGrid | Latest | Email delivery |
| **Testing** | pytest | Latest | Unit testing |
| **Security** | bcrypt | Latest | Password hashing |
| **Deployment** | Docker, Gunicorn | Latest | Containerization |

---

## Component Breakdown

### 1. Authentication Module

#### User Registration
```python
# Input validation
- Email format validation
- Password strength (min 8 chars, uppercase, number)
- Required fields check

# Security
- Hash password with bcrypt (10+ rounds)
- Generate email verification token
- Store securely in database

# Email verification
- Send verification email
- Token expires in 24 hours
- Activate account on verification
```

#### Login Process
```python
# Input validation
- Email exists in database
- Password provided

# Security
- Rate limiting: 10 attempts per IP per minute
- Account lockout after 5 failed attempts
- Bcrypt password verification
- Session creation with timeout

# Session management
- Store session in Redis
- 30-minute inactivity timeout
- Secure cookie flags (HttpOnly, Secure)
```

#### Password Reset
```python
# Reset request
- Email exists validation
- Generate reset token
- Send reset email

# Reset process
- Token validation (not expired)
- New password validation
- Hash new password
- Invalidate all active sessions
```

### 2. Product Management

#### Product Catalog
- **Product Display:** Browse by category, search, filter
- **Product Details:** Description, images, ratings, reviews
- **Stock Management:** Real-time stock updates
- **Pricing:** Dynamic pricing, discounts, promotions

#### Search & Filtering
```python
# Search capabilities
- Full-text search on name, description
- Category filtering
- Price range filtering
- Rating filtering
- Availability filtering

# Performance
- Elasticsearch for full-text search
- Database indexes on frequently filtered fields
- Redis caching for popular searches
- Pagination (20 items per page)
```

### 3. Shopping Cart

#### Cart Operations
- **Add Item:** Validate stock, check duplicate
- **Remove Item:** Delete from cart
- **Update Quantity:** Validate stock availability
- **Clear Cart:** Remove all items

#### Cart Persistence
```python
# Cart storage
- Session-based for anonymous users
- Database for logged-in users
- Redis for performance
- Auto-expire after 30 days

# Cart consistency
- Check stock before checkout
- Update prices from current product
- Validate quantities
- Handle price changes
```

### 4. Order Processing

#### Order Creation
```python
# Workflow
1. Validate cart items
2. Calculate totals (subtotal, tax, shipping)
3. Create order record
4. Reduce inventory
5. Clear cart
6. Send confirmation email
7. Return order details
```

#### Order Status Management
```python
# Status flow
Pending → Processing → Shipped → Delivered
                    ↓
              Cancelled (within 24h)
                    ↓
                 Refunded
```

### 5. Payment Processing

#### Payment Gateway Integration
```python
# Stripe integration
- Tokenize card details
- Create payment intent
- Handle 3D Secure
- Capture payment
- Handle webhooks

# Security
- Never store full card numbers
- Use Stripe tokens
- PCI DSS compliance
- HTTPS only
```

#### Card Validation
```python
# Validation steps
1. Format validation (16 digits, spaces)
2. Luhn algorithm check
3. Expiry date validation (not expired)
4. CVV validation (3-4 digits)
5. Cardholder name validation
```

#### Payment Security
```python
# PCI DSS Compliance
- No card storage on server
- Use tokenization
- Encrypted transmission (TLS 1.2+)
- Access logging
- Regular security audits

# Fraud Prevention
- AVS (Address Verification System)
- CVV verification
- 3D Secure (3DS) for high-value transactions
- Velocity checks (multiple attempts)
```

### 6. User Management

#### User Profile
- **Personal Info:** Name, email, phone
- **Addresses:** Shipping and billing addresses
- **Payment Methods:** Saved cards (tokenized)
- **Order History:** All past orders
- **Preferences:** Newsletter, notifications

#### User Settings
- **Account Security:** Password change, 2FA
- **Email Preferences:** Newsletter, notifications
- **Privacy Settings:** Data sharing preferences
- **Account Deletion:** Permanent account removal

---

## Data Flow & Workflows

### Complete Purchase Flow

```
Customer Browses Products
    ↓
┌──────────────────────────────────────┐
│ 1. Product Selection                 │
│    - View product details            │
│    - Check stock                     │
│    - Add to cart                     │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│ 2. Cart Review                       │
│    - View all items                  │
│    - Update quantities               │
│    - Proceed to checkout             │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│ 3. Shipping Information              │
│    - Enter/select address            │
│    - Validate address                │
│    - Calculate shipping              │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│ 4. Tax Calculation                   │
│    - Based on shipping address       │
│    - Apply tax rate                  │
│    - Display total tax               │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│ 5. Order Review                      │
│    - Items & quantities              │
│    - Subtotal, tax, shipping         │
│    - Final total                     │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│ 6. Payment Details                   │
│    - Card number, expiry, CVV        │
│    - Billing address                 │
│    - Validate input                  │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│ 7. Payment Processing                │
│    - Tokenize card                   │
│    - Send to payment gateway         │
│    - Verify authorization            │
│    - Capture payment                 │
└──────────────────────────────────────┘
    ↓
Payment Success?
    ├─ YES ───────────────────────┐
    │                             │
    ↓                             ↓
Create Order             Payment Failed
Reduce Stock             Redirect to retry
Clear Cart               Show error message
Send Confirmation
    ↓
Order Complete
```

### Database Transaction Flow

```
BEGIN TRANSACTION
    ↓
┌──────────────────────────────────────┐
│ 1. Validate cart items               │
│    - Check stock quantities          │
│    - Verify prices                   │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│ 2. Create order record               │
│    - INSERT into orders table        │
│    - INSERT into order_items table   │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│ 3. Process payment                   │
│    - External API call               │
│    - Verify success                  │
└──────────────────────────────────────┘
    ↓
Payment Success?
    ├─ YES ───────────────────────┐
    │                             │
    ↓                             ↓
Update Stock           ROLLBACK
Clear Cart             Restore state
INSERT Payment         Notify user
COMMIT TRANSACTION     RETURN error
    ↓
Order Confirmed
```

---

## Testing Strategy

### Test Categories

#### 1. Authentication Tests
```python
def test_user_registration_success():
    """Test successful user registration"""
    response = client.post('/register', data={
        'email': 'test@example.com',
        'password': 'SecurePass123',
        'name': 'Test User'
    })
    assert response.status_code == 302  # Redirect
    assert User.query.filter_by(email='test@example.com').first()

def test_password_hashing():
    """Test password is hashed with bcrypt"""
    user = User(email='test@example.com', password='SecurePass123')
    assert user.password != 'SecurePass123'  # Should be hashed
    assert bcrypt.checkpw(b'SecurePass123', user.password)

def test_login_rate_limiting():
    """Test account lockout after failed attempts"""
    for _ in range(5):
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'WrongPassword'
        })
    # 6th attempt should be blocked
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'CorrectPassword'
    })
    assert response.status_code == 429  # Too Many Requests
```

#### 2. Security Tests
```python
def test_sql_injection_prevention():
    """Test SQL injection is prevented"""
    # Attempt SQL injection
    response = client.get('/products?search="; DROP TABLE users; --')
    # Should return safe results, not execute SQL
    assert response.status_code == 200
    assert User.query.count() > 0  # Table still exists

def test_xss_prevention():
    """Test XSS attacks are prevented"""
    # Attempt XSS in product search
    response = client.get('/products?search=<script>alert("XSS")</script>')
    # Script tags should be escaped
    assert '<script>' not in response.data.decode()

def test_csrf_protection():
    """Test CSRF token validation"""
    # POST without CSRF token
    response = client.post('/checkout', data={
        'items': [1, 2, 3]
    })
    assert response.status_code == 400  # Bad Request

def test_https_enforcement():
    """Test HTTPS is enforced"""
    response = client.get('http://localhost/products')
    # Should redirect to HTTPS
    assert response.status_code == 308  # Permanent Redirect
```

#### 3. Payment Tests
```python
def test_card_validation_luhn():
    """Test Luhn algorithm for card validation"""
    # Valid card number
    assert validate_card_number('4532015112830366')
    # Invalid card number
    assert not validate_card_number('4532015112830367')

def test_payment_processing():
    """Test complete payment flow"""
    with patch('stripe.PaymentIntent.create') as mock_stripe:
        mock_stripe.return_value = {
            'id': 'pi_123',
            'status': 'succeeded'
        }
        
        order = create_order(user_id=1, items=[...])
        payment = process_payment(order_id=order.id, card_token='tok_123')
        
        assert payment.status == 'completed'
        assert order.status == 'processing'

def test_payment_failure_handling():
    """Test handling of payment failures"""
    with patch('stripe.PaymentIntent.create') as mock_stripe:
        mock_stripe.side_effect = stripe.error.CardError(
            'Your card was declined',
            'card_declined',
            'card_declined'
        )
        
        order = create_order(user_id=1, items=[...])
        with pytest.raises(PaymentError):
            process_payment(order_id=order.id, card_token='tok_123')
        
        assert order.status == 'pending'
```

#### 4. Database Tests
```python
def test_order_transaction_rollback():
    """Test transaction rollback on failure"""
    initial_stock = Product.query.get(1).stock
    
    with pytest.raises(PaymentError):
        with db.session.begin():
            # Reduce stock
            product = Product.query.get(1)
            product.stock -= 5
            
            # Simulate payment failure
            raise PaymentError('Payment failed')
    
    # Stock should be restored
    assert Product.query.get(1).stock == initial_stock

def test_order_data_integrity():
    """Test order data is stored correctly"""
    order = Order(
        user_id=1,
        total=99.99,
        status='completed'
    )
    db.session.add(order)
    db.session.commit()
    
    retrieved = Order.query.get(order.id)
    assert retrieved.total == 99.99
    assert retrieved.status == 'completed'
```

#### 5. Integration Tests
```python
def test_complete_checkout_flow():
    """Test complete checkout from cart to order"""
    # Login
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'SecurePass123'
    })
    
    # Add to cart
    client.post('/cart/add', data={'product_id': 1, 'quantity': 2})
    
    # Proceed to checkout
    response = client.get('/checkout')
    assert response.status_code == 200
    
    # Submit order
    with patch('stripe.PaymentIntent.create') as mock_stripe:
        mock_stripe.return_value = {'id': 'pi_123', 'status': 'succeeded'}
        
        response = client.post('/checkout/submit', data={
            'email': 'test@example.com',
            'shipping_address': '123 Main St',
            'card_token': 'tok_123'
        })
        
        assert response.status_code == 302  # Redirect to confirmation
        assert Order.query.count() == 1
        assert Cart.query.get(current_user.id).items.count() == 0
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_payments.py

# Run specific test
pytest tests/test_payments.py::test_card_validation_luhn

# Run security tests only
pytest tests/test_security.py -v

# Run with detailed output
pytest -v --tb=short tests/
```

---

## Custom AI Instructions

### Code Generation Guidelines

1. **Input Validation & Sanitization**
   - Validate all user inputs (form data, URLs, API params)
   - Sanitize HTML to prevent XSS
   - Use parameterized queries to prevent SQL injection
   - Validate email format with regex
   - Validate URLs and file paths

2. **Password Security**
   - Always hash with bcrypt (minimum 10 rounds)
   - Never store plain text passwords
   - Never log passwords
   - Implement rate limiting on login
   - Enforce minimum 8-character passwords

3. **Payment Security**
   - Never store full card numbers
   - Use payment gateway tokenization
   - Validate card with Luhn algorithm
   - Require CVV verification
   - Implement 3D Secure for high-value orders
   - Log all payment attempts
   - Comply with PCI DSS standards

4. **Database Operations**
   - Use parameterized queries always
   - Implement transaction management
   - Handle database errors gracefully
   - Log all data modifications
   - Use ORM for abstraction

5. **Error Handling**
   - Catch specific exceptions
   - Log errors with context
   - Show user-friendly messages
   - Never expose system details to users
   - Implement proper HTTP status codes

### Code Detection & Violation Patterns

1. **SQL Injection Violations**
   - ❌ `query = f"SELECT * FROM users WHERE email = '{email}'"`
   - ❌ String concatenation in SQL
   - ❌ User input directly in SQL
   - ✅ `query = "SELECT * FROM users WHERE email = ?"` with parameters

2. **XSS Violations**
   - ❌ `{{ user_input }}` in Jinja2 without escaping
   - ❌ `innerHTML = user_input` in JavaScript
   - ❌ Rendering HTML from user input
   - ✅ `{{ user_input|escape }}` or using safe HTML filters

3. **Password Security Violations**
   - ❌ Storing plain text passwords
   - ❌ Using weak hashing (MD5, SHA1)
   - ❌ Logging passwords
   - ❌ Using fixed salt
   - ✅ Bcrypt with 10+ rounds, no logging

4. **Payment Security Violations**
   - ❌ Storing full card numbers
   - ❌ No card validation
   - ❌ Skipping CVV verification
   - ❌ No HTTPS
   - ✅ Tokenization, validation, HTTPS, PCI compliance

5. **CSRF Violations**
   - ❌ POST requests without CSRF token
   - ❌ No CSRF token validation
   - ❌ Tokens not tied to user sessions
   - ✅ CSRF tokens on all forms, validation on POST/PUT/DELETE

### Example: Secure Payment Processing

```python
from flask import request, jsonify
from werkzeug.security import safe_str_cmp
import stripe
from app.models import Order, Payment
from app.utils.security import validate_card_number, encrypt_payment_data

@app.route('/api/checkout', methods=['POST'])
@login_required
def process_checkout():
    """
    Process payment securely with PCI compliance.
    
    Security measures:
    - HTTPS only (enforced at server level)
    - CSRF token validation (via Flask-WTF)
    - Card tokenization (no card storage)
    - Input validation and sanitization
    - Rate limiting (via decorator)
    - Bcrypt password verification
    - Transaction management
    """
    # Validate CSRF token
    if not request.form.get('csrf_token'):
        return jsonify({'error': 'CSRF token missing'}), 400
    
    # Get request data
    data = request.get_json()
    
    # Validate input
    if not data.get('card_token'):
        return jsonify({'error': 'Card token required'}), 400
    
    if not data.get('amount') or data['amount'] <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    
    if not data.get('order_id'):
        return jsonify({'error': 'Order ID required'}), 400
    
    # Retrieve order
    order = Order.query.get(data['order_id'])
    if not order or order.user_id != current_user.id:
        return jsonify({'error': 'Order not found'}), 404
    
    # Verify amount matches order
    if data['amount'] != order.total:
        logger.warning(
            f"Amount mismatch for order {order.id}: "
            f"expected {order.total}, got {data['amount']}"
        )
        return jsonify({'error': 'Amount mismatch'}), 400
    
    try:
        # Create Stripe payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(data['amount'] * 100),  # Convert to cents
            currency='usd',
            payment_method=data['card_token'],
            confirm=True,
            metadata={
                'order_id': order.id,
                'user_id': current_user.id
            }
        )
        
        # Check payment status
        if intent['status'] == 'succeeded':
            # Create payment record
            payment = Payment(
                order_id=order.id,
                amount=data['amount'],
                status='completed',
                transaction_id=intent['id'],
                last_4_digits=data.get('card_last_4')  # From frontend
            )
            
            # Update order status
            order.status = 'processing'
            order.payment_id = payment.id
            
            # Reduce inventory
            for item in order.items:
                product = Product.query.get(item.product_id)
                product.stock -= item.quantity
            
            # Commit transaction
            db.session.add(payment)
            db.session.commit()
            
            # Send confirmation email
            send_order_confirmation_email(order)
            
            logger.info(
                f"Payment processed successfully for order {order.id}",
                extra={'user_id': current_user.id}
            )
            
            return jsonify({
                'success': True,
                'order_id': order.id,
                'message': 'Payment processed successfully'
            }), 200
            
        else:
            # Payment not yet completed (3D Secure, etc.)
            logger.info(
                f"Payment pending for order {order.id}: {intent['status']}"
            )
            return jsonify({
                'success': False,
                'status': intent['status'],
                'message': 'Payment processing'
            }), 202
            
    except stripe.error.CardError as e:
        # Card declined
        logger.warning(
            f"Card declined for order {order.id}: {e.user_message}",
            extra={'user_id': current_user.id}
        )
        return jsonify({
            'error': e.user_message,
            'code': e.code
        }), 402
        
    except stripe.error.RateLimitError:
        # Too many requests to Stripe
        logger.error("Stripe rate limit exceeded")
        return jsonify({'error': 'Service temporarily unavailable'}), 503
        
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters
        logger.error(f"Invalid Stripe request: {e}")
        return jsonify({'error': 'Invalid payment details'}), 400
        
    except Exception as e:
        # Unexpected error
        logger.error(
            f"Unexpected error processing payment: {str(e)}",
            extra={'user_id': current_user.id},
            exc_info=True
        )
        # Rollback transaction
        db.session.rollback()
        return jsonify({'error': 'Payment processing failed'}), 500
```

---

## Performance Optimization

### Database Optimization

#### Indexing Strategy
```sql
-- User queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Product queries
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_stock ON products(stock);

-- Order queries
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_status ON orders(status);

-- Cart queries
CREATE INDEX idx_cart_user_id ON cart(user_id);
CREATE INDEX idx_cart_expires_at ON cart(expires_at);

-- Payment queries
CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_status ON payments(status);
```

#### Query Optimization
- Use SELECT specific columns, not SELECT *
- Implement pagination for large result sets
- Use JOIN instead of multiple queries
- Cache frequently accessed data in Redis
- Use database connection pooling

### Caching Strategy

```python
# Cache product catalog (1 hour)
@cache.cached(timeout=3600)
def get_product_by_id(product_id):
    return Product.query.get(product_id)

# Cache category listings (30 minutes)
@cache.cached(timeout=1800)
def get_products_by_category(category):
    return Product.query.filter_by(category=category).all()

# Cache user sessions (Redis)
# 30-minute inactivity timeout
# Stored in Redis for distributed access
```

### Frontend Optimization
- Minify CSS and JavaScript
- Compress images
- Lazy load product images
- Use CDN for static assets
- Implement browser caching headers

---

## Monitoring & Observability

### Application Metrics

```python
# User metrics
- Active users (daily, monthly)
- New registrations
- Login success/failure rate
- Password reset requests

# Product metrics
- Product views
- Search queries
- Category popularity
- Stock levels

# Order metrics
- Orders per day
- Average order value
- Conversion rate
- Cart abandonment rate

# Payment metrics
- Payment success rate
- Failed payments
- Payment methods used
- Average payment time

# Performance metrics
- Page load time
- API response time
- Database query time
- Cache hit rate
```

### Health Checks

```bash
# Database connectivity
SELECT 1;

# Redis connectivity
redis-cli ping

# Payment gateway
curl https://api.stripe.com/v1/account

# Email service
Test email delivery

# SSL certificate
openssl x509 -in cert.pem -noout -dates
```

### Error Tracking

```python
# Log all errors with context
logger.error(
    f"Payment processing failed",
    extra={
        'user_id': user_id,
        'order_id': order_id,
        'amount': amount,
        'error_code': error_code
    },
    exc_info=True
)

# Alert on critical errors
- Database connection failures
- Payment gateway errors
- Authentication failures
- Data integrity violations
```

---

## Development Workflow

### Local Setup

```bash
# Clone repository
git clone https://github.com/Amruta101998/Ecommerce-website.git
cd Ecommerce-website

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python scripts/init_db.py

# Run migrations
flask db upgrade

# Start development server
python run.py

# Run tests
pytest tests/
```

### Development Process

1. **Create feature branch**
   ```bash
   git checkout -b feature/new-payment-method
   ```

2. **Implement feature**
   - Write tests first (TDD)
   - Implement feature code
   - Add security measures
   - Update documentation

3. **Verify security**
   - Input validation
   - SQL injection prevention
   - XSS prevention
   - CSRF protection
   - Password security

4. **Run tests**
   ```bash
   pytest tests/ --cov
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add: New payment method support"
   git push origin feature/new-payment-method
   ```

---

## Contributing Guidelines

### Security Checklist

- [ ] All inputs validated and sanitized
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (HTML escaping)
- [ ] CSRF tokens on all forms
- [ ] Passwords hashed with bcrypt
- [ ] No sensitive data in logs
- [ ] HTTPS enforced
- [ ] Rate limiting implemented
- [ ] Error messages don't expose system details
- [ ] Security tests written and passing

### Code Review Checklist

- [ ] Code follows style guide
- [ ] Tests written and passing (90%+ coverage)
- [ ] Security measures implemented
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Database migrations created
- [ ] Performance impact assessed
- [ ] Commit messages descriptive

---

## Resources & References

### Security Resources
- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **PCI DSS Compliance:** https://www.pcisecuritystandards.org/
- **Bcrypt Guide:** https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- **SQL Injection Prevention:** https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html

### Payment Processing
- **Stripe Documentation:** https://stripe.com/docs
- **PayPal Documentation:** https://developer.paypal.com/
- **3D Secure Guide:** https://stripe.com/docs/payments/3d-secure

### Database
- **PostgreSQL Docs:** https://www.postgresql.org/docs/
- **SQLAlchemy ORM:** https://docs.sqlalchemy.org/
- **Database Optimization:** https://use-the-index-luke.com/

### Testing
- **pytest Documentation:** https://docs.pytest.org/
- **Mocking Guide:** https://docs.python.org/3/library/unittest.mock.html

---

## FAQ

**Q: How do I securely store payment information?**  
A: Use Stripe/PayPal tokenization. Never store full card numbers. Comply with PCI DSS.

**Q: How is the password hashing implemented?**  
A: Bcrypt with minimum 10 rounds. Use `bcrypt.hashpw()` for hashing, `bcrypt.checkpw()` for verification.

**Q: How do I prevent SQL injection?**  
A: Use parameterized queries with ORM. Never concatenate user input into SQL strings.

**Q: How do I prevent XSS attacks?**  
A: Escape all user input in templates. Use Jinja2's auto-escaping. Sanitize HTML if needed.

**Q: How do I implement CSRF protection?**  
A: Use Flask-WTF CSRF tokens. Include token in all forms. Validate on POST/PUT/DELETE.

---

## License & Attribution

This e-commerce platform is designed for educational and commercial use with full security compliance.

**Last Updated:** 2026-05-04  
**Version:** 1.0.0  
**Maintainer:** Amruta
