# Nguyen Phu Huy

**Senior Software Engineer | Business Complexity Specialist**
Ho Chi Minh City, Vietnam
(+84) 353.072.938 · huy.nguyen.it.work@gmail.com
LinkedIn: linkedin.com/in/nguyen-phu-huy-580180250/

## Profile

Senior Software Engineer with 6+ years of experience building enterprise systems, specializing in turning **complex business processes and domain logic** into stable, accurate, and long-term maintainable software.
Experienced across **F&B, Retail, Manufacturing, ERP, POS, and Finance**, acting as the bridge between business and technology. Core strengths: **business modeling, system integration, backend engineering, architecture, and reliability**.
Hands-on experience with **SAP ↔ E-commerce ↔ POS** integrations, ERP, and internal business systems; designed **validation, retry, idempotency, monitoring, and auto-healing** mechanisms to control errors and keep data in sync.
Primary technical foundation: **.NET/C#** and **Python/Odoo**. Ready to transfer architectural thinking and system design practices to **Java (Spring Boot)** and **Golang** environments.

## Core Capabilities

| Capability                  | Scope                                                                                    |
| --------------------------- | ---------------------------------------------------------------------------------------- |
| **Business Modeling**       | Business rules, business logic, workflows, business processes                            |
| **System Integration**      | POS, SAP, e-commerce, REST API, webhooks, data synchronization                           |
| **Architecture**            | Clean architecture, API design, schema design, microservices                             |
| **Reliability**             | Validation, retry, fallback, idempotency, monitoring, tracing, auto-healing              |
| **Backend Core**            | .NET/C#, ASP.NET Core, Python/Odoo                                                       |
| **Tech Expansion**          | Java (Spring Boot ecosystem), Golang (concurrency, Gin framework)                        |
| **Database Design**         | SQL Server, PostgreSQL, MySQL, schema design, query optimization                         |
| **Documentation**           | Technical specifications, BRD, UML, API contracts                                        |
| **AI-Assisted Engineering** | AI coding assistants, code review, debugging, testing, technical research, documentation |
| **Supporting**              | Docker, Linux/Unix, CLI, Bash, Angular, ReactJS, TypeScript/JavaScript                   |
| **Language**                | English: proficient in reading in-depth technical documentation                          |

## Professional Experience

### DCorp Technology Corporation

**Senior Developer · 10/2025 – Present**
**POS Integration Platform: SAP ↔ E-commerce ↔ POS**
**Business Problem**
An F&B chain needed to synchronize data across multiple systems. Master data, sales, and promotion data had to be transmitted **completely, accurately, and on time**, while connections between systems could be interrupted and promotion logic involved many rules.
**Solution**

- Collaborated with the BA and PM to analyze requirements and design the integration solution.
- Designed a **promotion engine** to translate e-commerce promotion scenarios down to the RK7 POS.
- Designed the data layer and API contracts for menus, products, prices, stores, bills, and store data.
- Built **validation rules** for promotion types such as open discounts and order discounts.
- Built a **queue, retry, and fallback** mechanism via RefAgent so synchronization can continue when connections are interrupted.
- Designed the SkyTransfer and SkyCRM schemas to track **sync task status** and timelines.
- Applied **idempotency** to prevent duplicate data during retries.
- Standardized **logging, tracing, monitoring, and auto-healing**.
  **Impact**
- Faulty data is detected and blocked at the validation layer.
- Synchronization can resume after connection interruptions.
- Sync history and status are available for auditing and debugging.
- **Reduced production incident investigation and resolution time by 40%.**
  **Technology:** .NET Core 6–10, PostgreSQL, SQL Server, MySQL, XML, Next.js, GitLab, Grafana

### Nagakawa Joint Stock Company

**ERP Developer · 08/2023 – 10/2025**
**Internal ERP for Manufacturing Enterprises**
**Business Problem**
The company needed to digitize many internal processes and replace legacy software. Business requirements differed across manufacturing, HR, accounting, warehouse, and approval workflows.
**Solution**

- Developed modules for **proposals, workflows, projects, HR, notifications, and operations overview**.
- Customized the system for the business needs of multiple enterprises: urban landscaping, garment manufacturing, refrigeration/home appliances, mechanical & electrical engineering, and construction.
- Developed the backend in **Python/Odoo** and customized the frontend with XML/JavaScript.
- Carried out migration from the Base platform to Odoo.
- Wrote technical specifications for the modules.
- Performed unit testing, UAT, bug fixing, and performance optimization.
- Used Docker to standardize the development environment.
  **Impact**
- The new system **fully replaced the legacy software**.
- Enabled digitization of internal operations on a single unified system.
- **Saved 100% of license costs** by migrating from Base to Odoo.
  **Technology:** Python, Odoo, PostgreSQL, XML, JavaScript, Docker, Git

### Hachinet Vietnam Trading Solutions Joint Stock Company

**IT Engineer Staffing · 07/2020 – 07/2023**

#### RJ Travels Web Portal

**Business Problem:** The system needed to manage multiple types of travel services and customer care.
**Solution:** Developed the Angular frontend and ASP.NET Boilerplate backend, designed the database and queries, containerized backend services with Docker, wrote unit tests, and maintained the system.
**Technology:** Angular 16, ASP.NET Boilerplate, SQL Server, Docker, Git

#### Lightning BIM: ARENT Inc., Japan

**Business Problem:** Support the creation and optimization of rebar layouts in construction projects on the Revit platform.
**Solution:** Developed modules for rebar processing, clash detection alerts, and sections; researched and integrated the Revit API; stored data using Extensible Storage; built tests with NUnit and Revit.TestRunner.
**Technology:** C#, WPF, .NET Framework 4.7.2, Revit API, Git

#### eGov: Bkav Corporation

**Business Problem:** Manage electronic documents and processing workflows for e-government.
**Solution:** Analyzed requirements and developed modules for documents, processing, authorization, and workflows; integrated APIs with ASP.NET MVC5.
**Technology:** C#, ASP.NET MVC5/Web API, Entity Framework 6, BackboneJS, MySQL

### DFT Vietnam Technology Joint Stock Company

**Full Stack Developer · 06/2018 – 06/2020**

#### FinPortal: Thinh Phat Portal

**Business Problem:** Manage vouchers/documents, control approvals, and track cash flow for an internal financial system.
**Solution:** Designed and developed APIs for voucher management, controlled the approval workflow, and integrated visual reporting.
**Technology:** C#, ASP.NET Boilerplate, Angular, SQL Server, Chart.js

#### MobiFone Customer Portal

**Business Problem:** Provide a portal for managing telecom services, transactions, and service registration.
**Solution:** Developed account management, transaction history, and promotion notifications; participated in deployment and maintenance.
**Technology:** C#, ASP.NET Boilerplate, Angular, SQL Server, Bootstrap

### EZCloud Global

**Full Stack Developer · 11/2016 – 06/2018**

#### EZFolio

**Business Problem:** Manage the entire hotel operation process, including reservations, stays, room rates, housekeeping, reporting, and distribution via OTAs.
**Solution:** Developed reservations, room calendar, flexible pricing, staff permissions, and integrations with OTA channels such as Agoda and Booking.com.
**Technology:** C#, ASP.NET MVC5, SQL Server, Vue.js, Bootstrap

## Education

**Hanoi University of Civil Engineering (HUCE)**
Major: Software Engineering · 2013 – 2017
