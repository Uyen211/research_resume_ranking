# MLAR: Multi-layer Large Language Model-based Robotic Process Automation Applicant Tracking

Mohamed T. Younes * 

Computer Science Dept. 

MSA University 

Giza, Egypt 

mohamed.tarek61@msa.edu.eg 

Omar Walid 

Computer Science Dept. 

MSA University 

Giza, Egypt 

omar.walid2@msa.edu.eg 

Mai Hassan 

Computer Science Dept. 

MSA University 

Giza, Egypt 

maisalem@msa.edu.eg 

Ali Hamdi 

Computer Science Dept. 

MSA University 

Giza, Egypt 

ahamdi@msa.edu.eg 

Abstract—This paper introduces an innovative Applicant Tracking System (ATS) enhanced by a novel Robotic process automation (RPA) framework or as further referred to as MLAR. Traditional recruitment processes often encounter bottlenecks in resume screening and candidate shortlisting due to time and resource constraints. MLAR addresses these challenges employing Large Language Models (LLMs) in three distinct layers: extracting key characteristics from job postings in the first layer, parsing applicant resume to identify education, experience, skills in the second layer, and similarity matching in the third layer. These features are then matched through advanced semantic algorithms to identify the best candidates efficiently. Our approach integrates seamlessly into existing RPA pipelines, automating resume parsing, job matching, and candidate notifications. Extensive performance benchmarking shows that MLAR outperforms the leading RPA platforms, including UiPath and Automation Anywhere, in high-volume resume-processing tasks. When processing 2,400 resumes, MLAR achieved an average processing time of 5.4 seconds per resume, reducing processing time by approximately $1 6 . 9 \%$ compared to Automation Anywhere and $1 7 . 1 \%$ compared to UiPath. These results highlight the potential of MLAR to transform recruitment workflows by providing an efficient, accurate, and scalable solution tailored to modern hiring needs. 

Index Terms—Applicant Tracking System (ATS), Robotic Process Automation (RPA), Large Language Models (LLMs). 

# I. INTRODUCTION

Recruitment is a vital yet challenging process, as HR teams face difficulties managing large volumes of applications. Manual candidate selection is labor intensive, error prone and involves risks overlooking qualified applicants or introducing biases. The integration of RPA technologies augmented with LLMs offers a solution to optimize recruitment workflows [1], [2]. Research shows that RPA reduces time spent on repetitive administrative tasks, enabling HR professionals to prioritize strategic initiatives [3], [4]. 

Traditional ATS have played a pivotal role in automating aspects of the recruitment process, such as filtering resumes based on keyword matching [5]. However, these systems face significant limitations. Keyword-based filtering often fails to capture the context of job requirements and applicant qualifications, resulting in suboptimal matching [6]. Moreover, existing NLP-based text similarity and matching methods, while promising, struggle to process complex structures and large-scale recruitment data effectively and efficiently [7]. 

Research on ATS and RPA highlights the importance of semantic understanding in overcoming such challenges, with AI-powered models being increasingly adopted to enhance matching accuracy [8], [9], [10]. 

The emergence of Large Language Models (LLMs) has transformed text comprehension through advanced, contextsensitive processing. In recruitment, LLMs analyze unstructured text to identify essential attributes like education, experience, skills, and competencies, enhancing semantic interpretation of resumes and job descriptions [11]. Innovative frameworks such as MockLLM replicate mock interviews to optimize candidate assessment, strengthening job-applicant alignment via refined semantic analysis [12]. RPA systems integrated with AI and LLMs boost operational efficiency while minimizing biases and fostering ethical hiring practices [11], [13]. Recent research demonstrates that specialized LLM-driven pipelines detect and mitigate biases in recruitment workflows, promoting equitable candidate selection [14]. 

This paper introduces MLAR, a novel Applicant Tracking System that leverages RPA and LLM technologies to automate end-to-end recruitment workflows. The system employs an LLM to identify critical attributes from resumes and job postings, compute compatibility metrics, and automatically notify top candidates. Unlike generic RPA tools, MLAR is specifically designed for high-volume resume analysis and recruitment enhancement, addressing shortcomings of current systems [15], [16]. Research shows that integrating LLMs into platforms like MLAR enhances semantic analysis and accelerates hiring workflows up to 11-fold compared to manual processes [17]. Additionally, advanced semantic models, including GPT-based architectures, exhibit measurable F1-score improvements in aligning extensive resumes with job profiles [18], emphasizing the efficacy of LLM-centric methods. 

The main contributions of this paper include: 

1) An innovative ATS architecture combining LLMs for feature extraction and candidate-job alignment. 

2) Comprehensive evaluation of MLAR against top RPA platforms like UiPath and Automation Anywhere, demonstrating greater speed and efficiency [19], [20]. 

3) Validation of the system’s capability to handle 2, 400 resumes within 3.5 hours, averaging 5.4 seconds per resume, surpassing existing solutions. 

4) An in-depth examination of LLMs impact on recruitment automation, emphasizing semantic matching’s superiority over conventional keyword-based methods. 

The remainder of this paper is organized as follows: Section II reviews related work in ATS, NLP techniques for recruitment, and RPA applications. Section III presents the problem formulation and challenges addressed by MLAR. Section IV details the proposed system architecture and methodology. Section V discusses the experimental results and benchmarks. Finally, Section VI concludes the paper with insights and future directions. 

# II. RELATED WORK

Robotic Process Automation (RPA) is a technology designed to automate repetitive rules-based tasks traditionally performed by humans. RPA bots simulate human interactions with software systems, handling tasks such as data entry, email management, and workflow orchestration. Unlike traditional automation methods that require integration at the code level, RPA operates at the interface level, offering flexibility and ease of deployment across existing systems [21]. Recent studies have shown how RPA can reduce the workload in recruitment processes and make them much faster [3]. 

Popular RPA platforms, such as UiPath [19] and Automation Anywhere [20], provide comprehensive tools for task automation across various industries, including recruitment. UiPath emphasizes user-friendly interfaces, featuring dragand-drop functionality for building automation workflows. Its ”Studio” environment allows developers and non-developers to create bots efficiently, supporting both attended and unattended bots. In contrast, Automation Anywhere offers cloud-native solutions with a focus on analytics. Its ”Bot Insight” tool provides real-time tracking of bot performance, making it suitable for large-scale, data-driven operations. However, as pointed out by [8], while these platforms are powerful, they still need significant customization to be useful for recruitment tasks like parsing resumes or matching candidates to jobs. 

Several research efforts have explored the application of RPA in recruitment. For example, [5] demonstrated how RPA can automate resume parsing and categorization using document classification techniques. This approach utilized Na¨ıve Bayes classifiers and custom-trained Named Entity Recognition (NER) models to extract essential details, including skills, experience, and education. But their system struggled with understanding the deeper context needed to match candidates to the right jobs. To tackle this, newer approaches have started combining RPA with AI, as discussed by [9]. AI tools add smarter decision-making abilities and improve how scalable these systems can be. 

In more recent work, Large Language Models (LLMs) have started to play a big role in making Applicant Tracking Systems (ATS) smarter. For instance, [6], the authors proposed a BERT-based framework for evaluating resumes and job descriptions, calculating similarity scores to predict candidate suitability. Another example is the ProspectCV system introduced in [7]. It uses Gemini Pro, an advanced LLM, to process 

resumes and job descriptions, providing detailed compatibility scores and feedback for candidates. These systems are much better at understanding the meaning behind words, which makes them more accurate than traditional RPA systems. Research by [17] also showed how LLMs could summarize resumes and grade candidates effectively, which saves time for recruiters. 

Some studies even explored using LLMs for tasks like mock interviews. For example, [12] suggested a system where an LLM acts as both the interviewer and the candidate to simulate job interviews. This kind of setup helps create a better understanding of whether a candidate is a good fit for the job. While these ideas are promising, they also raise important ethical questions about privacy and fairness in recruitment, as pointed out by [11]. They highlight the need to balance innovation with ethical practices. 

Even though these systems are improving, many of them still struggle with scalability and efficiency, especially when it comes to handling end-to-end recruitment workflows. To address these challenges, our proposed MLAR combines the automation of RPA with the intelligence of LLMs to deliver a state-of-the-art alternative to existing platforms. By using LLMs to extract important features from resumes and job postings, MLAR aims to make candidate-job matching faster and more accurate. This approach is supported by findings from [8] and [11], who stress the importance of building systems that are both efficient and ethical. 

This study positions MLAR as a specialized solution for recruitment, addressing the gaps in current systems and providing a more efficient, accurate, and scalable alternative to traditional RPA-powered ATS platforms. It takes advantage of the latest developments in RPA and LLM technologies to create a better recruitment process [3], [12]. 

# III. RESEARCH METHODOLOGY

# A. Problem Formulation

Recruitment is one of the most crucial yet complex functions within any organization. It directly impacts a company’s ability to achieve its strategic objectives by ensuring the right talent is hired for the right roles. However, the recruitment process often faces significant challenges that hinder efficiency, and accuracy and scalability. 

One of the most pressing challenges is managing the large volume of job applications received for each position, modern recruitment processes frequently involve handling thousands of resumes for a single job posting. As companies scale their operations or open multiple roles simultaneously, this volume multiplies, creating bottlenecks in the screening and evaluation phases. Handling such large datasets manually is both timeintensive and impractical. [1], [5]. 

The reliance on traditional methods further worsens these challenges. Manual resume screening is a time-consuming process prone to human errors. Recruiters may overlook highly qualified candidates due to fatigue or inefficiencies in handling large datasets. Additionally, unconscious biases can influence decision-making, resulting in inequities in candidate 

selection. For example, factors such as gender, ethnicity, or the formatting of a resume can unintentionally affect hiring decisions, compromising fairness and diversity in recruitment outcomes[2] [1]. Studies have shown that poorly formatted resumes, despite containing relevant information, are often disregarded during manual screening [11]. 

To address these challenges, many organizations have adopted Applicant Tracking Systems ATS, which partially automate the recruitment process. However, these systems are not without their limitations. Most traditional ATS rely on keyword-matching algorithms to filter resumes. While this approach is a step forward, it often fails to capture the full context of a candidate’s qualifications [1]. A candidate with relevant skills and experience may be excluded simply because their resume does not contain specific keywords matching the job description. This shortcoming results in a narrower pool of candidates for consideration, potentially eliminating highly suitable applicants. Moreover, ATS often require HR professionals to manually review and refine the system’s outputs, which reintroduces inefficiencies and diminishes the potential time savings. 

Another critical challenge lies in the end-to-end recruitment workflow, which involves multiple stages, including job posting, resume parsing, candidate shortlisting, and notification. In traditional systems, these stages often require a combination of manual intervention and semi-automated processes, leading to delays and inconsistencies [17], [21]. The inefficiency of these workflows directly impacts the time-to-hire, reducing an organization’s ability to secure top talent in competitive markets. For companies operating at scale, these delays can result in lost opportunities and reduced organizational productivity. [11] [8] 

# B. MLAR model

Job Description and Resume Parsing The system parses job descriptions and resumes to extract key features. Let $J$ represent the set of all job descriptions, and $R$ represent the set of all resumes. The system detects key features as follows: 

$$
F _ {J} (j) = \{f _ {1}, f _ {2}, \dots , f _ {m} \}, \quad F _ {R} (r) = \{f _ {1}, f _ {2}, \dots , f _ {n} \} (1)
$$

where $F _ { J }$ and $F _ { R }$ are functions mapping job descriptions and resumes to feature sets. 

Semantic Matching Using Gemini LLM To calculate the similarity score $S$ between a job description $j$ and a resume $r$ , a language model $L$ is employed. The formula is given by: 

$$
S (j, r) = L \left(F _ {J} (j), F _ {R} (r)\right) \tag {2}
$$

where $L$ computes the semantic similarity. 

Ranking and Filtering Resumes are ranked based on similarity scores, where the ranking is performed as follows: 

$$
\operatorname {R a n k} (r) = \operatorname {s o r t} (\{S (j, r) \mid r \in R \}, \text {d e s c e n d i n g}) \tag {3}
$$

The top 3 resumes are selected using: 

$$
R _ {\text {s e l e c t e d}} = \left\{r _ {1}, r _ {2}, r _ {3} \right\} \subseteq R \tag {4}
$$

Automated Communication For each selected resume $r _ { i }$ , the system generates an automated response $C$ using the formula: 

$$
C \left(r _ {i}\right) = \text {G e n e r a t e R e s p o n s e} \left(r _ {i}, j\right) \tag {5}
$$

where GenerateResponse is the function responsible for personalized communication. 

Performance Metrics and Benchmarking The performance of MLAR is compared to UiPath and Automation Anywhere. Let $T _ { \mathrm { U i P a t h } }$ , TAutomationAnywhere, and $T _ { \mathrm { M L A R } }$ represent the processing times for the respective systems. The comparison is performed using: 

$$
\Delta T = T _ {\text {B e n c h m a r k}} - T _ {\text {M L A R}} \tag {6}
$$

where $T _ { \mathrm { B e n c h m a r k } }$ is the processing time for UiPath and Automation Anywhere. 

Continuous Operation Loop The system operates continuously by monitoring new inputs. The process is described as: 

While $t \in T$ , perform MLAR process on $\{ J , R \}$ 


Algorithm 1 The MLAR Algorithm


1: Initialize monitoring of the job descriptions $J$ and resumes $R$ 2: while True do  
3: Check for new job descriptions or resumes in $J$ and $R$ 4: if new job description $j \in J$ or resume $r \in R$ is detected then  
5: Parse job description $j$ and resume $r$ to extract feature sets $F_{J}(j)$ and $F_{R}(r)$ 6: Compute similarity score $S(j, r)$ using LLM $L$ 7: Rank resumes based on similarity scores $\text{Rank}(r)$ 8: Select top 3 resumes  
9: for each resume $r_i \in R_{\text{selected}}$ do  
10: Generate personalized response $C(r_i)$ for $j$ 11: Notify job seeker associated with $r_i$ 12: end for  
13: else  
14: Ignore unrelated or invalid inputs  
15: end if  
16: Log all operations and results to the database  
17: end while 

# C. Tools and Dataset

Firstly, the LLM - Gemini, serves as the backbone of the system, enabling advanced natural language processing tasks such as resume parsing and similarity matching. Its ability to extract structured information from unstructured documents like Portable Document Formats (PDFs) and job postings makes it an indispensable component of the system. 

$$
R _ {\text {s e l e c t e d}} = \left\{r _ {1}, r _ {2}, r _ {3} \right\} \subseteq R \tag {4}
$$

![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-07/35bd25bc-cdab-4f78-8362-59f0bc2befcf/09a3299997c6e445f7b4a80bcfbf87f2ce914c3b9fd53b822d8a225e8b231de2.jpg)



Fig. 1: System architecture of the MLAR model. The diagram demonstrates the integration of Large Language Models (LLMs) at various stages of the recruitment process. It starts with job post requests from recruiters (a) and proceeds to LLM-based job description parsing (b). Candidate resumes (c) are parsed using LLMs (d) and stored in a parsed resume database (e). Finally, similarity and ranking are performed by the LLM (f), ensuring accurate matching between job descriptions and candidate profiles.


Secondly, RPA Tools: 

• UiPath’s automation capabilities were utilized to orchestrate the workflow, including file handling and email integration. 

• Automation Anywhere: Similar to UiPath, Automation Anywhere was used to test automation scripts and compare performance metrics. 

• MLAR: This is the custom-built RPA solution integrated with the Gemini API, which demonstrated superior efficiency and performance in processing resumes and job descriptions. 

The Kaggle Resume Dataset was chosen for its diversity, containing 2400 resumes across 24 professions. These are: Human Resources (HR), Designer, Information-Technology, Teacher, Advocate, Business-Development, Healthcare, Fitness, Agriculture, Business process outsourcing (BPO), Sales, Consultant, Digital-Media, Automobile, Chef, Finance, Apparel, Engineering, Accountant, Construction, Public-Relations, Banking, Arts, Aviation. All of the resumes were provided in PDF format. The dataset provided a realistic simulation of large-scale recruitment scenarios [16]. 

# IV. EXPERIMENTAL DESIGN

The flow diagram in Figure 2 provides an overview of the MLAR system’s operational workflow. The process begins with input from HR professionals, where job descriptions are saved into the database, and emails are prepared for notifications. Simultaneously, the system processes candidate resumes, parsing their information (e.g., skills, experience, and education) and saving the structured data into the database. 

Next, the MLAR system performs a similarity matching between the job descriptions and resumes to compute scores 

based on alignment. The resumes are ranked accordingly, and the top-ranked candidates are identified. Finally, automated emails are sent to these candidates, streamlining the recruitment process and ensuring efficient communication. 

The architecture of the MLAR system is centered around automating critical steps in the recruitment process. It optimizes efficiency by integrating RPA with AI-powered tools like LLMs. The system architecture is divided into four main stages: Job Posting, Resume Parsing, Resume Matching, and Candidate Notification, which work cohesively to streamline the workflow. 

Job Posting: This step (represented as part (a) in Figure 1) focuses on processing job descriptions provided by HR professionals. Initially, HR enters the recipient’s email address for sending job postings. The system processes 24 job descriptions stored in a local folder, each representing a unique role across different departments. These job descriptions are then emailed to the specified address. To make the job descriptions machine-readable and ready for downstream tasks, the system leverages the Gemini LLM (part (b) in Figure 1), a state-ofthe-art (SOTA) LLM. The LLM extracts crucial details from each job post, including Job Title, Required Skills, Experience Level, Educational Qualifications, and Additional Preferences if available. 

Resume Parsing: Resume parsing (depicted as part (d) in Figure 1) is a key component of the system’s architecture. The system processes 2400 resumes in PDF format (stored as part (c) in Figure 1), sourced from the Kaggle Resume Dataset, to simulate a high-volume recruitment scenario. Using Gemini LLM, the system extracts fields from each resume, such as candidate name, contact information (email and phone number), professional skills, work experience, educational back-

![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-07/35bd25bc-cdab-4f78-8362-59f0bc2befcf/9caca7796c2c57dff6c29f30a1fc174277040308bfd6ed48c8859820a1ceb1c6.jpg)



Fig. 2: The MLAR flow diagram


ground and predicted department classification. The parsed resumes are stored in a structured manner within the Parsed resumes Database (shown as part (e) in Figure 1). For example, if LLM predicts that a resume belongs to the ”Engineering” category, it is stored in the ”Engineering” department table within the database. This classification ensures that resumes are grouped logically, improving the speed and accuracy of subsequent processes. 

Resume Matching: In this step (represented as part (f) in Figure 1), the system performs a similarity analysis between the parsed resumes and the job descriptions stored in MongoDB. Gemini LLM computes a similarity score between each resume and job description, ranging from 0 to 100. This score quantifies the alignment of the candidate’s qualifications and experience with the job requirements. The results, including similarity scores and rankings, are stored in MongoDB. This 

approach allows the system to identify the most suitable candidates for each job in a data-driven manner, significantly reducing the time and effort required for manual screening. 

Candidate Notification: Finally, the system automates candidate notifications (depicted as part (g) in Figure 1). After identifying the top three candidates for each job posting based on similarity scores, the system generates acceptance emails and sends them to the selected candidates. These emails include key details about the job and instructions for the next steps. This final step ensures that both job seekers and recruiters benefit from a seamless and automated experience, completing the overall workflow. 

# V. RESULTS AND DISCUSSION

The total time taken and time per resume for processing 2,400 resumes across UiPath, Automation Anywhere, and MLAR are summarized in Table 1: 

<table><tr><td>System</td><td>Total Time Taken (seconds)</td><td>Time Per Resume (seconds)</td></tr><tr><td>UiPath</td><td>15,258</td><td>6.45</td></tr><tr><td>Automation Anywhere</td><td>15,350</td><td>6.50</td></tr><tr><td>MLAR (Proposed system)</td><td>12,414</td><td>5.25</td></tr></table>


TABLE I: Comparison of average automation speed between UiPath, Automation Anywhere, and MLAR for job posting, parsing, matching, and email-sending tasks.


The data show that MLAR was the most efficient system, completing all tasks (job posting, resume parsing, resume matching, and email notifications) in 12,414 seconds, averaging 5.25 seconds per resume. By comparison: UiPath required 15,258 seconds, or 6.45 seconds per resume, making it 22.8 $\%$ slower than MLAR. Furthermore, Automation Anywhere took 15,350 seconds, or 6.50 seconds per resume, performing slightly worse than UiPath and $2 3 . 6 ~ \%$ slower than MLAR. 

Although the same Python scripts were used for all three systems, differences in execution speed can be attributed to how each platform manages external scripts and orchestrates processes, for example, UiPath is optimized for automation workflows; not running external Python scripts involves additional orchestration overhead, such as initializing environments, managing dependencies, and handling inter-process communication. This slightly increases execution time for compute-intensive tasks like resume parsing and matching. Moreover, Automation Anywhere introduces even greater latency, likely due to its reliance on cloud-based architecture for script execution. Although this makes it versatile for distributed workflows, it adds noticeable delays when processing large datasets such as 2,400 resumes. 

MLAR bypasses these orchestration layers by running scripts directly in Python, resulting in faster initialization and execution. This advantage is particularly evident in highvolume scenarios where the elimination of overhead translates to significant time savings. 

The time differences may seem marginal per resume, but they become significant when scaled to large datasets, MLAR 

saves 2,844 seconds (47.4 minutes) compared to UiPath and 2,936 seconds (48.9 minutes) compared to Automation Anywhere. This time savings can be critical for real-world recruitment workflows, where speed directly impacts the ability to shortlist and contact candidates quickly, particularly in competitive hiring scenarios. 

Although UiPath and Automation Anywhere are robust and versatile tools, their reliance on additional orchestration layers introduces inefficiencies when handling large-scale data processing. In contrast, MLAR’s direct execution model demonstrates superior performance, making it an optimal choice for automation scenarios that prioritize speed and scalability. 

# A. Future Work

The MLAR system achieved an accuracy of $6 3 . 4 5 \%$ and a precision of $7 4 . 2 4 \%$ in matching candidates with job requirements, laying a solid foundation for automated recruitment workflows. Although, the system demonstrates promising results, there is significant potential for improvement in future iterations. 

The primary area for improvement involves the use of different fine-tuned LLMs specifically trained on recruitment datasets. By fine-tuning these local LLMs to better understand the relationships between job descriptions and resumes, the system can significantly improve its prediction accuracy. 

# VI. CONCLUSION

The integration of RPA with advanced AI tools such as LLMs has transformed recruitment automation, as demonstrated by the MLAR system. Our study shows that MLAR significantly improves efficiency, processing resumes in 5.25 seconds on average—faster than UiPath (6.45s) and Automation Anywhere (6.5s). This performance gain is due to MLAR’s seamless Gemini LLM integration and optimized data operations. 

MLAR establishes a new benchmark for recruitment automation by reducing processing time and enhancing accuracy. Future work may focus on integrating additional datasets, refining LLM models, and incorporating features like interview scheduling and advanced applicant tracking. This study highlights the potential of AI-driven automation to optimize talent acquisition workflows efficiently. 

# REFERENCES



[1] S. Laumer, C. Maier, and A. Eckhardt, “The impact of business process management and applicant tracking systems on recruiting process performance: an empirical study,” Journal of Business Economics, vol. 85, pp. 421–453, 2015. 





[2] S. Balasundaram and S. Venkatagiri, “A structured approach to implementing robotic process automation in hr,” Journal of Physics: Conference Series, vol. 1427, no. 1, p. 012008, jan 2020. [Online]. Available: https://dx.doi.org/10.1088/1742-6596/1427/1/012008 





[3] N. Nawaz, “Robotic process automation for recruitment process,” International Journal of Advanced Research in Engineering and Technology (IJARET), vol. 10, no. 2, pp. 608–611, March-April 2019. 





[4] S. Wang, P. Patel, A. Dubey, and A. Jakubik, “A survey on hr process automation: Trends, technologies, and future directions,” IEEE Transactions on Automation Science and Engineering, vol. 20, no. 2, pp. 689–701, 2023. 





[5] N. Roopesh and C. N. Babu, “Robotic process automation for resume processing system,” in 2021 International Conference on Recent Trends on Electronics, Information, Communication and Technology (RTEICT), 2021, pp. 180–184. 





[6] E. Abdollahnejad, M. Kalman, and B. H. Far, “A deep learning bertbased approach to person-job fit in talent recruitment,” in 2021 International Conference on Computational Science and Computational Intelligence (CSCI), 2021, pp. 98–104. 





[7] G. Vagale, S. Y. Bhat, P. P. P. Dharishini, and P. GK, “Prospectcv: Llm-based advanced cv-jd evaluation platform,” in 2024 IEEE Students Conference on Engineering and Systems (SCES), 2024, pp. 1–6. 





[8] L. Patr´ıcio, L. Varela, and Z. Silveira, “Integration of artificial intelligence and robotic process automation: Literature review and proposal for a sustainable model,” Applied Sciences, vol. 14, no. 21, 2024. [Online]. Available: https://www.mdpi.com/2076- 3417/14/21/9648 





[9] L. Schaudt and D. Schlegel, “Combining robotic process automation with artificial intelligence: Applications, terminology, benefits, and challenges,” in Eurasian Business and Economics Perspectives, M. Bilgin, H. Danis, E. Demir, L. Wincenciak, and S. T. Er, Eds. Cham: Springer Nature Switzerland, 2023, pp. 83–99. 





[10] P. Mishra, R. Kumar, and Y. Chen, “Automated applicant ranking using hybrid nlp and machine learning techniques,” in 2021 IEEE 15th International Conference on Semantic Computing (ICSC), 2021, pp. 145–152. 





[11] L. Bajzikova and T. Smerdova, Improving the Recruitment Process in Multinational Organizations Using Robotic Process Automation and Artificial Intelligence. Cham: Springer Nature Switzerland, 2024, pp. 29–60. 





[12] H. Sun, H. Lin, H. Yan, C. Zhu, Y. Song, X. Gao, S. Shang, and R. Yan, “Facilitating multi-role and multi-behavior collaboration of large language models for online job seeking and recruiting,” 2024. [Online]. Available: https://arxiv.org/abs/2405.18113 





[13] Y. Lin, J. Bose, and R. Narkhede, “Explainable rpa in hr: Integrating xai methods to enhance transparency in automated talent acquisition,” Expert Systems with Applications, vol. 216, p. 119451, 2023. 





[14] J. Zhang, C. Martin, and D. Ray, “Ats 2.0: Leveraging large language models for bias mitigation in automated hiring,” in 2024 IEEE International Conference on Computational Intelligence in Data Science (CIDS), 2024, pp. 233–240. 





[15] R. Syed, S. Suriadi, M. Adams, W. Bandara, S. J. Leemans, C. Ouyang, A. H. ter Hofstede, I. van de Weerd, M. T. Wynn, and H. A. Reijers, “Robotic process automation: Contemporary themes and challenges,” Computers in Industry, vol. 115, p. 103162, 2020. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0166361519304609 





[16] S. Anbhawal, “Resume dataset,” 2021, accessed: November 30, 2024. [Online]. Available: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset 





[17] C. Gan, Q. Zhang, and T. Mori, “Application of llm agents in recruitment: A novel framework for resume screening,” 2024. [Online]. Available: https://arxiv.org/abs/2401.08315 





[18] C. Almada and O. Jerez, “Semantic matching of resumes and job descriptions using large-scale generative pre-trained transformers,” IEEE Access, vol. 11, pp. 114 567–114 581, 2023. 





[19] UiPath, “Uipath - automation platform for rpa,” 2024, accessed: 2024-11-30. [Online]. Available: https://www.uipath.com/ 





[20] A. Anywhere, “Automation anywhere - rpa software used for ats,” 2024, accessed: 2024-11-30. [Online]. Available: https://www.automationanywhere.com/ 





[21] H. Leopold, H. van der Aa, and H. A. Reijers, “Identifying candidate tasks for robotic process automation in textual process descriptions,” in Enterprise, Business-Process and Information Systems Modeling, J. Gulden, I. Reinhartz-Berger, R. Schmidt, S. Guerreiro, W. Guedria, ´ and P. Bera, Eds. Cham: Springer International Publishing, 2018, pp. 67–81. 

