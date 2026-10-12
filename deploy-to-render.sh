#!/bin/bash
set -e

echo "🚀 استقرار خودکار سیستم اتوماسیون اجتماعی روی رندر"
echo "----------------------------------------------------"

if [ -z "$RENDER_API_KEY" ]; then
  echo "❌ لطفا ابتدا متغیر RENDER_API_KEY را با کلید API که از رندر گرفتید تنظیم کنید:"
  echo "export RENDER_API_KEY=رندر-کلید-api-شما-اینجا"
  exit 1
fi

if ! command -v curl &> /dev/null; then
  echo "❌ لطفا curl را روی سیستم خود نصب کنید"
  exit 1
fi

echo "✅ کلید API دریافت شد. در حال ارسال درخواست استقرار..."

# ساخت سرویس با استفاده از API رندر
curl -s -X POST "https://api.render.com/v1/services" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "type": "web_service",
  "name": "mehdi-social-automation",
  "ownerId": null,
  "repo": "https://github.com/mehtiyoox/kaarYaabi-automas",
  "branch": "arena/570d6046-kaaryaabi-automas",
  "autoDeploy": "yes",
  "rootDir": "social-automation/deploy/render",
  "dockerCommand": "n8n start",
  "dockerfilePath": "./Dockerfile",
  "plan": "free",
  "region": "frankfurt",
  "envVars": [
    {"key": "TZ", "value": "Asia/Tehran"},
    {"key": "GENERIC_TIMEZONE", "value": "Asia/Tehran"},
    {"key": "N8N_PROTOCOL", "value": "https"},
    {"key": "NODE_ENV", "value": "production"},
    {"key": "EXECUTIONS_DATA_PRUNE", "value": "true"},
    {"key": "EXECUTIONS_DATA_MAX_AGE", "value": "168"},
    {"key": "N8N_BASIC_AUTH_ACTIVE", "value": "true"},
    {"key": "N8N_BASIC_AUTH_USER", "value": "admin"}
  ]
}
EOF

echo ""
echo "✅ درخواست استقرار با موفقیت ارسال شد."
echo "لطفا به داشبورد رندر بروید، بعد از ۵-۷ دقیقه سرویس شما آماده خواهد شد."
echo "بعد از آماده شدن سرویس، به من بگویید تا با هم تنظیمات نهایی و اتصال اکانت‌های لینکدین و توییتر را انجام دهیم."
