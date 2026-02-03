#!/usr/bin/env python3
"""
QA Documentation Validation Test Suite
Validates alignment between JIRA and Confluence requirements

This script parses requirements_mapping.json and identifies:
- MATCH: Fully aligned requirements
- PARTIAL_MATCH: Incomplete or vague alignment
- CONFLICT: Direct contradictions between sources

JIRA Reference: https://bito.atlassian.net/browse/BITO-12071
Confluence Reference: https://bito.atlassian.net/wiki/spaces/EN/pages/1132003418/Quality+Assurance+QA
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class AlignmentStatus(Enum):
    """Enumeration for requirement alignment status."""
    MATCH = "MATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    CONFLICT = "CONFLICT"


@dataclass
class ValidationResult:
    """Data class to hold validation result for a single requirement."""
    req_id: str
    name: str
    status: AlignmentStatus
    severity: str
    notes: str
    recommendation: str = ""


class QADocumentationValidator:
    """
    Validates QA documentation alignment between JIRA and Confluence.
    
    Attributes:
        mapping_file (Path): Path to requirements_mapping.json
        requirements (List[Dict]): Parsed requirements from JSON
        results (List[ValidationResult]): Validation results
    """
    
    # ANSI color codes for terminal output
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    def __init__(self, mapping_file: str = "requirements_mapping.json"):
        """
        Initialize validator with mapping file.
        
        Args:
            mapping_file: Path to requirements_mapping.json
            
        Raises:
            FileNotFoundError: If mapping file doesn't exist
            json.JSONDecodeError: If JSON is invalid
        """
        self.mapping_file = Path(mapping_file)
        self.requirements: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {}
        self.results: List[ValidationResult] = []
        
        self._load_requirements()
    
    def _load_requirements(self) -> None:
        """Load and parse requirements from JSON file."""
        if not self.mapping_file.exists():
            raise FileNotFoundError(f"Mapping file not found: {self.mapping_file}")
        
        try:
            with open(self.mapping_file, 'r') as f:
                data = json.load(f)
                self.metadata = data.get('metadata', {})
                self.requirements = data.get('requirements', [])
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in {self.mapping_file}: {e.msg}",
                e.doc,
                e.pos
            )
    
    def validate(self) -> List[ValidationResult]:
        """
        Validate all requirements and return results.
        
        Returns:
            List of ValidationResult objects
        """
        self.results = []
        
        for req in self.requirements:
            result = ValidationResult(
                req_id=req.get('id', 'UNKNOWN'),
                name=req.get('name', 'Unknown'),
                status=AlignmentStatus(req.get('alignment_status', 'PARTIAL_MATCH')),
                severity=req.get('severity', 'MEDIUM'),
                notes=req.get('notes', ''),
                recommendation=req.get('recommendation', '')
            )
            self.results.append(result)
        
        return self.results
    
    def _get_status_icon(self, status: AlignmentStatus) -> str:
        """Get colored icon for alignment status."""
        if status == AlignmentStatus.MATCH:
            return f"{self.GREEN}✔{self.RESET}"
        elif status == AlignmentStatus.PARTIAL_MATCH:
            return f"{self.YELLOW}⚠{self.RESET}"
        else:  # CONFLICT
            return f"{self.RED}✖{self.RESET}"
    
    def _get_severity_color(self, severity: str) -> str:
        """Get color code for severity level."""
        if severity == "CRITICAL":
            return self.RED
        elif severity == "HIGH":
            return self.YELLOW
        else:
            return self.BLUE
    
    def print_validation_summary(self) -> None:
        """Print formatted validation summary to console."""
        print(f"\n{self.BOLD}{self.BLUE}{'='*70}{self.RESET}")
        print(f"{self.BOLD}{self.BLUE}QA DOCUMENTATION VALIDATION REPORT{self.RESET}")
        print(f"{self.BOLD}{self.BLUE}{'='*70}{self.RESET}\n")
        
        # Print metadata
        print(f"{self.BOLD}JIRA Reference:{self.RESET}")
        print(f"  {self.metadata.get('jira_link', 'N/A')}\n")
        
        print(f"{self.BOLD}Confluence Reference:{self.RESET}")
        print(f"  {self.metadata.get('confluence_link', 'N/A')}\n")
        
        print(f"{self.BOLD}{self.BLUE}REQUIREMENT VALIDATION RESULTS{self.RESET}")
        print(f"{self.BLUE}{'-'*70}{self.RESET}\n")
        
        # Print each requirement result
        for result in self.results:
            icon = self._get_status_icon(result.status)
            status_text = result.status.value
            print(f"{icon} {result.req_id}: {result.name} – {status_text}")
            
            if result.severity in ["CRITICAL", "HIGH"]:
                severity_color = self._get_severity_color(result.severity)
                print(f"   {severity_color}[{result.severity}]{self.RESET} {result.notes}")
            else:
                print(f"   {result.notes}")
            
            if result.recommendation:
                print(f"   {self.BOLD}→ Recommendation:{self.RESET} {result.recommendation}")
            
            print()
        
        # Print summary statistics
        self._print_summary_statistics()
        
        # Print action items
        self._print_action_items()
    
    def _print_summary_statistics(self) -> None:
        """Print summary statistics of validation results."""
        total = len(self.results)
        matched = sum(1 for r in self.results if r.status == AlignmentStatus.MATCH)
        partial = sum(1 for r in self.results if r.status == AlignmentStatus.PARTIAL_MATCH)
        conflicts = sum(1 for r in self.results if r.status == AlignmentStatus.CONFLICT)
        
        print(f"{self.BOLD}{self.BLUE}VALIDATION SUMMARY{self.RESET}")
        print(f"{self.BLUE}{'-'*70}{self.RESET}")
        print(f"Total Requirements: {total}")
        print(f"{self.GREEN}✔ Fully Matched: {matched} ({matched*100//total}%){self.RESET}")
        print(f"{self.YELLOW}⚠ Partially Matched: {partial} ({partial*100//total}%){self.RESET}")
        print(f"{self.RED}✖ Conflicts: {conflicts} ({conflicts*100//total}%){self.RESET}\n")
        
        # Print severity breakdown
        critical = sum(1 for r in self.results if r.severity == "CRITICAL")
        high = sum(1 for r in self.results if r.severity == "HIGH")
        
        if critical > 0 or high > 0:
            print(f"{self.BOLD}{self.RED}SEVERITY BREAKDOWN{self.RESET}")
            if critical > 0:
                print(f"  {self.RED}Critical Issues: {critical}{self.RESET}")
            if high > 0:
                print(f"  {self.YELLOW}High Priority Issues: {high}{self.RESET}")
            print()
    
    def _print_action_items(self) -> None:
        """Print action items based on validation results."""
        conflicts = [r for r in self.results if r.status == AlignmentStatus.CONFLICT]
        partials = [r for r in self.results if r.status == AlignmentStatus.PARTIAL_MATCH]
        
        print(f"{self.BOLD}{self.BLUE}ACTION ITEMS{self.RESET}")
        print(f"{self.BLUE}{'-'*70}{self.RESET}")
        
        if conflicts:
            print(f"{self.RED}CONFLICTS DETECTED - IMMEDIATE ACTION REQUIRED:{self.RESET}")
            for conflict in conflicts:
                print(f"  • {conflict.req_id}: {conflict.name}")
                if conflict.recommendation:
                    print(f"    → {conflict.recommendation}")
            print()
        
        if partials:
            print(f"{self.YELLOW}PARTIAL MATCHES - CLARIFICATION NEEDED:{self.RESET}")
            for partial in partials:
                print(f"  • {partial.req_id}: {partial.name}")
                if partial.recommendation:
                    print(f"    → {partial.recommendation}")
            print()
        
        if not conflicts and not partials:
            print(f"{self.GREEN}✔ All requirements are aligned!{self.RESET}\n")
        else:
            print(f"{self.BOLD}Next Steps:{self.RESET}")
            print("  1. Review conflicts and prioritize resolution")
            print("  2. Update Confluence documentation with JIRA specifications")
            print("  3. Notify development team of requirement changes")
            print("  4. Re-run validation after updates\n")
    
    def generate_report(self, output_file: str = "validation_report.txt") -> None:
        """
        Generate detailed validation report to file.
        
        Args:
            output_file: Path to output report file
        """
        with open(output_file, 'w') as f:
            f.write("QA DOCUMENTATION VALIDATION REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"JIRA Reference: {self.metadata.get('jira_link', 'N/A')}\n")
            f.write(f"Confluence Reference: {self.metadata.get('confluence_link', 'N/A')}\n")
            f.write(f"Generated: {self.metadata.get('last_updated', 'N/A')}\n\n")
            
            for result in self.results:
                f.write(f"\n{'-' * 70}\n")
                f.write(f"Requirement: {result.req_id} - {result.name}\n")
                f.write(f"Status: {result.status.value}\n")
                f.write(f"Severity: {result.severity}\n")
                f.write(f"Notes: {result.notes}\n")
                if result.recommendation:
                    f.write(f"Recommendation: {result.recommendation}\n")
            
            f.write(f"\n{'=' * 70}\n")
            f.write("SUMMARY\n")
            f.write(f"{'=' * 70}\n")
            
            total = len(self.results)
            matched = sum(1 for r in self.results if r.status == AlignmentStatus.MATCH)
            partial = sum(1 for r in self.results if r.status == AlignmentStatus.PARTIAL_MATCH)
            conflicts = sum(1 for r in self.results if r.status == AlignmentStatus.CONFLICT)
            
            f.write(f"Total Requirements: {total}\n")
            f.write(f"Fully Matched: {matched} ({matched*100//total}%)\n")
            f.write(f"Partially Matched: {partial} ({partial*100//total}%)\n")
            f.write(f"Conflicts: {conflicts} ({conflicts*100//total}%)\n")
    
    def get_exit_code(self) -> int:
        """
        Get exit code for CI/CD integration.
        
        Returns:
            0 if all requirements match, 1 if any conflicts exist
        """
        conflicts = sum(1 for r in self.results if r.status == AlignmentStatus.CONFLICT)
        return 1 if conflicts > 0 else 0


def main() -> int:
    """
    Main entry point for validation script.
    
    Returns:
        Exit code (0 for success, 1 for conflicts)
    """
    try:
        # Initialize validator
        validator = QADocumentationValidator("requirements_mapping.json")
        
        # Run validation
        validator.validate()
        
        # Print results
        validator.print_validation_summary()
        
        # Generate detailed report
        validator.generate_report("validation_report.txt")
        print(f"{validator.BOLD}Detailed report saved to: validation_report.txt{validator.RESET}\n")
        
        # Return appropriate exit code
        exit_code = validator.get_exit_code()
        
        if exit_code == 0:
            print(f"{validator.GREEN}{validator.BOLD}✔ Validation PASSED{validator.RESET}\n")
        else:
            print(f"{validator.RED}{validator.BOLD}✖ Validation FAILED - Conflicts detected{validator.RESET}\n")
        
        return exit_code
    
    except FileNotFoundError as e:
        print(f"{validator.RED}Error: {e}{validator.RESET}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"{validator.RED}JSON Error: {e}{validator.RESET}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"{validator.RED}Unexpected error: {e}{validator.RESET}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
