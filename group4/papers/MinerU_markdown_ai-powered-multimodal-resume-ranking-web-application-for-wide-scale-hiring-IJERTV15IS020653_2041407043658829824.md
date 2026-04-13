# AI Powered Multimodal Resume Ranking Web Application for Wide Scale Hiring

Mr. Prathap Sathyavedu 

Assistant Professor, 

Department of CSE 

Annamacharya Institute of 

Technology and Sciences 

Tirupati - 517520, A.P, India 

P Hinduja 

UG Scholar, 

Department of CSE 

Annamacharya Institute of 

Technology and Sciences 

Tirupati - 517520, A.P, India 

M Deena 

UG Scholar, 

Department of CSE 

Annamacharya Institute of 

Technology and Sciences 

Tirupati - 517520, A.P, India 

M Lakshmi Chaithanya Sai 

UG Scholar, Department of CSE 

Annamacharya Institute of 

Technology and Sciences 

Tirupati - 517520, A.P, India 

Y Dilli Sravani 

UG Scholar, Department of CSE 

Annamacharya Institute of 

Technology and Sciences 

Tirupati - 517520, A.P, India 

Abstract - This work presents a web-based resume ranking system designed to support large-scale recruitment by automating resume analysis and candidate matching. The system combines modern deep learning models with traditional information re- trieval techniques to extract, organize, and compare resume content against job descriptions. Resume layouts are first segmented, after which textual information is extracted and classified into meaningful sections such as skills, education, and work experience. Relevant entities are then identified to enrich the extracted information. A hybrid matching strategy is applied, combining semantic similarity and keyword relevance to generate accurate and interpretable rankings. The application enables HR profes- sionals to upload resumes, configure job requirements, and view ranked candidates through an intuitive interface. Experimental results indicate that the system performs reliably across diverse resume formats, demonstrating its potential to reduce manual workload and improve the efficiency of recruitment processes. 

Index Terms - Artificial Intelligence, Natural Language Processing,g, Optical Character Recognition, Named Entity Recog- nition,n, Text Recognition 

# I. INTRODUCTION

The rapid expansion of online recruitment platforms and remote work opportunities has dramatically increased the number of job applications received by organizations. As a result, Human Resources (HR) teams face growing pressure to evaluate resumes quickly and accurately. Traditional manual screening methods are time-consuming, difficult to scale, and prone to human bias, which can lead to inconsistent 

decisions or the unintentional exclusion of qualified candidates. These challenges become more severe when resumes are submitted in diverse formats and layouts, making information extraction and comparison even harder. 

To address these issues, automated resume analysis systems have gained attention in recent years. By leveraging advances in artificial intelligence, particularly in computer vision and natural language processing, such systems aim to standardize resume interpretation and improve candidate-job alignment. In this work, we introduce a resume ranking web application that automates the extraction, organization, and comparison of resume content with job descriptions. The goal is to assist HR professionals by reducing manual workload while improving fairness, consistency, and efficiency in the recruitment process. General motivations for digital and AI-supported recruitment are well established in prior studies on e-recruitment and hiring challenges [1] [2]. 

# II. RELATED WORK

Resume parsing and ranking has been widely studied using a variety of machine learning and natural language processing techniques. Earlier approaches relied heavily on optical character recognition (OCR) combined with rule-based methods to extract key information from resumes. With the emergence of transformer-based language models, more recent systems employ models such as BERT for text classification and named entity recognition to better capture contextual information. 

Several studies have explored automated resume screening 

by matching candidate profiles with job descriptions using keyword-based similarity, semantic embeddings, or hybrid approaches. Machine learning classifiers and deep learning architectures, including convolutional neural networks and re- current models, have also been applied to resume segmentation and ranking tasks. While these systems demonstrate promising accuracy, many struggle with layout variability, multilingual resumes, or limited generalization across domains. 

Compared to prior work, our approach emphasizes a multimodal pipeline that first understands the visual structure of resumes before applying OCR and language models. This design improves robustness across different resume formats 

and supports more accurate downstream text analysis. The discussion in this section is based on a synthesis of established resume parsing and ranking literature rather than direct reuse of specific implementations [3] [4]. user 

# III. METHODOLOGY

# A. System Overview

The proposed resume ranking system adopts a multi-layer architecture that combines deep learning models with traditional information retrieval techniques. This hybrid design enables efficient processing, structured information extraction, and accurate matching between resumes and job descriptions. 

1) Resume Information Extraction: HR users upload re-sumes in PDF, DOCX, or image formats. These files are converted into images and processed using a YOLOv9-based model to detect and segment textual regions. Text recognition is performed on the segmented regions using EasyOCR. The extracted content is then classified into structured resume sections—such as personal details, education, experience, and skills—using a fine-tuned multilingual BERT model. Named entities, including locations and languages, are identified using a zero-shot NER model supported by regular expression rules. 

2) Job Description Definition: Recruiters define job descriptions through the system interface and assign weights to key attributes such as skills, experience, and education. This allows the matching process to reflect specific hiring priorities. 

3) Matching and Ranking: A hybrid matching strategy is applied to compare resumes with job descriptions. 

4) Semantic relevance is computed using cosine similarity over dense text embeddings, while keyword relevance is measured using BM25. Weighted scores are combined to generate a final ranking, and the most relevant candidates are presented to the computational cost [9]. After training and testing all models on a custom resume dataset, YOLOv9 demonstrated superior 

accuracy, recall, and mAP across diverse resume formats. These results are consistent with recent studies highlightingYOLO's effectiveness in document layout analysis [6]. Accurate layout detection prior to OCR significantly improves overall resume parsing and ranking performance. 

2) Text Recognition with OCR: Text recognition is performed using EasyOCR, which reliably extracts multilingual text from detected resume segments and prepares structured content for subsequent classification stages [10] [11] [12]. 

3) Text Classification: The extracted resume text is organized using a fine-tuned multilingual BERT model from the Hugging Face Transformers library. This model groups each text segment into meaningful resume sections, making the overall content easier to analyze and compare [13] [14]. 

4) Zero shot NER: Named entities are extracted using GLiNER, a zero-shot NER model that supports flexible, on- the-fly label definitions without retraining. It efficiently identifies key details from classified resume sections, complemented by rule-based patterns for contact information [15]. 

5) Embedding Model and Hybrid Matching: Resume and job description texts are embedded using the Sentence Trans-formers library with the gte-large-en-v1.5 model. Section-level weights for skills, experience, and education can be adjusted, and final rankings combine semantic similarity and keyword matching for precise matching. 

- Cosine Similarity Matching with Resume Parts: To measure how closely each resume section aligns with the job description, cosine similarity is computed between their respective embeddings, as defined in Equation (1). 

$$
C _ {i} = \frac {E _ {\text {j o b}} \cdot E _ {\text {r e s} , i}}{\| E _ {\text {j o b}} \| \| E _ {\text {r e s} , i} \|} \tag {1}
$$

# B. Overview of the dataset

The dataset was created by collecting resume templates from publicly available and royalty-free online sources, including resume websites, professional networking platforms, open-source resume builders, and university career portals. This process resulted in 2,751 resumes in PDF and DOCX formats, 

- Weighted Cosine Similarity Score: Where $E_{\mathrm{job}}$ represents the embedding vector of the job description, and $E_{\mathrm{res},i}$ is the embedding vector of the $i$ -th resume section. These similarity values are weighted and combined to obtain the final cosine similarity score, as shown in Equation (2). 

$$
\begin{array}{l} C = W _ {s} \cdot C _ {\text {s k i l l s}} + W _ {e} \cdot C _ {\text {e x p e r i e n c e}} \tag {2} \\ W _ {e d} \cdot C _ {\text {e d u c a t i o n}} + W _ {m} \cdot C _ {\text {m i s c e l l a n e o u s}} \\ \end{array}
$$

covering a wide range of layouts, styles, and content structures. All resumes were annotated using the Roboflow platform for object detection, with a single class labeled segment to represent text regions. The dataset was split into training (75%), validation (19%), and test (6%) sets. Preprocessing and data augmentation techniques were applied to improve model robustness and generalization [5]. 

# C. Implementation

1) Object Detection: Multiple object detection models were evaluated to analyze resume layouts. DETR and Detector2 in- troduce transformer-based and multiarchitecture frameworks that improve detection performance on complex documents 

[7] [8]. YOLOv9, the latest model in the YOLO family, incorporates the GELAN architecture and programmable gradient information, enabling efficient learning with reduced 

- Keyword Matching: The BM25 algorithm [16] is employed to match keywords, with particular attention given to location and language. Let $K_{\mathrm{loc}}$ and $K_{\mathrm{lang}}$ represent the BM25 scores for location and language keywords, respectively. The overall keyword matching score $K$ is then computed as the average of these two scores, as shown in Equation (3): 

$$
K = 0. 5 \cdot \left(K _ {\text {l o c}} + K _ {\text {l a n g}}\right) \tag {3}
$$

- Overall Matching Score: Finally, the overall matching score $S$ is obtained by combining the weighted cosine similarity score and the keyword matching score. Let $C$ denote the cosine similarity score and $K$ the keyword matching score, with $W_{k}$ as the weight for keyword importance. The combined score is computed as shown in Equation (4): 

$$
S = C + W _ {k} \cdot K \tag {4}
$$

6) Web Application: The web application developed in this study prioritizes ease of use and thorough review through a clean and intuitive interface. It allows users to upload up to 200 resumes at a time, directly observe the model's outputs, and modify job descriptions, including the assignment of weights and specification of job components. The system accommodates weight scores, job titles, company locations, job types, job details, and required skills. Additionally, it provides a detailed view of the matching results, enabling users to examine how each resume corresponds to the job description in a comprehensive manner. 

# IV. EXPERIMENTAL RESULTS

We first present the training performance of our object detection models, evaluated on a custom dataset designed for resume layout analysis. This dataset, featuring various resume formats, enabled comparison of YOLOv9, DETR, and Detec-tron2 in detecting structural elements. Next, we discuss OCR-based text extraction results, followed by text classification and NER outcomes, enhanced with regular expressions. Finally, we illustrate how embedding models match resumes with job descriptions, highlighting the effectiveness of our multi-stage resume ranking approach. 

# A. Custom Dataset Analysis

The study uses a custom dataset of 2,694 images, expanded to 4,304 via augmentation, containing 19,111 annotated instances across training, validation, and testing subsets. Each image averages 7.1 annotations, supporting thorough model training and evaluation. 

# B. Object Detection Model Training Results

Training parameters, including learning rate, batch size, op-timizer, and other hyperparameters for DETR, Detector2, and YOLOv9, were set based on their respective studies [7] [8] [9]. Model performance was evaluated using Average Precision (AP) and Average Recall (AR) across multiple IoU thresholds. AP reflects detection accuracy, AR measures coverage of essential resume sections, and IoU indicates localization preci-sion. Inference times on an L4 GPU were 1.05s (DETR), 1.17s (Detectron2), and 0.24s (YOLOv9), highlighting YOLOv9's speed and precision. 

# C. Text Processing and Analysis Results

1) OCR Results: EasyOCR generally achieved high text recognition accuracy across resume sections, but errors were observed that could affect downstream processing. Common issues included character confusions (e.g., 'O' vs. '0', 'l' vs. '1'), misreads of words such as "Manager" as "Mana9er," punctuation mistakes, and spacing inconsistencies like "high-quality" appearing as "high-quality." Font variations, especially in headers or logos, occasionally caused complete 

misinterpretations. These errors may impact job title, skill classification, and NER accuracy. Our findings emphasize the importance of post-processing corrections or manual review and highlight the need for diverse resume datasets to improve robustness. 

2) Text Classification Results: The text classification stage follows OCR-based text extraction. We employed a pre-trained Hugging Face model [17] to categorize resume sections. Its performance was evaluated on an unseen resume dataset, with metrics summarized in Table IV, showing high accuracy across categories such as certificates, contact details, education, lan- guages, work 

experience, and skills. Leveraging a pre-trained model allows the use of knowledge from large resume corpora, improving classification across diverse formats. Performance may vary depending on dataset similarity to the original train- ing data. The classified text serves as input for the subsequent named entity recognition step, ensuring structured and accurate information extraction. 

3) NER Results: Following text classification, specific entities are extracted from the classified text using the GLiNER model. The NER performance depends on prior stages, particularly OCR output. Our analysis shows GLiNER achieves generally good entity recognition but often produces lower confidence scores. This is expected, as the model uses a zero-shot approach and has not been trained specifically on resumes. Lower confidence may also result from resume format variability or OCR errors. Despite these limitations, GLiNER demonstrates the potential of zero-shot learning for specialized tasks, such as parsing resumes, highlighting its usefulness even in domains with limited training data. 

4) Matching Results: Choosing an appropriate embed- ding model is key for effective resume-job matching. Us- ing the MTEB Benchmark, which evaluates long-sequence performance, we selected the gte-large-en-v1.5 model [?], [?] for its strong handling of lengthy texts and balanced size-performance tradeoff. This model efficiently processes resumes and job descriptions, generating accurate embeddings for semantic similarity and BM25 keyword matching. Table VII illustrates flexible weighting, showing how candidate qualifications align with job requirements. 

# V. CONCLUSION AND FUTURE WORK

In this study, we developed a resume ranking web application that employs advanced deep learning techniques to streamline recruitment. The system integrates YOLOv9 for object detection, EasyOCR for text extraction, fine-tuned mBERT for text classification, and GLiNER for named entity recognition, enabling accurate extraction, categorization, and matching of resumes with job descriptions. Key contributions include a multi-model approach for comprehensive parsing, combined cosine similarity and BM25 scoring for precise matching, and an intuitive interface with adjustable weights for HR professionals. Challenges encountered involved OCR errors due to diverse fonts and layouts, lower confidence in zero-shot NER, and limitations in semantic representation using dense embeddings. Future work aims to enhance OCR 


TABLEI HYBRID MATCHING SCORES FOR AN EXAMPLE SCENARIO


<table><tr><td>Resume ID</td><td>Skills (0.2)</td><td>Experience (0.4)</td><td>Education (0.1)</td><td>Misc. (0.2)</td><td>Keyword (0.1)</td><td>Final Score</td></tr><tr><td>4</td><td>0.14</td><td>0.29</td><td>0.07</td><td>0.146</td><td>0</td><td>0.65</td></tr><tr><td>5</td><td>0.12</td><td>0.29</td><td>0.047</td><td>0.146</td><td>0</td><td>0.61</td></tr><tr><td>3</td><td>0.118</td><td>0.27</td><td>0.00</td><td>0.141</td><td>0.05</td><td>0.59</td></tr><tr><td>6</td><td>0.148</td><td>0.27</td><td>0.062</td><td>0.108</td><td>0</td><td>0.59</td></tr><tr><td>7</td><td>0.146</td><td>0.27</td><td>0.00</td><td>0.144</td><td>0</td><td>0.56</td></tr><tr><td>1</td><td>0.10</td><td>0.20</td><td>0.03</td><td>0.108</td><td>0.05</td><td>0.44</td></tr><tr><td>2</td><td>0.103</td><td>0.20</td><td>0.05</td><td>0.078</td><td>0</td><td>0.44</td></tr><tr><td>8</td><td>0.121</td><td>0.27</td><td>0.048</td><td>0.00</td><td>0</td><td>0.44</td></tr></table>

performance, develop a resume-specific NER dataset, refine information extraction, adopt hybrid embedding techniques, expand features for job seekers, update datasets continuously, and optimize models for real-time processing. These improve-ments will create a more accurate, adaptable, and efficient recruitment tool. 

# ACKNOWLEDGMENT

The authors would like to express their sincere gratitude to the faculty advisors and mentors for their continuous guidance, encouragement, and valuable feedback throughout the course of this work. We also thank our peers and colleagues for their constructive discussions and support, which greatly contributed to the completion of this document. 

# REFERENCES



[1] Baykal, E. (2020). Digital Era and New Methods for Employee Recruitment. 10.4018/978-1-7998-1125-1.ch018. 





[2] Solanki, S., & Gujarati, D. (2024). The Digital Revolution In Recruitment: Unraveling The Impact And Challenges Of E-Recruitment. Educational Administration Theory and Practices, 30. doi: 10.53555/kuey.v30i6(S).5362 





[3] Rozario, S. D., Venkatraman, S., & Abbas, A. (2019). Challenges in recruitment and selection process: An empirical study. Challenges, 10(2), 35. 





[4] Palshikar, G. K., Pawar, S., Banerjee, A. S., Srivastava, R., Ramrakhiyani, N., Patil, S., ... & Chalavadi, D. (2023). RINX: A system for information and knowledge extraction from resumes. Data & Knowledge Engineering, 147, 102202. 





[5] Kinge, B., Mandhare, S., Chavan, P., & Chaware, S. M. (2022). Resume Screening using Machine Learning and NLP: A proposed system. International Journal of Scientific Research in Computer Science, Engineering and Information Technology, 8(2), 253-258. 





[6] Tanberk, S., Helli, S. S., Kesim, E., & Cavsak, S. N. (2023, September). Resume Matching Framework via Ranking and Sorting Using NLP and Deep Learning. In 2023 8th International Conference on Computer Science and Engineering (UBMK) (pp. 453-458). IEEE. 





[7] Carion, N., Massa, F., Synnaeve, G., Usunier, N., Kirillov, A., & Zagoruyko, S. (2020, August). End-to-end object detection with transformers. In European Conference on Computer Vision (pp. 213-229). Cham: Springer International Publishing. 





[8] Kirillov, A., Wu, Y., He, K., & Girshick, R. (2020). PointRend: Image segmentation as rendering. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (pp. 9799-9808). 





[9] Wang, C. Y., Yeh, I. H., & Liao, H. Y. M. (2024). YOLOv9: Learning What You Want to Learn Using Programmable Gradient Information. arXiv preprint arXiv:2402.13616. 





[10] JadedAI. (2023). EasyOCR. GitHub. Retrieved from https://github.com/JadedAI/EasyOCR 





[11] Vedhaviyassh, D. R., Sudhan, R., Saranya, G., Safa, M., & Arun, D. (2022, December). Comparative analysis of EasyOCR and Tesseract-OCR for automatic license plate recognition using a deep learning algorithm. In 2022 6th International Conference on Electronics, Communication and Aerospace Technology (pp. 966–971). IEEE. 





[12] Wu, X., Luo, C., Zhang, Q., Zhou, J., Yang, H., & Li, Y. (2019). Text Detection and Recognition for Natural Scene Images Using Deep Convolutional Neural Networks. Computers, Materials & Continua, 61(1). 





[13] Wolf, T., Debut, L., Sanh, V., Chaumont, J., Delangue, C., Moi, A., ... & Rush, A. M. (2019). HuggingFace's transformers: State-of-the-art natural language processing. arXiv preprint arXiv:1910.03771. 





[14] Abdaoui, A., Pradel, C., & Sigel, G. (2020). Load what you need: Smaller versions of multilingual BERT. In Proceedings of SustainNLP / EMNLP. 





[15] Zaratiana, U., Tomeh, N., Holat, P., & Charnois, T. (2023). GLiNER: Generalist model for named entity recognition using a bidirectional transformer. arXiv preprint arXiv:2311.08526. 





[16] Li, Z., Zhang, X., Zhang, Y., Long, D., Xie, P., & Zhang, M. (2023). Towards general text embeddings with multi-stage contrastive learning. arXiv preprint arXiv:2308.03281. 





[17] Abida, H. (2022). distilBERT-finetuned-resumes-sections. Hugging Face. Retrieved from https://huggingface.co/has-abi/distilBERT-finetuned-resumes-sections 





[18] Hugging Face. DistilBERT Authorized. Retrieved from https://huggingface.co/has-abi/distilBERTAuthorized 

