# Kubecore Python REST API Template

A production-ready Python REST API template built with FastAPI, designed for cloud-native deployments within the Kubecore platform. This repository provides a complete development ecosystem with GitOps integration, automated CI/CD pipelines, and an intelligent agentic development framework.

## 🎯 **Repository Overview**

This template serves as the foundation for building scalable, secure, and observable Python microservices. It includes:

- **FastAPI** framework for high-performance REST APIs
- **Poetry** for dependency management and packaging
- **Docker** containerization with multi-architecture support
- **GitOps** workflow integration with Argo CD and Argo Rollouts
- **Comprehensive observability** with OpenTelemetry, Prometheus, and Grafana
- **Security-first approach** with Zitadel authentication and RBAC
- **Intelligent development assistance** through specialized AI agents

## 📁 **Project Structure**

```
kubeapp-python-rest/
├── app/                          # Application code
│   ├── app/                      # Main FastAPI application
│   │   ├── main.py              # Application entry point
│   │   ├── config.py            # Configuration management
│   │   ├── __version__.py       # Version information
│   │   └── core/                # Core functionality modules
│   │       ├── fastapi/         # FastAPI-specific components
│   │       │   ├── models/      # Pydantic models
│   │       │   └── routers/     # API route handlers
│   │       ├── otlp/           # OpenTelemetry utilities
│   │       └── zitadel/        # Authentication & authorization
│   ├── tests/                   # Unit tests and fixtures
│   ├── Dockerfile              # Container configuration
│   ├── pyproject.toml          # Poetry dependencies
│   └── README.md               # Application-specific docs
├── etc/                         # Configuration files
│   ├── dashboards/             # Grafana dashboards
│   ├── grafana/               # Grafana configuration
│   └── prometheus/            # Prometheus configuration
├── .github/                     # CI/CD workflows
│   └── release-strategy-gitflow.md  # Comprehensive GitFlow strategy
├── .cursor/                     # AI agent configurations
│   └── rules/                  # Agent rule definitions
└── docker-compose.yaml        # Local development setup
```

## 🚀 **Getting Started**

### Prerequisites

- **Python 3.11+**
- **Poetry** for dependency management
- **Docker** and **Docker Compose**
- **Git** with proper configuration

### Quick Start

1. **Clone and Setup**:
   ```bash
   git clone <repository-url>
   cd kubeapp-python-rest
   poetry install
   poetry shell
   ```

2. **Local Development**:
   ```bash
   # Start all services (app, monitoring stack)
   docker-compose up -d
   
   # Or run just the application
   cd app
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access Services**:
   - **API**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health
   - **Grafana**: http://localhost:3000 (admin/admin)
   - **Prometheus**: http://localhost:9090

### Development Workflow

Our development process follows a structured GitFlow strategy with preview environments and automated deployments. See the [comprehensive GitFlow strategy guide](.github/release-strategy-gitflow.md) for detailed workflows.

**Quick Development Flow**:
1. Create feature branch from `dev`
2. Implement with tests
3. Open PR to `dev` with `preview` label
4. Test in preview environment
5. Merge to `dev` → staging → production

## 📋 **GitFlow Strategy & Release Management**

This repository implements a comprehensive branching and release strategy integrated with GitOps workflows. Key aspects include:

### Branch Strategy
- **`main`**: Production-ready code
- **`dev`**: Integration branch for ongoing development
- **`feature/*`**: New features and enhancements
- **`rc/vX.Y.Z`**: Release candidate stabilization
- **`hotfix/*`**: Critical production fixes

### Environment Progression
```
feature → dev → staging → production
    ↓        ↓        ↓        ↓
preview   dev-env  staging  production
```

### Key Features
- **Automatic Preview Environments** for every PR
- **Progressive Deployments** with Argo Rollouts
- **Automated Version Management** based on branch prefixes
- **Multi-Architecture Image Builds** (AMD64/ARM64)
- **Security Scanning** at every stage

📖 **For complete details, see**: [**GitFlow Strategy Guide**](.github/release-strategy-gitflow.md)

## 🤖 **Agentic Development Framework**

This repository includes an intelligent AI-powered development assistant system with specialized agents to guide you through the entire development lifecycle.

### Available Agents

#### 🏠 **Welcome Agent** *(Always Active)*
Your entry point and guide to the development environment.

**Capabilities**:
- Personal welcome and orientation
- Project status overview
- Intelligent routing to specialist agents
- Workflow guidance

**Activation**: Automatically active when you open the repository

---

#### 🔧 **New Endpoint Agent**
Specialized in creating new API endpoints and features.

**Capabilities**:
- PRD-guided feature development
- FastAPI endpoint generation
- Authentication & authorization integration
- GitFlow workflow management
- Feature branch creation and management

**Triggers**: `"new endpoint"`, `"create API"`, `"new feature"`, `"implement feature"`

---

#### 🧪 **Testing Agent**
Ensures code quality through comprehensive testing.

**Capabilities**:
- Automatic unit test generation
- Test coverage validation
- Code quality assessment
- Integration with CI/CD pipelines
- Pytest configuration and execution

**Triggers**: `"test"`, `"unit test"`, `"validate"`, `"quality check"`

---

#### 📋 **PRD Agent**
Manages Product Requirements Documents and feature planning.

**Capabilities**:
- PRD creation and management
- Requirement tracking
- User story development
- Acceptance criteria definition
- Feature scope management

**Triggers**: `"PRD"`, `"requirements"`, `"plan"`, `"specification"`

---

#### 🚀 **Release Management Agent**
Handles pull requests, deployments, and release coordination.

**Capabilities**:
- PR creation and management
- Preview environment deployment
- GitFlow workflow enforcement
- CI/CD pipeline monitoring
- Release coordination

**Triggers**: `"PR"`, `"pull request"`, `"deploy"`, `"preview"`, `"ready to merge"`

### How to Use the Agentic Framework

#### 1. **Natural Language Interaction**
Simply describe what you want to do in natural language:

```
"I want to create a new user management endpoint"
"Test my current implementation"
"I'm ready to create a pull request"
"Plan a new authentication feature"
```

#### 2. **Agent Workflow Integration**
The agents work together seamlessly:

```
Feature Planning → Development → Testing → Release
      ↓               ↓           ↓         ↓
  PRD Agent → New Endpoint → Testing → Release Mgmt
```

#### 3. **Intelligent Routing**
The Welcome Agent automatically routes you to the right specialist:

- **Feature Development**: Routes to New Endpoint Agent
- **Quality Assurance**: Routes to Testing Agent
- **Planning & Documentation**: Routes to PRD Agent
- **Deployment & Integration**: Routes to Release Management Agent

#### 4. **Contextual Assistance**
Each agent maintains context about:
- Your current branch and git status
- Project structure and dependencies
- Development workflow state
- Previous interactions and progress

### Getting Started with Agents

1. **Open the repository** - Welcome Agent automatically greets you
2. **Describe your goal** - Use natural language to explain what you want to do
3. **Follow guided workflow** - Each agent provides step-by-step guidance
4. **Seamless handoffs** - Agents coordinate with each other automatically

**Example Interactions**:
```
You: "I want to add a new API endpoint for user profiles"
→ Welcome Agent routes you to New Endpoint Agent
→ New Endpoint Agent guides you through PRD creation
→ Implementation with tests
→ PR creation and deployment
```

### Agent Benefits

- **🎯 Focused Expertise**: Each agent specializes in specific development phases
- **📋 Structured Workflow**: Enforces best practices and GitFlow compliance
- **🔄 Continuous Integration**: Seamless handoffs between development phases
- **📖 Knowledge Retention**: Agents remember context and project patterns
- **🚀 Accelerated Development**: Reduces cognitive load and decision fatigue

## 🛠 **Development Tools & Integration**

### Built-in Observability
- **OpenTelemetry**: Distributed tracing and metrics
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Dashboards and visualization
- **Health checks**: Comprehensive health monitoring

### Security & Authentication
- **Zitadel Integration**: Enterprise-grade authentication
- **RBAC Support**: Role-based access control
- **Security Scanning**: Automated vulnerability detection
- **Container Security**: Multi-layer security scanning

### CI/CD Integration
- **GitHub Actions**: Automated testing and deployment
- **Argo CD**: GitOps-based deployment management
- **Argo Rollouts**: Progressive deployment strategies
- **Multi-arch Builds**: AMD64 and ARM64 support

## 📚 **Additional Resources**

- 📖 [**GitFlow Strategy Guide**](.github/release-strategy-gitflow.md) - Comprehensive branching and release strategy
- 🔧 [**Application README**](app/README.md) - Application-specific documentation
- 🐳 [**Docker Configuration**](docker-compose.yaml) - Local development setup
- 📊 [**Grafana Dashboards**](etc/dashboards/) - Observability configurations

## 🤝 **Contributing**

1. Use the **Agentic Framework** for guided development
2. Follow the **GitFlow Strategy** for branch management
3. Ensure **comprehensive testing** before PR creation
4. Use **preview environments** for validation
5. Follow **security best practices** throughout development

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎯 Ready to start developing?** Just open this repository and say hello to begin your guided development experience!