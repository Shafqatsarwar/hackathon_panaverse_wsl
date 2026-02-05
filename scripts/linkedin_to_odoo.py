"""
LinkedIn Post Engagement to Odoo CRM
This script helps you manually add LinkedIn post engagement data to Odoo CRM.
Since LinkedIn doesn't provide API access for post analytics without premium,
this is a manual workflow helper.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from skills.odoo_skill.skill import OdooSkill
from src.utils.config import Config

def add_linkedin_lead_to_odoo(name: str, company: str = "", notes: str = ""):
    """
    Add a LinkedIn contact to Odoo CRM as a lead
    
    Args:
        name: Person's name
        company: Their company (optional)
        notes: Additional notes (e.g., "Liked post about AI", "Viewed profile")
    """
    odoo = OdooSkill()
    
    if not odoo.enabled:
        print("❌ Odoo is not configured. Please check your .env file.")
        return False
    
    # Create lead data
    lead_data = {
        "name": f"LinkedIn: {name}",
        "contact_name": name,
        "description": f"Source: LinkedIn Post Engagement\n{notes}",
        "type": "opportunity",
        "tag_ids": [(6, 0, [])],  # You can add tags here
    }
    
    if company:
        lead_data["partner_name"] = company
    
    result = odoo.create_lead(lead_data)
    
    if result.get("success"):
        print(f"✅ Added {name} to Odoo CRM (Lead ID: {result.get('id')})")
        return True
    else:
        print(f"❌ Failed to add {name}: {result.get('error')}")
        return False

def interactive_mode():
    """Interactive mode to add multiple contacts"""
    print("=" * 60)
    print("LinkedIn Post Engagement → Odoo CRM")
    print("=" * 60)
    print("\nHow to use:")
    print("1. Open your LinkedIn post in a browser")
    print("2. Check who liked/viewed/commented")
    print("3. Enter their details below")
    print("\nType 'done' when finished.\n")
    
    count = 0
    while True:
        print(f"\n--- Contact #{count + 1} ---")
        name = input("Name (or 'done' to finish): ").strip()
        
        if name.lower() == 'done':
            break
        
        if not name:
            print("⚠️ Name cannot be empty. Try again.")
            continue
        
        company = input("Company (optional): ").strip()
        engagement = input("Engagement type (liked/viewed/commented): ").strip()
        
        notes = f"Engagement: {engagement}"
        if engagement:
            notes += f"\nDate: {input('Date (optional): ').strip()}"
        
        if add_linkedin_lead_to_odoo(name, company, notes):
            count += 1
    
    print(f"\n✅ Added {count} contacts to Odoo CRM!")

def batch_mode(contacts_list):
    """
    Batch add contacts from a list
    
    Example:
        contacts = [
            {"name": "John Doe", "company": "Tech Corp", "notes": "Liked AI post"},
            {"name": "Jane Smith", "company": "StartupXYZ", "notes": "Commented on ML article"},
        ]
        batch_mode(contacts)
    """
    count = 0
    for contact in contacts_list:
        if add_linkedin_lead_to_odoo(
            contact.get("name", ""),
            contact.get("company", ""),
            contact.get("notes", "")
        ):
            count += 1
    
    print(f"\n✅ Added {count}/{len(contacts_list)} contacts to Odoo CRM!")

if __name__ == "__main__":
    # Check if Odoo is configured
    if not Config.ODOO_URL or not Config.ODOO_USERNAME:
        print("❌ Odoo is not configured!")
        print("\nPlease add these to your .env file:")
        print("ODOO_URL=https://your-instance.odoo.com")
        print("ODOO_DB=your-database-name")
        print("ODOO_USERNAME=your-email@example.com")
        print("ODOO_PASSWORD=your-password")
        sys.exit(1)
    
    # Run interactive mode
    interactive_mode()
