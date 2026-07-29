from collections import Counter
from statistics import mean


def dashboard(jobs):

    if not jobs:

        return {
            "total_jobs": 0,
            "average_match": 0,
            "high_priority": 0,
            "remote_jobs": 0,
            "companies": 0,
            "locations": 0
        }

    scores = []
    companies = set()
    locations = set()
    remote = 0
    high = 0

    for job in jobs:

        score = job.get("analysis", {}).get(
            "overall_score",
            0
        )

        scores.append(score)

        companies.add(
            job["job"].get("company", "")
        )

        locations.add(
            job["job"].get("location", "")
        )

        if job["job"].get("remote"):
            remote += 1

        if job["analysis"].get(
            "priority",
            ""
        ).lower() == "high":
            high += 1

    return {

        "total_jobs": len(jobs),

        "average_match": round(
            mean(scores),
            2
        ),

        "high_priority": high,

        "remote_jobs": remote,

        "companies": len(companies),

        "locations": len(locations)

    }


def skill_demand(jobs):

    counter = Counter()

    for job in jobs:

        skills = job["job"].get(
            "required_skills",
            []
        )

        counter.update(skills)

    return dict(
        counter.most_common()
    )


def missing_skill_analysis(jobs):

    counter = Counter()

    for job in jobs:

        skills = job["analysis"].get(
            "missing_skills",
            []
        )

        counter.update(skills)

    return dict(
        counter.most_common()
    )


def company_hiring(jobs):

    counter = Counter()

    for job in jobs:

        company = job["job"].get(
            "company",
            "Unknown"
        )

        counter[company] += 1

    return dict(
        counter.most_common()
    )


def location_distribution(jobs):

    counter = Counter()

    for job in jobs:

        location = job["job"].get(
            "location",
            "Unknown"
        )

        counter[location] += 1

    return dict(
        counter.most_common()
    )


def remote_vs_onsite(jobs):

    remote = 0
    onsite = 0

    for job in jobs:

        if job["job"].get("remote"):

            remote += 1

        else:

            onsite += 1

    return {

        "Remote": remote,

        "Onsite/Hybrid": onsite

    }


def salary_statistics(jobs):

    salaries = []

    for job in jobs:

        salary = job["job"].get(
            "salary",
            ""
        )

        if not salary:

            continue

        salaries.append(salary)

    return {

        "total_salary_records": len(salaries),

        "salary_examples": salaries[:10]

    }


def experience_distribution(jobs):

    counter = Counter()

    for job in jobs:

        exp = job["job"].get(
            "experience",
            "Unknown"
        )

        counter[exp] += 1

    return dict(
        counter.most_common()
    )


def priority_distribution(jobs):

    counter = Counter()

    for job in jobs:

        priority = job["analysis"].get(
            "priority",
            "Unknown"
        )

        counter[priority] += 1

    return dict(
        counter.most_common()
    )


def match_distribution(jobs):

    ranges = {

        "90-100": 0,

        "80-89": 0,

        "70-79": 0,

        "60-69": 0,

        "<60": 0

    }

    for job in jobs:

        score = job["analysis"].get(
            "overall_score",
            0
        )

        if score >= 90:

            ranges["90-100"] += 1

        elif score >= 80:

            ranges["80-89"] += 1

        elif score >= 70:

            ranges["70-79"] += 1

        elif score >= 60:

            ranges["60-69"] += 1

        else:

            ranges["<60"] += 1

    return ranges


def top_companies(jobs, limit=10):

    companies = company_hiring(jobs)

    return dict(

        list(companies.items())[:limit]

    )


def top_locations(jobs, limit=10):

    locations = location_distribution(jobs)

    return dict(

        list(locations.items())[:limit]

    )


def top_skills(jobs, limit=20):

    skills = skill_demand(jobs)

    return dict(

        list(skills.items())[:limit]

    )


def top_missing_skills(jobs, limit=20):

    skills = missing_skill_analysis(jobs)

    return dict(

        list(skills.items())[:limit]

    )


def generate_dashboard(jobs):

    return {

        "overview": dashboard(jobs),

        "top_skills": top_skills(jobs),

        "missing_skills": top_missing_skills(jobs),

        "companies": top_companies(jobs),

        "locations": top_locations(jobs),

        "remote": remote_vs_onsite(jobs),

        "priority": priority_distribution(jobs),

        "experience": experience_distribution(jobs),

        "match_distribution": match_distribution(jobs),

        "salary": salary_statistics(jobs)

    }


def print_dashboard(data):

    overview = data["overview"]

    print("\n")

    print("=" * 60)

    print("SMARTSCOUT DASHBOARD")

    print("=" * 60)

    print(f"Jobs Found        : {overview['total_jobs']}")

    print(f"Average Match     : {overview['average_match']}%")

    print(f"High Priority     : {overview['high_priority']}")

    print(f"Companies         : {overview['companies']}")

    print(f"Locations         : {overview['locations']}")

    print(f"Remote Jobs       : {overview['remote_jobs']}")

    print()

    print("Top Skills")

    print("-" * 60)

    for skill, count in data["top_skills"].items():

        print(f"{skill:<30}{count}")

    print()

    print("Most Missing Skills")

    print("-" * 60)

    for skill, count in data["missing_skills"].items():

        print(f"{skill:<30}{count}")

    print()

    print("Top Hiring Companies")

    print("-" * 60)

    for company, count in data["companies"].items():

        print(f"{company:<30}{count}")

    print()

    print("=" * 60)