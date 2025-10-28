#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script to deploy infrastructure with Terraform
echo -e "${GREEN}🚀 E-commerce Terraform Deployment Script${NC}"
echo ""

# Check if environment is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Environment not specified${NC}"
    echo "Usage: ./deploy.sh <environment> [action]"
    echo "Environments: dev, staging, prod"
    echo "Actions: plan, apply, destroy (default: plan)"
    exit 1
fi

ENVIRONMENT=$1
ACTION=${2:-plan}

# Validate environment
if [ "$ENVIRONMENT" != "dev" ] && [ "$ENVIRONMENT" != "staging" ] && [ "$ENVIRONMENT" != "prod" ]; then
    echo -e "${RED}Error: Invalid environment '$ENVIRONMENT'${NC}"
    echo "Valid environments: dev, staging, prod"
    exit 1
fi

# Validate action
if [ "$ACTION" != "plan" ] && [ "$ACTION" != "apply" ] && [ "$ACTION" != "destroy" ]; then
    echo -e "${RED}Error: Invalid action '$ACTION'${NC}"
    echo "Valid actions: plan, apply, destroy"
    exit 1
fi

echo -e "${YELLOW}Environment: $ENVIRONMENT${NC}"
echo -e "${YELLOW}Action: $ACTION${NC}"
echo ""

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}Error: AWS credentials not configured${NC}"
    echo "Run: aws configure"
    exit 1
fi

echo -e "${GREEN}✓ AWS credentials validated${NC}"

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo -e "${RED}Error: Terraform not installed${NC}"
    echo "Install from: https://www.terraform.io/downloads.html"
    exit 1
fi

echo -e "${GREEN}✓ Terraform installed: $(terraform version -json | jq -r '.terraform_version')${NC}"

# Navigate to terraform directory
cd "$(dirname "$0")/.."

# Initialize Terraform
echo ""
echo -e "${YELLOW}Initializing Terraform...${NC}"
terraform init -upgrade

# Select or create workspace
echo ""
echo -e "${YELLOW}Selecting workspace: $ENVIRONMENT${NC}"
terraform workspace select $ENVIRONMENT 2>/dev/null || terraform workspace new $ENVIRONMENT

# Validate configuration
echo ""
echo -e "${YELLOW}Validating Terraform configuration...${NC}"
terraform validate

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Terraform validation failed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Terraform configuration valid${NC}"

# Set variables file
VAR_FILE="environments/$ENVIRONMENT/terraform.tfvars"

if [ ! -f "$VAR_FILE" ]; then
    echo -e "${RED}Error: Variables file not found: $VAR_FILE${NC}"
    exit 1
fi

# Execute action
echo ""
case $ACTION in
    plan)
        echo -e "${YELLOW}Planning changes for $ENVIRONMENT...${NC}"
        terraform plan -var-file="$VAR_FILE" -out="${ENVIRONMENT}.tfplan"
        
        echo ""
        echo -e "${GREEN}✓ Plan completed${NC}"
        echo "To apply these changes, run:"
        echo -e "${YELLOW}  ./deploy.sh $ENVIRONMENT apply${NC}"
        ;;
        
    apply)
        echo -e "${YELLOW}Applying changes for $ENVIRONMENT...${NC}"
        
        # Extra confirmation for production
        if [ "$ENVIRONMENT" == "prod" ]; then
            echo -e "${RED}⚠️  WARNING: You are about to apply changes to PRODUCTION${NC}"
            read -p "Type 'yes' to continue: " -r
            echo
            if [[ ! $REPLY =~ ^yes$ ]]; then
                echo "Deployment cancelled"
                exit 1
            fi
        fi
        
        # Check if plan exists
        if [ -f "${ENVIRONMENT}.tfplan" ]; then
            terraform apply "${ENVIRONMENT}.tfplan"
        else
            terraform apply -var-file="$VAR_FILE" -auto-approve
        fi
        
        echo ""
        echo -e "${GREEN}✓ Deployment completed successfully${NC}"
        
        # Show outputs
        echo ""
        echo -e "${YELLOW}Outputs:${NC}"
        terraform output
        ;;
        
    destroy)
        echo -e "${RED}⚠️  WARNING: You are about to DESTROY infrastructure for $ENVIRONMENT${NC}"
        
        # Extra confirmation
        read -p "Type 'destroy-$ENVIRONMENT' to continue: " -r
        echo
        if [[ ! $REPLY == "destroy-$ENVIRONMENT" ]]; then
            echo "Destroy cancelled"
            exit 1
        fi
        
        terraform destroy -var-file="$VAR_FILE"
        
        echo ""
        echo -e "${GREEN}✓ Infrastructure destroyed${NC}"
        ;;
esac

echo ""
echo -e "${GREEN}✓ Script completed successfully${NC}"
