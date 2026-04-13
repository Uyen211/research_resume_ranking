# AI Hiring with LLMs: A Context-Aware and Explainable Multi-Agent Framework for Resume Screening

Frank P.-W. Lo1 Jianing Qiu2 Zeyu Wang1 Haibao Yu3 Yeming Chen4 Gao Zhang5 Benny Lo1 

1Imperial College London 2The Chinese University of Hong Kong 3The University of Hong Kong 4Wedon Education Technologies 5Brest Business School 

{po.lo15, zeyu.wang20, benny.lo}@imperial.ac.uk, jianingqiu@cuhk.edu.hk, yuhaibao94@gmail.com, chenym@wedon.com, gao.zhang@brest-bs.com 

# Abstract

Resume screening is a critical yet time-intensive process in talent acquisition, requiring recruiters to analyze vast volume of job applications while remaining objective, accurate, and fair. With the advancements in Large Language Models (LLMs), their reasoning capabilities and extensive knowledge bases demonstrate new opportunities to streamline and automate recruitment workflows. In this work, we propose a multi-agent framework for resume screening using LLMs to systematically process and evaluate resumes. The framework consists of four core agents, including a resume extractor, an evaluator, a summarizer, and a score formatter. To enhance the contextual relevance of candidate assessments, we integrate Retrieval-Augmented Generation (RAG) within the resume evaluator, allowing incorporation of external knowledge sources, such as industry-specific expertise, professional certifications, university rankings, and company-specific hiring criteria. This dynamic adaptation enables personalized recruitment, bridging the gap between AI automation and talent acquisition. We assess the effectiveness of our approach by comparing AI-generated scores with ratings provided by HR professionals on a dataset of anonymized online resumes. The findings highlight the potential of multi-agent RAG-LLM systems in automating resume screening, enabling more efficient and scalable hiring workflows. 

# 1. Introduction

Automated resume screening is a critical component of the hiring process. Companies often receive a high volume of job applications, making it difficult to manually review every resume or CV efficiently. Traditional resume screening methods primarily rely on rule-based approaches, and key-

![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-07/39844859-0744-47b7-9a58-2eee9b7c27da/7912d513d5cd25f1bdde060c3c9d0976e8e01723b6899037f7a0a515e4e25e22.jpg)



Figure 1. Illustration diagram of fine-tuned LLM and RAG-LLM for resume screening. (a) Traditional fine-tuning approaches (e.g., LoRA) require updating model parameters to adapt to new tasks (i.e., new companies’ hiring requirements). (b) Our model uses RAG, eliminating the need for fine-tuning by dynamically retrieving relevant information from external sources.


word matching, which often fail to include job-specific requirements and lack adaptability. In addition, such methods provide limited transparency and feedback, making it difficult for recruiters to interpret and validate AI-driven decisions. Traditional methods also face several technical challenges, including difficulties in comprehending the nuanced choice of words in a resume and accurately interpreting the syntax of unstructured written language [1]. Most importantly, resume screening systems are expected to keep up with the constantly changing job market and business needs. Therefore, models need to be updated frequently as new job opportunities emerge. For instance, a recommendation that was relevant last month might become obsolete if the job market shifts, such as due to a sudden surge in demand for specific skills. Hence, the integration of real-time data and 

continuous learning is still a key focus of ongoing research. 

Recent advancements in LLMs have demonstrated remarkable reasoning capabilities [7], enabling new possibilities for intelligent resume screening. However, most existing LLM-driven screening systems operate as monolithic models [8], where resume parsing, evaluation, and feedback generation are handled in a single-step process (i.e., single LLM). The major drawback of single LLM approaches is their lack of modularity. Since resume extraction, evaluation, and feedback generation are coupled in a single model call, modifying the scoring logic requires retraining or finetuning the entire model (e.g., using Low-Rank Adaptation (LoRA)) as shown in Figure 1(a). This makes it difficult to adapt screening criteria across different industries and job roles, reducing overall scalability1. Additionally, when multiple reasoning steps (e.g., extracting information from resume, applying scoring criteria, and justifying decisions) are handled simultaneously, it becomes difficult to interpret the decision-making process. This lack of transparency limits recruiters’ ability to validate AI-driven evaluations and adjust the system without extensive reconfiguration. 

To address these challenges, we propose a multi-agent framework for resume screening, leveraging Retrieval-Augmented Generation enhanced LLMs (RAG-LLMs) [9] within an agentic architecture [10]. Unlike single-step models, our framework consists of four core agents, each responsible for a distinct function: resume extraction (hiring assistant agent), evaluation (hiring manager agent), summarization (hiring coordinator agent), and score formatting (data curator agent). This modular structure provides greater flexibility, and in our design, the evaluation agent can dynamically retrieve company-specific hiring criteria via RAG. Instead of requiring fine-tuning, the system can adjust its evaluation standards in real-time by allowing HR professionals to upload job requirement documents to the backend, making it highly adaptable across different industries and job roles as shown in Figure 1(b). Moreover, by dividing the screening process into multiple independent agents, the framework enhances transparency and explainability. Each stage of the process remains clearly defined, allowing recruiters to trace how a candidate was assessed and why a particular score was assigned (i.e., instead of outputting a score alone, the evaluation criteria can be inferred from the extracted resume content and the generated feedback, resulting in more meaningful and explainable outcomes). This also ensures that changes in scoring criteria does not interfere with data extraction and feedback generation. By leveraging multi-agent modularity and RAG-based dynamic retrieval, our framework provides a scalable, trans-

parent, and adaptable solution for AI-driven resume screening. Figure 2 illustrates how AI-driven hiring technologies have evolved to address other challenges as well. The contributions of this paper are summarized as follows: 

• We propose a multi-agent architecture that introduces a modular structure, enhancing explainability and transparency in resume screening. 

• Our framework is designed to adapt to diverse hiring criteria across different roles (e.g., leadership skills for department directors, HR expertise for human resource associates), enabling a more context-aware and roleadaptive screening process. 

• By integrating RAG, our system allows recruiters to dynamically adjust screening parameters (e.g., prioritizing specific university rankings, certifications, or domain expertise) without requiring LLM retraining/fine-tuning, thereby enhancing adaptability and customization. 

• We discuss the future of AI in hiring, addressing ethical considerations, bias mitigation, and regulatory challenges, while also examining how LLMs can enhance fairness and efficiency in recruitment. 

# 2. Related Work

# 2.1. AI-driven hiring

The adoption of AI in hiring has significantly transformed recruitment processes, enabling automation in resume screening [11], resume classification [12–19], resume ranking [20, 21], interview evaluation [22–25], salary prediction [26, 27], and also bias mitigation [28–31]. With the emergence of ML, DL, and LLMs, AI-driven hiring systems have evolved from simple keyword-based matching to context-aware decision-making. 

# 2.2. Resume screening systems

Early AI-driven resume screening systems primarily relied on traditional machine learning methods, such as Bag-of-Words (BoW), Support Vector Machines (SVM), and Random Forests (RF) [12]. These methods treated resumes as structured data, applying rule-based decision-making to assess candidate qualifications. However, these models lacked semantic understanding and relied solely on keyword matching (e.g., failing to recognize that software developer is equivalent to software engineer), leading to high error rates in candidate selection. The transition from traditional machine learning to deep learning marked a significant shift in resume screening, enabling models to process sequential and semantic text information. Convolutional Neural Networks (CNNs), Recurrent Neural Networks (RNNs) and Long Short-Term Memory (LSTMs) [15] were among the first deep learning models applied to resume screening, improving accuracy by capturing sequential dependencies in text data. Further advancements in-

![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-07/39844859-0744-47b7-9a58-2eee9b7c27da/79ca26988e8b6122b38d6826c5c52a731838c7ef6a9b83ccd289521c2912a9d8.jpg)



Figure 2. The evolution of AI-driven hiring technologies. This figure presents the transition of AI-driven hiring methods across three major eras: traditional machine learning (2010-2016), deep learning (2016-2022), and large language models (2022-present). It highlights key advancements in AI hiring technologies and notable case studies demonstrating their real-world applications [2–6].


troduced word embeddings (e.g., Word2Vec [32]), which replaced keyword matching with semantic similarity, allowing AI to recognize that terms like software engineer and software developer are contextually related. However, these embeddings are context-independent. More recently, transformer-based models (e.g., BERT [33]) introduced context-aware text understanding, enabling AI to assess resume relevance in full-sentence representations rather than isolated keywords. While deep learning improved resume parsing, job matching, and ranking, these models required large-scale labeled data for training, limiting their adaptability across diverse hiring contexts. The advancements of LLMs have transformed AI-driven resume screening, enabling zero-shot and few-shot learning to assess candidates without extensive labeled training data. Unlike traditional machine learning and early deep learning models, LLMs could leverage large-scale pre-training to extract key resume attributes, analyze job relevance, and infer contextual qualifications dynamically. Prior advancements, such as Word2Vec and BERT, already improved semantic resumejob matching, reducing reliance on exact keyword matches. However, LLMs further enhance contextual reasoning, allowing for deeper candidate evaluation, such as identifying transferable skills (i.e., recognizing transferable skills such as proficiency in $\mathrm { C } { + } { + }$ from experience with embedded systems or Python from data analysis projects, even if not explicitly stated in the resume) and inferring implicit qualifications. Nevertheless, there are limited studies on applying LLMs to resume screening [11, 34, 35], and key challenges 

remain. For instances, LLMs rely on static pretraining data, restricting their ability to adapt to dynamic hiring criteria and evolving job requirements as mentioned. 

# 2.3. LLMs with RAG

RAG has been widely explored in fields like customer support [36], legal research [37], medicine [38, 39], finance [40], and education [41, 42], enhancing LLMs by integrating real-time, domain-specific information retrieval. It improves accuracy, reduces hallucinations, and enables context-aware decision-making [43]. However, its application in resume screening remains limited, with most AI resume screening systems relying on static embeddings or rule-based models. Exploring RAG-enhanced resume screening could improve hiring procedure by integrating real-time labor market data and hiring trends, offering a more adaptive and intelligent screening process. 

# 3. Problem Definition

Our framework enables dynamic, context-aware resume screening by adapting evaluation scores based on the applied job role. Unlike traditional models with fixed evaluation scores, our framework assesses candidates using rolespecific standards. Given a resume $R$ , the model generates a score vector: 

$$
S ^ {J} = \left\{S _ {S} ^ {J}, S _ {K} ^ {J}, S _ {W} ^ {J}, S _ {B} ^ {J}, S _ {E} ^ {J} \right\} \tag {1}
$$

![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-07/39844859-0744-47b7-9a58-2eee9b7c27da/f9c17d8f58bb580b42b1586f17c394c1c0fea669f13fe81030c8d902f749ff3a.jpg)



Figure 3. Illustration of the proposed multi-agent framework for resume screening. The framework consists of four core agents: Resume extractor, responsible for parsing and structuring resume content; Resume evaluator, which assigns scores based on predefined criteria while integrating external knowledge via RAG; Resume summarizer, which consists of three sub-agents that generate feedback through collective decision-making, ensuring a comprehensive evaluation of the candidate’s strengths and weaknesses; Score formatter, which organizes evaluation results into a structured format for future analysis. This modular approach enhances explainability and adaptability, as recruiters can review each step of the evaluation process without requiring to examine the raw resume directly.


where $S _ { S } ^ { J }$ refers to the score of self-evaluation, $S _ { K } ^ { J }$ refers to the score of skills & specialties, $S _ { W } ^ { J }$ refers to the score of work experience, $S _ { B } ^ { J }$ refers to the score of basic information, $S _ { E } ^ { J }$ refers to the score of education background and $J$ refers to the applied job position. Each evaluation criterion is assigned a fixed weight across all job roles: 

$$
W = \left\{w _ {S}, w _ {K}, w _ {W}, w _ {B}, w _ {E} \right\}, \quad \sum w _ {i} = 1 \tag {2}
$$

where $w _ { i }$ remains constant regardless of the applied job position. Besides, one of the most challenging aspects of this work is role-specific scoring. A candidate applying for a HR intern versus a HR director should receive different scores, even with the same resume: 

$$
S _ {W} ^ {\text {I n t e r n}} > S _ {W} ^ {\text {D i r e c t o r}} \quad (\text {f o r l o w - e x p i e r i e n c e c a n d i d a t e s}) \tag {3}
$$

Different aspects of evaluation should be interpreted contextually based on job requirements. In our work, the LLM generates job-specific evaluation scores via job applied $J$ : 

$$
S ^ {J} = \operatorname {L L M} (R, J). \tag {4}
$$

The final score for a candidate is computed as: 

$$
S _ {\text {f i n a l}} ^ {J} = \sum w _ {i} S _ {i} ^ {J}, \tag {5}
$$

# 4. Detailed Information and Methodology

The proposed framework streamlines resume screening using a multi-agent approach, where different components work together to analyze and evaluate job applications efficiently. The framework consists of four core agents: the resume extractor, resume evaluator, resume summarizer, and score formatter, each handling a specific task in the process as shown in Figure 3. First, the resume extractor identifies key details from a candidate’s resume. Since resumes come in different formats, this step ensures that all information is structured in a clear and standardized way. Next, the resume evaluator reviews the extracted details and assigns scores based on how well the candidate’s qualifications match the job requirements. The resume summarizer then generates a concise, easy-to-understand report, highlighting the candidate’s strengths and areas for improvement. This helps recruiters quickly assess candidates without going through lengthy resumes. Finally, the score formatter standardizes the evaluation output into a structured numerical format. This ensures consistency in how candidate scores are presented, making it easier to compare applicants and integrate results into decision-making systems. 

# 4.1. Resume extractor agent

The extractor agent, acting as the hiring assistant, leverages reasoning capabilities of LLM to extract structured information from unstructured text accurately, ensuring the precise identification of key details such as the 1) position applied for (i.e., position name and its level: junior, mid-level, senior, or leadership) 2) self-evaluation 3) skills & specialties 4) work experience (i.e., company name, duration, and responsibilities) 5) basic information, and 6) education background. Unlike traditional keyword-based extraction methods, the LLM processes unstructured text with contextual understanding, allowing it to infer missing details, and recognize implicit skills. 

# 4.2. Resume evaluator agent

The evaluator agent, functioning as a hiring manager, assigns scores based on five evaluation categories: selfevaluation (score: 0-1), skills & specialties (score: 0-2), work experience (score: 0-4), basic information (score: 0- 1), and educational background (score: 0-2). Instead of relying solely on predefined rules, the evaluator agent leverages RAG to dynamically retrieve company-specific hiring criteria, job descriptions, and other relevant information from an external source. The details of the RAG pipeline can be structured as follows: 

# 4.2.1. Vector embedding

All document (i.e., external source) chunks are encoded into dense vector representations using an embedding function $f _ { \mathrm { e m b e d } }$ . Let the original job query (e.g., a job requirement) and document chunks be denoted as $q _ { \mathrm { t e x t } }$ and $d _ { i , \mathrm { t e x t } }$ . 

$$
q = f _ {\text {e m b e d}} \left(q _ {\text {t e x t}}\right), \quad d _ {i} = f _ {\text {e m b e d}} \left(d _ {i, \text {t e x t}}\right) \tag {6}
$$

where $q , d _ { i } \in \mathbb { R } ^ { D }$ , and $D$ is the embedding dimension (i.e., we use OpenAIEmbeddings to generate dense vector representations and ChromaDB as the vector database). 

# 4.2.2. Cosine similarity computation

The relevance of document chunks to the query is quantified using cosine similarity. For the query $q$ and the $i$ -th document chunk $d _ { i }$ : 

$$
\operatorname {s i m} (q, d _ {i}) = \frac {q \cdot d _ {i}}{\| q \| \| d _ {i} \|} \tag {7}
$$

where $\sin ( q , d _ { i } )$ is the similarity between the vectors, with higher values indicating greater relevance. A relevance threshold $\tau = 0 . 3$ is used to filter out low-relevance document chunks: 

$$
\operatorname {s i m} (q, d _ {i}) \geq \tau \iff \text {R e t r i e v e} d _ {i} \tag {8}
$$

where $q$ refers to the query and $d _ { i }$ refers to the document chunks. 

Query Q:Score the extracted resume details，ensuring skills,work experience，and education are evaluated based on their relevance to the [Applied job J].Specific job-wise scoring requirement as follows:[Retrieved chunks C] 

Figure 4. Query formulation for resume evaluation agent. The query instructs the system to score extracted resume details by assessing skills, work experience, and education in relation to the applied job (J). It incorporates retrieved knowledge chunks (C) to ensure job-specific scoring criteria are considered. 

# 4.2.3. Contextual prompt construction

Retrieved chunks are formatted into a structured input prompt $P$ as follows: 

$$
P = \operatorname {c o n c a t} (Q, J, C) \tag {9}
$$

$$
C = d _ {1} ^ {(\text {r e t r i e v e d})} \cup d _ {2} ^ {(\text {r e t r i e v e d})} \cup \dots \cup d _ {i} ^ {(\text {r e t r i e v e d})} \tag {10}
$$

where $C$ is the concatenation of the retrieved document chunks, $Q$ represents the query text, and $J$ denotes the applied job position. The formatted prompt $P$ serves as the input to the evaluator agent, which processes the structured information to assess the candidate’s background against predefined job-specific criteria and assigns a resume score accordingly as shown in Figure 4. 

# 4.2.4. Specific requirements from external sources

In addition to structured attributes such as university rankings and professional certifications, we further analyze historical resumes of outstanding candidates and incorporate up-to-date skill demands to refine job-specific requirements. By leveraging LLM-driven summarization, we extract key qualifications, skills, and experience patterns from past hires, establishing a dynamic baseline for evaluating different job positions. This approach ensures that screening criteria remain relevant and adaptive to evolving industry needs. 

# 4.3. Resume summarizer agent

The summarizer agent functions as an hiring coordinator, generating personalized resume feedback by analyzing a candidate’s profile against job requirements. It consists of three sub-agents including the CEO agent, CTO agent, and HR agent, which engage in an internal discussion to refine the feedback based on the scores provided by the evaluator agent. The CEO agent assesses leadership potential, the CTO agent evaluates technical expertise, and the HR agent focuses on soft skills and cultural fit. Through collaborative reasoning, these sub-agents exchange insights, debate strengths and weaknesses, and produce structured feedback. This multi-agent approach ensures context-aware, balanced, and actionable recommendations, enhancing the adaptability and explainability of AI-driven resume evaluations. 


Table 1. Comparison of single LLMs and the multi-agent RAG-LLMs with different LLM backbones


<table><tr><td></td><td>Model</td><td>PC20↑*</td><td>SC20↑</td><td>PC15↑</td><td>SC15↑</td><td>PC10↑</td><td>SC10↑</td><td>MAE↓</td></tr><tr><td rowspan="2">Single LLM</td><td>GPT-4o</td><td>0.67</td><td>0.59</td><td>0.69</td><td>0.62</td><td>0.74</td><td>0.65</td><td>1.26</td></tr><tr><td>DeepSeek-V3</td><td>0.67</td><td>0.60</td><td>0.67</td><td>0.62</td><td>0.70</td><td>0.71</td><td>1.08</td></tr><tr><td rowspan="2">RAG-LLM (ours)</td><td>GPT-4o</td><td>0.69</td><td>0.66</td><td>0.72</td><td>0.70</td><td>0.80</td><td>0.74</td><td>1.05</td></tr><tr><td>DeepSeek-V3</td><td>0.70</td><td>0.66</td><td>0.75</td><td>0.69</td><td>0.84</td><td>0.74</td><td>0.90</td></tr></table>


*↑ indicates that higher values are better, while $\downarrow$ indicates that lower values are better. PC refers to Pearson Correlation, and SC refers to Spearman Correlation. MAE refers to Mean Absolute Error. The number following PC/SC represents the percentage of scores used in the evaluation. For example, $\mathrm { P C _ { 1 0 } }$ evaluates model performance only on the subset of candidates whose ground truth scores lie in the top and bottom $10 \%$ percentiles. 



Table 2. Ablation study of multi-agent RAG-LLMs with and without resume extraction agent


<table><tr><td></td><td>Model</td><td>PC20</td><td>SC20</td><td>PC15</td><td>SC15</td><td>PC10</td><td>SC10</td></tr><tr><td>RAG-LLM</td><td>GPT-4o</td><td>0.63</td><td>0.66</td><td>0.70</td><td>0.71</td><td>0.81</td><td>0.74</td></tr><tr><td>w/o extract.</td><td>DS-V3</td><td>0.65</td><td>0.63</td><td>0.69</td><td>0.68</td><td>0.80</td><td>0.79</td></tr><tr><td>RAG-LLM</td><td>GPT-4o</td><td>0.69</td><td>0.66</td><td>0.72</td><td>0.70</td><td>0.80</td><td>0.74</td></tr><tr><td>w/ extract.</td><td>DS-V3</td><td>0.70</td><td>0.66</td><td>0.75</td><td>0.69</td><td>0.84</td><td>0.74</td></tr></table>


*DS-V3 refers to DeepSeek-V3 


# 4.4. Score formatter agent

The score formatter agent (i.e., acting as the data curator) standardizes the output of candidate evaluations into a structured format (e.g., [1.0, 1.5, 3.5, 0.8, 1.5]), ensuring consistency across different assessment components. It takes raw scores generated by various evaluation agents (e.g., experience, skills, education) and converts them into a uniform numerical array for downstream processing. This structured output enables easy integration with ranking models and decision-making pipelines. 

# 5. Experimental Results

Our LLM-driven resume screening system is implemented using CrewAI, which coordinates multiple AI agents to enable structured and automated resume evaluation. The framework runs on a PC equipped with an NVIDIA A6000 GPU, ensuring efficient processing of large-scale resume data. It integrates LLMs via the OpenRouter API, utilizing models such as DeepSeek-V3, and GPT-4o, with LangChain facilitating seamless interaction between components. For RAG, the system employs ChromaDB as a vector database for efficient semantic search, enabling retrieval of relevant hiring criteria and context-aware job matching. Additionally, OpenAI embeddings are used to generate dense vector representations, enhancing the accuracy of similarity-based retrieval. Note that for users requiring local implementation due to privacy concerns, Ollama can be integrated to facilitate the local execution of LLMs. 

# 5.1. Dataset

We evaluated our model on a dataset consisting of 105 fully anonymized online resumes. The dataset was labeled by HR professionals, who assigned scores based on five key 

aspects: self-evaluation, skills & specialties, work experience, basic information, and education. To ensure privacy, all personally identifiable information, including names and company names, was removed. The resumes in the dataset correspond to various job positions, primarily in the field of human resources. The job levels can be categorized into four groups: junior, mid-level, senior, and leadership. The junior-level positions include HR intern and HR assistant, while the mid-level roles consist of HR associate and HR specialist. Senior-level positions include HR manager and senior HR, whereas leadership roles encompass HR director and strategic HR partner. 

# 5.2. Evaluation metrics

To evaluate our proposed resume screening system, we employ the following evaluation metrics: a) Pearson correlation measures the linear relationship between the AIestimated scores and the human reviewer scores. This metric helps evaluate if the AI system assigns scores in a manner similar to human evaluators b) Spearman correlation assesses the rank-based monotonic relationship between AI and human reviewer scores. Unlike Pearson correlation, it captures non-linear relationships by ranking the scores before computing the correlation c) MAE measures the absolute difference between AI predictions and HR scores, capturing the average magnitude of errors. This metric is particularly useful in understanding the extent of AI’s deviation from human judgment. 

# 5.3. Performance of multi-agent RAG-LLMs

# 5.3.1. Comparison with single model approaches

To evaluate the effectiveness of the proposed multi-agent RAG-LLMs, we first compare their performance against single LLMs across multiple evaluation metrics. Table 1 presents results using different LLM backbones, including GPT-4o and DeepSeek-V3. The results demonstrate that our proposed RAG-LLM framework achieves satisfactory performance and consistently outperforms single LLMs, confirming its robustness and reliability in AI-driven resume screening. Our evaluation focuses on candidates whose ground truth scores fall within the top and bottom $10 \%$ , $1 5 \%$ , and $20 \%$ percentiles, enabling a more nuanced analysis of ranking performance under varying se-

![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-07/39844859-0744-47b7-9a58-2eee9b7c27da/41870779604e9362cab3289d92f69f2283b5255a89f700f00301374426da8ab7.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-07/39844859-0744-47b7-9a58-2eee9b7c27da/0b42416ca5c130856bb0809a5af48aa78e8172d9a37b3f32f250fec014fdb2cb.jpg)



Figure 5. Comparison of candidate scores assigned by human evaluators (HR) and a RAG-LLM (DeepSeek-V3). (a) The scatter plot showing the distribution of scores (b) Histogram showing the number of candidates in each score range based on HR and LLM evaluations.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-04-07/39844859-0744-47b7-9a58-2eee9b7c27da/544bb0132e4f7f3af624e53ca9e9650c19d18ec39a50bd640c7f6dfda883140e.jpg)



Figure 6. Comparison of candidate scores estimated by human evaluators (HR) and RAG-LLM (DeepSeek-V3) across different resume attributes. The scatter plot visualizes the distribution of scores across five main categories.


lection thresholds. As shown in Table 1, our RAG-LLM with DeepSeek-V3 achieves the highest Pearson correlation $( P C _ { 1 0 } = 0 . 8 4 $ , $p$ -value $< ~ 0 . 0 0 1$ ), Spearman correlation $S C _ { 1 0 } = 0 . 7 4$ , $p$ -value $< 0 . 0 0 1 $ ), and lowest MAE (0.90), outperforming single LLM baselines. Similar trends persist across the $15 \%$ and $20 \%$ thresholds, highlighting RAG-LLM’s consistent ability to accurately differentiate top-tier candidates from lower-performing ones, ensuring stable and reliable assessments. For borderline candidates, discrepan-

cies between human evaluations and LLM predictions may arise due to subjective judgment, but such variations are expected and fall within a reasonable margin. 

# 5.3.2. Evaluating the impact of extraction agent

We further conducted an ablation study to assess the impact of the resume extraction agent, as presented in Table 2. The results show that incorporating structured extraction consistently improves Pearson correlation (PC) and Spearman correlation (SC) across all evaluation thresholds, with DeepSeek-V3 achieving the highest performance when using the extraction module. These findings highlight the importance of high-quality structured resume parsing in enhancing LLM-based candidate evaluations. 

# 5.3.3. Comparison of AI and human resume screening

To assess the alignment between human evaluators (HR) and the RAG-LLM model, we analyze the score distributions of both systems. Figure 5(a) presents a scatter plot comparing candidate scores assigned by HR and RAG-LLM (DeepSeek-V3), where the mean scores remain close (i.e., 7.68 for HR vs. 7.76 for LLM), indicating high agreement. Figure 5(b) further illustrates this distribution through a histogram, showing that the number of candidates in each score range follows a similar pattern between HR and LLM. These results suggest that RAG-LLM not only achieves strong correlation with human evaluations but also maintains score distribution consistency, reinforcing its reliability for AI-driven hiring applications. Besides, we evaluate the alignment between HR and RAG-LLM assessments across different resume attributes, as shown in Figure 6, which compares the score distributions for self-evaluation, skills & specialties, work experience, basic information, and education background. 

# 5.4. Qualitative analysis of feedback system

As shown in Figure 7 , the summarizer agent consolidates insights from multiple sub-agents, allowing for traceable evaluations. This process reduces recruiter workload by highlighting key strengths and pinpointing missing competencies, eliminating the need for manual resume reviews. Additionally, the system dynamically adapts feedback to different job roles, ensuring that recommendations align with position-specific requirements. To further improve usability, these insights can even be presented in bullet points that summarize strengths and weaknesses, allowing recruiters to efficiently compare multiple candidates. 

# 6. Discussion

With the advancement of LLMs and multi-agent systems, AI-driven resume screening has become more effective and reliable than ever. Our study demonstrates that a multiagent approach offers several advantages over traditional 

Example 1:Your resume demonstrates a strong foundation in HR administration and customer service,with a clear focus on organizational and communication skills.However，to better align with the [DIRECTV HR Recruiter/Administration] role, consider emphasizing quantifiable achievements,such as the number of candidates recruited or efficiency improvements in processes.Tailor your skills section to highlight HRspecific competencies like conflict resolution,employee onboarding，and compliance management.Additionally，expand on your education by showcasing relevant certifications or training in HR or recruitment.Lastly，ensure consistency in formatting and remove redundant skills to create a more concise and impactful resume. 

Example 2:Your resume demonstrates strong experience in HR and leadership，particularly in employee engagement，talent management，and organizational design.However，it could benefit from more concise and targeted language to align with the [HR Business Partner II] role.Focus on quantifiable achievements，such as specific improvements in employee retention，engagement scores，or project outcomes.Streamline the skills section by removing less relevant entries (e.g. "nursing," "driving"） and emphasizing HR-specific competencies.Additionally，clarify overlapping education entries and ensure consistency in formatting.Tailoring your resume to highlight measurable impacts and HR expertise will make it more compelling for mid-level HR roles. 

Figure 7. Qualitative analysis of resume screening feedback. Targeted recommendations generated by the summarizer agent after internal discussion among multiple sub-agents (i.e., CEO, CTO, HR agent). 

single deep learning models or single LLM-driven screening, particularly in terms of explainability, decision efficiency, and evaluation reliability. One of the most notable findings is that the modular architecture of our system potentially enhances transparency and explainability in AIdriven resume screening. Unlike single model approaches, where recruiters receive only a final score without insight into the reasoning process, our system decomposes resume evaluation into multiple specialized agents. This modularity allows for step-by-step tracking of how each extracted information contributes to the final assessment, improving overall decision accountability. Furthermore, our study highlights an important technical consideration. The extraction agent has a measurable impact on the assessment quality. Specifically, we found that extraction can enhance evaluation by structuring the input data more effectively. However, its effectiveness depends on the model’s reasoning ability, particularly in determining what information should be extracted. Models with stronger reasoning capabilities and a larger number of parameters tend to perform better in this step. This suggests that model selection is crucial, especially in systems where the quality of extraction directly influences the reliability of post-extraction evaluation. 

# 7. Future Work

In future work, the integration of multimodal data in LLMdriven hiring has great potential. Current LLM-driven hiring systems mainly focus on text-based resume evaluation, limiting the assessment of soft skills and communication abilities. Incorporating LLM-driven video interview analysis alongside textual evaluation could further provide a more comprehensive assessment of candidate suitability. The system may also generate suitable aptitude and attitude tests to validate a candidate’s actual capabilities (i.e., to verify whether the individual can truly perform the skills or tasks they claim to possess). Apart from this, bias in AI-driven hiring remains a critical concern due to imbalanced training data (e.g., certain demographic groups are underrepresented in the dataset). RAG presents a potential solution by enabling the dynamic retrieval of diverse 

and up-to-date hiring criteria, reducing reliance on static, historically biased datasets. Future work should explore bias-aware retrieval mechanisms and ranking strategies to enhance the equity and transparency of automated evaluations. Last, privacy considerations in AI-driven hiring remain a critical area for future research, especially as LLMs inference APIs become integral to downstream applications. While external APIs enhance model effectiveness, they also introduce risks of exposing sensitive data to thirdparty providers. Companies with sufficient computational resources may opt for local LLM deployment to reduce these risks. The future of AI-driven hiring will likely focus on privacy-preserving architectures that enable API-based inference while ensuring compliance with data protection regulations (e.g., GDPR, CCPA). End-to-end encrypted inference techniques, enabling LLMs to compute without directly accessing sensitive data, along with Model Context Protocol (MCP) for structured data flow and context management, are emerging as key research directions. Their integration is expected to play a crucial role in developing secure, scalable, and legally compliant AI-driven hiring systems in the future. 

# 8. Conclusion

In this work, we proposed a multi-agent framework for resume screening using RAG-LLMs. The framework is designed with four core agents that work together to extract key resume information, evaluate candidates based on predefined scoring criteria, generate a concise evaluation summary, and format the output in a structured manner. By leveraging RAG, the system can assess resumes against company-specific scoring criteria in a context-aware and tailored manner without requiring model retraining or finetuning. To evaluate the effectiveness of our approach, we tested the model using online resume datasets and compared its performance against HR evaluations. The results demonstrated that our proposed framework achieved comparable performance to human evaluators, highlighting the potential of LLMs as an alternative solution for automated and scalable AI hiring. 

# References



[1] Arvind Kumar Sinha, Md Amir Khusru Akhtar, and Ashwani Kumar. Resume screening using natural language processing and machine learning: A systematic review. Machine Learning and Information Processing: Proceedings of ICM-LIP 2020, pages 207–214, 2021. 1 





[2] LinkedIn Corporate Communications. Linkedin to acquire bright, 2014. URL https://news.linkedin.com/ 2014/02/linkedin- to- acquire- bright. Accessed: 2023-03-14. 3 





[3] Forbes. Checkr — company overview & news, 2024. URL https : / / www . forbes . com / companies / checkr/. Accessed: 2025-03-14. 





[4] Forbes. Recruiters and job candidates love talking with this ai assistant, 2019. URL https://www.forbes. com/sites/sap/2019/08/06/recruiters-andjob- candidates- love- talking- with- thisai-assistant/. Accessed: 2025-03-14. 





[5] Google Cloud. Google introduces hire, a new recruiting app that integrates with g suite, 2017. URL https:// cloud.google.com/blog/products/g-suite/ google- introduces- hire- new- recruitingapp-integrates-g-suite. Accessed: 2025-03-14. 





[6] Ms Swati Samadhiya and Archana Awasthi. Importance of artificial intelligence in hiring and recruitment process. of the Book: A Flourishing Digital Era: Innovations in Industry, Education, 1(1):524, 2022. 3 





[7] Jiankai Sun, Chuanyang Zheng, Enze Xie, Zhengying Liu, Ruihang Chu, Jianing Qiu, Jiaqi Xu, Mingyu Ding, Hongyang Li, Mengzhe Geng, et al. A survey of reasoning with foundation models. arXiv preprint arXiv:2312.11562, 2023. 2 





[8] Daniel-Costel Bouleanu, Marco Alfredo Loaiza Carrillo, Costin Badic ˘ a, Raffaele Gravina, and Giancarlo Fortino. ˘ Benefits of agent-oriented transitioning from monolithic to service-based architectures. In 2024 International Conference on INnovations in Intelligent SysTems and Applications (INISTA), pages 1–6. IEEE, 2024. 2 





[9] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Kuttler, Mike Lewis, Wen-tau Yih, Tim Rockt ¨ aschel, et al. ¨ Retrieval-augmented generation for knowledge-intensive nlp tasks. Advances in neural information processing systems, 33:9459–9474, 2020. 2 





[10] Jianing Qiu, Kyle Lam, Guohao Li, Amish Acharya, Tien Yin Wong, Ara Darzi, Wu Yuan, and Eric J Topol. Llmbased agentic systems in medicine and healthcare. Nature Machine Intelligence, 6(12):1418–1420, 2024. 2 





[11] Chengguang Gan, Qinghao Zhang, and Tatsunori Mori. Application of llm agents in recruitment: A novel framework for automated resume screening. Journal of Information Processing, 32:881–893, 2024. 2, 3 





[12] Riya Pal, Shahrukh Shaikh, Swaraj Satpute, and Sumedha Bhagwat. Resume classification using various machine learning algorithms. In ITM web of conferences, volume 44, page 03011. EDP Sciences, 2022. 2 





[13] Irfan Ali, Nimra Mughal, Zahid Hussain Khand, Javed Ahmed, and Ghulam Mujtaba. Resume classification system using natural language processing and machine learning techniques. Mehran University Research Journal Of Engineering & Technology, 41(1):65–79, 2022. 





[14] Kameni Florentin Flambeau Jiechieu and Norbert Tsopze. Skills prediction based on multi-label resume classification using cnn with model predictions explanation. Neural Computing and Applications, 33(10):5069–5087, 2021. 





[15] Amirreza Jalili, Hamed Tabrizchi, Jafar Razmara, and Amir Mosavi. Bilstm for resume classification. In 2024 IEEE 22nd World Symposium on Applied Machine Intelligence and Informatics (SAMI), pages 000519–000524. IEEE, 2024. 2 





[16] Shabna Nasser, C Sreejith, and M Irshad. Convolutional neural network with word embedding based approach for resume classification. In 2018 International Conference on Emerging Trends and Innovations In Engineering And Technological Research (ICETIETR), pages 1–6. IEEE, 2018. 





[17] S Ramraj, V Sivakumar, et al. Real-time resume classification system using linkedin profile descriptions. In 2020 International Conference on Computational Intelligence for Smart Power System and Sustainable Energy (CISPSSE), pages 1–4. IEEE, 2020. 





[18] Panagiotis Skondras, Panagiotis Zervas, and Giannis Tzimas. Generating synthetic resume data with large language models for enhanced job description classification. Future Internet, 15(11):363, 2023. 





[19] S Bharadwaj, Rudra Varun, Potukuchi Sreeram Aditya, Macherla Nikhil, and G Charles Babu. Resume screening using nlp and lstm. In 2022 international conference on inventive computation technologies (ICICT), pages 238–241. IEEE, 2022. 2 





[20] K Satheesh, A Jahnavi, L Iswarya, K Ayesha, G Bhanusekhar, and K Hanisha. Resume ranking based on job description using spacy ner model. International Research Journal of Engineering and Technology, 7(05): 74–77, 2020. 2 





[21] K Tejaswini, V Umadevi, Shashank M Kadiwal, and Sanjay Revanna. Design and development of machine learning based resume ranking system. Global Transitions Proceedings, 3(2):371–375, 2022. 2 





[22] Agata Mirowska and Laura Mesnet. Preferring the devil you know: Potential applicant reactions to artificial intelligence evaluation of interviews. Human Resource Management Journal, 32(2):364–383, 2022. 2 





[23] Padma Jyothi Uppalapati, Madhavi Dabbiru, and Venkata Rao Kasukurthi. Ai-driven mock interview assessment: leveraging generative language models for automated evaluation. International Journal of Machine Learning and Cybernetics, pages 1–23, 2025. 





[24] Changwoo Kim, Jinho Choi, Jongyeon Yoon, Daehun Yoo, and Woojin Lee. Fairness-aware multimodal learning in automatic video interview assessment. IEEE Access, 11: 122677–122693, 2023. 





[25] Sri Roshan RK, GS Vidharsana, et al. Ai-enhanced eye tracking for candidate assessment in job interviews. In 2025 6th International Conference on Mobile Computing and Sustainable Informatics (ICMCSI), pages 810–815. IEEE, 2025. 2 





[26] Sayan Das, Rupashri Barik, and Ayush Mukherjee. Salary prediction using regression techniques. Proceedings of Industry Interactive Innovations in Science, Engineering & Technology (I3SET2K19), 2020. 2 





[27] Sananda Dutta, Airiddha Halder, and Kousik Dasgupta. Design of a novel prediction engine for predicting suitable salary for a job. In 2018 Fourth International Conference on Research in Computational Intelligence and Communication Networks (ICRCICN), pages 275–279. IEEE, 2018. 2 





[28] Ketki V Deshpande, Shimei Pan, and James R Foulds. Mitigating demographic bias in ai-based resume filtering. In Adjunct publication of the 28th ACM conference on user modeling, adaptation and personalization, pages 268–275, 2020. 2 





[29] Kyra Wilson and Aylin Caliskan. Gender, race, and intersectional bias in resume screening via language model retrieval. In Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society, volume 7, pages 1578–1590, 2024. 





[30] Le Chen, Ruijun Ma, Aniko Hann ´ ak, and Christo Wilson. ´ Investigating the impact of gender on rank in resume search engines. In Proceedings of the 2018 chi conference on human factors in computing systems, pages 1–14, 2018. 





[31] Dena F Mujtaba and Nihar R Mahapatra. Ethical considerations in ai-based recruitment. In 2019 IEEE International Symposium on Technology and Society (ISTAS), pages 1–7. IEEE, 2019. 2 





[32] Kenneth Ward Church. Word2vec. Natural Language Engineering, 23(1):155–162, 2017. 3 





[33] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. In Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers), pages 4171– 4186, 2019. 3 





[34] Esmail Salakar, Jivitesh Rai, Aayush Salian, Yasha Shah, and Jyoti Wadmare. Resume screening using large language models. In 2023 6th International Conference on Advances in Science and Technology (ICAST), pages 494–499. IEEE, 2023. 3 





[35] Srushti Haryan, Rupin Malik, Prathamesh Redij, and Sujata Kulkarni. Fairhire: A fair and automated candidate screening system. In International Conference on Machine Intelligence, Tools, and Applications, pages 372–382. Springer, 2024. 3 





[36] Zhentao Xu, Mark Jerome Cruz, Matthew Guevara, Tie Wang, Manasi Deshpande, Xiaofeng Wang, and Zheng Li. Retrieval-augmented generation with knowledge graphs for customer service question answering. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, pages 2905–2909, 2024. 3 





[37] Nirmalie Wiratunga, Ramitha Abeyratne, Lasal Jayawardena, Kyle Martin, Stewart Massie, Ikechukwu Nkisi-Orji, Ruvan Weerasinghe, Anne Liret, and Bruno Fleisch. Cbrrag: case-based reasoning for retrieval augmented generation in llms for legal question answering. In International Con-





ference on Case-Based Reasoning, pages 445–460. Springer, 2024. 3 





[38] Cyril Zakka, Rohan Shad, Akash Chaurasia, Alex R Dalal, Jennifer L Kim, Michael Moor, Robyn Fong, Curran Phillips, Kevin Alexander, Euan Ashley, et al. Almanac—retrieval-augmented language models for clinical medicine. Nejm ai, 1(2):AIoa2300068, 2024. 3 





[39] Guangzhi Xiong, Qiao Jin, Zhiyong Lu, and Aidong Zhang. Benchmarking retrieval-augmented generation for medicine. In Findings of the Association for Computational Linguistics ACL 2024, pages 6233–6251, 2024. 3 





[40] Antonio Jimeno Yepes, Yao You, Jan Milczek, Sebastian Laverde, and Renyu Li. Financial report chunking for effective retrieval augmented generation. arXiv preprint arXiv:2402.05131, 2024. 3 





[41] Zachary Levonian, Chenglu Li, Wangda Zhu, Anoushka Gade, Owen Henkel, Millie-Ellen Postle, and Wanli Xing. Retrieval-augmented generation to improve math questionanswering: Trade-offs between groundedness and human preference. arXiv preprint arXiv:2310.03184, 2023. 3 





[42] Hao Wei, Jianing Qiu, Haibao Yu, and Wu Yuan. Medco: Medical education copilots based on a multi-agent framework. European Conference on Computer Vision Workshop, 2024. 3 





[43] Huayang Li, Yixuan Su, Deng Cai, Yan Wang, and Lemao Liu. A survey on retrieval-augmented text generation. arXiv preprint arXiv:2202.01110, 2022. 3 

