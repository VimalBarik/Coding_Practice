PROMPTS = {

    "resume": """
You are an expert ATS resume parser.

Extract every important piece of information from the resume.

Return ONLY valid JSON.

{
    "name":"",
    "email":"",
    "phone":"",
    "summary":"",
    "skills":[],
    "experience":[
        {
            "company":"",
            "role":"",
            "duration":"",
            "description":""
        }
    ],
    "education":[
        {
            "institution":"",
            "degree":"",
            "year":""
        }
    ],
    "projects":[
        {
            "title":"",
            "description":"",
            "technologies":[]
        }
    ],
    "certifications":[],
    "languages":[]
}

Resume

{resume}
""",


    "job_analysis": """
You are an experienced technical recruiter.

Analyse how well the candidate matches this job.

Consider

- Skills
- Experience
- Projects
- Education
- Seniority
- Overall fit

Return ONLY JSON.

{
    "overall_score":0,
    "skill_match":0,
    "experience_match":0,
    "project_match":0,
    "education_match":0,
    "priority":"High",
    "strengths":[],
    "missing_skills":[],
    "pros":[],
    "cons":[],
    "explanation":""
}

Resume

{resume}

Job

{job}
""",


    "learning": """
The candidate is missing these skills.

{skills}

Generate a realistic learning roadmap.

Return ONLY JSON.

{
    "weeks":[
        {
            "week":1,
            "topics":[],
            "goal":""
        }
    ],
    "estimated_duration":"",
    "final_goal":""
}
""",


    "interview": """
You are a senior interviewer.

Generate interview questions based on this resume and job.

Return ONLY JSON.

{
    "technical":[],
    "behavioural":[],
    "project_based":[],
    "hr":[]
}

Resume

{resume}

Job

{job}
""",


    "company": """
Summarise this company.

Focus on

- What the company does
- Products
- Culture
- Hiring
- Tech stack
- Career growth

Return ONLY JSON.

{
    "summary":"",
    "industry":"",
    "culture":"",
    "growth":"",
    "tech_stack":[],
    "pros":[],
    "cons":[]
}

Company

{company}
""",


    "job_extraction": """
Extract structured information from this job description.

Return ONLY JSON.

{
    "title":"",
    "company":"",
    "location":"",
    "salary":"",
    "experience":"",
    "employment_type":"",
    "remote":false,
    "required_skills":[],
    "preferred_skills":[],
    "responsibilities":[],
    "requirements":[],
    "benefits":[],
    "application_deadline":"",
    "job_summary":""
}

Job Description

{job}
""",


    "resume_improvement": """
You are an ATS resume expert.

Compare the resume with the job.

Suggest improvements.

Return ONLY JSON.

{
    "ats_score":0,
    "missing_keywords":[],
    "improvements":[],
    "new_bullet_points":[]
}

Resume

{resume}

Job

{job}
""",


    "career_summary": """
Analyse all analysed jobs.

Provide career insights.

Return ONLY JSON.

{
    "career_direction":"",
    "best_roles":[],
    "top_strengths":[],
    "largest_skill_gaps":[],
    "recommended_certifications":[],
    "market_summary":""
}

Jobs

{jobs}
""",


    "salary_analysis": """
Analyse the following salary information.

Return ONLY JSON.

{
    "average_salary":"",
    "highest_salary":"",
    "lowest_salary":"",
    "salary_trend":"",
    "insights":[]
}

Salary Data

{salaries}
""",


    "market_analysis": """
Analyse these job listings.

Return ONLY JSON.

{
    "top_skills":[],
    "fastest_growing_skills":[],
    "most_common_locations":[],
    "remote_percentage":0,
    "top_companies":[],
    "market_summary":""
}

Jobs

{jobs}
""",


    "job_priority": """
You are helping a candidate prioritise applications.

Evaluate this opportunity.

Consider

- Resume match
- Salary
- Company
- Career growth
- Missing skills
- Competition

Return ONLY JSON.

{
    "priority_score":0,
    "priority":"High",
    "apply_now":true,
    "reason":""
}

Resume

{resume}

Job

{job}
""",


    "job_comparison": """
Compare these jobs.

Return ONLY JSON.

{
    "best_job":"",
    "comparison":[
        {
            "company":"",
            "pros":[],
            "cons":[],
            "score":0
        }
    ],
    "recommendation":""
}

Jobs

{jobs}
""",


    "cover_letter": """
Write a professional cover letter.

Resume

{resume}

Job

{job}
""",


    "recruiter_message": """
Write a concise LinkedIn recruiter message.

Resume

{resume}

Job

{job}
""",


    "job_summary": """
Summarise this job in under 200 words.

Highlight

- Responsibilities
- Skills
- Experience
- Salary
- Benefits
- Remote policy

Job

{job}
"""
}