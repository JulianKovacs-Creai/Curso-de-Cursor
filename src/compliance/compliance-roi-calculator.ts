/**
 * Compliance ROI Calculator
 * Calculates Return on Investment for GDPR and SOX compliance implementations
 */

export interface ComplianceImplementation {
  gdpr: {
    implemented: boolean;
    features: string[];
    coverage: number; // percentage
    estimatedCost: number;
  };
  sox: {
    implemented: boolean;
    features: string[];
    coverage: number; // percentage
    estimatedCost: number;
  };
  infrastructure: {
    database: boolean;
    monitoring: boolean;
    auditLogging: boolean;
    reporting: boolean;
    estimatedCost: number;
  };
  training: {
    employees: number;
    costPerEmployee: number;
    totalCost: number;
  };
  maintenance: {
    annualCost: number;
    supportCost: number;
    updateCost: number;
  };
}

export interface ComplianceCosts {
  implementation: number;
  infrastructure: number;
  training: number;
  maintenance: number;
  total: number;
}

export interface ComplianceBenefits {
  gdprSavings: {
    finePrevention: number;
    legalCosts: number;
    reputationProtection: number;
    operationalEfficiency: number;
  };
  soxSavings: {
    finePrevention: number;
    auditCosts: number;
    investorConfidence: number;
    operationalEfficiency: number;
  };
  generalBenefits: {
    riskReduction: number;
    competitiveAdvantage: number;
    customerTrust: number;
    operationalEfficiency: number;
  };
  total: number;
}

export interface ComplianceROIReport {
  timeframe: number; // months
  costs: ComplianceCosts;
  benefits: ComplianceBenefits;
  roi: number; // percentage
  paybackPeriod: number; // months
  riskReduction: RiskReductionMetrics;
  complianceValue: ComplianceValueMetrics;
  recommendations: ROIRecommendation[];
  breakdown: {
    gdprROI: number;
    soxROI: number;
    infrastructureROI: number;
    trainingROI: number;
  };
}

export interface RiskReductionMetrics {
  gdprRiskReduction: number; // percentage
  soxRiskReduction: number; // percentage
  overallRiskReduction: number; // percentage
  potentialLossPrevention: number; // monetary value
}

export interface ComplianceValueMetrics {
  gdprComplianceValue: number;
  soxComplianceValue: number;
  overallComplianceValue: number;
  marketValue: number;
}

export interface ROIRecommendation {
  category: string;
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
  description: string;
  expectedROI: number;
  implementationCost: number;
  timeframe: number; // months
}

export class ComplianceROICalculator {
  private readonly gdprFineRanges = {
    minor: 100000, // €100K
    moderate: 500000, // €500K
    major: 2000000, // €2M
    severe: 20000000 // €20M (4% of annual revenue)
  };

  private readonly soxFineRanges = {
    minor: 1000000, // $1M
    moderate: 5000000, // $5M
    major: 25000000, // $25M
    severe: 100000000 // $100M
  };

  async calculateComplianceROI(
    implementation: ComplianceImplementation,
    timeframe: number // months
  ): Promise<ComplianceROIReport> {
    const costs = await this.calculateTotalCosts(implementation, timeframe);
    const benefits = await this.calculateBenefits(implementation, timeframe);

    const roi = (benefits.total - costs.total) / costs.total * 100;
    const paybackPeriod = costs.total / (benefits.total / timeframe);

    return {
      timeframe,
      costs,
      benefits,
      roi,
      paybackPeriod,
      riskReduction: await this.calculateRiskReduction(implementation),
      complianceValue: await this.calculateComplianceValue(implementation),
      recommendations: await this.generateROIRecommendations(roi, paybackPeriod, implementation),
      breakdown: await this.calculateROIBreakdown(implementation, costs, benefits)
    };
  }

  private async calculateTotalCosts(
    implementation: ComplianceImplementation,
    timeframe: number
  ): Promise<ComplianceCosts> {
    const implementationCost = implementation.gdpr.estimatedCost + implementation.sox.estimatedCost;
    const infrastructureCost = implementation.infrastructure.estimatedCost;
    const trainingCost = implementation.training.totalCost;
    const maintenanceCost = (implementation.maintenance.annualCost / 12) * timeframe;

    return {
      implementation: implementationCost,
      infrastructure: infrastructureCost,
      training: trainingCost,
      maintenance: maintenanceCost,
      total: implementationCost + infrastructureCost + trainingCost + maintenanceCost
    };
  }

  private async calculateBenefits(
    implementation: ComplianceImplementation,
    timeframe: number
  ): Promise<ComplianceBenefits> {
    const gdprSavings = await this.calculateGDPRSavings(implementation, timeframe);
    const soxSavings = await this.calculateSOXSavings(implementation, timeframe);
    const generalBenefits = await this.calculateGeneralBenefits(implementation, timeframe);

    const total = gdprSavings.finePrevention + gdprSavings.legalCosts + gdprSavings.reputationProtection + gdprSavings.operationalEfficiency +
                  soxSavings.finePrevention + soxSavings.auditCosts + soxSavings.investorConfidence + soxSavings.operationalEfficiency +
                  generalBenefits.riskReduction + generalBenefits.competitiveAdvantage + generalBenefits.customerTrust + generalBenefits.operationalEfficiency;

    return {
      gdprSavings,
      soxSavings,
      generalBenefits,
      total
    };
  }

  private async calculateGDPRSavings(
    implementation: ComplianceImplementation,
    timeframe: number
  ): Promise<ComplianceBenefits['gdprSavings']> {
    const coverage = implementation.gdpr.coverage / 100;
    
    // Fine prevention based on coverage
    const finePrevention = this.gdprFineRanges.moderate * coverage * (timeframe / 12);
    
    // Legal costs reduction
    const legalCosts = 50000 * coverage * (timeframe / 12);
    
    // Reputation protection value
    const reputationProtection = 100000 * coverage * (timeframe / 12);
    
    // Operational efficiency gains
    const operationalEfficiency = 25000 * coverage * (timeframe / 12);

    return {
      finePrevention,
      legalCosts,
      reputationProtection,
      operationalEfficiency
    };
  }

  private async calculateSOXSavings(
    implementation: ComplianceImplementation,
    timeframe: number
  ): Promise<ComplianceBenefits['soxSavings']> {
    const coverage = implementation.sox.coverage / 100;
    
    // Fine prevention based on coverage
    const finePrevention = this.soxFineRanges.moderate * coverage * (timeframe / 12);
    
    // Audit costs reduction
    const auditCosts = 100000 * coverage * (timeframe / 12);
    
    // Investor confidence value
    const investorConfidence = 200000 * coverage * (timeframe / 12);
    
    // Operational efficiency gains
    const operationalEfficiency = 50000 * coverage * (timeframe / 12);

    return {
      finePrevention,
      auditCosts,
      investorConfidence,
      operationalEfficiency
    };
  }

  private async calculateGeneralBenefits(
    implementation: ComplianceImplementation,
    timeframe: number
  ): Promise<ComplianceBenefits['generalBenefits']> {
    const avgCoverage = (implementation.gdpr.coverage + implementation.sox.coverage) / 200;
    
    // Risk reduction value
    const riskReduction = 150000 * avgCoverage * (timeframe / 12);
    
    // Competitive advantage
    const competitiveAdvantage = 75000 * avgCoverage * (timeframe / 12);
    
    // Customer trust value
    const customerTrust = 100000 * avgCoverage * (timeframe / 12);
    
    // Operational efficiency
    const operationalEfficiency = 30000 * avgCoverage * (timeframe / 12);

    return {
      riskReduction,
      competitiveAdvantage,
      customerTrust,
      operationalEfficiency
    };
  }

  private async calculateRiskReduction(implementation: ComplianceImplementation): Promise<RiskReductionMetrics> {
    const gdprRiskReduction = implementation.gdpr.implemented ? 
      Math.min(implementation.gdpr.coverage, 95) : 0;
    
    const soxRiskReduction = implementation.sox.implemented ? 
      Math.min(implementation.sox.coverage, 90) : 0;
    
    const overallRiskReduction = (gdprRiskReduction + soxRiskReduction) / 2;
    
    const potentialLossPrevention = (this.gdprFineRanges.moderate + this.soxFineRanges.moderate) * (overallRiskReduction / 100);

    return {
      gdprRiskReduction,
      soxRiskReduction,
      overallRiskReduction,
      potentialLossPrevention
    };
  }

  private async calculateComplianceValue(implementation: ComplianceImplementation): Promise<ComplianceValueMetrics> {
    const gdprComplianceValue = implementation.gdpr.implemented ? 
      implementation.gdpr.coverage * 1000 : 0;
    
    const soxComplianceValue = implementation.sox.implemented ? 
      implementation.sox.coverage * 2000 : 0;
    
    const overallComplianceValue = gdprComplianceValue + soxComplianceValue;
    
    const marketValue = overallComplianceValue * 1.5; // Market premium for compliance

    return {
      gdprComplianceValue,
      soxComplianceValue,
      overallComplianceValue,
      marketValue
    };
  }

  private async generateROIRecommendations(
    roi: number,
    paybackPeriod: number,
    implementation: ComplianceImplementation
  ): Promise<ROIRecommendation[]> {
    const recommendations: ROIRecommendation[] = [];

    // ROI-based recommendations
    if (roi < 100) {
      recommendations.push({
        category: 'Implementation',
        priority: 'HIGH',
        description: 'Focus on high-impact, low-cost compliance features to improve ROI',
        expectedROI: 150,
        implementationCost: 50000,
        timeframe: 6
      });
    }

    if (paybackPeriod > 24) {
      recommendations.push({
        category: 'Cost Optimization',
        priority: 'HIGH',
        description: 'Implement phased approach to reduce upfront costs and improve payback period',
        expectedROI: 120,
        implementationCost: 30000,
        timeframe: 12
      });
    }

    // Coverage-based recommendations
    if (implementation.gdpr.coverage < 80) {
      recommendations.push({
        category: 'GDPR Enhancement',
        priority: 'MEDIUM',
        description: 'Increase GDPR coverage to 80%+ to maximize fine prevention benefits',
        expectedROI: 200,
        implementationCost: 40000,
        timeframe: 8
      });
    }

    if (implementation.sox.coverage < 70) {
      recommendations.push({
        category: 'SOX Enhancement',
        priority: 'MEDIUM',
        description: 'Improve SOX compliance coverage to reduce audit risks and costs',
        expectedROI: 180,
        implementationCost: 60000,
        timeframe: 10
      });
    }

    // Infrastructure recommendations
    if (!implementation.infrastructure.monitoring) {
      recommendations.push({
        category: 'Infrastructure',
        priority: 'LOW',
        description: 'Implement compliance monitoring to reduce manual oversight costs',
        expectedROI: 130,
        implementationCost: 25000,
        timeframe: 4
      });
    }

    return recommendations;
  }

  private async calculateROIBreakdown(
    implementation: ComplianceImplementation,
    costs: ComplianceCosts,
    benefits: ComplianceBenefits
  ): Promise<ComplianceROIReport['breakdown']> {
    const gdprROI = implementation.gdpr.estimatedCost > 0 ? 
      (benefits.gdprSavings.finePrevention + benefits.gdprSavings.legalCosts + benefits.gdprSavings.reputationProtection + benefits.gdprSavings.operationalEfficiency) / implementation.gdpr.estimatedCost * 100 : 0;
    
    const soxROI = implementation.sox.estimatedCost > 0 ? 
      (benefits.soxSavings.finePrevention + benefits.soxSavings.auditCosts + benefits.soxSavings.investorConfidence + benefits.soxSavings.operationalEfficiency) / implementation.sox.estimatedCost * 100 : 0;
    
    const infrastructureROI = implementation.infrastructure.estimatedCost > 0 ? 
      (benefits.generalBenefits.operationalEfficiency + benefits.generalBenefits.riskReduction) / implementation.infrastructure.estimatedCost * 100 : 0;
    
    const trainingROI = implementation.training.totalCost > 0 ? 
      (benefits.generalBenefits.operationalEfficiency + benefits.generalBenefits.competitiveAdvantage) / implementation.training.totalCost * 100 : 0;

    return {
      gdprROI,
      soxROI,
      infrastructureROI,
      trainingROI
    };
  }

  // Utility methods for specific calculations
  public async calculateBreachPreventionSavings(
    implementation: ComplianceImplementation,
    timeframe: number
  ): Promise<number> {
    const gdprSavings = await this.calculateGDPRSavings(implementation, timeframe);
    const soxSavings = await this.calculateSOXSavings(implementation, timeframe);
    
    return gdprSavings.finePrevention + soxSavings.finePrevention;
  }

  public async calculateComplianceSavings(
    implementation: ComplianceImplementation,
    timeframe: number
  ): Promise<number> {
    const gdprSavings = await this.calculateGDPRSavings(implementation, timeframe);
    const soxSavings = await this.calculateSOXSavings(implementation, timeframe);
    
    return gdprSavings.legalCosts + soxSavings.auditCosts;
  }

  public async calculateEfficiencyGains(
    implementation: ComplianceImplementation,
    timeframe: number
  ): Promise<number> {
    const gdprSavings = await this.calculateGDPRSavings(implementation, timeframe);
    const soxSavings = await this.calculateSOXSavings(implementation, timeframe);
    const generalBenefits = await this.calculateGeneralBenefits(implementation, timeframe);
    
    return gdprSavings.operationalEfficiency + soxSavings.operationalEfficiency + generalBenefits.operationalEfficiency;
  }

  public async calculateReputationValue(
    implementation: ComplianceImplementation,
    timeframe: number
  ): Promise<number> {
    const gdprSavings = await this.calculateGDPRSavings(implementation, timeframe);
    const generalBenefits = await this.calculateGeneralBenefits(implementation, timeframe);
    
    return gdprSavings.reputationProtection + generalBenefits.customerTrust;
  }

  public async calculateInsuranceSavings(
    implementation: ComplianceImplementation,
    timeframe: number
  ): Promise<number> {
    const riskReduction = await this.calculateRiskReduction(implementation);
    const baseInsuranceCost = 100000; // Annual base insurance cost
    
    return baseInsuranceCost * (riskReduction.overallRiskReduction / 100) * (timeframe / 12);
  }

  // Method to generate detailed financial projections
  public async generateFinancialProjections(
    implementation: ComplianceImplementation,
    timeframe: number
  ): Promise<{
    monthly: Array<{
      month: number;
      cumulativeCosts: number;
      cumulativeBenefits: number;
      netValue: number;
      roi: number;
    }>;
    yearly: Array<{
      year: number;
      costs: number;
      benefits: number;
      netValue: number;
      roi: number;
    }>;
  }> {
    const monthlyProjections = [];
    const yearlyProjections = [];
    
    const monthlyCosts = (await this.calculateTotalCosts(implementation, timeframe)).total / timeframe;
    const monthlyBenefits = (await this.calculateBenefits(implementation, timeframe)).total / timeframe;
    
    let cumulativeCosts = 0;
    let cumulativeBenefits = 0;
    
    for (let month = 1; month <= timeframe; month++) {
      cumulativeCosts += monthlyCosts;
      cumulativeBenefits += monthlyBenefits;
      const netValue = cumulativeBenefits - cumulativeCosts;
      const roi = cumulativeCosts > 0 ? (netValue / cumulativeCosts) * 100 : 0;
      
      monthlyProjections.push({
        month,
        cumulativeCosts,
        cumulativeBenefits,
        netValue,
        roi
      } as never);
      
      if (month % 12 === 0) {
        const year = month / 12;
        const yearCosts = monthlyCosts * 12;
        const yearBenefits = monthlyBenefits * 12;
        const yearNetValue = yearBenefits - yearCosts;
        const yearROI = yearCosts > 0 ? (yearNetValue / yearCosts) * 100 : 0;
        
        yearlyProjections.push({
          year,
          costs: yearCosts,
          benefits: yearBenefits,
          netValue: yearNetValue,
          roi: yearROI
        } as never);
      }
    }
    
    return {
      monthly: monthlyProjections,
      yearly: yearlyProjections
    };
  }
}
