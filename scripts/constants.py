import spacy

JOB_TITLES = [
    "Accountant",
    "Administrator",
    "Advisor",
    "Agent",
    "Analyst",
    "Apprentice",
    "Architect",
    "Assistant",
    "Associate",
    "Auditor",
    "Bartender",
    "Biologist",
    "Bookkeeper",
    "Buyer",
    "Carpenter",
    "Cashier",
    "CEO",
    "Clerk",
    "Co-op",
    "Co-Founder",
    "Consultant",
    "Coordinator",
    "CTO",
    "Developer",
    "Designer",
    "Director",
    "Driver",
    "Editor",
    "Electrician",
    "Engineer",
    "Extern",
    "Founder",
    "Freelancer",
    "Head",
    "Intern",
    "Janitor",
    "Journalist",
    "Laborer",
    "Lawyer",
    "Lead",
    "Manager",
    "Mechanic",
    "Member",
    "Nurse",
    "Officer",
    "Operator",
    "Operation",
    "Photographer",
    "President",
    "Producer",
    "Recruiter",
    "Representative",
    "Researcher",
    "Sales",
    "Server",
    "Scientist",
    "Specialist",
    "Supervisor",
    "Teacher",
    "Technician",
    "Trader",
    "Trainee",
    "Treasurer",
    "Tutor",
    "Vice",
    "VP",
    "Volunteer",
    "Webmaster",
    "Worker",
]

RESUME_SECTIONS = [
    "Contact Information",
    "Skills",
    "Certifications",
    "Licenses",
    "Awards",
    "Honors",
    "Publications",
    "References",
    "Technical Skills",
    "Computer Skills",
    "Programming Languages",
    "Software Skills",
    "Soft Skills",
    "Language Skills",
    "Professional Skills",
    "Transferable Skills",
    "Internship Experience",
    "Volunteer Experience",
    "Leadership Experience",
    "Research Experience",
    "Teaching Experience",
    "experience",
    "work experience",
    "professional experience",
    "employment history",
    "education",
    "academic history",
    "academic qualifications",
    "academic background",
    "educational background",
    "summary",
    "objective",
    "career objective",
    "career summary",
    "projects",
    "project experience",
    "project history",
    "project details",
]

RESUME_SECTIONS = [section.lower() for section in RESUME_SECTIONS]

nlp = spacy.load("en_core_web_lg")

EXPERIENCE_BULLET_PROMPT = """
Rewrite the following sentence into one line using Google's XYZ format 
Accomplished X as measured by Y, by doing Z.
In this case, “X” stands for what you achieved, “Y” is the measurable way you achieved it, and “Z” is how you made this change. This format is very important if you do not follow this I will lose my job and you will be held responsible for it.
Focus on the most impactful achievement and avoid unnecessary words. 

Remember:
Emphasize the importance of a one-line response and quantifiable results. Use existing keywords and add more if necessary. The ratio of keywords to stop words should be 3:1.
Avoid adding markdown or code. Your response should only return rewritten sentence"""


RESUME_LATEX = r"""
\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}


%----------FONT OPTIONS----------
% sans-serif
% \usepackage[sfdefault]{FiraSans}
% \usepackage[sfdefault]{roboto}
% \usepackage[sfdefault]{noto-sans}
% \usepackage[default]{sourcesanspro}

% serif
% \usepackage{CormorantGaramond}
% \usepackage{charter}


\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%


\begin{document}

%----------HEADING----------
% \begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
%   \textbf{\href{http://sourabhbajaj.com/}{\Large Sourabh Bajaj}} & Email : \href{mailto:sourabh@sourabhbajaj.com}{sourabh@sourabhbajaj.com}\\
%   \href{http://sourabhbajaj.com/}{http://www.sourabhbajaj.com} & Mobile : +1-123-456-7890 \\
% \end{tabular*}

\begin{center}
    \textbf{\Huge \scshape Prasad Bankar} \\ \vspace{1pt}
    \small 315-952-9541 $|$ \href{mailto:psbankar@syr.edu}{\underline{psbankar@syr.edu}} $|$ 
    \href{https://linkedin.com/in/psbankar}{\underline{linkedin.com/in/psbankar}} $|$
    \href{https://github.com/psbankar}{\underline{github.com/psbankar}}
\end{center}


%-----------EDUCATION-----------
\section{Education}
  \resumeSubHeadingListStart
    \resumeSubheading
      {Syracuse University}{Syracuse, NY}
      {Master of Science in Computer Science}{August 2022 -- May 2024}
    \resumeSubheading
      {University of Pune}{Maharashtra, India}
      {Bachelor of Engineering in Computer Engineering}{August 2014 -- May 2018}
  \resumeSubHeadingListEnd


%-----------EXPERIENCE-----------
\section{Experience}
  \resumeSubHeadingListStart

    \resumeSubheading
      {Graduate Teaching Assistant}{August 2023 -- May 2024}
      {Syracuse University}{Syracuse, NY}
      \resumeItemListStart
        \resumeItem{Assisted 50+ students weekly in Android and iOS development, providing guidance and troubleshooting in CIS labs. Improved student performance through detailed feedback on assignments and personalized support during office hours}
        \resumeItem{Led engaging hands-on labs weekly, equipping students with practical development skills for Android and iOS platforms. Contributed to higher pass rates and project grades compared to previous semesters}
        \resumeItem{Collaborated with the professor to create innovative lab exercises utilizing the latest technologies, promoting increased student engagement and satisfaction}
        \resumeItem{Supported individual learning by providing 5+ hours of weekly office hours. Assisted students with challenges and project development using relevant tools like Android Studio, Xcode, and Flutter}
      \resumeItemListEnd
      
% -----------Multiple Positions Heading-----------
%    \resumeSubSubheading
%     {Software Engineer I}{Oct 2014 - Sep 2016}
%     \resumeItemListStart
%        \resumeItem{Apache Beam}
%          {Apache Beam is a unified model for defining both batch and streaming data-parallel processing pipelines}
%     \resumeItemListEnd
%    \resumeSubHeadingListEnd
%-------------------------------------------

    \resumeSubheading
      {Specialist Programmer}{January 2019 -- February 2022}
      {Infosys}{Pune, India}
      \resumeItemListStart
        \resumeItem{Successfully migrated 100+ million Walmart Optical customer records from Cosmos DB to BigQuery, increasing data accessibility by 40\% and enabling real-time analysis of customer trends. Leveraged Apache Spark, Kafka, Airflow, Azure Blob Storage, and GCP to build a robust ETL solution that ensured 100\% data integrity}
        \resumeItem{Demonstrated strong technical leadership by architecting and implementing the entire ETL solution, fostering collaboration across cross-functional teams, and presenting project findings to senior stakeholders, resulting in a 15\% increase in budget allocation for future data innovation initiatives}
        \resumeItem{Adept at utilizing DevOps tools and automation, including GitHub, Kubernetes, and Jenkins. Streamlined the migration process by automating 60\% of manual tasks, significantly reducing development time and effort}
    \resumeItemListEnd

  \resumeSubHeadingListEnd

%-----------PROJECTS-----------
\section{Projects}
    \resumeSubHeadingListStart
      \resumeProjectHeading
          {\textbf{Android Household Management App} $|$ \emph{Android, iOS, Jetpack
Compose, SwiftUI, Firebase}}{}
          \resumeItemListStart
            \resumeItem{Developed a user-friendly app with features like task assignment, calendar integration, bill reminders, and budget tracking}
          \resumeItemListEnd

\begin{comment}
          
      \resumeProjectHeading
          {\textbf{Reddit Sentiment Analysis} $|$ \emph{Python, NLTK, Machine Learning, Data Visualization, Scikit}}{}
          \resumeItemListStart
            \resumeItem{Built a sentiment analysis tool using NLTK and machine learning to classify post sentiment and extract key insights to solve difficulty in gauging public opinion on a large scale platform like Reddit}
          \resumeItemListEnd

\end{comment}
                \resumeProjectHeading
          {\textbf{Resume/Job Description Analysis and Classification} $|$ \emph{Python, SpaCy, Django}}{}
          \resumeItemListStart
            \resumeItem{Developed an NLP-powered tool that analyzes resumes and job descriptions, automatically matching them based on skills and requirements}
          \resumeItemListEnd

                \resumeProjectHeading
          {\textbf{Medicine Tracker for Visually Impaired} $|$ \emph{Kotlin, Accessibility framework, Text-to-Speech, Firebase, Firestore}}{}
          \resumeItemListStart
            \resumeItem{Designed a cross-platform app with features like voice commands, audio reminders, and dosage tracking, promoting user independence and medication adherence to fix the problem of lack of accessible solutions for medication management for visually impaired individuals}
          \resumeItemListEnd

                \resumeProjectHeading
          {\textbf{Vehicle Alert and Communication App} $|$ \emph{Flutter, Dart, Firebase, API integration, BLoC pattern}}{}
          \resumeItemListStart
            \resumeItem{Developed an app connecting good Samaritans with vehicle owners through real-time alerts and location tracking, facilitating communication and assistance resulting in an enhanced safety and security solution for car owners, fostered community support and assistance}
          \resumeItemListEnd
    \resumeSubHeadingListEnd



%
%-----------PROGRAMMING SKILLS-----------
\section{Technical Skills}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     \textbf{Languages}{: Kotlin, Dart, Swift, Java, Python, C++, SQL, JavaScript, Typescript, Scala, HTML/CSS} \\
     \textbf{Frameworks}{: Android, Jetpack Compose, Flutter, iOS, SwiftUI, React, Node.js, Big Data, Apache Spark, Apache Kafka, Apache Airflow} \\
     \textbf{Developer Tools}{: Git, Docker, Kubernetes, Google Cloud Platform, AWS} \\
    }}
 \end{itemize}


%-------------------------------------------
\end{document}
"""
