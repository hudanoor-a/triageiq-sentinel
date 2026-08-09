# TriageIQ + Sentinel - Branch A was here
## Project Structure
The mono repo structure has been created where one repo contains multiple services. For this project, mono repo is suitable as all the services are interconnected and deployed together and one CI/CD pipeline can manage both.

triageiq/    → the Flask ML API code will live here

sentinel/    → the anomaly detection service will live here  

infra/       → Terraform configs will live here (Week 3)

scripts/     → operational scripts like health_check.sh

README.md    → project documentation
