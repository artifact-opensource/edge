#!/usr/bin/env python3
"""
Artifact Virtual GRC Audit Runner
Automated compliance checking and report generation

Usage:
    python3 audit_runner.py [--report] [--check CONTROL_ID]
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
AUDIT_ROOT = Path(__file__).parent.parent
GRC_ROOT = Path(__file__).parent
CONTROLS_FILE = GRC_ROOT / "controls.json"
MATRIX_FILE = GRC_ROOT / "compliance-matrix.json"
EVIDENCE_ROOT = AUDIT_ROOT / "evidence"
REPORTS_ROOT = AUDIT_ROOT / "reports"


class AuditRunner:
    """Main audit runner class."""
    
    def __init__(self):
        self.controls = self._load_controls()
        self.matrix = self._load_matrix()
        self.results = []
        
    def _load_controls(self) -> Dict:
        """Load control definitions."""
        if CONTROLS_FILE.exists():
            with open(CONTROLS_FILE) as f:
                return json.load(f)
        return {"controls": [], "summary": {}}
    
    def _load_matrix(self) -> Dict:
        """Load compliance matrix."""
        if MATRIX_FILE.exists():
            with open(MATRIX_FILE) as f:
                return json.load(f)
        return {}
    
    def check_control(self, control_id: str) -> Dict:
        """Check a specific control for compliance."""
        control = next(
            (c for c in self.controls.get("controls", []) if c["id"] == control_id),
            None
        )
        if not control:
            return {"error": f"Control {control_id} not found"}
        
        result = {
            "control_id": control_id,
            "control": control["control"],
            "status": control["status"],
            "priority": control["priority"],
            "checks": []
        }
        
        # Check evidence exists
        evidence_paths = control.get("evidence", [])
        for evidence_path in evidence_paths:
            full_path = AUDIT_ROOT.parent / evidence_path.lstrip("/")
            exists = full_path.exists()
            result["checks"].append({
                "type": "evidence_exists",
                "path": evidence_path,
                "passed": exists
            })
        
        # Check review date
        last_reviewed = control.get("lastReviewed")
        if last_reviewed:
            review_date = datetime.fromisoformat(last_reviewed)
            days_since = (datetime.now() - review_date).days
            result["checks"].append({
                "type": "review_currency",
                "days_since_review": days_since,
                "passed": days_since <= 90  # 90 day review cycle
            })
        else:
            result["checks"].append({
                "type": "review_currency",
                "days_since_review": None,
                "passed": False,
                "note": "Never reviewed"
            })
        
        # Determine overall check result
        all_passed = all(c["passed"] for c in result["checks"])
        result["overall_passed"] = all_passed
        
        return result
    
    def run_all_checks(self) -> List[Dict]:
        """Run checks on all controls."""
        results = []
        for control in self.controls.get("controls", []):
            result = self.check_control(control["id"])
            results.append(result)
        return results
    
    def calculate_readiness(self) -> Dict:
        """Calculate overall compliance readiness."""
        controls = self.controls.get("controls", [])
        total = len(controls)
        
        if total == 0:
            return {"readiness_percent": 0, "total": 0}
        
        status_counts = {
            "compliant": 0,
            "in_progress": 0,
            "not_started": 0,
            "non_compliant": 0
        }
        
        for control in controls:
            status = control.get("status", "not_started")
            if status in status_counts:
                status_counts[status] += 1
        
        # Readiness = compliant + (in_progress * 0.5)
        readiness = (status_counts["compliant"] + status_counts["in_progress"] * 0.5) / total * 100
        
        return {
            "readiness_percent": round(readiness, 1),
            "total": total,
            "status_counts": status_counts,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_report(self, output_format: str = "json") -> str:
        """Generate compliance report."""
        results = self.run_all_checks()
        readiness = self.calculate_readiness()
        
        report = {
            "report_type": "compliance_audit",
            "generated_at": datetime.now().isoformat(),
            "organization": "Artifact Virtual (SMC-Private) Limited",
            "readiness": readiness,
            "control_results": results,
            "frameworks": list(self.matrix.get("frameworkMappings", {}).keys()),
            "recommendations": self._generate_recommendations(results)
        }
        
        if output_format == "json":
            return json.dumps(report, indent=2)
        elif output_format == "markdown":
            return self._report_to_markdown(report)
        
        return json.dumps(report, indent=2)
    
    def _generate_recommendations(self, results: List[Dict]) -> List[Dict]:
        """Generate recommendations based on audit results."""
        recommendations = []
        
        # Find P0 controls not compliant
        for control in self.controls.get("controls", []):
            if control["priority"] == "P0" and control["status"] != "compliant":
                recommendations.append({
                    "priority": "CRITICAL",
                    "control_id": control["id"],
                    "recommendation": f"Complete {control['control']} implementation immediately",
                    "rationale": "P0 control required for baseline security"
                })
        
        # Find controls without evidence
        for result in results:
            for check in result.get("checks", []):
                if check["type"] == "evidence_exists" and not check["passed"]:
                    recommendations.append({
                        "priority": "HIGH",
                        "control_id": result["control_id"],
                        "recommendation": f"Add evidence for {result['control']}",
                        "rationale": f"Evidence path {check['path']} not found"
                    })
        
        return recommendations
    
    def _report_to_markdown(self, report: Dict) -> str:
        """Convert report to markdown format."""
        lines = [
            "# GRC Compliance Audit Report",
            "",
            f"**Generated:** {report['generated_at']}",
            f"**Organization:** {report['organization']}",
            "",
            "## Readiness Summary",
            "",
            f"- **Overall Readiness:** {report['readiness']['readiness_percent']}%",
            f"- **Total Controls:** {report['readiness']['total']}",
            f"- **Compliant:** {report['readiness']['status_counts']['compliant']}",
            f"- **In Progress:** {report['readiness']['status_counts']['in_progress']}",
            f"- **Not Started:** {report['readiness']['status_counts']['not_started']}",
            "",
            "## Recommendations",
            ""
        ]
        
        for rec in report.get("recommendations", []):
            lines.append(f"### [{rec['priority']}] {rec['control_id']}")
            lines.append(f"- **Recommendation:** {rec['recommendation']}")
            lines.append(f"- **Rationale:** {rec['rationale']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def save_report(self, report: str, filename: str = None):
        """Save report to file."""
        REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audit_report_{timestamp}.json"
        
        output_path = REPORTS_ROOT / filename
        with open(output_path, "w") as f:
            f.write(report)
        
        print(f"Report saved to: {output_path}")
        return output_path


def main():
    """Main entry point."""
    runner = AuditRunner()
    
    args = sys.argv[1:]
    
    if "--check" in args:
        idx = args.index("--check")
        if idx + 1 < len(args):
            control_id = args[idx + 1]
            result = runner.check_control(control_id)
            print(json.dumps(result, indent=2))
        else:
            print("Error: --check requires a control ID")
            sys.exit(1)
    
    elif "--report" in args:
        report = runner.generate_report("json")
        runner.save_report(report)
        print("\nReport generated successfully.")
        
        # Print summary
        readiness = runner.calculate_readiness()
        print(f"\nReadiness: {readiness['readiness_percent']}%")
        print(f"Compliant: {readiness['status_counts']['compliant']}")
        print(f"In Progress: {readiness['status_counts']['in_progress']}")
        print(f"Not Started: {readiness['status_counts']['not_started']}")
    
    elif "--summary" in args:
        readiness = runner.calculate_readiness()
        print(json.dumps(readiness, indent=2))
    
    else:
        print("Artifact Virtual GRC Audit Runner")
        print("=" * 40)
        print()
        print("Usage:")
        print("  python3 audit_runner.py --report    Generate full audit report")
        print("  python3 audit_runner.py --summary   Show readiness summary")
        print("  python3 audit_runner.py --check ID  Check specific control")
        print()
        
        # Show quick summary
        readiness = runner.calculate_readiness()
        print(f"Current Readiness: {readiness['readiness_percent']}%")


if __name__ == "__main__":
    main()
