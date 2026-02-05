# Odoo CRM Setup Guide

## 🎯 What is Odoo?

Odoo is an open-source ERP (Enterprise Resource Planning) system with a powerful CRM module. This integration allows you to automatically save LinkedIn connections and other contacts as leads in Odoo CRM.

---

## 🚀 Quick Setup (Free Trial - Recommended)

### Option 1: Odoo.com Free Trial (Easiest)

1. **Sign Up for Free Trial**
   - Go to: https://www.odoo.com/trial
   - Click "Start now - It's free"
   - Fill in your details:
     - Company name (e.g., "Panaversity")
     - Your email
     - Phone number
   - Choose "CRM" as the main app
   - Click "Start my trial"

2. **Get Your Credentials**
   After signup, you'll receive:
   - **URL**: `https://yourcompany.odoo.com` (e.g., `https://panaversity.odoo.com`)
   - **Database**: Usually your company name (e.g., `panaversity`)
   - **Username**: Your email address
   - **Password**: The password you set during signup

3. **Update .env File**
   ```bash
   ODOO_URL=https://yourcompany.odoo.com
   ODOO_DB=yourcompany
   ODOO_USERNAME=your_email@example.com
   ODOO_PASSWORD=your_password
   ```

4. **Test Connection**
   ```bash
   python tests/test_odoo_connection.py
   ```

---

## 🔧 Option 2: Self-Hosted Odoo

### Using Docker (Recommended for Development)

1. **Install Docker Desktop**
   - Download from: https://www.docker.com/products/docker-desktop

2. **Run Odoo Container**
   ```bash
   docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres --name db postgres:13
   
   docker run -p 8069:8069 --name odoo --link db:db -t odoo
   ```

3. **Access Odoo**
   - Open browser: http://localhost:8069
   - Create database:
     - Master Password: admin
     - Database Name: odoo_crm
     - Email: admin@example.com
     - Password: admin
     - Country: Your country
     - Demo data: No

4. **Update .env File**
   ```bash
   ODOO_URL=http://localhost:8069
   ODOO_DB=odoo_crm
   ODOO_USERNAME=admin@example.com
   ODOO_PASSWORD=admin
   ```

---

## 🔧 Option 3: Odoo.sh (For Production)

1. **Sign Up for Odoo.sh**
   - Go to: https://www.odoo.sh
   - Create account
   - Create a new project
   - Connect your GitHub repository

2. **Get Credentials**
   - URL: Provided by Odoo.sh (e.g., `https://yourproject.odoo.sh`)
   - Database: Your project name
   - Username: Your Odoo.sh email
   - Password: Your Odoo.sh password

---

## ✅ Testing Your Connection

After updating your `.env` file, run:

```bash
python tests/test_odoo_connection.py
```

**Expected Output:**
```
[SUCCESS] Connected to Odoo!
  User ID: 2
  Database: yourcompany
  URL: https://yourcompany.odoo.com

[SUCCESS] Test lead created!
  Lead ID: 1

Found 1 recent leads:
  - Test Lead - LinkedIn Connection (test.user@linkedin.com)

ODOO CONNECTION TEST: PASSED
```

---

## 🎯 What This Integration Does

Once configured, the system will:

1. **Extract LinkedIn Connections**
   - Automatically scrape your LinkedIn connections
   - Extract name, occupation, profile URL

2. **Create CRM Leads**
   - Save each connection as a lead in Odoo
   - Include occupation and LinkedIn profile
   - Tag as "LinkedIn Connection"

3. **Manage Leads**
   - View all leads in Odoo CRM dashboard
   - Track communication history
   - Convert leads to opportunities
   - Assign to team members

---

## 🔍 Troubleshooting

### Error: "getaddrinfo failed"
- **Cause**: Invalid URL or no internet connection
- **Fix**: Check ODOO_URL is correct and you have internet

### Error: "Authentication failed"
- **Cause**: Wrong credentials
- **Fix**: Verify username and password in Odoo web interface

### Error: "Access Denied"
- **Cause**: User doesn't have CRM permissions
- **Fix**: Log in to Odoo, go to Settings → Users, enable CRM access

### Error: "Database not found"
- **Cause**: Wrong database name
- **Fix**: Check ODOO_DB matches your actual database name

---

## 📚 Using Odoo CRM

### Accessing Your Leads

1. Log in to Odoo web interface
2. Click "CRM" app
3. View "Leads" or "Pipeline"
4. See all imported LinkedIn connections

### Converting Leads to Opportunities

1. Open a lead
2. Click "Convert to Opportunity"
3. Add expected revenue, probability
4. Track through sales pipeline

### Exporting Data

1. Go to CRM → Leads
2. Select leads (checkbox)
3. Click "Action" → "Export"
4. Choose fields to export
5. Download as Excel/CSV

---

## 🎓 Learning Resources

- **Odoo Documentation**: https://www.odoo.com/documentation
- **Odoo CRM Tutorial**: https://www.odoo.com/slides/crm-16
- **API Documentation**: https://www.odoo.com/documentation/16.0/developer/reference/external_api.html

---

## 💡 Pro Tips

1. **Use Tags**: Tag leads with "LinkedIn", "PIAIC", etc. for easy filtering
2. **Set Up Email Templates**: Create templates for follow-up emails
3. **Use Activities**: Schedule follow-up calls/meetings directly in Odoo
4. **Mobile App**: Download Odoo mobile app to manage leads on the go
5. **Automation**: Set up automated actions (e.g., send email when lead is created)

---

## 🔐 Security Notes

- **Never commit .env file** to Git (it's in .gitignore)
- **Use strong passwords** for Odoo accounts
- **Enable 2FA** if available in your Odoo instance
- **Regularly backup** your Odoo database
- **Use HTTPS** for production deployments

---

## ❓ Need Help?

If you're still having issues:

1. Check the error message in `tests/test_odoo_connection.py`
2. Verify you can log in to Odoo web interface
3. Check firewall/network settings
4. Try the Odoo.com free trial (easiest option)

---

**Ready to connect?** Update your `.env` file and run the test!

```bash
python tests/test_odoo_connection.py
```
