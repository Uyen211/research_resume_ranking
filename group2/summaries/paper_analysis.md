# Phân tích từng paper (Group 2: Multi-Agent Systems & LLM Automation)

## 1. AI Hiring with LLMs: A Context-Aware and Explainable Multi-Agent Framework for Resume Screening

* **Các vấn đề xảy ra trong bài báo**:
    * Các hệ thống LLM đơn khối (monolithic) thiếu tính mô đun, khó thay đổi logic chấm điểm mà không phải fine-tune lại.
    * Thiếu tính minh bạch và khả năng giải thích cho các quyết định của AI.
    * Khó thích ứng với tiêu chí tuyển dụng thay đổi liên tục của từng công ty/ngành nghề.
* **Dataset**:
    * **Tên dataset**: Bộ Resume trực tuyến ẩn danh.
    * **Quy mô**: 105 CV.
    * **Đặc điểm**: Văn bản phi cấu trúc, tương ứng với các vị trí nhân sự (HR) ở 4 cấp độ (Junior, Mid, Senior, Leadership).
* **Phương pháp**:
    * **Mô hình**: Multi-agent framework (sử dụng GPT-4o, DeepSeek-V3).
    * **Kỹ thuật chính**: Retrieval-Augmented Generation (RAG), Agentic Workflow (CrewAI), Vector Embedding (OpenAI Embeddings), Vector DB (ChromaDB).
* **Cách hoạt động** (Phương pháp giải quyết):
    1. **Modularizing with Agents**: Chia nhỏ quy trình thành 4 tác tử chuyên biệt: **Extractor** (trích xuất cấu trúc), **Evaluator** (chấm điểm), **Summarizer** (tóm tắt/phản hồi), và **Formatter** (định dạng đầu ra).
    2. **Context Adaptation via RAG**: Thay vì fine-tune model, tác tử **Evaluator** sử dụng **RAG** để truy vấn các "tri thức bên ngoài" (tiêu chuẩn riêng của công ty, bảng xếp hạng đại học, chứng chỉ chuyên ngành) từ **ChromaDB** dựa trên độ tương đồng Cosine (ngưỡng 0.3).
    3. **Collaborative Reasoning**: Tác tử **Summarizer** thực chất bao gồm 3 sub-agents (**CEO, CTO, HR**) tranh luận nội bộ để đưa ra cái nhìn đa chiều về ứng viên (lãnh đạo, kỹ thuật, văn hóa).
    4. **Chain of Logic**: Kết quả trích xuất từ Extractor được truyền làm ngữ cảnh cho Evaluator, sau đó Evaluator dùng RAG để nhúng tiêu chí job-specific vào prompt nhằm tính toán điểm số cho 5 danh mục (Self-eval, Skills, Experience, Basic info, Education).
* **Kết quả**:
    * **Metric**: Pearson Correlation (PC10 đạt 0.84), Spearman Correlation (SC10 đạt 0.74), MAE (0.90).
    * **So sánh**: Vượt trội rõ rệt so với các mô hình LLM đơn lẻ (Single LLM) trong việc phân loại ứng viên top đầu.
* **Điểm mạnh**: Tính giải thích cực cao nhờ quy trình làm việc minh bạch của các agent; dễ dàng tùy chỉnh tiêu chí tuyển dụng thông qua RAG mà không cần code lại.
* **Hạn chế**: Quy mô dataset thử nghiệm còn nhỏ (105 mẫu); độ trễ có thể tăng do sự phối hợp giữa nhiều agent.
* **Insight rút ra**: Nên tách biệt khâu trích xuất (Extraction) và đánh giá (Evaluation). Việc dùng RAG để nạp "văn hóa công ty" là chìa khóa để AI không bị lỗi thời.

---

## 2. Let’s Get You Hired: A Job Seeker’s Perspective on Multi-Agent Recruitment Systems

* **Các vấn đề xảy ra trong bài báo**:
    * Ứng viên hiếm khi nhận được phản hồi mang tính xây dựng hoặc giải thích lý do bị từ chối.
    * Các hệ thống ATS hiện tại là "hộp đen", gây mất lòng tin và cảm giác không công bằng cho người lao động.
    * LLM đơn lẻ thường gặp khó khăn khi phải đóng nhiều vai (context switching) dẫn đến ảo giác (hallucination).
* **Dataset**:
    * **Tên dataset**: CV và JD thực tế của người tham gia nghiên cứu.
    * **Quy mô**: 20 ứng viên đang tìm việc thực tế tham gia phỏng vấn định tính.
    * **Đặc điểm**: Dữ liệu thực tế, cá nhân hóa.
* **Phương pháp**:
    * **Mô hình**: User-centric Multi-agent System (GPT-4-Turbo, GPT-4o-Mini).
    * **Kỹ thuật chính**: Prompt Engineering (ReAct, Chain-of-Thought), User-Centered Design (UCD), LLM-as-a-Judge.
* **Cách hoạt động** (Phương pháp giải quyết):
    1. **Role Playing Agents**: Thiết lập 3 vai trò tác tử: **Recruiter** (đóng vai nhà tuyển dụng, chấm điểm khách quan/khánh kiệt), **Mentor** (đóng vai người hướng dẫn, tìm điểm mạnh và động viên), và **Moderator** (người điều phối cuối cùng).
    2. **Debate & Synthesis Logic**: **Moderator** quản lý giao dịch với người dùng, quyết định khi nào gọi Recruiter hay Mentor. Hai tác tử này trao đổi kết quả và "tranh luận" (counter-arguments) để đảm bảo phản hồi không quá khắt khe cũng không quá nịnh bợ.
    3. **Tool Orchestration**: Chỉ **Moderator** mới có quyền truy cập bộ công cụ (Web search, CV parser) để giảm thiểu sai sót (vì các sub-agents yếu hơn thường gọi tool lỗi).
    4. **Interactive Explanation**: Sử dụng UI trợ giúp như "Quick insights" (tóm tắt nhanh tick xanh/đỏ) và "Quick questions" để dẫn dắt ứng viên hiểu sâu về các Skill Gap mà AI phát hiện.
* **Kết quả**:
    * **Metric**: Điểm Actionability, Trust và Fairness đo qua khảo sát người dùng.
    * **So sánh**: Hệ thống được đánh giá cao hơn hẳn ATS truyền thống (Actionability +34%, Trust +30%, Fairness +40%).
* **Điểm mạnh**: Tạo ra phản hồi mang tính "người" và có ích cho ứng viên; giảm định kiến nhờ sự cân bằng giữa các góc nhìn agent.
* **Hạn chế**: Hiện tượng "Amnestic syndrome" (quên ngắn hạn) trong các phiên hội thoại dài; độ trễ cao (có khi lên tới 1 phút).
* **Insight rút ra**: Phản hồi cho người dùng nên có cả "điểm xấu" (Recruiter) lẫn "lời khuyên" (Mentor). Sự minh bạch trong cách AI so khớp CV-JD giúp tăng lòng tin của người dùng hơn là điểm số cao.

---

## 3. MLAR: Multi-layer Large Language Model-based Robotic Process Automation Applicant Tracking

* **Các vấn đề xảy ra trong bài báo**:
    * Quy trình tuyển dụng truyền thống gặp nút thắt cổ chai khi xử lý hàng nghìn CV cùng lúc.
    * Các hệ thống ATS dựa trên keyword thường bỏ lỡ ứng viên tiềm năng do không hiểu ngữ nghĩa.
    * Công cụ RPA phổ biến (UiPath, Automation Anywhere) khó tùy chỉnh cho các tác vụ hiểu văn bản phức tạp.
* **Dataset**:
    * **Tên dataset**: Kaggle Resume Dataset.
    * **Quy mô**: 2,400 CV thuộc 24 ngành nghề khác nhau.
    * **Đặc điểm**: Định dạng PDF, đa dạng lĩnh vực từ HR đến Kỹ thuật.
* **Phương pháp**:
    * **Mô hình**: RPA framework tích hợp LLM (Gemini API).
    * **Kỹ thuật chính**: Multi-layer Architecture, Semantic Matching, Automation Orchestration.
* **Cách hoạt động** (Phương pháp giải quyết):
    1. **Layer 1 - Job Parsing**: LLM trích xuất các đặc tính cốt lõi (skills, education, experience level) từ JD của nhà tuyển dụng.
    2. **Layer 2 - Resume Parsing**: Tự động duyệt qua hàng nghìn file PDF, dùng LLM để trích xuất thông tin ứng viên và phân loại vào các "Department table" trong database (ví dụ: CV Engineering vào bảng Kỹ thuật) để tối ưu tốc độ truy vấn sau này.
    3. **Layer 3 - Semantic Matching**: Thay vì so từ khóa, LLM tính toán điểm **Similarity (0-100)** dựa trên sự tương đồng ngữ nghĩa giữa các đặc tính đã trích xuất ở Layer 1 và 2.
    4. **Automated Communication Loop**: Hệ thống tự động chọn ra Top 3 ứng viên, dùng LLM tạo nội dung email cá nhân hóa (GenerateResponse) và gửi thông báo trực tiếp qua RPA pipeline.
* **Kết quả**:
    * **Metric**: Tốc độ xử lý (Processing time), Accuracy (63.45%), Precision (74.24%).
    * **So sánh**: MLAR đạt 5.4s/CV, nhanh hơn Automation Anywhere (16.9%) và UiPath (17.1%).
* **Điểm mạnh**: Khả năng mở rộng (scalability) cực tốt, xử lý xong 2,400 CV chỉ trong 3.5 giờ; tích hợp luồng từ đầu đến cuối (e2e) từ đăng tuyển đến gửi mail.
* **Hạn chế**: Độ chính xác matching (63%) vẫn còn dư địa để cải thiện thông qua fine-tuning; kiến trúc còn phụ thuộc vào API bên ngoài (Gemini).
* **Insight rút ra**: Để xử lý lượng dữ liệu lớn, cần phân loại CV vào các nhóm ngành (Department) ngay từ bước parsing. Tốc độ và tự động hóa email là yếu tố "wow" đối với nhà tuyển dụng trong thực tế.
