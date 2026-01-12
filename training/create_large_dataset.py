"""
Create Large Dataset for Spam Detection
Generates 200+ realistic job postings for training
"""

import json
import csv
from pathlib import Path
from datetime import datetime
import random

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Spam job templates
SPAM_TEMPLATES = [
    {
        "title": "Work from Home - Earn ${amount}/week!!!",
        "description": "Amazing opportunity to work from home and earn big money!!! No experience needed. Contact me at {phone} or email: {email} for more details. Must call now!!!"
    },
    {
        "title": "URGENT: {job_type} - ${rate}/hour!!!",
        "description": "Need someone immediately. Call {phone}. Send resume to {email}. Payment guaranteed! Wire transfer available."
    },
    {
        "title": "Make Money Fast - No Skills Required",
        "description": "Earn thousands per week from your phone!!! Text {phone} or whatsapp {phone2}. Limited spots available. Act now!!!"
    },
    {
        "title": "$$$ URGENT HIRING $$$ - {job_type}",
        "description": "Need {count} people ASAP!!! Email: {email} or call {phone}. Flexible hours!!! Earn ${amount1}-${amount2} monthly!!!"
    },
    {
        "title": "Easy Online Job - Start Today!!!",
        "description": "No interview needed. Just send your info to {email} or text {phone}. Get paid daily via PayPal or Western Union."
    },
    {
        "title": "{job_type} needed!!! HIGH PAY!!!",
        "description": "Must have phone and email. Contact {email} or call {phone}. Easy work, big money!!! Start ASAP!!!"
    },
    {
        "title": "MAKE ${amount} IN 30 DAYS - GUARANTEED",
        "description": "Revolutionary business opportunity. Call now: {phone} or email {email}. Limited time offer!!!"
    },
    {
        "title": "Work {hours} Hours Daily - Earn ${amount} Monthly",
        "description": "Perfect for stay-at-home parents!!! Email {email} to apply. Phone interviews at {phone}."
    },
    {
        "title": "🔥🔥🔥 HOT JOB ALERT 🔥🔥🔥 ${amount}/DAY!!!",
        "description": "CLICK HERE NOW!!! Email {email} or text {phone} IMMEDIATELY. Don't miss this chance!!!"
    },
    {
        "title": "BE YOUR OWN BOSS - ${amount} WEEKLY",
        "description": "Join our team today! No experience, no problem! Call {phone} or message {email}. Payment by cash/PayPal/Venmo!!!"
    }
]

# Poor quality templates
POOR_TEMPLATES = [
    {
        "title": "need help with stuff",
        "description": "looking for someone to help me with various tasks. pay is negotiable. contact for more info."
    },
    {
        "title": "Helper Needed",
        "description": "Need someone to help with project. Budget: ${budget}. Must start immediately."
    },
    {
        "title": "Quick task",
        "description": "i need this done asap. very simple task. looking for cheapest bidder."
    },
    {
        "title": "Do this for me",
        "description": "I need someone to do something. Budget is ${budget}. Must complete in 1 hour."
    },
    {
        "title": "{skill} expert",
        "description": "need quick help. small budget. message me"
    },
    {
        "title": "simple job",
        "description": "easy task need done fast. low pay but quick work"
    },
    {
        "title": "help needed urgently",
        "description": "i have a thing that needs doing. not much money but wont take long"
    },
    {
        "title": "{job_type} needed cheap",
        "description": "looking for someone cheap to do this. budget ${budget}. must be done today"
    }
]

# Good quality templates
GOOD_TEMPLATES = [
    {
        "title": "{skill} Developer for {project_type} Project",
        "description": "We need an experienced {skill} developer to build {project_desc}. Requirements: Strong {skill} skills, experience with {tech1} and {tech2}, knowledge of {concept}. Budget: ${budget1}-${budget2}. Timeline: {timeline}. Please include examples of previous {project_type} projects in your proposal."
    },
    {
        "title": "{skill} {role} - {project_type}",
        "description": "Looking for a skilled {skill} {role} to {task}. You'll work with our existing {tech1} and create {deliverable}. Requirements: {skill} expertise, experience with {tech2}, {capability} skills. Budget: ${budget1}-${budget2}. Project duration: {timeline}."
    },
    {
        "title": "{role} for {industry} Project",
        "description": "Seeking an experienced {role} to create {deliverable} for our {industry} platform. We need {count} {item} ({spec} each). Requirements: Strong {skill} skills, technical background in {field}, ability to {capability}. Rate: ${rate1}-${rate2} per {unit}."
    },
    {
        "title": "{project_type} Development",
        "description": "Need help {task} for our {project_type}. Tasks include: {task1}, {task2}, {task3}, and {task4}. Requirements: {skill} expertise, {tech1} knowledge, experience with {tech2}. Budget: ${budget1}-${budget2}. Expected completion: {timeline}."
    },
    {
        "title": "{skill} Specialist for {duration} Project",
        "description": "We have {amount} of {data_type} data and need {analysis_type}. Deliverables include: {deliv1}, {deliv2}, {deliv3}, and {deliv4} report. Requirements: {skill} proficiency, {tech1} experience, {tech2} skills. Budget: ${budget1}-${budget2}."
    }
]

# Excellent quality templates
EXCELLENT_TEMPLATES = [
    {
        "title": "Senior {role} - Long-term {project_type} Project",
        "description": "We're building a {industry} SaaS platform for {purpose} and need an experienced {role} for ongoing work. Tech stack: {tech1} frontend, {tech2} backend, {tech3} database, {tech4} infrastructure. Your responsibilities: architect new features, implement APIs, write comprehensive tests, mentor junior developers, participate in code reviews. Requirements: {years}+ years experience, strong {skill1}/{skill2} skills, {tech3} design expertise, RESTful API development, CI/CD pipeline knowledge, excellent communication. We value: clean code, documentation, scalability considerations. Long-term engagement: {hours} hours/week for {duration}. Rate: ${rate1}-${rate2}/hour. Please include: GitHub profile, portfolio, and examples of production applications you've built. We have {reviews} 5-star reviews and perfect payment history."
    },
    {
        "title": "{role} - {specialty} Project",
        "description": "Established {industry} company seeking {role} to develop {project_desc}. Project scope: {scope1}, {scope2}, {scope3}, {scope4}. Technical requirements: Strong {skill1} skills, {tech1}/{tech2} expertise, experience with {tech3}, knowledge of {concept}, {tech4} deployment. Deliverables: {deliv1}, {deliv2}, {deliv3}, {deliv4}. Budget: ${budget1}-${budget2}. Timeline: {timeline} with milestone-based payments. This is through our established company with verified payment record. Please include: relevant projects, published papers if applicable, and references from previous {specialty} work."
    },
    {
        "title": "{role} - {industry} Education Platform",
        "description": "Leading online education platform seeking {role} for comprehensive course on {topic}. Responsibilities: create curriculum for {duration}-hour course covering {topic1}, {topic2}, {topic3}, {topic4}; write detailed lesson scripts; create code examples and exercises; record video tutorials; develop hands-on projects. Requirements: {years}+ years {skill} experience, previous teaching/content creation, excellent verbal and written communication, native/near-native English proficiency. Course target audience: {audience} looking to build {skill_goal} skills. Budget: ${budget1}-${budget2} for complete course. Timeline: {timeline} with milestone-based payments. Our platform has served {students}+ students. We provide full production support and marketing."
    },
    {
        "title": "{role} - {tech} Infrastructure Redesign",
        "description": "Growing {industry} startup needs {role} expert to redesign our {tech} infrastructure for scalability and security. Current state: {current1}, {current2}, {current3}. Your mission: design {arch} architecture, implement IaC ({iac_tool}), set up CI/CD pipelines ({ci_tool}), configure monitoring ({monitor_tool}), implement security best practices, create disaster recovery plan. Requirements: {years}+ years experience, {cert} certification preferred, deep {tech1} knowledge, {tech2}/{tech3} expertise, security compliance understanding ({compliance}), on-call availability for migration phase. Project phases: assessment ({phase1}), architecture design ({phase2}), implementation ({phase3}), migration ({phase4}), documentation. Budget: ${budget1}-${budget2}. We're a {stage} funded company with strong growth trajectory and excellent team culture."
    }
]

# Helper data
PHONES = ["555-123-4567", "555-987-6543", "555-444-3333", "555-222-1111", "555-777-8888", "555-333-2222", "555-666-9999", "555-888-7777"]
EMAILS = ["hiring@example.com", "jobs@company.com", "contact@work.net", "apply@jobsite.com", "recruiting@hire.com"]
SKILLS = ["Python", "JavaScript", "React", "Node.js", "Java", "PHP", "Ruby", "Go", "TypeScript", "Vue.js", "Angular", "Django", "FastAPI", "Express", "Spring"]
ROLES = ["Developer", "Engineer", "Specialist", "Consultant", "Architect", "Designer", "Analyst", "Manager"]
PROJECT_TYPES = ["Web Application", "Mobile App", "API", "E-commerce Site", "Dashboard", "CRM System", "Analytics Platform", "Automation Tool"]
INDUSTRIES = ["FinTech", "HealthTech", "EdTech", "E-commerce", "SaaS", "Marketing", "Real Estate", "Logistics"]

def generate_spam_job(idx):
    template = random.choice(SPAM_TEMPLATES)
    return {
        "job_id": f"spam_{idx}",
        "title": template["title"].format(
            amount=random.choice([3000, 5000, 8000, 10000]),
            job_type=random.choice(["Data Entry", "Virtual Assistant", "Customer Service", "Admin Work"]),
            rate=random.choice([25, 35, 50, 75]),
            count=random.choice([5, 10, 20]),
            amount1=random.choice([2000, 3000, 5000]),
            amount2=random.choice([8000, 10000, 15000]),
            hours=random.choice([2, 3, 4])
        ),
        "description": template["description"].format(
            phone=random.choice(PHONES),
            phone2=random.choice(PHONES),
            email=random.choice(EMAILS),
            job_type=random.choice(["Data Entry", "Virtual Assistant", "Customer Service"]),
            count=random.choice([5, 10, 20]),
            amount=random.choice([5000, 8000, 10000]),
            amount1=random.choice([3000, 5000]),
            amount2=random.choice([8000, 10000]),
            hours=random.choice([2, 3, 4])
        ),
        "proposals": str(random.randint(50, 100)),
        "payment_verified": False,
        "client_spending": str(random.randint(0, 500)),
        "client_rating": str(random.uniform(2.0, 3.5)),
        "posted_time_seconds": str(random.randint(3600, 86400)),
        "job_type": "hourly",
        "budget": str(random.randint(50, 200)),
        "hourly_rate": str(random.randint(5, 15)),
        "quality_label": "spam",
        "labeled_at": datetime.now().isoformat(),
        "source": "generated"
    }

def generate_poor_job(idx):
    template = random.choice(POOR_TEMPLATES)
    return {
        "job_id": f"poor_{idx}",
        "title": template["title"].format(
            skill=random.choice(SKILLS),
            job_type=random.choice(["helper", "worker", "person"])
        ),
        "description": template["description"].format(
            budget=random.randint(5, 50),
            job_type=random.choice(["work", "task", "job"])
        ),
        "proposals": str(random.randint(30, 70)),
        "payment_verified": random.choice([True, False]),
        "client_spending": str(random.randint(100, 2000)),
        "client_rating": str(random.uniform(2.5, 4.0)),
        "posted_time_seconds": str(random.randint(7200, 172800)),
        "job_type": "fixed",
        "budget": str(random.randint(10, 100)),
        "hourly_rate": str(random.randint(10, 20)),
        "quality_label": "poor",
        "labeled_at": datetime.now().isoformat(),
        "source": "generated"
    }

def generate_good_job(idx):
    template = random.choice(GOOD_TEMPLATES)
    skill = random.choice(SKILLS)
    
    # Create all possible format parameters
    format_params = {
        "skill": skill,
        "role": random.choice(ROLES),
        "project_type": random.choice(PROJECT_TYPES),
        "industry": random.choice(INDUSTRIES),
        "project_desc": f"a {random.choice(PROJECT_TYPES).lower()} system",
        "tech1": random.choice(["React", "Vue", "Angular", "Python"]),
        "tech2": random.choice(["Node.js", "Django", "FastAPI", "Express"]),
        "concept": random.choice(["responsive design", "API integration", "database optimization"]),
        "budget1": random.randint(500, 1500),
        "budget2": random.randint(1500, 3000),
        "timeline": random.choice(["2 weeks", "3 weeks", "1 month", "6 weeks"]),
        "task": random.choice(["develop", "implement", "create", "build"]),
        "deliverable": random.choice(["a dashboard", "an API", "a mobile app"]),
        "capability": random.choice(["analytical", "problem-solving", "communication"]),
        "count": random.randint(5, 15),
        "item": random.choice(["screens", "pages", "components", "modules"]),
        "spec": random.choice(["high-quality", "responsive", "interactive"]),
        "field": random.choice(["web development", "software engineering", "data science"]),
        "rate1": random.randint(30, 60),
        "rate2": random.randint(60, 100),
        "unit": random.choice(["article", "hour", "page"]),
        "task1": random.choice(["UI design", "backend setup", "database schema"]),
        "task2": random.choice(["API integration", "authentication", "data processing"]),
        "task3": random.choice(["testing", "deployment", "documentation"]),
        "task4": random.choice(["optimization", "security", "monitoring"]),
        "amount": random.choice(["6 months", "1 year", "500GB"]),
        "data_type": random.choice(["customer", "transaction", "analytics"]),
        "analysis_type": random.choice(["statistical analysis", "pattern detection", "trend analysis"]),
        "deliv1": random.choice(["cleaned dataset", "data model", "ETL pipeline"]),
        "deliv2": random.choice(["statistical analysis", "visualizations", "dashboard"]),
        "deliv3": random.choice(["predictive model", "insights report", "recommendations"]),
        "deliv4": random.choice(["actionable insights", "implementation plan", "documentation"]),
        "duration": random.choice(["short-term", "medium-term", "long-term"])
    }
    
    return {
        "job_id": f"good_{idx}",
        "title": template["title"].format(**format_params),
        "description": template["description"].format(**format_params),
        "proposals": str(random.randint(10, 30)),
        "payment_verified": True,
        "client_spending": str(random.randint(5000, 30000)),
        "client_rating": str(random.uniform(4.0, 4.8)),
        "posted_time_seconds": str(random.randint(3600, 43200)),
        "job_type": random.choice(["fixed", "hourly"]),
        "budget": str(random.randint(800, 2500)),
        "hourly_rate": str(random.randint(30, 60)),
        "quality_label": "good",
        "labeled_at": datetime.now().isoformat(),
        "source": "generated"
    }

def generate_excellent_job(idx):
    template = random.choice(EXCELLENT_TEMPLATES)
    
    # Create all possible format parameters
    format_params = {
        "role": random.choice(["Full-Stack Developer", "ML Engineer", "DevOps Engineer", "Technical Content Creator"]),
        "project_type": random.choice(["SaaS", "Enterprise", "Platform", "Cloud"]),
        "specialty": random.choice(["Computer Vision", "NLP", "Cloud Infrastructure", "API Development"]),
        "industry": random.choice(INDUSTRIES),
        "tech": random.choice(["AWS", "Azure", "GCP", "Kubernetes"]),
        "purpose": random.choice(["project management", "customer analytics", "team collaboration"]),
        "tech1": random.choice(["React", "Vue", "Angular"]),
        "tech2": random.choice(["Node.js", "Python", "Java"]),
        "tech3": random.choice(["PostgreSQL", "MongoDB", "MySQL"]),
        "tech4": random.choice(["AWS", "Azure", "Docker"]),
        "years": random.choice([5, 7, 10]),
        "skill1": random.choice(["JavaScript", "Python", "TypeScript"]),
        "skill2": random.choice(["React", "Node.js", "Django"]),
        "hours": random.choice([30, 35, 40]),
        "duration": random.choice(["6+ months", "1+ year", "ongoing"]),
        "rate1": random.randint(60, 80),
        "rate2": random.randint(80, 120),
        "reviews": random.choice([50, 100, 200]),
        "project_desc": f"{random.choice(PROJECT_TYPES)} for {random.choice(INDUSTRIES)}",
        "scope1": random.choice(["dataset preparation", "system architecture", "API design"]),
        "scope2": random.choice(["model training", "implementation", "integration"]),
        "scope3": random.choice(["optimization", "testing", "deployment"]),
        "scope4": random.choice(["documentation", "monitoring", "maintenance"]),
        "skill": random.choice(SKILLS),
        "concept": random.choice(["microservices", "event-driven architecture", "serverless"]),
        "deliv1": random.choice(["trained model", "API documentation", "deployment guide"]),
        "deliv2": random.choice(["test suite", "monitoring dashboard", "CI/CD pipeline"]),
        "deliv3": random.choice(["performance report", "security audit", "scalability plan"]),
        "deliv4": random.choice(["user documentation", "admin guide", "troubleshooting manual"]),
        "budget1": random.randint(8000, 15000),
        "budget2": random.randint(15000, 25000),
        "timeline": random.choice(["8-10 weeks", "10-12 weeks", "3 months"]),
        "topic": random.choice(["modern web development", "cloud architecture", "machine learning"]),
        "topic1": random.choice(["React", "Python", "AWS"]),
        "topic2": random.choice(["Node.js", "Django", "Docker"]),
        "topic3": random.choice(["MongoDB", "PostgreSQL", "Redis"]),
        "topic4": random.choice(["authentication", "deployment", "testing"]),
        "audience": random.choice(["intermediate developers", "beginners", "professionals"]),
        "skill_goal": random.choice(["full-stack", "backend", "frontend"]),
        "students": random.choice(["100K", "500K", "1M"]),
        "current1": random.choice(["monolithic architecture", "manual deployments", "limited monitoring"]),
        "current2": random.choice(["single server", "basic backup", "no automation"]),
        "current3": random.choice(["minimal logging", "reactive maintenance", "tech debt"]),
        "arch": random.choice(["microservices", "serverless", "containerized"]),
        "iac_tool": random.choice(["Terraform", "CloudFormation", "Pulumi"]),
        "ci_tool": random.choice(["GitHub Actions", "GitLab CI", "Jenkins"]),
        "monitor_tool": random.choice(["Datadog", "CloudWatch", "Prometheus"]),
        "cert": random.choice(["AWS Certified", "Azure Certified", "GCP Certified"]),
        "compliance": random.choice(["SOC2", "PCI", "HIPAA"]),
        "phase1": random.choice(["1 week", "2 weeks"]),
        "phase2": random.choice(["2 weeks", "3 weeks"]),
        "phase3": random.choice(["6 weeks", "8 weeks"]),
        "phase4": random.choice(["2 weeks", "3 weeks"]),
        "stage": random.choice(["Series A", "Series B", "Series C"])
    }
    
    return {
        "job_id": f"excellent_{idx}",
        "title": template["title"].format(**format_params),
        "description": template["description"].format(**format_params),
        "proposals": str(random.randint(5, 20)),
        "payment_verified": True,
        "client_spending": str(random.randint(50000, 200000)),
        "client_rating": str(random.uniform(4.8, 5.0)),
        "posted_time_seconds": str(random.randint(1800, 21600)),
        "job_type": random.choice(["hourly", "fixed"]),
        "budget": str(random.randint(5000, 20000)),
        "hourly_rate": str(random.randint(60, 100)),
        "quality_label": "excellent",
        "labeled_at": datetime.now().isoformat(),
        "source": "generated"
    }

def create_large_dataset():
    """Create dataset with 200+ labeled jobs"""
    print("Creating large dataset with 200+ labeled jobs...")
    print("="*70)
    
    all_jobs = []
    
    # Generate 60 spam jobs
    print("\nGenerating 60 spam jobs...")
    for i in range(60):
        all_jobs.append(generate_spam_job(i+1))
    
    # Generate 40 poor quality jobs
    print("Generating 40 poor quality jobs...")
    for i in range(40):
        all_jobs.append(generate_poor_job(i+1))
    
    # Generate 70 good quality jobs
    print("Generating 70 good quality jobs...")
    for i in range(70):
        all_jobs.append(generate_good_job(i+1))
    
    # Generate 40 excellent quality jobs
    print("Generating 40 excellent quality jobs...")
    for i in range(40):
        all_jobs.append(generate_excellent_job(i+1))
    
    # Shuffle to mix quality levels
    random.shuffle(all_jobs)
    
    # Save to CSV
    csv_file = DATA_DIR / "large_dataset.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=all_jobs[0].keys())
        writer.writeheader()
        writer.writerows(all_jobs)
    
    # Save to JSON
    json_file = DATA_DIR / "large_dataset.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, indent=2)
    
    print(f"\n{'='*70}")
    print("Dataset created successfully!")
    print(f"{'='*70}")
    print(f"\nCSV: {csv_file}")
    print(f"JSON: {json_file}")
    
    print(f"\nDataset statistics:")
    print(f"  Total jobs: {len(all_jobs)}")
    print(f"  Spam: 60 (28.6%)")
    print(f"  Poor: 40 (19.0%)")
    print(f"  Good: 70 (33.3%)")
    print(f"  Excellent: 40 (19.0%)")
    
    print(f"\nFor spam detection (binary classification):")
    print(f"  Spam: 60 (28.6%)")
    print(f"  Not Spam: 150 (71.4%)")
    
    print(f"\nReady for training!")
    return csv_file

if __name__ == "__main__":
    create_large_dataset()
