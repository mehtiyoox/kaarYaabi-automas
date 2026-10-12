#!/usr/bin/env python3
"""
تولید خودکار تصویر پست با استایل ثابت برند
نحوه استفاده: python generate_post_image.py --hook "Most automation agencies sell you a demo that breaks in 2 months" --output post-1.png
"""

import argparse
from PIL import Image, ImageDraw, ImageFont
import os

# -------------------------- BRAND CONFIG --------------------------
CONFIG = {
    "width": 1200,
    "height": 675,
    "bg_color": "#121217",
    "text_color": "#FFFFFF",
    "accent_color": "#00D4AA",
    "muted_color": "#A1A1AA",
    "font_path_bold": "../assets/brand-style/Inter-Bold.ttf",
    "font_path_regular": "../assets/brand-style/Inter-Regular.ttf",
    "signature_text": "Mehdi Habibzadeh  •  AI Automation",
    "line_spacing": 18
}

def draw_wrapped_text(draw, text, font, max_width):
    """تقسیم متن طولانی به خطوط مناسب برای عرض تصویر"""
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines


def generate_post_image(hook_text: str, output_path: str):
    # ساخت تصویر پس‌زمینه
    img = Image.new('RGB', (CONFIG['width'], CONFIG['height']), CONFIG['bg_color'])
    draw = ImageDraw.Draw(img)

    # بارگذاری فونت‌ها
    try:
        font_bold = ImageFont.truetype("/opt/social-automation/assets/brand-style/Inter-Bold.ttf", 58)
        font_regular = ImageFont.truetype("/opt/social-automation/assets/brand-style/Inter-Regular.ttf", 28)
    except:
        try:
            font_bold = ImageFont.truetype("../assets/brand-style/Inter-Bold.ttf", 58)
            font_regular = ImageFont.truetype("../assets/brand-style/Inter-Regular.ttf", 28)
        except:
            # اگر فونت دانلود نشده بود از فونت پیش‌فرض سیستم استفاده کند
            font_bold = ImageFont.load_default(size=58)
            font_regular = ImageFont.load_default(size=28)

    # تقسیم متن هوک به خطوط
    max_text_width = CONFIG['width'] - 200
    lines = draw_wrapped_text(draw, hook_text, font_bold, max_text_width)
    total_text_height = len(lines) * (64 + CONFIG['line_spacing'])

    # جایگاه متن در مرکز
    y = (CONFIG['height'] - total_text_height) // 2
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font_bold)
        line_w = bbox[2] - bbox[0]
        x = (CONFIG['width'] - line_w) // 2
        draw.text((x, y), line, font=font_bold, fill=CONFIG['text_color'])
        y += 64 + CONFIG['line_spacing']

    # خط تاکید زیر متن
    accent_y = y + 10
    draw.rectangle(
        [(CONFIG['width']//2 - 60, accent_y), (CONFIG['width']//2 + 60, accent_y+4)],
        fill=CONFIG['accent_color']
    )

    # امضای برند گوشه پایین راست
    sig_bbox = draw.textbbox((0,0), CONFIG['signature_text'], font=font_regular)
    sig_w = sig_bbox[2] - sig_bbox[0]
    draw.text(
        (CONFIG['width'] - sig_w - 60, CONFIG['height'] - 55),
        CONFIG['signature_text'],
        font=font_regular,
        fill=CONFIG['muted_color']
    )

    # ذخیره تصویر نهایی
    img.save(output_path, quality=95)
    print(f"✅ تصویر پست با موفقیت در {output_path} ساخته شد")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="تولید تصویر پست با استایل ثابت برند")
    parser.add_argument("--hook", required=True, help="متن هوک/خط اول پست که روی تصویر نوشته می‌شود")
    parser.add_argument("--output", default="post-image.png", help="مسیر ذخیره تصویر خروجی")
    args = parser.parse_args()

    generate_post_image(args.hook, args.output)
