/**
 * Compliance ROI Calculator Example
 * Demonstrates how to use the ComplianceROICalculator
 */

import { ComplianceROICalculator, ComplianceImplementation } from '../compliance/compliance-roi-calculator';

// Example implementation scenarios
const currentImplementation: ComplianceImplementation = {
  gdpr: {
    implemented: true,
    features: ['Data Subject Rights API', 'Consent Management', 'Privacy Policy'],
    coverage: 60, // 60% implemented
    estimatedCost: 50000
  },
  sox: {
    implemented: false,
    features: [],
    coverage: 0, // Not implemented
    estimatedCost: 0
  },
  infrastructure: {
    database: true,
    monitoring: false,
    auditLogging: true,
    reporting: false,
    estimatedCost: 25000
  },
  training: {
    employees: 50,
    costPerEmployee: 500,
    totalCost: 25000
  },
  maintenance: {
    annualCost: 15000,
    supportCost: 10000,
    updateCost: 5000
  }
};

const proposedImplementation: ComplianceImplementation = {
  gdpr: {
    implemented: true,
    features: ['Data Subject Rights API', 'Consent Management', 'Privacy Policy', 'Data Portability', 'Right to Erasure'],
    coverage: 90, // 90% implemented
    estimatedCost: 75000
  },
  sox: {
    implemented: true,
    features: ['Financial Controls', 'Internal Controls Testing', 'Management Assertions', 'Audit Trail'],
    coverage: 80, // 80% implemented
    estimatedCost: 100000
  },
  infrastructure: {
    database: true,
    monitoring: true,
    auditLogging: true,
    reporting: true,
    estimatedCost: 50000
  },
  training: {
    employees: 50,
    costPerEmployee: 750,
    totalCost: 37500
  },
  maintenance: {
    annualCost: 25000,
    supportCost: 15000,
    updateCost: 10000
  }
};

const minimalImplementation: ComplianceImplementation = {
  gdpr: {
    implemented: true,
    features: ['Basic Data Subject Rights'],
    coverage: 30, // 30% implemented
    estimatedCost: 20000
  },
  sox: {
    implemented: false,
    features: [],
    coverage: 0,
    estimatedCost: 0
  },
  infrastructure: {
    database: false,
    monitoring: false,
    auditLogging: true,
    reporting: false,
    estimatedCost: 10000
  },
  training: {
    employees: 20,
    costPerEmployee: 300,
    totalCost: 6000
  },
  maintenance: {
    annualCost: 5000,
    supportCost: 3000,
    updateCost: 2000
  }
};

async function demonstrateROICalculations() {
  const calculator = new ComplianceROICalculator();
  const timeframe = 24; // 24 months

  console.log('🔍 Compliance ROI Calculator Demo\n');
  console.log('=' .repeat(60));

  // Calculate ROI for current implementation
  console.log('\n📊 CURRENT IMPLEMENTATION ROI:');
  const currentROI = await calculator.calculateComplianceROI(currentImplementation, timeframe);
  printROISummary(currentROI, 'Current');

  // Calculate ROI for proposed implementation
  console.log('\n📊 PROPOSED IMPLEMENTATION ROI:');
  const proposedROI = await calculator.calculateComplianceROI(proposedImplementation, timeframe);
  printROISummary(proposedROI, 'Proposed');

  // Calculate ROI for minimal implementation
  console.log('\n📊 MINIMAL IMPLEMENTATION ROI:');
  const minimalROI = await calculator.calculateComplianceROI(minimalImplementation, timeframe);
  printROISummary(minimalROI, 'Minimal');

  // Compare scenarios
  console.log('\n📊 SCENARIO COMPARISON:');
  const scenarios = [
    { id: 'current', name: 'Current Implementation', ...currentImplementation },
    { id: 'proposed', name: 'Proposed Implementation', ...proposedImplementation },
    { id: 'minimal', name: 'Minimal Implementation', ...minimalImplementation }
  ];

  const comparisons = await Promise.all(
    scenarios.map(async (scenario) => {
      const roi = await calculator.calculateComplianceROI(scenario, timeframe);
      return {
        name: scenario.name,
        roi: roi.roi,
        paybackPeriod: roi.paybackPeriod,
        totalCosts: roi.costs.total,
        totalBenefits: roi.benefits.total,
        netValue: roi.benefits.total - roi.costs.total
      };
    })
  );

  // Sort by ROI
  comparisons.sort((a, b) => b.roi - a.roi);

  console.log('\nRanking by ROI:');
  comparisons.forEach((scenario, index) => {
    console.log(`${index + 1}. ${scenario.name}`);
    console.log(`   ROI: ${scenario.roi.toFixed(1)}%`);
    console.log(`   Payback: ${scenario.paybackPeriod.toFixed(1)} months`);
    console.log(`   Net Value: €${scenario.netValue.toLocaleString()}`);
    console.log('');
  });

  // Generate financial projections for proposed implementation
  console.log('\n📈 FINANCIAL PROJECTIONS (Proposed Implementation):');
  const projections = await calculator.generateFinancialProjections(proposedImplementation, timeframe);
  
  console.log('\nMonthly Projections (First 12 months):');
  projections.monthly.slice(0, 12).forEach(projection => {
    console.log(`Month ${projection.month.toString().padStart(2)}: ` +
      `Costs: €${projection.cumulativeCosts.toLocaleString().padStart(10)} | ` +
      `Benefits: €${projection.cumulativeBenefits.toLocaleString().padStart(10)} | ` +
      `Net: €${projection.netValue.toLocaleString().padStart(10)} | ` +
      `ROI: ${projection.roi.toFixed(1)}%`);
  });

  console.log('\nYearly Projections:');
  projections.yearly.forEach(projection => {
    console.log(`Year ${projection.year}: ` +
      `Costs: €${projection.costs.toLocaleString().padStart(10)} | ` +
      `Benefits: €${projection.benefits.toLocaleString().padStart(10)} | ` +
      `Net: €${projection.netValue.toLocaleString().padStart(10)} | ` +
      `ROI: ${projection.roi.toFixed(1)}%`);
  });

  // Risk assessment
  console.log('\n⚠️  RISK ASSESSMENT:');
  const riskAssessment = await calculator['calculateRiskReduction'](proposedImplementation as ComplianceImplementation);
  console.log(`GDPR Risk Reduction: ${riskAssessment.gdprRiskReduction}%`);
  console.log(`SOX Risk Reduction: ${riskAssessment.soxRiskReduction}%`);
  console.log(`Overall Risk Reduction: ${riskAssessment.overallRiskReduction}%`);
  console.log(`Potential Loss Prevention: €${riskAssessment.potentialLossPrevention.toLocaleString()}`);

  // Compliance value
  console.log('\n💎 COMPLIANCE VALUE:');
  const complianceValue = await calculator['calculateComplianceValue'](proposedImplementation as ComplianceImplementation);
  console.log(`GDPR Compliance Value: €${complianceValue.gdprComplianceValue.toLocaleString()}`);
  console.log(`SOX Compliance Value: €${complianceValue.soxComplianceValue.toLocaleString()}`);
  console.log(`Overall Compliance Value: €${complianceValue.overallComplianceValue.toLocaleString()}`);
  console.log(`Market Value: €${complianceValue.marketValue.toLocaleString()}`);

  // Recommendations
  console.log('\n💡 RECOMMENDATIONS:');
  proposedROI.recommendations.forEach((rec, index) => {
    console.log(`${index + 1}. [${rec.priority}] ${rec.description}`);
    console.log(`   Expected ROI: ${rec.expectedROI}% | Cost: €${rec.implementationCost.toLocaleString()} | Timeframe: ${rec.timeframe} months`);
  });
}

function printROISummary(roi: any, label: string) {
  console.log(`\n${label} Implementation Summary:`);
  console.log(`  Total Costs: €${roi.costs.total.toLocaleString()}`);
  console.log(`  Total Benefits: €${roi.benefits.total.toLocaleString()}`);
  console.log(`  Net Value: €${(roi.benefits.total - roi.costs.total).toLocaleString()}`);
  console.log(`  ROI: ${roi.roi.toFixed(1)}%`);
  console.log(`  Payback Period: ${roi.paybackPeriod.toFixed(1)} months`);
  console.log(`  Risk Reduction: ${roi.riskReduction.overallRiskReduction}%`);
  
  console.log(`\n  Cost Breakdown:`);
  console.log(`    Implementation: €${roi.costs.implementation.toLocaleString()}`);
  console.log(`    Infrastructure: €${roi.costs.infrastructure.toLocaleString()}`);
  console.log(`    Training: €${roi.costs.training.toLocaleString()}`);
  console.log(`    Maintenance: €${roi.costs.maintenance.toLocaleString()}`);
  
  console.log(`\n  Benefit Breakdown:`);
  console.log(`    GDPR Savings: €${(roi.benefits.gdprSavings.finePrevention + roi.benefits.gdprSavings.legalCosts + roi.benefits.gdprSavings.reputationProtection + roi.benefits.gdprSavings.operationalEfficiency).toLocaleString()}`);
  console.log(`    SOX Savings: €${(roi.benefits.soxSavings.finePrevention + roi.benefits.soxSavings.auditCosts + roi.benefits.soxSavings.investorConfidence + roi.benefits.soxSavings.operationalEfficiency).toLocaleString()}`);
  console.log(`    General Benefits: €${(roi.benefits.generalBenefits.riskReduction + roi.benefits.generalBenefits.competitiveAdvantage + roi.benefits.generalBenefits.customerTrust + roi.benefits.generalBenefits.operationalEfficiency).toLocaleString()}`);
  
  console.log(`\n  ROI Breakdown:`);
  console.log(`    GDPR ROI: ${roi.breakdown.gdprROI.toFixed(1)}%`);
  console.log(`    SOX ROI: ${roi.breakdown.soxROI.toFixed(1)}%`);
  console.log(`    Infrastructure ROI: ${roi.breakdown.infrastructureROI.toFixed(1)}%`);
  console.log(`    Training ROI: ${roi.breakdown.trainingROI.toFixed(1)}%`);
}

// Run the demonstration
if ((globalThis as any).require?.main === (globalThis as any).module) {
  demonstrateROICalculations().catch(console.error);
}

export { demonstrateROICalculations };
