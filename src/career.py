# =========================================================
# DEVTRACK CAREER ENGINE
# Skill extraction, role requirements, skill gap analysis
# and personalized learning roadmaps
# =========================================================

import re


# =========================================================
# SKILL KEYWORDS
# =========================================================

SKILL_KEYWORDS = {

    # -------------------------
    # Programming Languages
    # -------------------------

    "Python": [
        "python",
        "django",
        "flask",
        "fastapi",
        "pandas",
        "numpy"
    ],

    "Java": [
        "java",
        "spring",
        "spring boot",
        "maven",
        "gradle",
        "hibernate"
    ],

    "JavaScript": [
        "javascript",
        "js",
        "node",
        "node.js",
        "react",
        "vue",
        "angular",
        "express"
    ],

    "TypeScript": [
        "typescript",
        "ts"
    ],

    "C++": [
        "c++",
        "cpp"
    ],

    # -------------------------
    # Backend
    # -------------------------

    "Spring Boot": [
        "spring boot",
        "springboot"
    ],

    "Node.js": [
        "node.js",
        "nodejs",
        "node"
    ],

    "Django": [
        "django"
    ],

    "Flask": [
        "flask"
    ],

    "FastAPI": [
        "fastapi"
    ],

    "REST APIs": [
        "rest api",
        "restful",
        "rest",
        "api",
        "apis",
        "http",
        "endpoints",
        "json"
    ],

    # -------------------------
    # Databases
    # -------------------------

    "SQL": [
        "sql",
        "mysql",
        "postgresql",
        "postgres",
        "sqlite",
        "database",
        "databases",
        "rdbms"
    ],

    "PostgreSQL": [
        "postgresql",
        "postgres"
    ],

    "MySQL": [
        "mysql"
    ],

    "SQLite": [
        "sqlite"
    ],

    "MongoDB": [
        "mongodb",
        "mongo",
        "nosql",
        "mongoose"
    ],

    "Redis": [
        "redis",
        "cache",
        "caching"
    ],

    # -------------------------
    # Cloud / DevOps
    # -------------------------

    "Docker": [
        "docker",
        "container",
        "containers",
        "containerization",
        "dockerfile"
    ],

    "AWS": [
        "aws",
        "amazon web services",
        "ec2",
        "s3",
        "lambda"
    ],

    "Azure": [
        "azure",
        "microsoft azure"
    ],

    "GCP": [
        "gcp",
        "google cloud",
        "google cloud platform"
    ],

    "Kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "Linux": [
        "linux",
        "unix",
        "bash",
        "shell",
        "terminal"
    ],

    "CI/CD": [
        "ci/cd",
        "cicd",
        "jenkins",
        "github actions",
        "gitlab ci",
        "pipeline",
        "continuous integration",
        "continuous deployment"
    ],

    # -------------------------
    # Development Tools
    # -------------------------

    "Git": [
        "git",
        "github",
        "gitlab",
        "version control",
        "branching",
        "pull request"
    ],

    "Testing": [
        "unit testing",
        "unit test",
        "testing",
        "jest",
        "junit",
        "pytest",
        "test automation"
    ],

    # -------------------------
    # Computer Science
    # -------------------------

    "Data Structures": [
        "data structures",
        "data structure",
        "dsa",
        "algorithms",
        "algorithm",
        "leetcode",
        "problem solving"
    ],

    "System Design": [
        "system design",
        "system architecture",
        "scalability",
        "microservices",
        "distributed systems"
    ],

    "OOP": [
        "object oriented",
        "object-oriented",
        "oop",
        "classes",
        "inheritance",
        "polymorphism",
        "encapsulation"
    ],

    # -------------------------
    # Data / AI
    # -------------------------

    "Machine Learning": [
        "machine learning",
        "ml",
        "scikit-learn",
        "scikit",
        "tensorflow",
        "pytorch"
    ],

    "Deep Learning": [
        "deep learning",
        "neural network",
        "neural networks",
        "tensorflow",
        "pytorch"
    ],

    "Pandas": [
        "pandas"
    ],

    "NumPy": [
        "numpy"
    ],

    "Data Visualization": [
        "data visualization",
        "matplotlib",
        "seaborn",
        "plotly",
        "tableau",
        "power bi"
    ],

    "Statistics": [
        "statistics",
        "statistical analysis",
        "probability",
        "hypothesis testing"
    ],

    # -------------------------
    # Frontend
    # -------------------------

    "HTML": [
        "html",
        "html5"
    ],

    "CSS": [
        "css",
        "css3",
        "tailwind",
        "bootstrap"
    ],

    "React": [
        "react",
        "react.js",
        "reactjs"
    ],

    "Vue": [
        "vue",
        "vue.js"
    ],

    "Angular": [
        "angular",
        "angular.js"
    ],

    # -------------------------
    # Other
    # -------------------------

    "Excel": [
        "excel",
        "microsoft excel"
    ],

    "Communication": [
        "communication",
        "communication skills",
        "verbal communication",
        "written communication"
    ]
}


# =========================================================
# ROLE SKILL REQUIREMENTS
# =========================================================

ROLE_SKILLS = {

    "Backend Java Developer": [
        "Java",
        "OOP",
        "Spring Boot",
        "SQL",
        "REST APIs",
        "Git",
        "Data Structures",
        "PostgreSQL",
        "Docker"
    ],

    "Backend Python Developer": [
        "Python",
        "OOP",
        "Flask",
        "REST APIs",
        "SQL",
        "Git",
        "Docker",
        "PostgreSQL",
        "Data Structures"
    ],

    "Full Stack Developer": [
        "JavaScript",
        "TypeScript",
        "React",
        "Node.js",
        "HTML",
        "CSS",
        "SQL",
        "REST APIs",
        "Git",
        "Docker"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Data Visualization",
        "Excel",
        "Statistics"
    ],

    "ML Engineer": [
        "Python",
        "NumPy",
        "Pandas",
        "Machine Learning",
        "Deep Learning",
        "Data Structures",
        "SQL",
        "Docker",
        "Git"
    ],

    "Cloud Engineer": [
        "AWS",
        "Linux",
        "Docker",
        "Kubernetes",
        "Python",
        "CI/CD",
        "Git",
        "System Design"
    ],

    "Frontend Developer": [
        "JavaScript",
        "TypeScript",
        "React",
        "HTML",
        "CSS",
        "Git",
        "REST APIs"
    ]
}


# =========================================================
# ROLE DESCRIPTIONS
# =========================================================

ROLE_DESCRIPTIONS = {

    "Backend Java Developer":
        "Build scalable server-side applications and APIs using Java, Spring Boot and databases.",

    "Backend Python Developer":
        "Develop backend services and APIs using Python frameworks, databases and modern development tools.",

    "Full Stack Developer":
        "Build complete web applications across frontend, backend, APIs and databases.",

    "Data Analyst":
        "Transform raw data into useful insights using Python, SQL, statistics and visualization.",

    "ML Engineer":
        "Build, evaluate and deploy machine learning systems and data-driven applications.",

    "Cloud Engineer":
        "Design, deploy and maintain cloud infrastructure, containers and automated deployment pipelines.",

    "Frontend Developer":
        "Build responsive and interactive web interfaces using modern frontend technologies."
}


# =========================================================
# LEARNING ROADMAPS
# =========================================================

ROADMAPS = {

    # =====================================================
    # BACKEND JAVA
    # =====================================================

    "Backend Java Developer": [

        (
            "Week 1",
            "Java Foundations",
            "Strengthen your core Java fundamentals.",
            [
                "Java OOP fundamentals",
                "Classes, objects and constructors",
                "Inheritance and polymorphism",
                "Collections & Generics",
                "Exception Handling"
            ]
        ),

        (
            "Week 2",
            "Databases & SQL",
            "Learn how backend applications store and retrieve data.",
            [
                "SQL fundamentals",
                "SELECT, INSERT, UPDATE and DELETE",
                "Joins & aggregations",
                "JDBC & database connectivity",
                "SQLite/PostgreSQL setup"
            ]
        ),

        (
            "Week 3",
            "Spring Boot",
            "Start building modern Java backend applications.",
            [
                "Spring Boot fundamentals",
                "Project structure",
                "Dependency Injection",
                "REST API fundamentals",
                "Build your first Spring Boot API"
            ]
        ),

        (
            "Week 4",
            "Spring Data",
            "Connect your backend to a production-style database.",
            [
                "Spring Data JPA",
                "Entities and repositories",
                "PostgreSQL integration",
                "CRUD APIs",
                "Validation and error handling"
            ]
        ),

        (
            "Week 5",
            "Authentication",
            "Understand how backend applications protect users and APIs.",
            [
                "Authentication fundamentals",
                "JWT authentication",
                "Spring Security basics",
                "Role-based authorization"
            ]
        ),

        (
            "Week 6",
            "Docker & Deployment",
            "Learn how to package and run backend applications.",
            [
                "Docker fundamentals",
                "Dockerfile",
                "Containerize your Spring Boot application",
                "Environment variables",
                "Basic deployment concepts"
            ]
        ),

        (
            "Week 7",
            "Backend Project",
            "Build a complete portfolio-level backend project.",
            [
                "Design database schema",
                "Create REST APIs",
                "Add authentication",
                "Connect PostgreSQL",
                "Write API documentation"
            ]
        ),

        (
            "Week 8",
            "Career Preparation",
            "Turn your learning into an interview-ready portfolio.",
            [
                "Deploy your project",
                "Improve GitHub README",
                "Prepare backend interview questions",
                "Practice DSA",
                "Update your resume"
            ]
        )
    ],


    # =====================================================
    # BACKEND PYTHON
    # =====================================================

    "Backend Python Developer": [

        (
            "Week 1",
            "Python Foundations",
            "Build strong Python programming fundamentals.",
            [
                "Python OOP",
                "Functions and modules",
                "File handling",
                "Error handling",
                "Virtual environments"
            ]
        ),

        (
            "Week 2",
            "Flask & APIs",
            "Learn how Python applications expose backend services.",
            [
                "Flask basics",
                "Routes",
                "Request and response",
                "REST APIs",
                "JSON"
            ]
        ),

        (
            "Week 3",
            "Databases",
            "Connect backend applications to databases.",
            [
                "SQL fundamentals",
                "PostgreSQL",
                "SQLAlchemy",
                "Database models",
                "CRUD operations"
            ]
        ),

        (
            "Week 4",
            "Authentication",
            "Build secure user-based applications.",
            [
                "Authentication",
                "JWT",
                "Password hashing",
                "Authorization"
            ]
        ),

        (
            "Week 5",
            "Docker",
            "Package and run your backend consistently.",
            [
                "Docker fundamentals",
                "Dockerfile",
                "Images and containers",
                "Environment variables"
            ]
        ),

        (
            "Week 6",
            "Testing",
            "Learn how to test backend systems.",
            [
                "pytest fundamentals",
                "Unit tests",
                "API testing",
                "Test organization"
            ]
        ),

        (
            "Week 7",
            "Portfolio Project",
            "Build a complete Python backend project.",
            [
                "Plan project architecture",
                "Build APIs",
                "Connect database",
                "Add authentication",
                "Test APIs"
            ]
        ),

        (
            "Week 8",
            "Deployment & Career",
            "Prepare your backend work for applications.",
            [
                "Deploy project",
                "Improve README",
                "Prepare interview questions",
                "Update resume"
            ]
        )
    ],


    # =====================================================
    # FULL STACK
    # =====================================================

    "Full Stack Developer": [

        (
            "Week 1",
            "Web Foundations",
            "Build a strong foundation for web development.",
            [
                "HTML fundamentals",
                "CSS fundamentals",
                "JavaScript basics",
                "DOM manipulation"
            ]
        ),

        (
            "Week 2",
            "React",
            "Learn modern frontend development.",
            [
                "React components",
                "Props and state",
                "Hooks",
                "Forms",
                "API integration"
            ]
        ),

        (
            "Week 3",
            "Node.js Backend",
            "Build backend services with JavaScript.",
            [
                "Node.js",
                "Express",
                "REST APIs",
                "Middleware",
                "Error handling"
            ]
        ),

        (
            "Week 4",
            "Database",
            "Connect your application to persistent data.",
            [
                "SQL",
                "PostgreSQL",
                "Database design",
                "CRUD operations"
            ]
        ),

        (
            "Week 5",
            "Authentication",
            "Build secure full-stack applications.",
            [
                "Authentication",
                "JWT",
                "Protected routes",
                "Authorization"
            ]
        ),

        (
            "Week 6",
            "Docker",
            "Understand application containerization.",
            [
                "Docker fundamentals",
                "Dockerfile",
                "Frontend container",
                "Backend container"
            ]
        ),

        (
            "Week 7",
            "Full Stack Project",
            "Build a complete application.",
            [
                "Design application",
                "Build frontend",
                "Build backend",
                "Connect database",
                "Authentication"
            ]
        ),

        (
            "Week 8",
            "Deployment",
            "Prepare your project for your portfolio.",
            [
                "Deploy application",
                "Write README",
                "Add screenshots",
                "Prepare interview questions"
            ]
        )
    ],


    # =====================================================
    # DATA ANALYST
    # =====================================================

    "Data Analyst": [

        (
            "Week 1",
            "Python & Pandas",
            "Learn the tools used to work with datasets.",
            [
                "Python basics",
                "NumPy fundamentals",
                "Pandas fundamentals",
                "DataFrames",
                "Data loading"
            ]
        ),

        (
            "Week 2",
            "Data Cleaning",
            "Turn messy datasets into usable data.",
            [
                "Missing values",
                "Duplicate data",
                "Data types",
                "Outlier detection",
                "Data transformation"
            ]
        ),

        (
            "Week 3",
            "SQL",
            "Learn to retrieve and analyze database data.",
            [
                "SQL queries",
                "Joins",
                "GROUP BY",
                "Aggregations",
                "Subqueries"
            ]
        ),

        (
            "Week 4",
            "Visualization",
            "Turn data into understandable visuals.",
            [
                "Matplotlib",
                "Seaborn",
                "Plotly",
                "Charts",
                "Dashboard fundamentals"
            ]
        ),

        (
            "Week 5",
            "Statistics",
            "Build the statistical foundation needed for analysis.",
            [
                "Mean, median and mode",
                "Probability",
                "Distributions",
                "Correlation",
                "Hypothesis testing"
            ]
        ),

        (
            "Week 6",
            "Machine Learning",
            "Understand the basics of predictive analytics.",
            [
                "Machine learning fundamentals",
                "Regression",
                "Classification",
                "Model evaluation"
            ]
        ),

        (
            "Week 7",
            "Analysis Project",
            "Create a complete data analysis project.",
            [
                "Choose dataset",
                "Clean data",
                "Perform analysis",
                "Create visualizations",
                "Present findings"
            ]
        ),

        (
            "Week 8",
            "Portfolio & Career",
            "Turn your analysis into a portfolio project.",
            [
                "Create project README",
                "Publish project",
                "Build portfolio",
                "Update resume",
                "Interview preparation"
            ]
        )
    ],


    # =====================================================
    # ML ENGINEER
    # =====================================================

    "ML Engineer": [

        (
            "Week 1",
            "Python for ML",
            "Strengthen the programming foundation required for ML.",
            [
                "Python",
                "NumPy",
                "Pandas",
                "Data preprocessing"
            ]
        ),

        (
            "Week 2",
            "ML Fundamentals",
            "Understand how machine learning systems work.",
            [
                "Supervised learning",
                "Unsupervised learning",
                "Training and testing",
                "Features and labels"
            ]
        ),

        (
            "Week 3",
            "ML Algorithms",
            "Implement common machine learning algorithms.",
            [
                "Linear regression",
                "Logistic regression",
                "Decision trees",
                "KNN",
                "Clustering"
            ]
        ),

        (
            "Week 4",
            "Deep Learning",
            "Understand neural networks and modern ML.",
            [
                "Neural networks",
                "TensorFlow basics",
                "PyTorch basics",
                "Training models"
            ]
        ),

        (
            "Week 5",
            "Model Evaluation",
            "Learn how to measure and improve model performance.",
            [
                "Accuracy",
                "Precision and recall",
                "F1 score",
                "Cross validation",
                "Hyperparameter tuning"
            ]
        ),

        (
            "Week 6",
            "ML APIs",
            "Turn your model into a usable application.",
            [
                "FastAPI or Flask",
                "Model serialization",
                "REST API",
                "API testing"
            ]
        ),

        (
            "Week 7",
            "End-to-End Project",
            "Build a complete machine learning application.",
            [
                "Collect data",
                "Train model",
                "Evaluate model",
                "Create API",
                "Build interface"
            ]
        ),

        (
            "Week 8",
            "ML Portfolio",
            "Prepare your project for internships and jobs.",
            [
                "Deploy model",
                "Write README",
                "Document experiments",
                "Prepare ML interview questions"
            ]
        )
    ],


    # =====================================================
    # CLOUD ENGINEER
    # =====================================================

    "Cloud Engineer": [

        (
            "Week 1",
            "Linux Foundations",
            "Build the operating-system knowledge required for cloud work.",
            [
                "Linux commands",
                "File permissions",
                "Processes",
                "Bash scripting",
                "SSH"
            ]
        ),

        (
            "Week 2",
            "AWS Fundamentals",
            "Understand the major AWS services.",
            [
                "AWS fundamentals",
                "EC2",
                "S3",
                "IAM",
                "VPC basics"
            ]
        ),

        (
            "Week 3",
            "Docker",
            "Learn application containerization.",
            [
                "Docker",
                "Images",
                "Containers",
                "Dockerfile",
                "Docker Compose"
            ]
        ),

        (
            "Week 4",
            "Kubernetes",
            "Understand container orchestration.",
            [
                "Kubernetes fundamentals",
                "Pods",
                "Deployments",
                "Services",
                "ConfigMaps"
            ]
        ),

        (
            "Week 5",
            "CI/CD",
            "Automate application delivery.",
            [
                "GitHub Actions",
                "Build pipelines",
                "Automated testing",
                "Deployment pipelines"
            ]
        ),

        (
            "Week 6",
            "Infrastructure",
            "Understand infrastructure automation.",
            [
                "Infrastructure as Code",
                "Terraform fundamentals",
                "Cloud networking",
                "Environment management"
            ]
        ),

        (
            "Week 7",
            "Cloud Project",
            "Deploy a real application in the cloud.",
            [
                "Containerize application",
                "Deploy to cloud",
                "Configure database",
                "Set up CI/CD"
            ]
        ),

        (
            "Week 8",
            "Career Preparation",
            "Prepare for cloud engineering opportunities.",
            [
                "Document project",
                "Review AWS services",
                "Practice cloud interview questions",
                "Resume preparation"
            ]
        )
    ],


    # =====================================================
    # FRONTEND
    # =====================================================

    "Frontend Developer": [

        (
            "Week 1",
            "HTML & CSS",
            "Build strong web fundamentals.",
            [
                "HTML5",
                "Semantic HTML",
                "CSS fundamentals",
                "Flexbox",
                "Grid"
            ]
        ),

        (
            "Week 2",
            "JavaScript",
            "Build a strong JavaScript foundation.",
            [
                "Variables and functions",
                "Arrays and objects",
                "DOM",
                "Events",
                "Async JavaScript"
            ]
        ),

        (
            "Week 3",
            "React",
            "Learn modern component-based development.",
            [
                "React components",
                "Props",
                "State",
                "Hooks",
                "Forms"
            ]
        ),

        (
            "Week 4",
            "API Integration",
            "Connect frontend applications with backend services.",
            [
                "REST APIs",
                "Fetch/Axios",
                "JSON",
                "Loading states",
                "Error handling"
            ]
        ),

        (
            "Week 5",
            "UI Engineering",
            "Build polished user interfaces.",
            [
                "Responsive design",
                "Reusable components",
                "Accessibility",
                "Design systems"
            ]
        ),

        (
            "Week 6",
            "Testing & Git",
            "Learn professional development practices.",
            [
                "Git",
                "GitHub",
                "Testing fundamentals",
                "Pull requests"
            ]
        ),

        (
            "Week 7",
            "Frontend Project",
            "Build a complete portfolio application.",
            [
                "Plan interface",
                "Build components",
                "Connect API",
                "Responsive design"
            ]
        ),

        (
            "Week 8",
            "Portfolio",
            "Prepare your work for applications.",
            [
                "Deploy project",
                "Improve GitHub README",
                "Create portfolio",
                "Resume preparation",
                "Interview preparation"
            ]
        )
    ]
}


# =========================================================
# NORMALIZATION
# =========================================================

def normalize_text(text):
    """
    Normalize text so skill matching is more reliable.
    """

    if not text:
        return ""

    text = str(text).lower()

    text = text.replace("&", " and ")

    text = re.sub(r"[^a-z0-9+#./ -]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# SKILL MATCHING
# =========================================================

def keyword_matches(text, keyword):
    """
    More reliable keyword matching than simple substring search.
    """

    text = normalize_text(text)
    keyword = normalize_text(keyword)

    if not text or not keyword:
        return False

    # Special handling for symbols such as C++
    if keyword in {"c++", "cpp"}:
        return "c++" in text or "cpp" in text

    # Multi-word skills can safely use substring matching.
    if " " in keyword or "/" in keyword or "." in keyword:
        return keyword in text

    pattern = rf"\b{re.escape(keyword)}\b"

    return bool(re.search(pattern, text))


# =========================================================
# EXTRACT SKILLS FROM JOB DESCRIPTION
# =========================================================

def extract_skills_from_jd(job_description):

    if not job_description:
        return []

    text = normalize_text(job_description)

    found_skills = []

    for skill, keywords in SKILL_KEYWORDS.items():

        for keyword in keywords:

            if keyword_matches(text, keyword):
                found_skills.append(skill)
                break

    return sorted(
        set(found_skills),
        key=lambda value: value.lower()
    )


# =========================================================
# EXTRACT SKILLS FROM GITHUB
# =========================================================

def get_github_skills(repos, analyzed_data):

    github_skills = set()

    repos = repos or []
    analyzed_data = analyzed_data or {}

    # -----------------------------------------------------
    # GitHub languages
    # -----------------------------------------------------

    languages = analyzed_data.get("languages", {})

    if isinstance(languages, dict):

        for language in languages.keys():

            language_normalized = normalize_text(language)

            for skill, keywords in SKILL_KEYWORDS.items():

                for keyword in keywords:

                    if keyword_matches(language_normalized, keyword):
                        github_skills.add(skill)
                        break

    # -----------------------------------------------------
    # Repository information
    # -----------------------------------------------------

    for repo in repos:

        if not isinstance(repo, dict):
            continue

        topics = repo.get("topics", []) or []

        description = repo.get("description", "") or ""

        name = repo.get("name", "") or ""

        homepage = repo.get("homepage", "") or ""

        combined = " ".join(
            [
                " ".join(str(topic) for topic in topics),
                description,
                name,
                homepage
            ]
        )

        for skill, keywords in SKILL_KEYWORDS.items():

            for keyword in keywords:

                if keyword_matches(combined, keyword):
                    github_skills.add(skill)
                    break

    return github_skills


# =========================================================
# COMBINE SKILLS
# =========================================================

def combine_skills(*skill_lists):

    combined = set()

    for skills in skill_lists:

        if not skills:
            continue

        for skill in skills:
            if skill:
                combined.add(str(skill).strip())

    return combined


# =========================================================
# SKILL GAP ANALYSIS
# =========================================================

def analyze_skill_gap(required_skills, known_skills):

    required = list(
        dict.fromkeys(
            str(skill).strip()
            for skill in (required_skills or [])
            if str(skill).strip()
        )
    )

    known = {
        str(skill).strip().lower()
        for skill in (known_skills or [])
        if str(skill).strip()
    }

    result = {
        "have": [],
        "partial": [],
        "missing": [],
        "total": len(required),
        "match_percentage": 0
    }

    for skill in required:

        if skill.lower() in known:
            result["have"].append(skill)

        else:
            result["missing"].append(skill)

    total = result["total"]

    if total:
        result["match_percentage"] = round(
            len(result["have"]) / total * 100
        )

    return result


# =========================================================
# ROLE HELPERS
# =========================================================

def get_role_skills(role):

    return ROLE_SKILLS.get(role, [])


def get_role_description(role):

    return ROLE_DESCRIPTIONS.get(
        role,
        "Build the skills and projects needed for your target career."
    )


def get_available_roles():

    return list(ROLE_SKILLS.keys())


# =========================================================
# ROADMAP HELPERS
# =========================================================

def get_roadmap(role):

    return ROADMAPS.get(role, [])


def get_roadmap_weeks(role):

    roadmap = get_roadmap(role)

    return len(roadmap)


def get_roadmap_total_tasks(role):

    roadmap = get_roadmap(role)

    return sum(
        len(week[3])
        for week in roadmap
    )


def get_roadmap_tasks(role):

    roadmap = get_roadmap(role)

    tasks = []

    for week_label, title, description, week_tasks in roadmap:

        for task in week_tasks:

            tasks.append({
                "week": week_label,
                "title": title,
                "description": description,
                "task": task
            })

    return tasks


# =========================================================
# ROADMAP PROGRESS
# =========================================================

def calculate_roadmap_progress(role, completed_tasks):

    all_tasks = get_roadmap_tasks(role)

    if not all_tasks:
        return {
            "completed": 0,
            "total": 0,
            "percentage": 0
        }

    completed_set = {
        str(task).strip()
        for task in (completed_tasks or [])
    }

    completed = sum(
        1
        for item in all_tasks
        if item["task"] in completed_set
    )

    total = len(all_tasks)

    percentage = round(
        completed / total * 100
    )

    return {
        "completed": completed,
        "total": total,
        "percentage": percentage
    }


# =========================================================
# ROLE READINESS
# =========================================================

def calculate_role_readiness(
    role,
    known_skills,
    github_skills=None
):

    required = get_role_skills(role)

    combined = combine_skills(
        known_skills,
        github_skills
    )

    gap = analyze_skill_gap(
        required,
        combined
    )

    return gap


# =========================================================
# SKILL RECOMMENDATIONS
# =========================================================

SKILL_RECOMMENDATIONS = {

    "Java":
        "Strengthen Java fundamentals and build small console or backend projects.",

    "Spring Boot":
        "Build a REST API using Spring Boot and connect it to PostgreSQL.",

    "SQL":
        "Practice joins, aggregations, subqueries and database design.",

    "REST APIs":
        "Build a CRUD REST API using proper HTTP methods and status codes.",

    "Git":
        "Practice branches, commits, pull requests and GitHub workflows.",

    "Data Structures":
        "Practice arrays, strings, linked lists, stacks, queues, trees and hashing.",

    "PostgreSQL":
        "Move one existing SQLite project to PostgreSQL.",

    "Docker":
        "Containerize one of your existing projects with a Dockerfile.",

    "Python":
        "Build a small Python project using clean functions, modules and error handling.",

    "React":
        "Build a dashboard with reusable React components and API integration.",

    "JavaScript":
        "Practice DOM manipulation, asynchronous JavaScript and API calls.",

    "TypeScript":
        "Convert a small JavaScript project to TypeScript.",

    "Node.js":
        "Build an Express REST API with authentication and a database.",

    "Machine Learning":
        "Build an end-to-end ML project from preprocessing to evaluation.",

    "AWS":
        "Learn EC2, S3, IAM and basic networking through a small deployment project.",

    "Kubernetes":
        "Learn Pods, Deployments and Services after becoming comfortable with Docker.",

    "Linux":
        "Practice terminal commands, permissions, processes and Bash scripting.",

    "CI/CD":
        "Create a GitHub Actions workflow that tests and builds your project.",

    "System Design":
        "Study APIs, databases, caching, scalability and distributed systems."
}


def get_skill_recommendation(skill):

    return SKILL_RECOMMENDATIONS.get(
        skill,
        f"Learn {skill} and build a small project that demonstrates it."
    )


# =========================================================
# CAREER SUMMARY
# =========================================================

def get_career_summary(
    role,
    known_skills,
    github_skills=None
):

    gap = calculate_role_readiness(
        role,
        known_skills,
        github_skills
    )

    missing = gap["missing"]

    recommendations = [
        {
            "skill": skill,
            "recommendation": get_skill_recommendation(skill)
        }
        for skill in missing[:6]
    ]

    return {
        "role": role,
        "description": get_role_description(role),
        "required_skills": get_role_skills(role),
        "skills_have": gap["have"],
        "skills_missing": gap["missing"],
        "match_percentage": gap["match_percentage"],
        "recommendations": recommendations
    }