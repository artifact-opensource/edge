# Project Management System

A comprehensive project management solution featuring an Angular SPA for tracking projects, tasks, dependencies, and telemetry data.

## 📁 Directory Structure

```
project_management/
├── data/                              # Data Files
│   ├── project.json                   # Main project manifest
│   ├── executive-roadmap.md           # Strategic roadmap
│   └── projects-dashboard.csv         # Operational telemetry
│
├── src/                               # Angular Application Source
│   ├── app/
│   │   ├── core/services/            # Core services (Data, Theme)
│   │   ├── features/dashboard/       # Dashboard feature
│   │   ├── models/                   # TypeScript data models
│   │   ├── theme/                    # Abstract theming system
│   │   └── shared/                   # Reusable components
│   └── assets/                       # Static assets
│
├── DESIGN_ITERATION_1.md             # Initial architecture
├── DESIGN_ITERATION_2.md             # Enhanced design
├── DESIGN_ITERATION_3.md             # Final production design
│
└── README_APP.md                      # Detailed application docs
```

## → Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

Application runs at **http://localhost:4200**

## ■ Data Sources

1. **project.json** - Complete project manifest with status, health, financials
2. **executive-roadmap.md** - Strategic planning and milestones
3. **projects-dashboard.csv** - Real-time operational telemetry

## ◆ Theming System - Zero Hardcoding

**Key Innovation**: All colors and styling are abstracted!

- Theme definitions in TypeScript
- Applied via CSS custom properties
- Runtime theme switching
- No hardcoded colors anywhere

See README_APP.md for complete theming documentation.

## 🏗️ Architecture

### Services
- **DataLoaderService** - Loads JSON/CSV/Markdown data
- **ProjectService** - Manages project state
- **TelemetryService** - Calculates metrics from CSV
- **ThemeService** - Manages abstract theming

### Components
- **DashboardComponent** - Main view with metrics and projects

## 📐 Design Documentation

Three comprehensive design iterations in `DESIGN_ITERATION_*.md` files covering:
- Architecture and requirements
- Theming abstraction and data flow
- Production-ready specifications

## ◉ Key Features

✓ **Abstract Theming** - Zero hardcoded styles  
✓ **Real-time Metrics** - Dashboard with portfolio insights  
✓ **Multiple Data Sources** - JSON, CSV, Markdown integration  
✓ **Performance Optimized** - Fast loading, efficient rendering  
✓ **User-Friendly** - Intuitive interface, zero learning curve  

## 📖 Documentation

- **README_APP.md** - Comprehensive application guide
- **DESIGN_ITERATION_*.md** - Complete design process

---

**Version**: 1.0.0 | **Status**: ✓ Production Ready  
**Artifact Virtual (SMC-Private) Limited** - Internal Tool
