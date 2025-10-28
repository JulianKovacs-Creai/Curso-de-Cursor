/**
 * GDPR Validation Utilities
 * Validation functions for GDPR compliance operations
 */

import { DataSubjectRequest } from '../compliance/gdpr';

export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

export function validateDataSubjectRequest(request: DataSubjectRequest): ValidationResult {
  const errors: string[] = [];

  // Validate required fields
  if (!request.id) {
    errors.push('Request ID is required');
  }

  if (!request.dataSubjectId) {
    errors.push('Data subject ID is required');
  }

  if (!request.type) {
    errors.push('Request type is required');
  }

  if (!request.verificationMethod) {
    errors.push('Verification method is required');
  }

  if (!request.timestamp) {
    errors.push('Timestamp is required');
  }

  // Validate request type
  const validTypes = ['ACCESS', 'RECTIFICATION', 'ERASURE', 'PORTABILITY'];
  if (request.type && !validTypes.includes(request.type)) {
    errors.push(`Invalid request type. Must be one of: ${validTypes.join(', ')}`);
  }

  // Validate verification method
  const validVerificationMethods = ['EMAIL', 'SMS', 'ID_DOCUMENT'];
  if (request.verificationMethod && !validVerificationMethods.includes(request.verificationMethod)) {
    errors.push(`Invalid verification method. Must be one of: ${validVerificationMethods.join(', ')}`);
  }

  // Validate verification code for EMAIL and SMS methods
  if ((request.verificationMethod === 'EMAIL' || request.verificationMethod === 'SMS') && !request.verificationCode) {
    errors.push('Verification code is required for EMAIL and SMS verification methods');
  }

  // Validate request data for RECTIFICATION requests
  if (request.type === 'RECTIFICATION' && !request.requestData) {
    errors.push('Request data is required for rectification requests');
  }

  // Validate data subject ID format (basic email validation)
  if (request.dataSubjectId && !isValidEmail(request.dataSubjectId) && !isValidUUID(request.dataSubjectId)) {
    errors.push('Data subject ID must be a valid email address or UUID');
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

export function validateConsentUpdate(data: any): ValidationResult {
  const errors: string[] = [];

  if (!data.purpose) {
    errors.push('Purpose is required');
  }

  if (!data.legalBasis) {
    errors.push('Legal basis is required');
  }

  if (typeof data.granted !== 'boolean') {
    errors.push('Granted status must be a boolean');
  }

  // Validate legal basis
  const validLegalBases = ['CONSENT', 'CONTRACT', 'LEGAL_OBLIGATION', 'VITAL_INTERESTS', 'PUBLIC_TASK', 'LEGITIMATE_INTERESTS'];
  if (data.legalBasis && !validLegalBases.includes(data.legalBasis)) {
    errors.push(`Invalid legal basis. Must be one of: ${validLegalBases.join(', ')}`);
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

export function validateIdentityVerification(data: any): ValidationResult {
  const errors: string[] = [];

  if (!data.dataSubjectId) {
    errors.push('Data subject ID is required');
  }

  if (!data.verificationMethod) {
    errors.push('Verification method is required');
  }

  if (!data.verificationData) {
    errors.push('Verification data is required');
  }

  // Validate verification method
  const validVerificationMethods = ['EMAIL', 'SMS', 'ID_DOCUMENT'];
  if (data.verificationMethod && !validVerificationMethods.includes(data.verificationMethod)) {
    errors.push(`Invalid verification method. Must be one of: ${validVerificationMethods.join(', ')}`);
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

// Helper functions
function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function isValidUUID(uuid: string): boolean {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  return uuidRegex.test(uuid);
}
