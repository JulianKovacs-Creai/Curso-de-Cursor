/**
 * Audit Logger
 * Centralized audit logging for compliance operations
 */

import { DataSubjectRequest, GDPRResponse } from '../compliance/gdpr';

export interface AuditEntry {
  id: string;
  timestamp: Date;
  action: string;
  dataSubjectId: string;
  requestType?: string;
  details: any;
  ipAddress?: string;
  userAgent?: string;
  sessionId?: string;
}

export class AuditLogger {
  private auditEntries: AuditEntry[] = [];

  async logGDPRRequest(request: DataSubjectRequest, response: GDPRResponse): Promise<void> {
    const auditEntry: AuditEntry = {
      id: this.generateAuditId(),
      timestamp: new Date(),
      action: 'GDPR_REQUEST_PROCESSED',
      dataSubjectId: request.dataSubjectId,
      requestType: request.type,
      details: {
        requestId: request.id,
        verificationMethod: request.verificationMethod,
        outcome: response.outcome,
        processingTime: response.processingTime,
        hasDataProvided: !!response.dataProvided,
        rejectionReason: response.rejectionReason
      }
    };

    this.auditEntries.push(auditEntry);
    
    // In production, this would be stored in a proper audit database
    console.log('GDPR Request Audited:', auditEntry);
  }

  async logSOXActivity(activity: string, details: any): Promise<void> {
    const auditEntry: AuditEntry = {
      id: this.generateAuditId(),
      timestamp: new Date(),
      action: 'SOX_ACTIVITY',
      dataSubjectId: 'system',
      details: {
        activity,
        ...details
      }
    };

    this.auditEntries.push(auditEntry);
    console.log('SOX Activity Audited:', auditEntry);
  }

  async logSecurityEvent(event: string, details: any): Promise<void> {
    const auditEntry: AuditEntry = {
      id: this.generateAuditId(),
      timestamp: new Date(),
      action: 'SECURITY_EVENT',
      dataSubjectId: 'system',
      details: {
        event,
        ...details
      }
    };

    this.auditEntries.push(auditEntry);
    console.log('Security Event Audited:', auditEntry);
  }

  async logComplianceViolation(violation: string, details: any): Promise<void> {
    const auditEntry: AuditEntry = {
      id: this.generateAuditId(),
      timestamp: new Date(),
      action: 'COMPLIANCE_VIOLATION',
      dataSubjectId: 'system',
      details: {
        violation,
        ...details
      }
    };

    this.auditEntries.push(auditEntry);
    console.log('Compliance Violation Audited:', auditEntry);
  }

  async getAuditEntries(startDate?: Date, endDate?: Date): Promise<AuditEntry[]> {
    let entries = this.auditEntries;

    if (startDate) {
      entries = entries.filter(entry => entry.timestamp >= startDate);
    }

    if (endDate) {
      entries = entries.filter(entry => entry.timestamp <= endDate);
    }

    return entries.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
  }

  async generateAuditReport(startDate: Date, endDate: Date): Promise<AuditReport> {
    const entries = await this.getAuditEntries(startDate, endDate);

    const report: AuditReport = {
      reportId: this.generateAuditId(),
      period: { start: startDate, end: endDate },
      totalEntries: entries.length,
      entriesByAction: this.groupEntriesByAction(entries),
      entriesByDataSubject: this.groupEntriesByDataSubject(entries),
      complianceViolations: entries.filter(e => e.action === 'COMPLIANCE_VIOLATION').length,
      securityEvents: entries.filter(e => e.action === 'SECURITY_EVENT').length,
      gdprRequests: entries.filter(e => e.action === 'GDPR_REQUEST_PROCESSED').length,
      soxActivities: entries.filter(e => e.action === 'SOX_ACTIVITY').length,
      entries: entries
    };

    return report;
  }

  private generateAuditId(): string {
    return `AUDIT-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private groupEntriesByAction(entries: AuditEntry[]): Record<string, number> {
    const groups: Record<string, number> = {};
    entries.forEach(entry => {
      groups[entry.action] = (groups[entry.action] || 0) + 1;
    });
    return groups;
  }

  private groupEntriesByDataSubject(entries: AuditEntry[]): Record<string, number> {
    const groups: Record<string, number> = {};
    entries.forEach(entry => {
      groups[entry.dataSubjectId] = (groups[entry.dataSubjectId] || 0) + 1;
    });
    return groups;
  }
}

// Export singleton instance
export const auditLogger = new AuditLogger();

// Supporting interfaces
interface AuditReport {
  reportId: string;
  period: { start: Date; end: Date };
  totalEntries: number;
  entriesByAction: Record<string, number>;
  entriesByDataSubject: Record<string, number>;
  complianceViolations: number;
  securityEvents: number;
  gdprRequests: number;
  soxActivities: number;
  entries: AuditEntry[];
}
