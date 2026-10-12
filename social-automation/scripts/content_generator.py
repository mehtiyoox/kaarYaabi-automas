#!/usr/bin/env python3
"""
تولید خودکار پست برای لینکدین و توییتر/X با استفاده از LLM
نویسنده: مهدی حبیب‌زاده
استفاده: python content_generator.py --topic "دستیار فروش هوشمند" --type project_result
"""

import os
import json
import argparse
from datetime import datetime
from groq import Groq

# -------------------------- CONFIG --------------------------
# تمام اطلاعات شخصی و نمونه کارهای شما در اینجا قرار دارد تا محتوا دقیقا مطابق با صدا و تجربه شما تولید شود
PROFILE = {
    "name": "مهدی حبیب‌زاده",
    "title": "AI Automation & Workflow Developer",
    "location": "Karaj, Iran, remote worldwide",
    "skills": ["n8n", "Python", "Telegram Bot API", "PostgreSQL", "WordPress", "WooCommerce", "Web Scraping", "LLM integration"],
    "projects": [
        "Smart Telegram Sales Assistant with conversation memory",
        "Automated news pipeline with RSS -> AI summary -> approve -> publish",
        "24/7 job matching and project scraping bot",
        "9+ WordPress/WooCommerce stores and websites"
    ],
    "tone": "professional but friendly, conversational, results focused, honest, no fluff, numbers and concrete examples",
    "target_audience": "small business owners, e-commerce managers, agency owners, looking for practical automation solutions not academic AI talk",
    "cta": "send me a DM if you have a project, free first consultation"
}

# پرامپت‌های آماده برای هر نوع پست
PROMPTS = {
    "project_result": """
Write two versions of a social media post in PERSIAN (Farsi):
1.  LinkedIn version: longer, more structured, professional, 200-300 words
2.  Twitter/X version: shorter, conversational, punchy, 50-100 words

Topic: {topic}
The post must:
- Talk about the result and real impact of the project for the client, not just features
- Include at least one concrete number (time saved, % increase in leads, cost saved etc.)
- End with a simple question to encourage comments
- Use relevant hashtags at the end
- Match my profile: {profile}
    """,

    "tip": """
Write two versions of a practical automation tip post in PERSIAN (Farsi):
1.  LinkedIn version: explanatory, practical, actionable steps
2.  Twitter/X version: short list of tips, easy to read

Topic: {topic}
The tip must be something a small business owner can implement today, no theory.
End with a simple question to encourage comments.
Match my profile: {profile}
    """,

    "personal_story": """
Write two versions of a personal story / experience post in PERSIAN (Farsi):
1.  LinkedIn version: reflective, with lesson learned, authentic
2.  Twitter/X version: short, relatable, casual

Topic: {topic}
The story must be honest, vulnerable if appropriate, end with a clear lesson or takeaway for the reader.
Match my profile: {profile}
    """,

    "cta": """
Write two versions of a call-to-action post in PERSIAN (Farsi):
1.  LinkedIn version: clear, list of services available, explain who it is for
2.  Twitter/X version: short, direct, state availability immediately

Topic: {topic} (e.g. new availability for projects, free consultation offer)
Clearly list what services I can deliver, mention that first consultation is free.
Match my profile: {profile}
    """
}


def generate_post(topic: str, post_type: str = "project_result", api_key: str = None):
    """تولید محتوا با استفاده از API Groq (سریع و ارزان)"""
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Please set GROQ_API_KEY environment variable or pass api_key parameter")

    client = Groq(api_key=api_key)

    prompt = PROMPTS[post_type].format(topic=topic, profile=json.dumps(PROFILE, ensure_ascii=False, indent=2))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert B2B social media content writer for freelance automation developers. You write natural, human Persian (Farsi) posts that sound like a real person not a corporate account. Never use formal academic language."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=1500
    )

    content = response.choices[0].message.content

    # ذخیره خودکار پست تولید شده در پوشه content/generated
    os.makedirs("content/generated", exist_ok=True)
    filename = f"content/generated/{datetime.now().strftime('%Y-%m-%d')}-{post_type}-{topic[:30].replace(' ', '-')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# پست تولید شده: {topic}\n")
        f.write(f"تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"نوع: {post_type}\n\n")
        f.write(content)

    print(f"✅ پست با موفقیت تولید شد و در {filename} ذخیره شد")
    print("\n" + "="*60)
    print(content)
    print("="*60 + "\n")
    return filename, content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="تولید خودکار پست‌های شبکه‌های اجتماعی")
    parser.add_argument("--topic", required=True, help="موضوع پست")
    parser.add_argument("--type", default="project_result", choices=list(PROMPTS.keys()), help="نوع پست")
    parser.add_argument("--api-key", help="کلید API Groq")
    args = parser.parse_args()

    generate_post(args.topic, args.type, args.api_key)
