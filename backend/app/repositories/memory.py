from datetime import date, timedelta

from app.models.company import CompanyProfile


def demo_tenders() -> list[dict]:
    today = date.today()
    return [
        {"id":"tnd-001","title":"Development of Enterprise Resource Planning System","organization":"Punjab Information Technology Board","category":"Software & IT","location":"Lahore, Punjab","procurement_method":"Open Competitive Bidding","published_at":str(today-timedelta(days=8)),"deadline":str(today+timedelta(days=12)),"estimated_value_pkr":12500000,"summary":"Design, implementation and support of an integrated ERP platform for provincial departments.","requirements":["Minimum 5 years enterprise software experience","At least 3 comparable public-sector projects","Active tax registration"],"source":"TenderIQ sample data","status":"open"},
        {"id":"tnd-002","title":"Cybersecurity Assessment and Penetration Testing","organization":"National Database & Registration Authority","category":"Cybersecurity","location":"Islamabad, ICT","procurement_method":"Request for Proposals","published_at":str(today-timedelta(days=4)),"deadline":str(today+timedelta(days=5)),"estimated_value_pkr":4800000,"summary":"Independent security assessment of web applications, infrastructure and security controls.","requirements":["Recognized information security certification","5 years of penetration testing experience","Three similar assignments"],"source":"TenderIQ sample data","status":"closing_soon"},
        {"id":"tnd-003","title":"Cloud Migration and Managed Infrastructure Services","organization":"State Bank of Pakistan","category":"Cloud & Infrastructure","location":"Karachi, Sindh","procurement_method":"Two-stage bidding","published_at":str(today-timedelta(days=11)),"deadline":str(today+timedelta(days=19)),"estimated_value_pkr":32000000,"summary":"Migration planning and managed cloud infrastructure for selected internal applications.","requirements":["Cloud partner certification","Experience with regulated financial institutions","24/7 operations capability"],"source":"TenderIQ sample data","status":"open"},
        {"id":"tnd-004","title":"Digital Skills Learning Management Platform","organization":"Higher Education Commission","category":"Software & IT","location":"Islamabad, ICT","procurement_method":"Request for Proposals","published_at":str(today-timedelta(days=6)),"deadline":str(today+timedelta(days=27)),"estimated_value_pkr":8900000,"summary":"A configurable learning platform with reporting, identity integration and support for universities.","requirements":["Learning platform implementation experience","Accessibility compliant interface","Local support team"],"source":"TenderIQ sample data","status":"open"},
        {"id":"tnd-005","title":"Network Equipment Supply and Installation","organization":"National Transmission & Despatch Company","category":"Networking","location":"Lahore, Punjab","procurement_method":"Single-stage bidding","published_at":str(today-timedelta(days=2)),"deadline":str(today+timedelta(days=3)),"estimated_value_pkr":6700000,"summary":"Supply, configuration and commissioning of network switches and security appliances.","requirements":["Manufacturer authorization","Relevant supply experience","Warranty and local service coverage"],"source":"TenderIQ sample data","status":"closing_soon"},
        {"id":"tnd-006","title":"Business Process Automation Consultancy","organization":"Khyber Pakhtunkhwa Revenue Authority","category":"Consultancy","location":"Peshawar, Khyber Pakhtunkhwa","procurement_method":"Quality and Cost Based Selection","published_at":str(today-timedelta(days=18)),"deadline":str(today-timedelta(days=1)),"estimated_value_pkr":3600000,"summary":"Process review and implementation roadmap for digitizing selected revenue services.","requirements":["Consulting firm with 7 years of experience","Three comparable transformation projects","Relevant domain experts"],"source":"TenderIQ sample data","status":"closed"},
    ]


class MemoryStore:
    def __init__(self):
        self.tenders = demo_tenders()
        self.company = CompanyProfile(name="ABC Technologies",industry="Software Development",services=["Web development","Cloud solutions","IT consultancy"],years_experience=6,employee_count=28,annual_turnover_pkr=42000000,certifications=["SECP registered","FBR registered"],past_projects=["Provincial e-services portal","Banking workflow automation"],location="Islamabad")
        self.analyses: dict[str, dict] = {}
        self.pipeline: dict[str, dict] = {}
