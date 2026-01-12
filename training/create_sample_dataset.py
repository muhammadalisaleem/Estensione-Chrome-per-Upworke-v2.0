"""
Create Sample Dataset for Spam Detection
Creates a small but realistic dataset for initial model training
"""

import json
import csv
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Sample spam job postings (typical characteristics)
SPAM_JOBS = [
    {
        "title": "Work from Home - Earn $5000/week!!! Easy Money!!!",
        "description": "Amazing opportunity to work from home and earn big money!!! No experience needed. Contact me at 555-123-4567 or email: easymoney@gmail.com for more details. Must call now!!!",
        "quality_label": "spam"
    },
    {
        "title": "URGENT: Data Entry - $50/hour!!!",
        "description": "Need someone immediately. Call 555-987-6543. Send resume to hiring@fakecompany.com. Payment guaranteed! Wire transfer available.",
        "quality_label": "spam"
    },
    {
        "title": "Make Money Fast - No Skills Required",
        "description": "Earn thousands per week from your phone!!! Text 555-444-3333 or whatsapp +1-555-444-3333. Limited spots available. Act now!!!",
        "quality_label": "spam"
    },
    {
        "title": "$$$ URGENT HIRING $$$  - Work From Anywhere",
        "description": "Need 10 people ASAP!!! Email: jobs123@yahoo.com or call 555-222-1111. Flexible hours!!! Earn $3000-$10000 monthly!!!",
        "quality_label": "spam"
    },
    {
        "title": "Easy Online Job - Start Today!!!",
        "description": "No interview needed. Just send your info to contact@easyjobs.net or text 555-777-8888. Get paid daily via PayPal or Western Union.",
        "quality_label": "spam"
    },
    {
        "title": "Remote Assistant needed!!! HIGH PAY!!!",
        "description": "Must have phone and email. Contact sarah.hiring@gmail.com or call 555-333-2222. Easy work, big money!!! Start ASAP!!!",
        "quality_label": "spam"
    },
    {
        "title": "MAKE $10000 IN 30 DAYS - GUARANTEED",
        "description": "Revolutionary business opportunity. Call now: 555-666-9999 or email success@fastmoney.com. Limited time offer!!!",
        "quality_label": "spam"
    },
    {
        "title": "Work 2 Hours Daily - Earn $5000 Monthly",
        "description": "Perfect for stay-at-home parents!!! Email yourname@email.com to apply. Phone interviews at 555-888-7777.",
        "quality_label": "spam"
    },
]

# Sample poor quality job postings
POOR_JOBS = [
    {
        "title": "need help with stuff",
        "description": "looking for someone to help me with various tasks. pay is negotiable. contact for more info.",
        "quality_label": "poor"
    },
    {
        "title": "Helper Needed",
        "description": "Need someone to help with project. Budget: $10. Must start immediately.",
        "quality_label": "poor"
    },
    {
        "title": "Quick task",
        "description": "i need this done asap. very simple task. looking for cheapest bidder.",
        "quality_label": "poor"
    },
    {
        "title": "Do this for me",
        "description": "I need someone to do something. Budget is $5. Must complete in 1 hour.",
        "quality_label": "poor"
    },
]

# Sample good quality job postings
GOOD_JOBS = [
    {
        "title": "Python Developer for Web Scraping Project",
        "description": "We need an experienced Python developer to build a web scraping tool for extracting product data from e-commerce websites. Requirements: Strong Python skills, experience with BeautifulSoup or Scrapy, knowledge of handling pagination and dynamic content. Budget: $500-$800. Timeline: 2 weeks. Please include examples of previous scraping projects in your proposal.",
        "quality_label": "good"
    },
    {
        "title": "React Frontend Developer - E-commerce Site",
        "description": "Looking for a skilled React developer to build the frontend for our e-commerce platform. You'll work with our existing API and create a modern, responsive interface. Requirements: React 18+, TypeScript, experience with state management (Redux or Context), responsive design skills. Budget: $1500-$2500. Project duration: 3-4 weeks.",
        "quality_label": "good"
    },
    {
        "title": "Content Writer for Tech Blog",
        "description": "Seeking an experienced technical writer to create articles about software development, cloud computing, and DevOps. We need 8 articles per month (1500-2000 words each). Requirements: Strong English writing skills, technical background in software development, ability to explain complex concepts clearly. Rate: $100-$150 per article.",
        "quality_label": "good"
    },
    {
        "title": "WordPress Site Customization",
        "description": "Need help customizing an existing WordPress site. Tasks include: theme modifications, plugin integration, performance optimization, and mobile responsiveness improvements. Requirements: WordPress expertise, PHP and CSS knowledge, experience with popular page builders. Budget: $300-$500. Expected completion: 1 week.",
        "quality_label": "good"
    },
    {
        "title": "Data Analysis - Customer Behavior Study",
        "description": "We have 6 months of customer transaction data and need analysis to identify patterns and trends. Deliverables include: cleaned dataset, statistical analysis, visualizations, and actionable insights report. Requirements: Python/R proficiency, pandas/numpy experience, data visualization skills (matplotlib/seaborn/tableau). Budget: $800-$1200.",
        "quality_label": "good"
    },
    {
        "title": "Mobile App UI/UX Design",
        "description": "Looking for a UI/UX designer to create mockups for our fitness tracking mobile app. Scope: user research analysis, wireframes, high-fidelity mockups for 15 screens, interactive prototype. Requirements: Figma expertise, mobile design experience, understanding of iOS/Android design guidelines. Budget: $600-$900. Timeline: 2-3 weeks.",
        "quality_label": "good"
    },
    {
        "title": "Database Optimization - PostgreSQL",
        "description": "Our PostgreSQL database is experiencing slow query performance. Need an expert to analyze, optimize queries, add appropriate indexes, and implement caching strategies. Requirements: Advanced PostgreSQL knowledge, query optimization experience, understanding of database architecture. Budget: $400-$700.",
        "quality_label": "good"
    },
    {
        "title": "API Integration - Payment Gateway",
        "description": "Need to integrate Stripe payment gateway into our existing Node.js application. Tasks: implement payment flow, handle webhooks, create subscription management features, add error handling. Requirements: Node.js/Express experience, Stripe API knowledge, understanding of payment security. Budget: $500-$800.",
        "quality_label": "good"
    },
]

# Sample excellent quality job postings
EXCELLENT_JOBS = [
    {
        "title": "Senior Full-Stack Developer - Long-term SaaS Project",
        "description": "We're building a B2B SaaS platform for project management and need an experienced full-stack developer for ongoing work. Tech stack: React/Next.js frontend, Node.js/Express backend, PostgreSQL database, AWS infrastructure. Your responsibilities: architect new features, implement APIs, write comprehensive tests, mentor junior developers, participate in code reviews. Requirements: 5+ years full-stack experience, strong JavaScript/TypeScript skills, database design expertise, RESTful API development, CI/CD pipeline knowledge, excellent communication. We value: clean code, documentation, scalability considerations. Long-term engagement: 30-40 hours/week for 6+ months. Rate: $60-$80/hour. Please include: GitHub profile, portfolio, and examples of production applications you've built. We have 50+ 5-star reviews and perfect payment history.",
        "quality_label": "excellent"
    },
    {
        "title": "Machine Learning Engineer - Computer Vision Project",
        "description": "Established AI company seeking ML engineer to develop object detection system for industrial quality control. Project scope: dataset preparation, model training (YOLO/EfficientDet), optimization for edge deployment, integration with existing pipeline. Technical requirements: Strong Python skills, PyTorch/TensorFlow expertise, experience with computer vision architectures, knowledge of model optimization (quantization, pruning), edge device deployment (Jetson Nano/Raspberry Pi). Deliverables: trained model, deployment package, comprehensive documentation, performance benchmarks. Budget: $8000-$12000. Timeline: 8-10 weeks. This is through our established company with verified payment record. Please include: relevant CV projects, published papers if applicable, and references from previous ML work.",
        "quality_label": "excellent"
    },
    {
        "title": "Technical Content Creator - Developer Education",
        "description": "Leading online education platform seeking technical content creator for comprehensive course on modern web development. Responsibilities: create curriculum for 40-hour course covering React, Node.js, MongoDB, authentication, deployment; write detailed lesson scripts; create code examples and exercises; record video tutorials; develop hands-on projects. Requirements: 7+ years web development experience, previous teaching/content creation, excellent verbal and written communication, native/near-native English proficiency. Course target audience: intermediate developers looking to build full-stack skills. Budget: $15000-$20000 for complete course. Timeline: 12-16 weeks with milestone-based payments. Our platform has served 500K+ students. We provide full production support and marketing.",
        "quality_label": "excellent"
    },
    {
        "title": "DevOps Engineer - AWS Infrastructure Redesign",
        "description": "Growing fintech startup needs DevOps expert to redesign our AWS infrastructure for scalability and security. Current state: monolithic architecture, manual deployments, limited monitoring. Your mission: design microservices architecture, implement IaC (Terraform), set up CI/CD pipelines (GitHub Actions), configure monitoring (Datadog/CloudWatch), implement security best practices, create disaster recovery plan. Requirements: 5+ years DevOps experience, AWS certification (Solutions Architect or DevOps preferred), deep Terraform knowledge, Docker/Kubernetes expertise, security compliance understanding (SOC2/PCI), on-call availability for migration phase. Project phases: assessment (1 week), architecture design (2 weeks), implementation (8 weeks), migration (2 weeks), documentation. Budget: $18000-$25000. We're a Series A funded company with strong growth trajectory and excellent team culture.",
        "quality_label": "excellent"
    },
]

def create_sample_dataset():
    """Create sample dataset for training"""
    print("Creating sample dataset for spam detection...")
    
    all_jobs = []
    
    # Add job metadata
    for job_list, label in [(SPAM_JOBS, "spam"), (POOR_JOBS, "poor"), 
                             (GOOD_JOBS, "good"), (EXCELLENT_JOBS, "excellent")]:
        for idx, job in enumerate(job_list):
            job_data = {
                "job_id": f"sample_{label}_{idx+1}",
                "title": job["title"],
                "description": job["description"],
                "proposals": "25",
                "payment_verified": True if label in ["good", "excellent"] else False,
                "client_spending": "50000" if label == "excellent" else "10000" if label == "good" else "1000",
                "client_rating": "5.0" if label == "excellent" else "4.5" if label == "good" else "3.0",
                "posted_time_seconds": "3600",  # 1 hour ago
                "job_type": "fixed",
                "budget": "5000" if label == "excellent" else "1500" if label == "good" else "500",
                "hourly_rate": "60" if label == "excellent" else "35" if label == "good" else "15",
                "quality_label": label,
                "labeled_at": datetime.now().isoformat(),
                "source": "sample_dataset"
            }
            all_jobs.append(job_data)
    
    # Save to CSV
    csv_file = DATA_DIR / "sample_jobs.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=all_jobs[0].keys())
        writer.writeheader()
        writer.writerows(all_jobs)
    
    # Save to JSON
    json_file = DATA_DIR / "sample_jobs.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, indent=2)
    
    print(f"\n✅ Sample dataset created!")
    print(f"   CSV: {csv_file}")
    print(f"   JSON: {json_file}")
    print(f"\n📊 Dataset statistics:")
    print(f"   Total jobs: {len(all_jobs)}")
    print(f"   Spam: {len(SPAM_JOBS)}")
    print(f"   Poor: {len(POOR_JOBS)}")
    print(f"   Good: {len(GOOD_JOBS)}")
    print(f"   Excellent: {len(EXCELLENT_JOBS)}")
    print(f"\n⚠️  This is a small sample dataset for testing.")
    print("   For production use, collect more labeled examples!")
    
    return csv_file


if __name__ == "__main__":
    create_sample_dataset()
