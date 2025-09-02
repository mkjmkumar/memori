# 🧪 GitHub Actions Workflow Testing Guide

**Before merging your PR, follow this comprehensive testing guide to ensure all workflows function properly.**

## 🎯 Pre-Merge Checklist Overview

✅ **Test Trigger Conditions**
✅ **Validate Manual Triggers**
✅ **Check Security & Permissions**
✅ **Test External Scripts**
✅ **Verify Error Handling**
✅ **Test on Feature Branch**

---

## 1. 🚀 **Test Workflow Triggers**

### **CI/CD Pipeline (ci.yml)**
```bash
# Test automatic triggers:
git push origin your-branch              # Should trigger CI
# Create a PR to main                     # Should trigger CI

# Test manual trigger:
```
1. Go to **Actions** tab → **CI/CD Pipeline**
2. Click **Run workflow**
3. Select your branch
4. Enable **debug mode** ✓
5. Click **Run workflow**

**✅ Expected Result**: All quality checks pass, no test failures

### **Code Formatting (code-format.yml)**
```bash
# Create a PR with unformatted code to test:
echo "x=1+2" >> memori/test.py          # Unformatted code
git add . && git commit -m "test formatting"
git push origin your-branch
# Create PR → Should auto-format and commit back
```

**✅ Expected Result**: Auto-formatting applied, PR comment posted

### **Dependencies (dependencies.yml)**
**Manual Testing** (don't run on schedule):
1. Go to **Actions** → **Dependencies**
2. **Run workflow** → Select **update_type: patch**
3. Monitor execution

**✅ Expected Result**: Creates PR with dependency updates

### **Security (security.yml)**
**Manual Testing**:
1. **Actions** → **Security**
2. **Run workflow** → **scan_type: full**
3. Check security results

**✅ Expected Result**: Security scans complete, SARIF uploaded

### **Documentation Generation (docs-generation.yml)**
```bash
# Test with example file change:
echo "# New example" > examples/test_example.py
git add . && git commit -m "test docs generation"
git push origin your-branch
# Create PR → Should generate docs
```

**✅ Expected Result**: Documentation generated, mkdocs.yml updated

---

## 2. 🔧 **Test External Scripts**

### **Test Documentation Script**
```bash
cd /Users/harshalmore31/code/github/memori

# Test dependency installation
python scripts/docs_dev.py --install-only

# Test build validation
python scripts/docs_dev.py --build

# Test issue detection
python scripts/docs_dev.py --check

# Test dev server (manual - check browser opens)
python scripts/docs_dev.py --serve --no-browser
# Ctrl+C to stop
```

### **Test Dependency PR Script**
**Note**: This requires GitHub token, test manually in workflow only

---

## 3. 🛡️ **Security & Permissions Testing**

### **Check Secret Access**
Ensure these secrets are available in your repo:
- `ANTHROPIC_API_KEY` (for docs generation)
- `GITHUB_TOKEN` (automatic)

**Test Access**:
1. **Settings** → **Secrets and variables** → **Actions**
2. Verify `ANTHROPIC_API_KEY` exists
3. Check repository permissions

### **Test Workflow Permissions**
Each workflow should have minimal required permissions:
- ✅ **CI**: `contents: read`, `pull-requests: write`
- ✅ **Code Format**: `contents: write`, `pull-requests: write`
- ✅ **Dependencies**: `contents: write`, `pull-requests: write`
- ✅ **Security**: `contents: read`, `security-events: write`

---

## 4. 📋 **Branch-Specific Testing**

### **Create Test Branch**
```bash
git checkout -b test-workflows-$(date +%s)
```

### **Test Each Workflow Individually**

#### **Test 1: CI Pipeline**
```bash
# Make a small change to trigger CI
echo "# Test change" >> README.md
git add . && git commit -m "test: trigger CI pipeline"
git push origin test-workflows-*
```
**Monitor**: Actions tab → CI/CD Pipeline

#### **Test 2: Code Formatting**
```bash
# Add unformatted code
echo 'x=1+2;y=3+4' > memori/format_test.py
git add . && git commit -m "test: formatting workflow"
git push origin test-workflows-*
# Create PR from this branch
```
**Monitor**: PR should get auto-formatting commits

#### **Test 3: Security Scanning**
**Manual**: Actions → Security → Run workflow

#### **Test 4: Documentation**
```bash
# Add example file
mkdir -p examples/test
echo 'print("test example")' > examples/test/test_integration.py
git add . && git commit -m "test: docs generation"
git push origin test-workflows-*
# Create PR
```
**Monitor**: Should generate documentation

---

## 5. 🔍 **Error Handling Testing**

### **Test Failure Scenarios**

#### **Test CI with Syntax Error**
```bash
echo 'invalid python syntax =' > memori/syntax_error.py
git add . && git commit -m "test: syntax error handling"
git push origin test-workflows-*
```
**✅ Expected**: CI fails gracefully with clear error messages

#### **Test Missing Dependencies**
Create temporary commit without required dependencies
**✅ Expected**: Auto-installation works or clear error message

#### **Test Invalid Configuration**
Temporarily break `mkdocs.yml`
**✅ Expected**: Build fails with helpful error message

---

## 6. 📊 **Monitoring & Validation**

### **Workflow Status Dashboard**
Monitor all workflows in **Actions** tab:

| Workflow | Status | Duration | Artifacts |
|----------|--------|----------|-----------|
| CI/CD Pipeline | ✅ | ~3-5 min | Security reports |
| Code Formatting | ✅ | ~1-2 min | None |
| Dependencies | ✅ | ~2-3 min | SBOM files |
| Security | ✅ | ~5-8 min | SARIF reports |
| Documentation | ✅ | ~2-4 min | Generated docs |

### **Check Workflow Logs**
For each workflow execution:
1. Click on workflow run
2. Expand each job
3. Review logs for errors/warnings
4. Check artifact uploads

---

## 7. 🎯 **Final Validation Checklist**

Before merging, ensure:

### **✅ Functionality Tests**
- [ ] All workflows trigger correctly
- [ ] Manual triggers work with all input options
- [ ] External scripts execute without errors
- [ ] Error handling works properly
- [ ] Security scans complete successfully

### **✅ Integration Tests**
- [ ] Code formatting creates proper commits
- [ ] Documentation generation works end-to-end
- [ ] Dependencies update creates valid PRs
- [ ] CI pipeline reports accurate results
- [ ] Security findings upload to GitHub

### **✅ Resource & Performance**
- [ ] No workflows timeout
- [ ] Artifact sizes are reasonable
- [ ] Cache strategies work effectively
- [ ] No resource waste from disabled tests

### **✅ Security & Compliance**
- [ ] No secrets exposed in logs
- [ ] Permissions are minimal and correct
- [ ] External scripts are safe
- [ ] API keys are properly validated

---

## 8. 🚨 **Troubleshooting Common Issues**

### **Problem**: Workflow doesn't trigger
**Solution**: 
- Check trigger conditions (paths, branches)
- Ensure workflow file is in `.github/workflows/`
- Check YAML syntax

### **Problem**: External script fails
**Solution**:
- Test script locally first
- Check file permissions and paths
- Verify dependencies are installed

### **Problem**: Security scan fails
**Solution**:
- Check if it's a real security issue
- Update dependencies if vulnerabilities found
- Review scan configuration

### **Problem**: Documentation generation fails
**Solution**:
- Verify `ANTHROPIC_API_KEY` secret exists
- Check mkdocs configuration
- Test external script manually

---

## 9. 🔄 **Testing Workflow Commands**

### **Quick Test Commands**
```bash
# Test all workflows in sequence
cd /Users/harshalmore31/code/github/memori

# 1. Test documentation locally
python scripts/docs_dev.py --check

# 2. Test build process
python scripts/docs_dev.py --build

# 3. Create test branch
git checkout -b workflow-test-$(date +%s)

# 4. Make test changes
echo "# Test" >> TESTING.md
git add . && git commit -m "test: workflow validation"

# 5. Push and monitor
git push origin workflow-test-*
```

### **GitHub UI Testing Steps**
1. **Create PR** from test branch
2. **Monitor Actions** tab for automatic triggers
3. **Test manual triggers** for each workflow
4. **Review results** and artifacts
5. **Check error handling** with intentional failures

---

## 10. ✅ **Final Approval Criteria**

**✅ Ready to Merge When:**
- All workflow tests pass
- Manual triggers work correctly
- External scripts execute properly
- Error handling is robust
- Security scans complete
- Documentation builds successfully
- No resource waste or performance issues
- All artifacts upload correctly

**🎉 Once everything passes, your workflows are production-ready!**

---

## 📞 **Need Help?**

If any workflow fails:
1. Check the **Actions** tab for detailed logs
2. Review the specific job that failed
3. Look for error messages in the output
4. Test the external scripts locally
5. Verify all secrets and permissions are correct

**Remember**: It's better to catch issues now than after merging! 🛡️