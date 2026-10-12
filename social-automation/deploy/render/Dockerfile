FROM n8nio/n8n:latest

USER root

# نصب پایتون و پکیج‌های مورد نیاز برای تولید تصویر
RUN apk add --no-cache python3 py3-pip py3-pillow fontconfig ttf-dejavu

# ساخت پوشه برای فایل‌های سیستم
RUN mkdir -p /opt/social-automation/scripts
RUN mkdir -p /opt/social-automation/assets/brand-style
RUN mkdir -p /opt/social-automation/content/generated/images

# کپی اسکریپت تولید تصویر
COPY scripts/generate_post_image.py /opt/social-automation/scripts/
COPY scripts/requirements.txt /opt/social-automation/scripts/

# کپی فونت‌ها و منابع استایل برند
RUN wget -q https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Bold.otf -O /opt/social-automation/assets/brand-style/Inter-Bold.ttf && \
    wget -q https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Regular.otf -O /opt/social-automation/assets/brand-style/Inter-Regular.ttf

# نصب پکیج‌های پایتون
RUN pip3 install --break-system-packages -r /opt/social-automation/scripts/requirements.txt

# بازگشت به کاربر n8n
USER node

# دستور پیش‌فرض
CMD ["n8n", "start"]
