# Phân tích từng paper (Group 1: Review, Datasets & Benchmarks)

## 1. Systematic Review of Methods for Analysis of Resumes

* **Các vấn đề xảy ra trong bài báo**:
    * Định kiến dữ liệu (Dataset bias) và thiếu sự đa dạng.
    * Định dạng CV không đồng nhất (Unbalanced resume formats).
    * Yêu cầu tài nguyên tính toán lớn cho các mô hình hiện đại.
    * Khó khăn trong việc hiểu ngữ cảnh (Contextual understanding) và các kỹ năng phi truyền thống.
* **Dataset**:
    * **Tên dataset**: Tổng hợp từ 44 nghiên cứu (bao gồm dữ liệu từ LinkedIn, Indeed, các cổng thông tin việc làm).
    * **Quy mô**: Rất lớn (tổng kết quả từ hơn 41,300 bài báo, rút trích 44 bài tiêu biểu).
    * **Đặc điểm**: Đa dạng định dạng (PDF, DOC), cấu trúc từ có sẵn đến phi cấu trúc hoàn toàn.
* **Phương pháp**:
    * **Mô hình**: ML (SVM, Decision Trees, Random Forest), DL (RNN, LSTM, CNN), Transformers (BERT, SentenceBERT).
    * **Kỹ thuật chính**: Parsing, Entity Extraction (NER), Ranking, Latent Dirichlet Allocation (LDA), Knowledge Graph.
* **Cách hoạt động** (Phương pháp giải quyết):
    1. **Hệ thống hóa quy trình**: Bài báo tổng hợp và chuẩn hóa quy trình phân tích CV từ 44 nghiên cứu khác nhau thành một pipeline chuẩn: Parsing (Trích xuất) -> Domain Prediction (Dự đoán ngành nghề) -> Skill Extraction (Trích xuất kỹ năng) -> Candidate Ranking (Xếp hạng).
    2. **Phân tích kỹ thuật Hybrid**: Giải thích cách kết hợp giữa các luật (Rule-based) để trích xuất thông tin cơ bản và học sâu (Deep Learning như BERT) để hiểu ngữ cảnh phức tạp.
    3. **Chuẩn hóa dữ liệu phi cấu trúc**: Sử dụng **NLTK/Spacy** để tiền xử lý, sau đó áp dụng **NER** và **POS Tagging** để biến các đoạn văn bản tự do trong CV thành các trường dữ liệu có cấu trúc (JSON/Database).
    4. **Đề xuất mô hình tối ưu**: Phân tích và chỉ ra rằng việc sử dụng **Knowledge Graph** kết hợp với **Embedding** giúp hệ thống không chỉ khớp từ khóa mà còn hiểu được các kỹ năng tương đương (ví dụ: hiểu Java và Spring Boot có liên quan mật thiết).
* **Kết quả**:
    * **Metric**: Accuracy thường đạt từ 85% - 94%.
    * **So sánh**: Các mô hình Deep Learning (như BERT) vượt trội về hiểu ngữ cảnh nhưng tốn tài nguyên hơn ML truyền thống.
* **Điểm mạnh**: Tổng quan cực kỳ chi tiết về toàn bộ quá trình từ parsing đến ranking, chỉ ra các xu hướng tương lai như đa phương thức (multimodal).
* **Hạn chế**: Hiệu năng giảm mạnh trên các format CV lạ hoặc không theo chuẩn.
* **Insight rút ra**: Bước Parsing là cốt lõi; nếu parsing sai, kết quả ranking phía sau sẽ không có ý nghĩa. Cần kết hợp cả Knowledge Graph để hiểu mối quan hệ giữa các kỹ năng.

---

## 2. ResumeAtlas: Revisiting Resume Classification with Large-Scale Datasets and Large Language Models

* **Các vấn đề xảy ra trong bài báo**:
    * Các bộ dữ liệu hiện tại quá nhỏ (vài nghìn mẫu) và ít nhãn (5-25 nhãn).
    * Thiếu các mẫu CV chuẩn hóa và lo ngại về quyền riêng tư dữ liệu.
    * Sự mơ hồ giữa các vai trò công việc tương đương (ví dụ: Python Developer vs Full-stack Engineer).
* **Dataset**:
    * **Tên dataset**: ResumeAtlas
    * **Quy mô**: 13,389 CV, phân loại vào 43 class khác nhau.
    * **Đặc điểm**: Dữ liệu từ ảnh (OCR), chứa nội dung text thực tế từ nhiều ngành nghề.
* **Phương pháp**:
    * **Mô hình**: Large Language Models (Gemma 1.1 2B, BERT).
    * **Kỹ thuật chính**: OCR (Google Cloud Vision), Fine-tuning với LoRA, Quantization.
* **Cách hoạt động** (Phương pháp giải quyết):
    1. **Mở rộng quy mô Dataset**: Giải quyết vấn đề thiếu dữ liệu nhãn bằng cách tự xây dựng tập **ResumeAtlas** (13k mẫu, 43 nhãn). Sử dụng **Google Cloud Vision** để "số hóa" các CV dạng ảnh/PDF quét, tạo ra bộ tài nguyên huấn luyện quy mô lớn.
    2. **Tận dụng LLM cho Classification**: Thay vì dùng các model ML đơn giản chỉ đếm từ (TF-IDF), bài báo sử dụng sức mạnh hiểu ngôn ngữ tự nhiên của **Gemma** và **BERT**. 
    3. **Huấn luyện thích nghi (Transfer Learning)**: Sử dụng kỹ thuật **LoRA** để "dạy" mô hình ngôn ngữ khổng lồ hiểu các thuật ngữ chuyên ngành trong CV mà không cần tốn quá nhiều tài nguyên tính toán.
    4. **Tối ưu hóa vùng tập trung (Header focus)**: Phương pháp chỉ tập trung vào 300 từ đầu tiên của CV dựa trên quan sát rằng thông tin về vị trí và kỹ năng cốt lõi thường tập trung ở phần đầu, giúp mô hình ra quyết định nhanh và chính xác hơn trên 43 nhóm ngành khác nhau.
* **Kết quả**:
    * **Metric**: Top-1 Accuracy đạt 92% (Gemma), Top-5 đạt 97.5%.
    * **So sánh**: Vượt qua các baseline ML truyền thống như XGBoost (83.5%) và MLP (81.6%).
* **Điểm mạnh**: Xây dựng bộ dữ liệu phân loại CV quy mô lớn và chứng minh LLM hiệu quả hơn hẳn ML truyền thống trong việc phân loại vai trò.
* **Hạn chế**: Chỉ tập trung vào 300 từ đầu tiên, có thể bỏ lỡ các dự án quan trọng ở cuối CV.
* **Insight rút ra**: Hầu hết thông tin về "job title" và "role" nằm ở phần đầu CV. Một ứng viên nên được gán Top-K nhãn thay vì chỉ một nhãn duy nhất để tăng độ chính xác tìm kiếm.

---

## 3. PJB: A Reasoning-Aware Benchmark for Person-Job Retrieval

* **Các vấn đề xảy ra trong bài báo**:
    * Các benchmark hiện tại chỉ chấm điểm tổng quát, không chỉ ra được hệ thống "sai ở đâu và tại sao".
    * Person-Job matching đòi hỏi cả suy luận song song (Parallel - khớp các ràng buộc cứng) và suy luận nối tiếp (Serial - hiểu sự chuyển đổi kỹ năng, kinh nghiệm tương đương).
* **Dataset**:
    * **Tên dataset**: PJB (Person-Job Benchmark) v1.0
    * **Quy mô**: 297 queries (JD), gần 200,000 resumes, 2,242 nhãn đánh giá khớp (positive judgments).
    * **Đặc điểm**: Dữ liệu thực tế từ 6 nhóm ngành công nghiệp, tập trung vào khả năng lập luận (reasoning).
* **Phương pháp**:
    * **Mô hình**: Dense Retrieval (CRE-T1-0.6B), Reranking (Qwen3-Reranker-8B).
    * **Kỹ thuật chính**: Diagnostic labeling (nhãn chẩn đoán lỗi), lý luận dựa trên năng lực (job-competency reasoning).
* **Cách hoạt động** (Phương pháp giải quyết):
    1. **Xây dựng hệ thống chẩn đoán (Diagnostic)**: Thay vì chỉ đánh giá "đúng/sai" tổng thể, bài báo giải quyết vấn đề "hộp đen" bằng cách gán nhãn cho truy vấn theo hai chiều: **Parallel width** (độ rộng lọc cứng - location, education, v.v.) và **Serial depth** (độ sâu suy luận ngữ nghĩa - hiểu kinh nghiệm tương đương).
    2. **Đánh giá dựa trên năng lực (Competency-driven)**: Sử dụng các mô hình ngôn ngữ mạnh (**Doubao, Kimi**) đóng vai trò làm chuyên gia chấm điểm (LLM-as-a-Judge) để đánh giá CV dựa trên bằng chứng về năng lực (evidence) thay vì chỉ so khớp từ khóa.
    3. **Phân tích lát cắt (Sliced Analysis)**: Phương pháp này chia nhỏ kết quả đánh giá theo từng "domain family" (ngành nghề) và "reasoning type" (loại lý luận). Điều này giúp xác định chính xác hệ thống đang yếu ở bước lọc điều kiện hay bước suy luận kinh nghiệm.
    4. **Chứng minh vai trò của Reranking**: Thông qua pipeline so sánh, bài báo chỉ ra rằng mô hình **Dense Retrieval** mạnh về tìm kiếm sơ bộ, nhưng cần kết hợp thêm **Reranker** (như Qwen3-Reranker) để giải quyết các truy vấn đòi hỏi suy luận sâu (Serial reasoning).
* **Kết quả**:
    * **Metric**: nDCG@10, Recall@20.
    * **So sánh**: Mô hình domain-specific (huấn luyện trên dữ liệu tuyển dụng) vượt xa mô hình đa năng (general-purpose). Reranking mang lại cải thiện ổn định nhất.
* **Điểm mạnh**: Cung cấp khả năng "chẩn đoán" lỗi. Chỉ ra rằng Query Understanding (viết lại câu truy vấn) đôi khi làm giảm hiệu năng nếu làm mất cấu trúc JD.
* **Hạn chế**: Nhãn chẩn đoán dựa trên heuristic (quy tắc tự động) có thể chưa bao phủ hết các ca phức tạp.
* **Insight rút ra**: Đừng tin vào điểm trung bình. Hệ thống có thể rất tốt ở ngành Sales nhưng cực tệ ở ngành Tech. Cần huấn luyện model nhúng (Embedding) riêng cho domain tuyển dụng.

---

## 4. A Comprehensive Review of AI-Powered Resume Screening and Analysis Systems

* **Các vấn đề xảy ra trong bài báo**:
    * Khối lượng ứng dụng lớn gây khó khăn cho việc sàng lọc thủ công.
    * Định kiến vô thức (unconscious bias) của con người trong tuyển dụng.
    * Dữ liệu phi cấu trúc gây khó khăn cho việc phân tích tự động.
* **Dataset**:
    * **Tên dataset**: Tổng hợp lý thuyết và các nghiên cứu về hệ thống ATS thực tế.
    * **Quy mô**: Review hệ thống.
    * **Đặc điểm**: Tập trung vào tích hợp hệ thống (ATS integration) và đạo đức AI (Ethical AI).
* **Phương pháp**:
    * **Mô hình**: NLP, ML, Deep Learning, Generative AI (Gemini 1.5).
    * **Kỹ thuật chính**: Semantic analysis, Keyword matching, XAI (Explainable AI - AI có thể giải thích được).
* **Cách hoạt động** (Phương pháp giải quyết):
    1. **Tự động hóa hoàn toàn chu trình tuyển dụng**: Đề xuất tích hợp AI vào mọi bước của hệ thống ATS, từ Parsing đến Ranking và Phỏng vấn.
    2. **Ứng dụng Generative AI cho phân tích sâu**: Sử dụng **Gemini 1.5** không chỉ để so khớp mà còn để "đọc hiểu" CV, từ đó tóm tắt các điểm mạnh/yếu của ứng viên liên quan đến JD.
    3. **Cá nhân hóa quy trình tuyển dụng**: Phương pháp này sử dụng AI để tự động tạo ra các bộ câu hỏi phỏng vấn đặc thù cho từng ứng viên (personalized interview questions) dựa trên các "khoảng trống" (skill gaps) được phát hiện trong CV.
    4. **Giảm thiểu định kiến (Bias Mitigation)**: Sử dụng các thuật toán ẩn danh thông tin nhạy cảm và áp dụng tiêu chí chấm điểm khách quan dựa trên dữ liệu (Data-driven insights) thông qua Dashboard phân tích trực quan.
* **Kết quả**:
    * **Metric**: Thời gian xử lý (giảm 40% cho nhà tuyển dụng).
    * **So sánh**: Nhấn mạnh vào việc AI giúp tăng tính minh bạch và khách quan hơn so với con người.
* **Điểm mạnh**: Đề cập sâu đến Explainable AI (XAI) và tính đa phương thức (xử lý cả giọng nói, video trong tương lai).
* **Hạn chế**: Phần lớn là tổng quan lý thuyết, thiếu các thử nghiệm thực nghiệm quy mô lớn trên codebase cụ thể.
* **Insight rút ra**: Việc giải thích "tại sao ứng viên này được xếp hạng cao" (XAI) là yếu tố sống còn để xây dựng lòng tin với nhà tuyển dụng.
