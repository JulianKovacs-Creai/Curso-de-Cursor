/**
 * GDPR API Endpoints
 * RESTful API endpoints for GDPR compliance operations
 */

import { Request, Response } from 'express';
import { GDPRComplianceEngine, DataSubjectRequest, GDPRResponse } from '../compliance/gdpr';
import { validateDataSubjectRequest } from '../validation/gdpr-validation';
import { auditLogger } from '../audit/audit-logger';

const gdprEngine = new GDPRComplianceEngine();

/**
 * POST /api/v1/gdpr/access-request
 * Handle data subject access requests
 */
export async function handleAccessRequest(req: Request, res: Response): Promise<void> {
  try {
    const request: DataSubjectRequest = {
      id: req.body.id || generateRequestId(),
      type: 'ACCESS',
      dataSubjectId: req.body.dataSubjectId,
      timestamp: new Date(),
      verificationMethod: req.body.verificationMethod,
      verificationCode: req.body.verificationCode,
      requestData: req.body.requestData
    };

    // Validate the request
    const validation = validateDataSubjectRequest(request);
    if (!validation.valid) {
      res.status(400).json({
        error: 'Invalid request',
        details: validation.errors
      });
      return;
    }

    // Process the request
    const response: GDPRResponse = await gdprEngine.handleDataSubjectRequest(request);

    // Log the request for audit purposes
    await auditLogger.logGDPRRequest(request, response);

    res.status(200).json(response);
  } catch (error) {
    console.error('Access request error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to process access request'
    });
  }
}

/**
 * POST /api/v1/gdpr/rectification-request
 * Handle data subject rectification requests
 */
export async function handleRectificationRequest(req: Request, res: Response): Promise<void> {
  try {
    const request: DataSubjectRequest = {
      id: req.body.id || generateRequestId(),
      type: 'RECTIFICATION',
      dataSubjectId: req.body.dataSubjectId,
      timestamp: new Date(),
      verificationMethod: req.body.verificationMethod,
      verificationCode: req.body.verificationCode,
      requestData: req.body.requestData
    };

    // Validate the request
    const validation = validateDataSubjectRequest(request);
    if (!validation.valid) {
      res.status(400).json({
        error: 'Invalid request',
        details: validation.errors
      });
      return;
    }

    // Process the request
    const response: GDPRResponse = await gdprEngine.handleDataSubjectRequest(request);

    // Log the request for audit purposes
    await auditLogger.logGDPRRequest(request, response);

    res.status(200).json(response);
  } catch (error) {
    console.error('Rectification request error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to process rectification request'
    });
  }
}

/**
 * POST /api/v1/gdpr/erasure-request
 * Handle data subject erasure requests (right to be forgotten)
 */
export async function handleErasureRequest(req: Request, res: Response): Promise<void> {
  try {
    const request: DataSubjectRequest = {
      id: req.body.id || generateRequestId(),
      type: 'ERASURE',
      dataSubjectId: req.body.dataSubjectId,
      timestamp: new Date(),
      verificationMethod: req.body.verificationMethod,
      verificationCode: req.body.verificationCode,
      requestData: req.body.requestData
    };

    // Validate the request
    const validation = validateDataSubjectRequest(request);
    if (!validation.valid) {
      res.status(400).json({
        error: 'Invalid request',
        details: validation.errors
      });
      return;
    }

    // Process the request
    const response: GDPRResponse = await gdprEngine.handleDataSubjectRequest(request);

    // Log the request for audit purposes
    await auditLogger.logGDPRRequest(request, response);

    res.status(200).json(response);
  } catch (error) {
    console.error('Erasure request error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to process erasure request'
    });
  }
}

/**
 * POST /api/v1/gdpr/portability-request
 * Handle data subject portability requests
 */
export async function handlePortabilityRequest(req: Request, res: Response): Promise<void> {
  try {
    const request: DataSubjectRequest = {
      id: req.body.id || generateRequestId(),
      type: 'PORTABILITY',
      dataSubjectId: req.body.dataSubjectId,
      timestamp: new Date(),
      verificationMethod: req.body.verificationMethod,
      verificationCode: req.body.verificationCode,
      requestData: req.body.requestData
    };

    // Validate the request
    const validation = validateDataSubjectRequest(request);
    if (!validation.valid) {
      res.status(400).json({
        error: 'Invalid request',
        details: validation.errors
      });
      return;
    }

    // Process the request
    const response: GDPRResponse = await gdprEngine.handleDataSubjectRequest(request);

    // Log the request for audit purposes
    await auditLogger.logGDPRRequest(request, response);

    res.status(200).json(response);
  } catch (error) {
    console.error('Portability request error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to process portability request'
    });
  }
}

/**
 * GET /api/v1/gdpr/request-status/{requestId}
 * Get the status of a data subject request
 */
export async function getRequestStatus(req: Request, res: Response): Promise<void> {
  try {
    const { requestId } = req.params;

    if (!requestId) {
      res.status(400).json({
        error: 'Request ID is required'
      });
      return;
    }

    // Get request status from the engine
    const status = await gdprEngine.getRequestStatus(requestId);

    if (!status) {
      res.status(404).json({
        error: 'Request not found'
      });
      return;
    }

    res.status(200).json(status);
  } catch (error) {
    console.error('Request status error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to get request status'
    });
  }
}

/**
 * GET /api/v1/gdpr/consent/{dataSubjectId}
 * Get consent information for a data subject
 */
export async function getConsentInfo(req: Request, res: Response): Promise<void> {
  try {
    const { dataSubjectId } = req.params;

    if (!dataSubjectId) {
      res.status(400).json({
        error: 'Data subject ID is required'
      });
      return;
    }

    // Get consent information
    const consentInfo = await gdprEngine.getConsentInfo(dataSubjectId);

    res.status(200).json(consentInfo);
  } catch (error) {
    console.error('Consent info error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to get consent information'
    });
  }
}

/**
 * POST /api/v1/gdpr/consent/{dataSubjectId}
 * Update consent for a data subject
 */
export async function updateConsent(req: Request, res: Response): Promise<void> {
  try {
    const { dataSubjectId } = req.params;
    const { purpose, legalBasis, granted } = req.body;

    if (!dataSubjectId) {
      res.status(400).json({
        error: 'Data subject ID is required'
      });
      return;
    }

    if (!purpose || !legalBasis || typeof granted !== 'boolean') {
      res.status(400).json({
        error: 'Purpose, legal basis, and granted status are required'
      });
      return;
    }

    // Update consent
    const result = await gdprEngine.updateConsent(dataSubjectId, purpose, legalBasis, granted);

    res.status(200).json(result);
  } catch (error) {
    console.error('Update consent error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to update consent'
    });
  }
}

/**
 * GET /api/v1/gdpr/privacy-policy
 * Get the current privacy policy
 */
export async function getPrivacyPolicy(req: Request, res: Response): Promise<void> {
  try {
    const privacyPolicy = await gdprEngine.getPrivacyPolicy();

    res.status(200).json(privacyPolicy);
  } catch (error) {
    console.error('Privacy policy error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to get privacy policy'
    });
  }
}

/**
 * GET /api/v1/gdpr/data-processing-activities
 * Get information about data processing activities
 */
export async function getDataProcessingActivities(req: Request, res: Response): Promise<void> {
  try {
    const activities = await gdprEngine.getDataProcessingActivities();

    res.status(200).json(activities);
  } catch (error) {
    console.error('Data processing activities error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to get data processing activities'
    });
  }
}

/**
 * GET /api/v1/gdpr/compliance-report
 * Generate a GDPR compliance report
 */
export async function generateComplianceReport(req: Request, res: Response): Promise<void> {
  try {
    const { startDate, endDate } = req.query;

    if (!startDate || !endDate) {
      res.status(400).json({
        error: 'Start date and end date are required'
      });
      return;
    }

    const start = new Date(startDate as string);
    const end = new Date(endDate as string);

    if (isNaN(start.getTime()) || isNaN(end.getTime())) {
      res.status(400).json({
        error: 'Invalid date format'
      });
      return;
    }

    const report = await gdprEngine.generateComplianceReport(start, end);

    res.status(200).json(report);
  } catch (error) {
    console.error('Compliance report error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to generate compliance report'
    });
  }
}

/**
 * POST /api/v1/gdpr/verify-identity
 * Verify the identity of a data subject
 */
export async function verifyIdentity(req: Request, res: Response): Promise<void> {
  try {
    const { dataSubjectId, verificationMethod, verificationData } = req.body;

    if (!dataSubjectId || !verificationMethod || !verificationData) {
      res.status(400).json({
        error: 'Data subject ID, verification method, and verification data are required'
      });
      return;
    }

    const verification = await gdprEngine.verifyIdentity(dataSubjectId, verificationMethod, verificationData);

    res.status(200).json(verification);
  } catch (error) {
    console.error('Identity verification error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to verify identity'
    });
  }
}

/**
 * GET /api/v1/gdpr/rights-info
 * Get information about data subject rights
 */
export async function getRightsInfo(req: Request, res: Response): Promise<void> {
  try {
    const rightsInfo = {
      access: {
        description: 'Right to access personal data',
        howToExercise: 'Submit an access request with identity verification',
        timeframe: '30 days',
        cost: 'Free'
      },
      rectification: {
        description: 'Right to correct inaccurate personal data',
        howToExercise: 'Submit a rectification request with the correct information',
        timeframe: '30 days',
        cost: 'Free'
      },
      erasure: {
        description: 'Right to be forgotten',
        howToExercise: 'Submit an erasure request with identity verification',
        timeframe: '30 days',
        cost: 'Free'
      },
      portability: {
        description: 'Right to data portability',
        howToExercise: 'Submit a portability request to receive data in a machine-readable format',
        timeframe: '30 days',
        cost: 'Free'
      },
      restriction: {
        description: 'Right to restrict processing',
        howToExercise: 'Submit a restriction request with valid grounds',
        timeframe: '30 days',
        cost: 'Free'
      },
      objection: {
        description: 'Right to object to processing',
        howToExercise: 'Submit an objection request with valid grounds',
        timeframe: '30 days',
        cost: 'Free'
      }
    };

    res.status(200).json(rightsInfo);
  } catch (error) {
    console.error('Rights info error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to get rights information'
    });
  }
}

// Helper function to generate request IDs
function generateRequestId(): string {
  return `GDPR-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

// Export all endpoints
export const gdprEndpoints = {
  handleAccessRequest,
  handleRectificationRequest,
  handleErasureRequest,
  handlePortabilityRequest,
  getRequestStatus,
  getConsentInfo,
  updateConsent,
  getPrivacyPolicy,
  getDataProcessingActivities,
  generateComplianceReport,
  verifyIdentity,
  getRightsInfo
};
