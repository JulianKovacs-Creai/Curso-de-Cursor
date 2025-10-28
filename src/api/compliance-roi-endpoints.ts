/**
 * Compliance ROI API Endpoints
 * RESTful API endpoints for compliance ROI calculations
 */

import { Request, Response } from 'express';
import { ComplianceROICalculator, ComplianceImplementation, ComplianceROIReport } from '../compliance/compliance-roi-calculator';

const roiCalculator = new ComplianceROICalculator();

/**
 * POST /api/v1/compliance/roi/calculate
 * Calculate ROI for compliance implementation
 */
export async function calculateComplianceROI(req: Request, res: Response): Promise<void> {
  try {
    const { implementation, timeframe } = req.body;

    if (!implementation) {
      res.status(400).json({
        error: 'Implementation details are required'
      });
      return;
    }

    if (!timeframe || timeframe < 1) {
      res.status(400).json({
        error: 'Valid timeframe in months is required'
      });
      return;
    }

    // Validate implementation structure
    const validation = validateImplementation(implementation);
    if (!validation.valid) {
      res.status(400).json({
        error: 'Invalid implementation structure',
        details: validation.errors
      });
      return;
    }

    const roiReport: ComplianceROIReport = await roiCalculator.calculateComplianceROI(
      implementation as ComplianceImplementation,
      timeframe
    );

    res.status(200).json(roiReport);
  } catch (error) {
    console.error('ROI calculation error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to calculate compliance ROI'
    });
  }
}

/**
 * GET /api/v1/compliance/roi/breach-prevention
 * Calculate breach prevention savings
 */
export async function calculateBreachPreventionSavings(req: Request, res: Response): Promise<void> {
  try {
    const { implementation, timeframe } = req.query;

    if (!implementation || !timeframe) {
      res.status(400).json({
        error: 'Implementation and timeframe parameters are required'
      });
      return;
    }

    const implementationData = JSON.parse(implementation as string);
    const timeframeNum = parseInt(timeframe as string);

    const savings = await roiCalculator.calculateBreachPreventionSavings(
      implementationData as ComplianceImplementation,
      timeframeNum
    );

    res.status(200).json({
      timeframe: timeframeNum,
      breachPreventionSavings: savings,
      breakdown: {
        gdprFinePrevention: implementationData.gdpr?.coverage ? 
          (2000000 * implementationData.gdpr.coverage / 100 * timeframeNum / 12) : 0,
        soxFinePrevention: implementationData.sox?.coverage ? 
          (5000000 * implementationData.sox.coverage / 100 * timeframeNum / 12) : 0
      }
    });
  } catch (error) {
    console.error('Breach prevention calculation error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to calculate breach prevention savings'
    });
  }
}

/**
 * GET /api/v1/compliance/roi/efficiency-gains
 * Calculate operational efficiency gains
 */
export async function calculateEfficiencyGains(req: Request, res: Response): Promise<void> {
  try {
    const { implementation, timeframe } = req.query;

    if (!implementation || !timeframe) {
      res.status(400).json({
        error: 'Implementation and timeframe parameters are required'
      });
      return;
    }

    const implementationData = JSON.parse(implementation as string);
    const timeframeNum = parseInt(timeframe as string);

    const efficiencyGains = await roiCalculator.calculateEfficiencyGains(
      implementationData as ComplianceImplementation,
      timeframeNum
    );

    res.status(200).json({
      timeframe: timeframeNum,
      efficiencyGains,
      breakdown: {
        gdprEfficiency: implementationData.gdpr?.coverage ? 
          (25000 * implementationData.gdpr.coverage / 100 * timeframeNum / 12) : 0,
        soxEfficiency: implementationData.sox?.coverage ? 
          (50000 * implementationData.sox.coverage / 100 * timeframeNum / 12) : 0,
        generalEfficiency: (30000 * ((implementationData.gdpr?.coverage || 0) + (implementationData.sox?.coverage || 0)) / 200 * timeframeNum / 12)
      }
    });
  } catch (error) {
    console.error('Efficiency gains calculation error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to calculate efficiency gains'
    });
  }
}

/**
 * GET /api/v1/compliance/roi/financial-projections
 * Generate detailed financial projections
 */
export async function generateFinancialProjections(req: Request, res: Response): Promise<void> {
  try {
    const { implementation, timeframe } = req.query;

    if (!implementation || !timeframe) {
      res.status(400).json({
        error: 'Implementation and timeframe parameters are required'
      });
      return;
    }

    const implementationData = JSON.parse(implementation as string);
    const timeframeNum = parseInt(timeframe as string);

    const projections = await roiCalculator.generateFinancialProjections(
      implementationData as ComplianceImplementation,
      timeframeNum
    );

    res.status(200).json(projections);
  } catch (error) {
    console.error('Financial projections error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to generate financial projections'
    });
  }
}

/**
 * GET /api/v1/compliance/roi/risk-assessment
 * Calculate risk reduction metrics
 */
export async function calculateRiskAssessment(req: Request, res: Response): Promise<void> {
  try {
    const { implementation } = req.query;

    if (!implementation) {
      res.status(400).json({
        error: 'Implementation parameter is required'
      });
      return;
    }

    const implementationData = JSON.parse(implementation as string);
    const riskReduction = await roiCalculator['calculateRiskReduction'](implementationData as ComplianceImplementation);

    res.status(200).json(riskReduction);
  } catch (error) {
    console.error('Risk assessment error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to calculate risk assessment'
    });
  }
}

/**
 * GET /api/v1/compliance/roi/compliance-value
 * Calculate compliance value metrics
 */
export async function calculateComplianceValue(req: Request, res: Response): Promise<void> {
  try {
    const { implementation } = req.query;

    if (!implementation) {
      res.status(400).json({
        error: 'Implementation parameter is required'
      });
      return;
    }

    const implementationData = JSON.parse(implementation as string);
    const complianceValue = await roiCalculator['calculateComplianceValue'](implementationData as ComplianceImplementation);

    res.status(200).json(complianceValue);
  } catch (error) {
    console.error('Compliance value calculation error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to calculate compliance value'
    });
  }
}

/**
 * GET /api/v1/compliance/roi/benchmarks
 * Get industry benchmarks for compliance ROI
 */
export async function getComplianceBenchmarks(req: Request, res: Response): Promise<void> {
  try {
    const benchmarks = {
      industry: {
        averageROI: 150,
        averagePaybackPeriod: 18,
        topQuartileROI: 250,
        topQuartilePaybackPeriod: 12
      },
      gdpr: {
        averageROI: 180,
        averagePaybackPeriod: 15,
        finePreventionValue: 2000000,
        legalCostReduction: 50000
      },
      sox: {
        averageROI: 200,
        averagePaybackPeriod: 20,
        finePreventionValue: 5000000,
        auditCostReduction: 100000
      },
      recommendations: {
        minimumROI: 100,
        maximumPaybackPeriod: 36,
        optimalCoverage: {
          gdpr: 85,
          sox: 80
        }
      }
    };

    res.status(200).json(benchmarks);
  } catch (error) {
    console.error('Benchmarks error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to get compliance benchmarks'
    });
  }
}

/**
 * POST /api/v1/compliance/roi/compare
 * Compare multiple compliance implementation scenarios
 */
export async function compareComplianceScenarios(req: Request, res: Response): Promise<void> {
  try {
    const { scenarios, timeframe } = req.body;

    if (!scenarios || !Array.isArray(scenarios) || scenarios.length < 2) {
      res.status(400).json({
        error: 'At least two scenarios are required for comparison'
      });
      return;
    }

    if (!timeframe || timeframe < 1) {
      res.status(400).json({
        error: 'Valid timeframe in months is required'
      });
      return;
    }

    const comparisons = await Promise.all(
      scenarios.map(async (scenario: any, index: number) => {
        const roiReport = await roiCalculator.calculateComplianceROI(
          scenario as ComplianceImplementation,
          timeframe
        );
        return {
          scenarioId: scenario.id || `scenario-${index + 1}`,
          scenarioName: scenario.name || `Scenario ${index + 1}`,
          ...roiReport
        };
      })
    );

    // Sort by ROI descending
    comparisons.sort((a, b) => b.roi - a.roi);

    const summary = {
      bestROI: comparisons[0],
      worstROI: comparisons[comparisons.length - 1],
      averageROI: comparisons.reduce((sum, c) => sum + c.roi, 0) / comparisons.length,
      averagePaybackPeriod: comparisons.reduce((sum, c) => sum + c.paybackPeriod, 0) / comparisons.length,
      totalScenarios: comparisons.length
    };

    res.status(200).json({
      comparisons,
      summary,
      recommendations: generateComparisonRecommendations(comparisons)
    });
  } catch (error) {
    console.error('Scenario comparison error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'Failed to compare compliance scenarios'
    });
  }
}

// Helper functions
function validateImplementation(implementation: any): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!implementation.gdpr) {
    errors.push('GDPR implementation details are required');
  } else {
    if (typeof implementation.gdpr.implemented !== 'boolean') {
      errors.push('GDPR implemented status must be boolean');
    }
    if (typeof implementation.gdpr.coverage !== 'number' || implementation.gdpr.coverage < 0 || implementation.gdpr.coverage > 100) {
      errors.push('GDPR coverage must be a number between 0 and 100');
    }
    if (typeof implementation.gdpr.estimatedCost !== 'number' || implementation.gdpr.estimatedCost < 0) {
      errors.push('GDPR estimated cost must be a positive number');
    }
  }

  if (!implementation.sox) {
    errors.push('SOX implementation details are required');
  } else {
    if (typeof implementation.sox.implemented !== 'boolean') {
      errors.push('SOX implemented status must be boolean');
    }
    if (typeof implementation.sox.coverage !== 'number' || implementation.sox.coverage < 0 || implementation.sox.coverage > 100) {
      errors.push('SOX coverage must be a number between 0 and 100');
    }
    if (typeof implementation.sox.estimatedCost !== 'number' || implementation.sox.estimatedCost < 0) {
      errors.push('SOX estimated cost must be a positive number');
    }
  }

  if (!implementation.infrastructure) {
    errors.push('Infrastructure details are required');
  }

  if (!implementation.training) {
    errors.push('Training details are required');
  }

  if (!implementation.maintenance) {
    errors.push('Maintenance details are required');
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

function generateComparisonRecommendations(comparisons: any[]): string[] {
  const recommendations: string[] = [];
  const best = comparisons[0];
  const worst = comparisons[comparisons.length - 1];

  if (best.roi > 200) {
    recommendations.push(`Scenario "${best.scenarioName}" shows excellent ROI (${best.roi.toFixed(1)}%) and should be prioritized`);
  }

  if (worst.roi < 50) {
    recommendations.push(`Scenario "${worst.scenarioName}" shows poor ROI (${worst.roi.toFixed(1)}%) and should be reconsidered`);
  }

  if (best.paybackPeriod < 12) {
    recommendations.push(`Scenario "${best.scenarioName}" has a quick payback period (${best.paybackPeriod.toFixed(1)} months)`);
  }

  if (worst.paybackPeriod > 36) {
    recommendations.push(`Scenario "${worst.scenarioName}" has a long payback period (${worst.paybackPeriod.toFixed(1)} months) - consider phased implementation`);
  }

  const avgROI = comparisons.reduce((sum, c) => sum + c.roi, 0) / comparisons.length;
  if (avgROI > 150) {
    recommendations.push('Overall compliance implementation shows strong ROI potential across all scenarios');
  }

  return recommendations;
}

// Export all endpoints
export const complianceROIEndpoints = {
  calculateComplianceROI,
  calculateBreachPreventionSavings,
  calculateEfficiencyGains,
  generateFinancialProjections,
  calculateRiskAssessment,
  calculateComplianceValue,
  getComplianceBenchmarks,
  compareComplianceScenarios
};
