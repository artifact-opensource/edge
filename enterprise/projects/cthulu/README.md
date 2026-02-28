# Cthulu Trading System

> MQL5/MetaTrader 5 trading system with GCP VM deployment

---

## 📁 Project Structure

### Documentation
- **[SUBPROGRAM_RECOMMENDATIONS.md](SUBPROGRAM_RECOMMENDATIONS.md)** - Recommended subprograms and modules
- **[gcp_accesscontrol.md](gcp_accesscontrol.md)** - GCP access control configuration

### System Review
Complete system review documentation:
- **[EXECUTIVE_SUMMARY.md](review/EXECUTIVE_SUMMARY.md)** - Executive summary
- **[COMPREHENSIVE_SYSTEM_REVIEW.md](review/COMPREHENSIVE_SYSTEM_REVIEW.md)** - Detailed system review
- **[SYSTEM_OVERVIEW_COMPACT.md](review/SYSTEM_OVERVIEW_COMPACT.md)** - Compact overview
- **[REVIEW_SUMMARY_TABLE.md](review/REVIEW_SUMMARY_TABLE.md)** - Summary table
- **[REVIEW_DOCS_README.md](review/REVIEW_DOCS_README.md)** - Review documentation index

---

## 🖥️ Infrastructure

### GCP VM Instance
- **Type**: n2-standard-2 Spot instance
- **OS**: Ubuntu 22.04 host + Windows 11 container
- **External IP**: 34.171.231.16 [DECOMMISSIONED] (see internal access record for current status)

### Access Points
| Service | Port | Notes |
|---------|------|-------|
| Windows 11 Desktop | 8006 | Remote desktop access |
| VS Code Server | 8443 | Remote development |

---

## → Deployment

### Current Status
The system is deployed on GCP with:
- Dedicated VM for trading operations
- MetaTrader 5 platform
- VS Code Server for remote development
- Repository cloned and ready for configuration

### Setup Documentation
See the following for deployment and setup:
- Virtual machine access guide (internal)
- SSH setup instructions (internal)
- Working directory status (internal)

---

## 🛠️ Platform

### MetaTrader 5
- **Language**: MQL5
- **Platform**: MetaTrader 5
- **Purpose**: Algorithmic trading strategy execution

### Integration
- Works with GoldMax market analysis system
- Coordinates with Herald execution agent
- VM-based persistent runtime

---

## ▫ Related Documentation

### MQL5 Development
- [MQL5 Handbook](../../docs/research/mql5/README.md) - Comprehensive MQL5 strategy documentation
- [MQL5 Manifest](../../docs/research/mql5/manifest.md) - Strategy catalog

### Infrastructure
- [Architecture Overview](../../03_INFRA_MAP.md) - System architecture
- [GCP Startup Scripts](../../../scripts/) - Deployment automation

---

## 🔧 Scripts & Utilities

Relevant scripts for Cthulu operations:
- `gcp_startup_odyssey.sh` - GCP startup automation
- `mt5_automate.sh` - MT5 automation
- `desktop_launch_herald_and_mt5.ps1` - Launch script
- `integration_run_dry.ps1` - Integration testing

---

## 📝 Next Steps

1. Complete MetaTrader 5 configuration
2. Deploy trading strategies from MQL5 handbook
3. Configure integration with Herald execution agent
4. Set up monitoring and logging

---

## 🔒 Security & Access

- **Private Repository**: Access controlled
- **GCP Access**: Restricted to authorized users
- **VM Access**: SSH key authentication required
- Credentials are stored in the internal secrets registry

---

## ☎ Contact

For questions or access requests, contact: [`amuzetnoM`](https://github.com/amuzetnoM)

---

*Part of the Gladius research repository*
