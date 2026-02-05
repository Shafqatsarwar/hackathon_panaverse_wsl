import os
import sys
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills.odoo_skill.skill import OdooSkill

logging.basicConfig(level=logging.INFO)

def test_odoo():
    try:
        odoo = OdooSkill()
        success = odoo.authenticate()
        print(f"ODOO AUTH: {'SUCCESS' if success else 'FAILED'}")
        if success:
            leads = odoo.get_leads(limit=1)
            print(f"LEADS FOUND: {len(leads)}")
    except Exception as e:
        print(f"ODOO ERROR: {e}")

if __name__ == "__main__":
    test_odoo()
