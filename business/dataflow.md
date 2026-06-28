 # Context
Product: memory-sleuth
Repo: https://github.com/arkashira/memory-sleuth
Hypothesis: A memory optimization tool that helps developers identify and fix memory-related issues in their codebase.
BD rationale: The pain point of memory usage management is not addressed by any existing Axentx product, and the evidence suggests a willingness to pay for a solution.
Market data:
- Number of developers expressing pain: 12,345
- Average monthly subscription price: $29.99
- Total addressable market (TAM): 1,500,000 developers

# Task
Generate `dataflow.md`. Generate a system dataflow architecture. Sections: External data sources, Ingestion layer, Processing/transform layer, Storage tier, Query/serving layer, Egress to user. ASCII block diagram + bullet list of components per tier. Include auth boundaries.

```
## Dataflow Architecture for Memory-Sleuth

```

```
### External Data Sources
- Code repositories (e.g., GitHub, GitLab, Bitbucket)
- Continuous Integration/Continuous Deployment (CI/CD) tools (e.g., Jenkins, Travis CI, CircleCI)
- Application Performance Monitoring (APM) tools (e.g., New Relic, Dynatrace, Datadog)

### Ingestion Layer
- Webhooks from code repositories and CI/CD tools
- APIs from APM tools
- Authentication: OAuth2, API keys

### Processing/Transform Layer
- Code semantic search (Code-Semantic-Search)
- Memory usage analysis
- Issue detection and prioritization
- Code optimization suggestions

### Storage Tier
- Global Memory Index (Token-Optimized)
- Code repositories (for storing optimized code)
- Authentication: Role-based access control (RBAC)

### Query/Serving Layer
- REST API for querying memory usage issues and optimization suggestions
- GraphQL API for complex queries
- Authentication: JWT tokens

### Egress to User
- Web dashboard for viewing memory usage issues and optimization suggestions
- Email notifications for critical issues
- Integration with Slack, Microsoft Teams, and other collaboration tools
```