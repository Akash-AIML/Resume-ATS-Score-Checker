from database import engine, Base, SessionLocal
from models import JobSection

# Create all tables
Base.metadata.create_all(bind=engine)

# Seed default job sections
def seed_job_sections():
    db = SessionLocal()
    
    # Check if sections already exist
    existing = db.query(JobSection).first()
    if existing:
        print("Job sections already exist. Skipping seed.")
        db.close()
        return
    
    sections = [
        JobSection(
            name="Software Engineering",
            description="Software development, backend, frontend, full-stack roles",
            icon="💻",
            display_order=1
        ),
        JobSection(
            name="Data Science",
            description="Data analysis, machine learning, AI, data engineering",
            icon="📊",
            display_order=2
        ),
        JobSection(
            name="Product Management",
            description="Product managers, product owners, product analysts",
            icon="📱",
            display_order=3
        ),
        JobSection(
            name="DevOps & Cloud",
            description="DevOps engineers, cloud architects, SRE roles",
            icon="☁️",
            display_order=4
        ),
        JobSection(
            name="Design & UX",
            description="UI/UX designers, product designers, graphic designers",
            icon="🎨",
            display_order=5
        )
    ]
    
    db.add_all(sections)
    db.commit()
    
    print("✅ Successfully seeded 5 job sections!")
    db.close()

if __name__ == "__main__":
    print("Initializing database...")
    seed_job_sections()
    print("Database initialization complete!")
