# 🔐 Security Guide - API Key Management

This guide provides comprehensive security best practices for managing API keys and sensitive configuration in Memori.

## ⚠️ Critical Security Rules

### 1. Never Commit API Keys to Version Control
```bash
# ❌ WRONG - Don't do this
git add .env
git commit -m "Add configuration"

# ✅ CORRECT - Keep secrets out of version control
git add .env.example  # Template file only
git add .gitignore    # Ensure .env is ignored
```

### 2. Use Environment Variables for Sensitive Data
```bash
# Set API key as environment variable
export OPENAI_API_KEY="sk-your-actual-api-key-here"

# Use in your application
python your_app.py
```

### 3. Create Secure Environment Files
```bash
# Create .env file for local development
cp .env.example .env

# Edit with your actual keys
nano .env

# Set secure permissions
chmod 600 .env
```

## 🔧 Configuration Methods (Security Priority)

### 1. Environment Variables (Most Secure)
```bash
# Set before running your application
export MEMORI_AGENTS__OPENAI_API_KEY="sk-your-key-here"
export MEMORI_DATABASE__CONNECTION_STRING="postgresql://user:pass@localhost/db"

# Run your application
python app.py
```

### 2. .env Files (Development Only)
```bash
# Create .env file
MEMORI_AGENTS__OPENAI_API_KEY=sk-your-key-here
MEMORI_DATABASE__CONNECTION_STRING=postgresql://user:pass@localhost/db
```

**⚠️ Important:** Always add `.env` to `.gitignore` and never commit it.

### 3. Configuration Files (Less Secure)
Use placeholders in configuration files:
```json
{
  "agents": {
    "openai_api_key": "sk-your-key-here",
    "default_model": "gpt-4o"
  }
}
```

## 🔒 Environment Variable Format

Memori uses the following environment variable naming convention:

```
MEMORI_<SECTION>__<SETTING_NAME>
```

### Examples:
- `MEMORI_AGENTS__OPENAI_API_KEY`
- `MEMORI_DATABASE__CONNECTION_STRING`
- `MEMORI_MEMORY__NAMESPACE`
- `MEMORI_LOGGING__LEVEL`

### Nested Settings:
```bash
# Database settings
export MEMORI_DATABASE__POOL_SIZE="20"
export MEMORI_DATABASE__CONNECTION_STRING="postgresql://..."

# Agent settings
export MEMORI_AGENTS__OPENAI_API_KEY="sk-..."
export MEMORI_AGENTS__DEFAULT_MODEL="gpt-4o"

# Memory settings
export MEMORI_MEMORY__NAMESPACE="production"
export MEMORI_MEMORY__CONTEXT_LIMIT="5"
```

## 🛡️ Production Security

### 1. Use Secret Management Services
- **AWS Secrets Manager**
- **Azure Key Vault**
- **Google Secret Manager**
- **HashiCorp Vault**

### 2. Container Environment Variables
```yaml
# docker-compose.yml
services:
  memori-app:
    image: your-app
    environment:
      - MEMORI_AGENTS__OPENAI_API_KEY=${OPENAI_API_KEY}
      - MEMORI_DATABASE__CONNECTION_STRING=${DATABASE_URL}
```

### 3. Kubernetes Secrets
```yaml
# k8s-secret.yml
apiVersion: v1
kind: Secret
metadata:
  name: memori-secrets
type: Opaque
data:
  openai-api-key: <base64-encoded-key>
  database-url: <base64-encoded-connection-string>
```

## 🔍 Security Checklist

### ✅ Development Environment
- [ ] Create `.env` file from `.env.example`
- [ ] Add `.env` to `.gitignore`
- [ ] Set secure file permissions (`chmod 600 .env`)
- [ ] Use environment variables for sensitive config
- [ ] Test configuration loading works correctly

### ✅ Version Control
- [ ] No API keys in repository
- [ ] No database passwords in repository
- [ ] No sensitive tokens in repository
- [ ] `.env` files properly ignored
- [ ] Configuration templates included

### ✅ Production Environment
- [ ] Use secret management service
- [ ] Environment variables for all secrets
- [ ] No hardcoded secrets in code
- [ ] Regular key rotation schedule
- [ ] Access logging enabled

## 🚨 Incident Response

### If API Key is Exposed:

1. **Immediately rotate the key** at the provider
2. **Check for unauthorized usage** in your account
3. **Update all environments** with new key
4. **Review access logs** for suspicious activity
5. **Implement additional security measures** (IP restrictions, etc.)

### Key Rotation Process:
```bash
# 1. Generate new API key at provider
NEW_KEY="sk-new-key-here"

# 2. Update environment variables
export MEMORI_AGENTS__OPENAI_API_KEY="$NEW_KEY"

# 3. Update .env file
sed -i 's/sk-old-key.*/'$NEW_KEY'/g' .env

# 4. Restart applications
# 5. Verify everything works
# 6. Revoke old key at provider
```

## 📚 Additional Resources

- [OpenAI API Security](https://platform.openai.com/docs/security)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Environment Variables Best Practices](https://12factor.net/config)
- [GitHub Security Lab](https://securitylab.github.com/)

## 🔐 Security Contact

If you discover a security vulnerability, please report it responsibly by contacting the security team at: security@your-organization.com

---

**Remember**: Security is an ongoing process. Regularly review and update your security practices as threats evolve.
