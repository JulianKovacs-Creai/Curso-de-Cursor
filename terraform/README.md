# 🏗️ Terraform Infrastructure as Code - E-commerce

Esta carpeta contiene la configuración completa de Terraform para desplegar el e-commerce en AWS.

## 📋 Arquitectura

### Componentes Principales

- **VPC**: Red virtual con subnets públicas, privadas y de base de datos
- **ECS Fargate**: Cluster para ejecutar contenedores sin gestionar servidores
- **RDS PostgreSQL**: Base de datos relacional gestionada
- **ElastiCache Redis**: Cache distribuido en memoria
- **ALB**: Application Load Balancer para distribución de tráfico
- **CloudWatch**: Monitoreo y logging
- **Auto Scaling**: Escalado automático basado en métricas

## 🚀 Quick Start

### Prerrequisitos

1. **Terraform** >= 1.0 instalado
2. **AWS CLI** configurado con credenciales
3. **S3 bucket** para el estado de Terraform (ver Backend Setup)

### Backend Setup (Primera vez)

```bash
# Crear bucket para el estado de Terraform
aws s3api create-bucket \
  --bucket ecommerce-terraform-state \
  --region us-east-1

# Habilitar versionado
aws s3api put-bucket-versioning \
  --bucket ecommerce-terraform-state \
  --versioning-configuration Status=Enabled

# Habilitar encriptación
aws s3api put-bucket-encryption \
  --bucket ecommerce-terraform-state \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'
```

### Deployment

#### 1. Inicializar Terraform

```bash
cd terraform
terraform init
```

#### 2. Seleccionar Workspace (Ambiente)

```bash
# Para desarrollo
terraform workspace new dev
terraform workspace select dev

# Para staging
terraform workspace new staging
terraform workspace select staging

# Para producción
terraform workspace new prod
terraform workspace select prod
```

#### 3. Planificar Cambios

```bash
# Desarrollo
terraform plan -var-file="environments/dev/terraform.tfvars"

# Staging
terraform plan -var-file="environments/staging/terraform.tfvars"

# Producción
terraform plan -var-file="environments/prod/terraform.tfvars"
```

#### 4. Aplicar Cambios

```bash
# Desarrollo
terraform apply -var-file="environments/dev/terraform.tfvars"

# Staging
terraform apply -var-file="environments/staging/terraform.tfvars"

# Producción
terraform apply -var-file="environments/prod/terraform.tfvars"
```

## 📁 Estructura de Archivos

```
terraform/
├── main.tf                 # Configuración principal
├── variables.tf            # Variables globales
├── outputs.tf              # Outputs globales
├── provider.tf             # Configuración de providers
├── backend.tf              # Configuración del backend S3
├── modules/
│   ├── vpc/               # Módulo VPC
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ecs/               # Módulo ECS
│   ├── alb/               # Módulo ALB
│   ├── rds/               # Módulo RDS
│   ├── redis/             # Módulo Redis
│   └── monitoring/        # Módulo Monitoring
└── environments/
    ├── dev/               # Configuración desarrollo
    ├── staging/           # Configuración staging
    └── prod/              # Configuración producción
```

## 🔧 Configuración de Variables

### Variables Requeridas

- `db_password`: Contraseña de la base de datos (sensible)
- `backend_image`: Imagen Docker del backend
- `frontend_image`: Imagen Docker del frontend

### Variables Opcionales

Ver `variables.tf` para la lista completa de variables configurables.

## 🔒 Seguridad

### Secrets Management

**NO** commitear passwords o secretos en el código. Usar:

1. **AWS Secrets Manager**:
```bash
aws secretsmanager create-secret \
  --name ecommerce/prod/db-password \
  --secret-string "your-secure-password"
```

2. **Terraform Variables de Entorno**:
```bash
export TF_VAR_db_password="your-secure-password"
```

3. **`.tfvars` local** (no versionado):
```bash
# secrets.tfvars (añadir a .gitignore)
db_password = "your-secure-password"
```

### Security Groups

Los security groups están configurados con el principio de menor privilegio:
- ALB: Solo 80/443 desde internet
- ECS: Solo desde ALB
- RDS: Solo desde ECS
- Redis: Solo desde ECS

## 📊 Monitoreo

### CloudWatch Dashboard

Después del deployment, acceder al dashboard:
```
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=ecommerce-{environment}-dashboard
```

### Alarmas Configuradas

- **ECS**: CPU y Memory utilization
- **ALB**: Response time y errores 5XX
- **RDS**: CPU, storage y conexiones
- **Redis**: CPU y cache hits

### Logs

Los logs están centralizados en CloudWatch Logs:
```bash
# Ver logs del backend
aws logs tail /ecs/ecommerce-{environment}-backend --follow

# Ver logs del frontend
aws logs tail /ecs/ecommerce-{environment}-frontend --follow
```

## 🔄 Auto Scaling

### Políticas Configuradas

- **Target Tracking**: CPU 70%, Memory 80%
- **Min Capacity**: 1-3 (según ambiente)
- **Max Capacity**: 3-20 (según ambiente)

### Modificar Auto Scaling

Editar en `environments/{env}/terraform.tfvars`:
```hcl
min_capacity = 2
max_capacity = 10
target_cpu_utilization = 70
target_memory_utilization = 80
```

## 💰 Optimización de Costos

### Spot Instances

Para ambientes no críticos, habilitar Spot instances:
```hcl
enable_spot_instances = true
```

### Graviton Processors

Usar instancias ARM para mejor precio/performance:
```hcl
enable_graviton = true
```

### Tagging para Cost Allocation

Todos los recursos están taggeados automáticamente:
- `Project`: ecommerce
- `Environment`: dev/staging/prod
- `ManagedBy`: terraform

## 🔧 Troubleshooting

### Error: Backend not initialized

```bash
terraform init -reconfigure
```

### Error: State lock

```bash
# Forzar unlock (usar con cuidado)
terraform force-unlock <LOCK_ID>
```

### Error: Resource already exists

```bash
# Importar recurso existente
terraform import aws_vpc.main vpc-xxxxx
```

## 🧹 Cleanup

### Destruir Infraestructura

⚠️ **CUIDADO**: Esto eliminará TODOS los recursos.

```bash
# Desarrollo
terraform destroy -var-file="environments/dev/terraform.tfvars"

# NUNCA ejecutar en producción sin backup
```

### Backup antes de Destroy

```bash
# Backup del estado
aws s3 cp s3://ecommerce-terraform-state/terraform.tfstate ./backup/

# Backup de RDS
aws rds create-db-snapshot \
  --db-instance-identifier ecommerce-prod-db \
  --db-snapshot-identifier ecommerce-prod-backup-$(date +%Y%m%d)
```

## 📚 Referencias

- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

## 🆘 Soporte

Para problemas o preguntas:
1. Revisar logs en CloudWatch
2. Verificar security groups
3. Revisar estado de Terraform: `terraform show`
4. Contactar al equipo DevOps

---

**Nota**: Esta configuración está diseñada para ambientes de producción con high availability, auto-scaling y monitoreo completo.