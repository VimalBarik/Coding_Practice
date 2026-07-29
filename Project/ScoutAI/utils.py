import hashlib
import json
import os
import re
import time
from functools import wraps
from pathlib import Path

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def timer(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        print(f"{func.__name__} completed in {round(end-start,2)} sec")

        return result

    return wrapper


def cache_key(text):

    return hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()


def load_cache(key):

    path = CACHE_DIR / f"{key}.json"

    if not path.exists():

        return None

    with open(path, "r", encoding="utf-8") as f:

        return json.load(f)


def save_cache(key, data):

    path = CACHE_DIR / f"{key}.json"

    with open(path, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def cached(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        key = cache_key(
            str(args) + str(kwargs)
        )

        cached_result = load_cache(key)

        if cached_result is not None:

            return cached_result

        result = func(*args, **kwargs)

        save_cache(key, result)

        return result

    return wrapper


def clean_text(text):

    if not text:

        return ""

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    text = text.replace("\xa0", " ")

    return text.strip()


def normalize_skill(skill):

    return clean_text(
        skill
    ).lower()


def normalize_skills(skills):

    return sorted(

        list({

            normalize_skill(skill)

            for skill in skills

            if skill

        })

    )


def unique_jobs(jobs):

    seen = set()

    unique = []

    for job in jobs:

        key = (

            job.get(
                "title",
                ""
            ).lower(),

            job.get(
                "company",
                ""
            ).lower(),

            job.get(
                "location",
                ""
            ).lower()

        )

        if key not in seen:

            seen.add(key)

            unique.append(job)

    return unique


def sort_jobs(jobs):

    return sorted(

        jobs,

        key=lambda x: x.get(
            "match_score",
            0
        ),

        reverse=True

    )


def safe_json(text):

    if not text:

        return {}

    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    text = text.strip()

    try:

        return json.loads(text)

    except:

        return {}


def extract_emails(text):

    return re.findall(

        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

        text

    )


def extract_phone(text):

    phones = re.findall(

        r"(\+?\d[\d\s\-]{8,15}\d)",

        text

    )

    return phones[0] if phones else ""


def score_to_grade(score):

    if score >= 90:

        return "A"

    elif score >= 80:

        return "B"

    elif score >= 70:

        return "C"

    elif score >= 60:

        return "D"

    return "F"


def percentage(part, whole):

    if whole == 0:

        return 0

    return round(

        (part / whole) * 100,

        2

    )


def flatten(items):

    result = []

    for item in items:

        if isinstance(item, list):

            result.extend(item)

        else:

            result.append(item)

    return result


def top_n(counter_dict, n=10):

    return dict(

        sorted(

            counter_dict.items(),

            key=lambda x: x[1],

            reverse=True

        )[:n]

    )


def save_json(data, filename):

    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )


def load_json(filename):

    if not os.path.exists(filename):

        return None

    with open(

        filename,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)


def timestamp():

    return time.strftime(

        "%Y-%m-%d %H:%M:%S"

    )


def print_title(title):

    print()

    print("=" * 70)

    print(title.upper())

    print("=" * 70)


def print_success(message):

    print(f"✅ {message}")


def print_error(message):

    print(f"❌ {message}")


def print_warning(message):

    print(f"⚠️ {message}")


def print_info(message):

    print(f"ℹ️ {message}")