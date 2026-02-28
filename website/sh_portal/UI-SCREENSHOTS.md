# Stakeholder Portal 2.0 - UI Documentation

## Visual Design System

### Color Palette
- **Primary Blue**: #3B82F6 (Tailwind blue-500)
- **Success Green**: #10B981 (Tailwind emerald-500)
- **Warning Orange**: #F59E0B (Tailwind amber-500)
- **Error Red**: #EF4444 (Tailwind red-500)
- **Purple Accent**: #8B5CF6 (Tailwind violet-500)
- **Gray Scale**: #111827 to #F9FAFB (Tailwind gray)

---

## 1. Analytics Dashboard - Overview Tab

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  📊 Analytics                                    [Overview] [Products] [Query]  │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │💰 Revenue   │  │👥 Users     │  │🛒 Orders    │  │⭐ Rating    │          │
│  │  $1.85M     │  │  45.2K      │  │  12.4K      │  │  4.7/5      │          │
│  │  ↑ +15.3%   │  │  ↑ +12.7%   │  │  ↑ +8.2%    │  │  ↑ +0.3     │          │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐    │
│  │  Revenue Trend (Last 30 Days)                                         │    │
│  │                                                                        │    │
│  │  $200K ┤                                               ╭─────────╮    │    │
│  │        │                                        ╭──────╯          ╰─  │    │
│  │  $150K ┤                            ╭──────────╯                     │    │
│  │        │                    ╭───────╯                                 │    │
│  │  $100K ┤        ╭──────────╯                                          │    │
│  │        │╭───────╯                                                     │    │
│  │   $50K ┼────────────────────────────────────────────────────────────→│    │
│  │        │  Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec │    │
│  └───────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ┌──────────────────────────┐  ┌──────────────────────────────────────────┐  │
│  │ Revenue by Category      │  │ Regional Performance                     │  │
│  │                          │  │                                          │  │
│  │  Enterprise    $450K ██  │  │  North America    $520K   ↑ +15.3%  ███ │  │
│  │  Professional  $280K ██  │  │  Europe           $380K   ↑ +12.7%  ██  │  │
│  │  Starter       $120K █   │  │  Asia Pacific     $290K   ↑ +28.4%  ██  │  │
│  │  Individual     $80K █   │  │  Latin America    $125K   ↑ +19.1%  █   │  │
│  │                          │  │  Middle East       $95K   ↑ +22.6%  █   │  │
│  └──────────────────────────┘  └──────────────────────────────────────────┘  │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐    │
│  │  User Activity Heatmap                                                │    │
│  │                                                                        │    │
│  │       00:00  04:00  08:00  12:00  16:00  20:00                        │    │
│  │  Mon    ░      ░      ██     ███     ██      █                        │    │
│  │  Tue    ░      ░      ██     ███     ██      █                        │    │
│  │  Wed    ░      ░      ██     ███     ███     █                        │    │
│  │  Thu    ░      ░      ██     ███     ███     ██                       │    │
│  │  Fri    ░      ░      ███    ███     ███     ██                       │    │
│  │  Sat    █      ░      ██     ██      ██      █                        │    │
│  │  Sun    █      ░      █      ██      █       ░                        │    │
│  │                                                                        │    │
│  │  ░ Low    █ Medium    ██ High    ███ Very High                        │    │
│  └───────────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────────────┘
```

**Key Features:**
- 4 metric cards with trend indicators (up/down arrows)
- Interactive line chart with 30-day revenue trend
- Pie chart showing revenue by category breakdown
- Bar chart comparing regional performance with growth rates
- Heatmap visualization showing user activity patterns by day and hour
- Responsive grid layout adapting to screen size
- Color-coded status indicators (green=up, red=down)

---

## 2. Analytics Dashboard - Products Tab

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  📊 Analytics                                    [Overview] [Products] [Query]  │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │  Product Performance                           [🔍 Search] [⬇️ Export CSV] │ │
│  ├──────────────┬──────────┬──────────┬───────┬────────┬────────────────────┤ │
│  │ Product      │ Category │ Revenue  │ Units │ Rating │ Trend              │ │
│  ├──────────────┼──────────┼──────────┼───────┼────────┼────────────────────┤ │
│  │ Artifact ERP │Enterprise│ $425,000 │   89  │ 4.9 ⭐ │ ↗️ Up    [████░░]  │ │
│  │ ARC Vector DB│ AI/ML    │ $285,000 │  145  │ 4.8 ⭐ │ ↗️ Up    [███░░░]  │ │
│  │ HEKTOR       │ AI/ML    │ $195,000 │  112  │ 4.7 ⭐ │ ↗️ Up    [███░░░]  │ │
│  │ GLADIUS      │ Security │ $165,000 │   98  │ 4.6 ⭐ │ → Stable [██░░░░]  │ │
│  │ Sentinel     │ AI/ML    │ $148,000 │   76  │ 4.5 ⭐ │ ↗️ Up    [██░░░░]  │ │
│  │ GOLDMAX      │Collab    │ $132,000 │  234  │ 4.4 ⭐ │ ↘️ Down  [██░░░░]  │ │
│  │ Outcome      │Blockchain│ $118,000 │   45  │ 4.3 ⭐ │ → Stable [█░░░░░]  │ │
│  │ AVPM         │Operations│  $95,000 │   67  │ 4.2 ⭐ │ ↗️ Up    [█░░░░░]  │ │
│  ├──────────────┴──────────┴──────────┴───────┴────────┴────────────────────┤ │
│  │  ← Previous   1  2  3  [4]  5  6  7  8  9  10   Next →                   │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌──────────────────────────┐  ┌──────────────────────────────────────────┐  │
│  │ Top Performers (Revenue) │  │ Category Distribution                    │  │
│  │                          │  │                                          │  │
│  │  Artifact ERP   ████████ │  │  AI/ML         35%  ████████             │  │
│  │  ARC Vector DB  ██████   │  │  Enterprise    28%  ██████               │  │
│  │  HEKTOR         ████     │  │  Security      18%  ████                 │  │
│  │  GLADIUS        ███      │  │  Operations    12%  ███                  │  │
│  │  Sentinel       ███      │  │  Blockchain     7%  ██                   │  │
│  └──────────────────────────┘  └──────────────────────────────────────────┘  │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐    │
│  │  Customer Segments                                                    │    │
│  ├───────────────┬───────────┬─────────────┬──────────────────────────────┤   │
│  │ Segment       │ Customers │ Revenue     │ Avg Order Value              │   │
│  ├───────────────┼───────────┼─────────────┼──────────────────────────────┤   │
│  │ Enterprise    │    145    │  $850,000   │  $5,862   ████████████████   │   │
│  │ Professional  │    892    │  $445,000   │    $499   ████               │   │
│  │ Startup       │  1,243    │  $248,000   │    $199   ██                 │   │
│  │ Individual    │  3,421    │  $171,000   │     $50   ░                  │   │
│  └───────────────┴───────────┴─────────────┴──────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────┘
```

**Key Features:**
- Advanced data table with sorting, filtering, and pagination
- Export to CSV/Excel/PDF functionality
- Visual trend indicators (up/down/stable arrows)
- Progress bars showing relative performance
- Star ratings for product quality
- Bar charts for top performers
- Pie chart for category distribution
- Customer segment analysis table
- Search and filter controls
- Responsive table design with horizontal scroll on mobile

---

## 3. Analytics Dashboard - Query Builder Tab

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  📊 Analytics                                    [Overview] [Products] [Query]  │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐    │
│  │  🔍 Query Builder                                                     │    │
│  ├───────────────────────────────────────────────────────────────────────┤    │
│  │                                                                        │    │
│  │  Data Source: [Stakeholders ▼]                                        │    │
│  │                                                                        │    │
│  │  ┌──────────────────────────────────────────────────────────────┐    │    │
│  │  │  Fields to Display:                                          │    │    │
│  │  │  ☑ Name        ☑ Email         ☑ Tier       ☐ Department     │    │    │
│  │  │  ☑ Joined Date ☑ Last Activity ☐ Documents  ☐ Comments      │    │    │
│  │  └──────────────────────────────────────────────────────────────┘    │    │
│  │                                                                        │    │
│  │  ┌──────────────────────────────────────────────────────────────┐    │    │
│  │  │  Filters:                                                    │    │    │
│  │  │                                                              │    │    │
│  │  │  Tier          [is]          [EXECUTIVE ▼]      [+ Add]     │    │    │
│  │  │  Last Activity [after]       [2024-01-01]       [+ Add]     │    │    │
│  │  │  Documents     [greater than][10          ]     [+ Add]     │    │    │
│  │  │                                                              │    │    │
│  │  │  [+ Add Filter]                                              │    │    │
│  │  └──────────────────────────────────────────────────────────────┘    │    │
│  │                                                                        │    │
│  │  Sort By: [Last Activity ▼]  [Descending ▼]                          │    │
│  │                                                                        │    │
│  │  Limit: [100 ▼] records                                               │    │
│  │                                                                        │    │
│  │  [ Run Query ]  [ Save Query ]  [ Export Results ]                    │    │
│  └───────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐    │
│  │  📊 Query Results (24 records)                       [⬇️ Export CSV]  │    │
│  ├──────────────┬─────────────────┬──────────┬────────────┬──────────────┤   │
│  │ Name         │ Email           │ Tier     │ Joined     │ Last Activity│   │
│  ├──────────────┼─────────────────┼──────────┼────────────┼──────────────┤   │
│  │ John Smith   │ john@example.com│EXECUTIVE │ 2023-01-15 │ 2024-02-05   │   │
│  │ Jane Doe     │ jane@example.com│STRATEGIC │ 2023-03-22 │ 2024-02-04   │   │
│  │ Bob Johnson  │ bob@example.com │STANDARD  │ 2023-06-10 │ 2024-02-03   │   │
│  │ Alice Brown  │alice@example.com│EXECUTIVE │ 2023-02-18 │ 2024-02-02   │   │
│  │ ...          │ ...             │ ...      │ ...        │ ...          │   │
│  ├──────────────┴─────────────────┴──────────┴────────────┴──────────────┤   │
│  │  Showing 1-10 of 24   ← 1 2 3 →                                        │   │
│  └───────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐      │
│  │  💾 Saved Queries                                                   │      │
│  │  • Active Executive Stakeholders                      [Load] [×]    │      │
│  │  • High-Value Partners Last 30 Days                   [Load] [×]    │      │
│  │  • Recently Joined Users                              [Load] [×]    │      │
│  └─────────────────────────────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────────────────────────────┘
```

**Key Features:**
- Visual query builder interface (no SQL required)
- Dynamic field selection with checkboxes
- Multiple filter conditions with AND/OR logic
- Sorting and limiting options
- Real-time query execution
- Export results to CSV/Excel/PDF
- Save and reuse queries
- Results displayed in interactive table
- Drag-and-drop query building (planned)

---

## 4. Dashboard Page

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  🏠 Dashboard                                        [Profile ▼]  [🔔 3]  [⚙️]  │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Welcome back, John Smith (EXECUTIVE)                                          │
│  Last login: February 7, 2024 at 2:45 PM                                       │
│                                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │📄 Documents │  │💬 Comments  │  │👥 Stakehldrs│  │🔔 Alerts    │          │
│  │     247     │  │     89      │  │    1,234    │  │      3      │          │
│  │  View All → │  │  View All → │  │  View All → │  │  View All → │          │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐    │
│  │  📊 Quick Stats                                                       │    │
│  │                                                                        │    │
│  │  Document Activity (Last 7 Days)                                      │    │
│  │  ████████░░░░░░░░░░░  42 documents created/modified                   │    │
│  │                                                                        │    │
│  │  Engagement Score                                                      │    │
│  │  ████████████████░░░  87% (Excellent)                                 │    │
│  │                                                                        │    │
│  │  Active Stakeholders                                                   │    │
│  │  ████████████░░░░░░░  68% active in last 30 days                      │    │
│  └───────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ┌────────────────────────────────────┐  ┌──────────────────────────────────┐ │
│  │  📢 Recent Activity                │  │  ⭐ Top Documents               │ │
│  │                                    │  │                                  │ │
│  │  🟢 New stakeholder joined         │  │  Q1 2024 Financial Report  4.9⭐ │ │
│  │     Alice Johnson - 2h ago         │  │  Product Roadmap 2024      4.8⭐ │ │
│  │                                    │  │  Market Analysis - USA     4.7⭐ │ │
│  │  📝 Document updated                │  │  Security Audit Report     4.6⭐ │ │
│  │     "API Documentation" - 3h ago   │  │  Partnership Agreement     4.5⭐ │ │
│  │                                    │  │                                  │ │
│  │  💬 New comment                     │  │  [View All Documents →]         │ │
│  │     on "Budget 2024" - 5h ago      │  │                                  │ │
│  │                                    │  │                                  │ │
│  │  [View All Activity →]             │  │                                  │ │
│  └────────────────────────────────────┘  └──────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────┘
```

**Key Features:**
- Personalized welcome message with user tier
- 4 quick metric cards linking to main sections
- Progress bars for key statistics
- Real-time activity feed
- Top documents ranked by rating
- Color-coded status indicators
- Responsive card layout
- Quick navigation to all major sections

---

## 5. Documents Page

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  📄 Documents                                        [+ New Document]  [🔍]     │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Filters: [All Types ▼] [All Tiers ▼] [All Categories ▼] [Date Range ▼]       │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐    │
│  │  Title                                │ Type    │ Tier   │ Modified   │    │
│  ├───────────────────────────────────────┼─────────┼────────┼────────────┤    │
│  │  📊 Q1 2024 Financial Report          │ Report  │ EXEC   │ 2h ago     │    │
│  │  📖 Product Roadmap 2024              │ Plan    │ STRAT  │ 1d ago     │    │
│  │  📈 Market Analysis - United States   │ Report  │ EXEC   │ 3d ago     │    │
│  │  🔐 Security Audit Report Q4 2023     │ Audit   │ LIMIT  │ 1w ago     │    │
│  │  📋 Partnership Agreement Template    │ Legal   │ EXEC   │ 2w ago     │    │
│  │  📝 API Documentation v2.0            │ Tech    │ PUBLIC │ 3w ago     │    │
│  │  📊 Customer Satisfaction Survey      │ Report  │ STRAT  │ 1m ago     │    │
│  │  📄 Employee Handbook 2024            │ Policy  │ STAND  │ 2m ago     │    │
│  ├───────────────────────────────────────┴─────────┴────────┴────────────┤    │
│  │  ← Previous   1  2  3  [4]  5  6  7  8  9  10   Next →                │    │
│  └───────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  [Click any document to view details and download]                             │
└────────────────────────────────────────────────────────────────────────────────┘
```

**Key Features:**
- Document list with sorting and filtering
- Type icons for quick recognition
- Tier-based access control indicators
- Last modified timestamps
- Pagination for large document sets
- Search functionality
- Create new document button
- Quick preview on hover (planned)

---

## 6. Component Library Samples

### Metric Card Component
```
┌──────────────────────┐
│ 💰 Total Revenue     │
│                      │
│    $1,850,000        │
│                      │
│    ↗️ +15.3%          │
│    vs last month     │
└──────────────────────┘
```

### Data Table Component
```
┌────────────────────────────────────────────────────────┐
│  [🔍 Search]  [⬇️ Export]  [⚙️ Columns]  [🔄 Refresh]  │
├─────────┬──────────┬──────────┬──────────┬────────────┤
│ Name ▼  │ Email    │ Status   │ Joined   │ Actions    │
├─────────┼──────────┼──────────┼──────────┼────────────┤
│ John    │ john@... │ 🟢 Active│ 01/15/23 │ [👁️][✏️]  │
│ Jane    │ jane@... │ 🟢 Active│ 03/22/23 │ [👁️][✏️]  │
│ Bob     │ bob@...  │ 🔴 Inact │ 06/10/23 │ [👁️][✏️]  │
├─────────┴──────────┴──────────┴──────────┴────────────┤
│ Showing 1-10 of 247      [←] 1 2 3 [4] 5 6 [→]        │
└────────────────────────────────────────────────────────┘
```

### Chart Components

**Line Chart:**
```
  $200K ┤                     ╭─────────╮
        │              ╭──────╯          ╰─
  $150K ┤      ╭───────╯
        │╭─────╯
  $100K ┼────────────────────────────────→
        │  Jan  Feb  Mar  Apr  May  Jun
```

**Bar Chart:**
```
North America  ████████████ $520K
Europe         █████████    $380K
Asia Pacific   ███████      $290K
Latin America  ███          $125K
```

**Pie Chart:**
```
        ┌───────────┐
        │  ████  35%│  Enterprise
        │██    ██   │
        │█  ⊙   █ 28│  Professional
        │██    ██   │
        │  ████  20%│  Starter
        └───────────┘
```

---

## Design System

### Typography
- **Headings**: Inter font family, font-semibold to font-bold
- **Body**: Inter font family, font-normal
- **Code**: Monospace font family

### Spacing
- **Card Padding**: 1rem to 1.5rem (16px - 24px)
- **Section Margins**: 1.5rem to 2rem (24px - 32px)
- **Component Gaps**: 0.5rem to 1rem (8px - 16px)

### Icons
- **Source**: Heroicons (outline and solid variants)
- **Size**: 1rem to 1.5rem (16px - 24px)
- **Color**: Matches text color or accent colors

### Responsive Breakpoints
- **Mobile**: < 640px (sm)
- **Tablet**: 640px - 1024px (sm to lg)
- **Desktop**: ≥ 1024px (lg+)

### Accessibility
- **Color Contrast**: WCAG AA compliant (4.5:1 minimum)
- **Keyboard Navigation**: Full support with visible focus states
- **Screen Readers**: ARIA labels on all interactive elements
- **Focus Indicators**: Blue ring with 2px width

---

## Interactive Features

### Hover States
- **Cards**: Subtle shadow elevation on hover
- **Buttons**: Background color darkens 10%
- **Table Rows**: Background changes to gray-50
- **Links**: Underline appears on hover

### Loading States
- **Skeleton Screens**: Animated gray bars for content loading
- **Spinners**: Rotating circle for actions in progress
- **Progress Bars**: For long-running operations

### Animations
- **Transitions**: 150ms-300ms ease-in-out
- **Chart Animations**: Smooth data updates with 500ms transitions
- **Modal Entry/Exit**: Fade and scale animation

---

## Export Functionality

### Supported Formats
1. **CSV**: Basic data export for spreadsheets
2. **Excel (XLSX)**: Advanced formatting and multiple sheets
3. **PDF**: Print-ready formatted reports
4. **PNG**: Chart screenshots for presentations

### Export Options
- Current view only or all data
- Include/exclude filtered results
- Custom column selection
- Date range specification

---

## Mobile Responsive Design

### Mobile View (< 640px)
- Single column layout
- Stacked metric cards
- Simplified tables with horizontal scroll
- Collapsible filters
- Touch-optimized buttons (min 44px height)

### Tablet View (640px - 1024px)
- Two column layout for cards
- Full-width tables with scroll
- Side-by-side charts where space permits

### Desktop View (≥ 1024px)
- Multi-column grid layouts
- Full table visibility
- Side-by-side chart comparisons
- Expanded filter panels

---

## Performance Optimizations

- **Lazy Loading**: Charts and heavy components load on demand
- **Pagination**: Default 25-50 items per page
- **Data Caching**: React Query caches API responses
- **Code Splitting**: Route-based code splitting with React.lazy()
- **Image Optimization**: WebP format with fallbacks
- **Debounced Search**: 300ms delay on search inputs

---

This documentation provides a comprehensive visual overview of the Stakeholder Portal 2.0 UI. All components are production-ready, fully responsive, and accessible. The design system ensures consistency across all pages and features.
