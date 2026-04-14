# Tài liệu Kiến trúc Hệ thống Lõi: Pipeline 0 - Xử lý và Làm giàu Job Description (JD Enrichment) qua Mô hình Không gian Từ vựng Não Kép

> 📌 **File Code Triển Khai Thực Tế (Colab):** [preprocessJD_V2.ipynb](../../../code/jd_processing/preprocessJD_V2.ipynb)

Tài liệu này xác định ranh giới kỹ thuật tối cao cho ứng dụng đánh giá CV tự động. Trọng tâm của **Pipeline 0** là loại bỏ sự phụ thuộc mù quáng vào các mô hình tạo sinh (Black-box LLMs) dễ sinh ảo giác (Hallucination) và độ trễ cao. Biện pháp thay thế là một triết lý **Hybrid Extraction (GLiNER + S-BERT + Dual-Brain Ontology)** có tính Giải thích được (Explainable AI - XAI), có khả năng chạy độc lập, chi phí bằng Zero và độ tin cậy tiệm cận 100%.

---

## 1. Tầm nhìn và Mục tiêu Kiến trúc (Architectural Goal)
Chuyển đổi một đoạn văn bản JD phi cấu trúc, đầy tính văn chương mơ hồ thành một Vector Schema có tính định lượng khắt khe để phân giải lên Hệ tọa độ Ứng viên.

**Input (Đầu vào dạng văn bản phi chuẩn):** 
```text
"Tuyển Fullstack Dev. Yêu cầu 3 năm kinh nghiệm, chắc OOP. Ưu tiên có chứng chỉ AWS. Kỹ năng làm việc nhóm tốt."
```

**Output (Mô hình XAI Structured Output):**
```json
{
  "Metadata": {
    "Job_Title": "Fullstack Developer",
    "Processed_At": "2024-05-12T10:00:00Z"
  },
  "Hard_Constraints": {
    "Min_Experience_Years": 3,
    "Required_Degree": "Bachelor"
  },
  "Hard_Skills": {
    "Must_Have": {
      "Tech_Skills": ["OOP", "Python", "React.js"],
      "Certifications": []
    },
    "Nice_To_Have": {
      "From_JD_Desirable": ["AWS Certified", "Docker"],
      "From_Taxonomy_Expansion": ["Django", "FastAPI", "Vue.js"] 
    }
  },
  "Soft_Skills": [
    "Teamwork", 
    "Cross-functional Communication"
  ]
}
```

---

## 2. Chi tiết Triển khai các Bước (Step-by-Step Implementation)

### Bước 1: Khởi tạo Cơ chế "Não Kép" và Ngưỡng Vector (The Dual-Brain Ontology Engine)
Đây là "hồn cốt" của hệ thống. Hai bộ não này sở hữu quy tắc đo lường Cosine Similarity độc lập hoàn toàn nhau:
*   **Não Trái (Left Brain - `tech_ontology.json`):** Mạng đồ thị quy tắc nghiêm ngặt (Strict Graph). Phụ trách Công nghệ, Chứng chỉ tuyệt đối (AWS, PMP) và Fundamental CS (OOP, Algorithm). 
    *   *Chiến lược Vector:* Ưu tiên rà soát Exact String Match. Nếu dùng S-BERT, ngưỡng khoảng cách ngữ nghĩa (Distance Threshold) được thiết lập chung là **Threshold < 0.4**.
*   **Não Phải (Right Brain - `soft_skills_ontology.json`):** Mạng không gian mờ. Xử lý các câu giao tiếp đa nghĩa ("Làm việc nhóm", "Chịu áp lực số").
    *   *Chiến lược Vector:* Dùng chung ngưỡng khoảng cách ngữ nghĩa với Não Trái (**Threshold < 0.4**).

***Cơ sở Tối ưu Bộ nhớ (Memory & Indexing Design):***
Tuyệt đối KHÔNG gộp chung file JSON thành 1 vector khổng lồ duy nhất (điều này sẽ làm mất khả năng ánh xạ). Hệ thống sử dụng kỹ thuật **Danh sách Song song (Parallel Lists / Index Mapping)**:
* Việc làm phẳng (Flatten) Cây JSON nhiều nhánh được thực thi bằng một **Thuật toán Đệ quy (Recursive Algorithm)**. Đệ quy linh hoạt lặn xuống mọi ngóc ngách của Cây JSON bất kể độ sâu bao nhiêu tầng, từ đó bóc tách dữ liệu thành 2 danh sách song song: `Text_List` chứa các chữ gốc (Vd: "React.js") và `Metadata_List` (Sổ hộ khẩu) lưu giữ lại dấu vết đường đi của chữ đó (Vd: `Software_Dev -> Frontend -> Core_Frameworks`).
* Khi S-BERT trượt qua `Text_List` chứa 1000 chữ, nó đúc ra chính xác 1000 Vector độc lập, tạo thành Ma trận Không gian (Vector Matrix) có kích thước `[1000 x 384]`. Số Vị trí (Index) của Vector trong Ma trận bị khóa chặt vào Index của Sổ hộ khẩu.

### Bước 1.5: Phân rã văn bản và Xử lý vùng dữ liệu (Semantic Slicing & Chunking)
Đây là kỹ thuật then chốt để xử lý JD dài và phân loại mức độ ưu tiên:
1.  **Semantic Slicing (Greedy Regex Tags):** Sử dụng các cụm Regex đồng nghĩa để bao phủ các cách viết headers của HR:
    *   **Vùng Bắt Buộc (`MUST_ZONE`):** Nhận diện qua: `(essential|requirements|required|must have|key responsibilities|qualifications|technical expertise)`.
    *   **Vùng Ưu Tiên (`WISH_ZONE`):** Nhận diện qua: `(desirable|pluses|nice to have|preferred|advantage|plus|good to have)`.
2.  **Smart Stop Markers:** AI dừng chiết xuất khi gặp các tiêu đề ngoại vi như: `(benefits|what we offer|about company|closing date|equal opportunity)`.
3.  **Chunking:** Nếu một phân vùng dài quá 1500 ký tự (tương đương khoảng 200 từ), hệ thống tự động băm nhỏ thành các "Chunks" để GLiNER không bỏ sót dữ liệu.

### Bước 2: Bố ráp Thực thể bằng GLiNER và Regex (2-Pass Window Scanning)
Hệ thống chạy mô hình trên từng phân vùng và từng mảnh (Chunk) theo chiến thuật "Bắn tỉa 2 lượt":
1.  **Lượt 1 - Chuyên môn:** Quét các nhãn cứng: `["Job Role", "Technical Skill", "Methodology", "Tool", "Certification", "Domain Knowledge", "Language", "Education"]`.
2.  **Lượt 2 - Kỹ năng mềm:** Quét riêng nhãn `["Soft Skill"]` để tránh bị nhiễu bởi thuật ngữ kỹ thuật, đảm bảo độ nhạy tối đa.
*   **Deterministic Regex:** Cấy Regex vào luồng để bắt ép các Ràng buộc cứng (Số năm kinh nghiệm, Độ học vấn) vì cấu trúc số rất quy chuẩn và chống sai số suy luận AI tuyệt đối.

### Bước 3: Ánh xạ Không gian Song song & Hậu kiểm Phân loại (Mapping & Category Correction)
Những dải danh từ do GLiNER ném ra sẽ được chuẩn hóa (`replace("-", " ")`) và ánh xạ vào Taxonomy:

*   **Hậu kiểm Phân loại (Category Correction):** Đây là chốt chặn tinh vi. Nếu một thực thể bị GLiNER gán nhãn `Certification` nhưng khi tra cứu S-BERT lại khớp với dữ liệu thuộc nhánh `Tools` trong Taxonomy, hệ thống sẽ tự động chuyển nó về đúng rổ `Tech_Skills` (Ví dụ: Chuyển Apple Carplay từ Certification sang Tool).
*   **Cơ chế Nhìn Ngược (Reverse Lookup):** Khi thuật toán Đại số tìm ra độ khớp giữa cụm từ JD và Ma trận Não bộ, hệ thống tra cứu ngược ra cành gốc sinh ra nó. 
*   **Bảo hiểm Điểm mù - Out Of Vocabulary (OOV) Fallback:** Nếu không tìm thấy cụm từ trong Taxonomy, hệ thống thiết kế bắt buộc phải nhét nguyên cụm chuỗi thô vào `Must_Have_Skills` để đảm bảo không đánh rơi yêu cầu sống còn của HR.

### Bước 4: Lan truyền Thuật toán Đồ thị & Giới hạn Nhiễu (Top-K Enrichment)
Đây chính là khâu làm nên chữ **"Enrichment" (Làm giàu)** xuất chúng của hệ thống mà không vướng Ảo giác (Hallucination).

1.  **Ghim tọa độ (Point-of-Impact):** GLiNER cắm mũi kim vào Node gốc trên Não Trái.
2.  **Chiết xuất Tương đồng (Sibling Extraction):** Kéo các Node đồng cấp (Sibling) vào rổ `Taxonomy_Expansion`.
3.  **Lọc nhiễu Top-K:** Chỉ lấy tối đa **10 hàng xóm gần nhất** từ Taxonomy để đảm bảo rổ Nice-to-have luôn tập trung và tinh khiết, tránh quá tải thông tin.
4.  **Lưới Lọc Trùng Lặp Toán Học (Set Difference Deduplication):** Loại bỏ các kỹ năng Expansion đã tồn tại trong mảng Must-have của chính bản JD đó.
5.  **Lệnh cấm Não Phải (Strict Ban on Soft Skills Expansion):** Tuyệt đối không dùng thuật toán này cho Khối kỹ năng mềm để bám sát định hình tính cách gốc do HR yêu cầu.

---

### Triết lý Thiết kế: Tại sao phải tách biệt Nice-to-Have? (XAI Explained)
Việc chia nhỏ giỏ "Nice-to-Have" thành 2 nguồn gốc riêng biệt (`From_JD_Desirable` và `From_Taxonomy_Expansion`) là một quyết định chiến lược về mặt **Giải thích được (Explainable AI)**:

*   **Tính Công bằng trong Chấm điểm (Scoring Weighting):** Kỹ năng do Nhà tuyển dụng trực tiếp ghi (Desirable) có trọng số ưu tiên cao hơn hẳn so với kỹ năng do trí tuệ nhân tạo tự suy luận (Expansion). Việc tách biệt cho phép Thuật toán Ranking áp dụng các hệ số nhân (Multipliers) khác nhau cho từng nhóm.
*   **Tính Minh bạch (Transparency):** Người dùng (HR) có thể truy vết được đâu là yêu cầu gốc của họ và đâu là gợi ý từ hệ thống tri thức chuyên gia. Điều này xây dựng niềm tin vào kết quả xếp hạng.
*   **Kiểm soát Ảo giác (Hallucination Guardrail):** Việc tách riêng giúp hệ thống dễ dàng đặt ra các ngưỡng giới hạn (Top-K) cho phần mở rộng, tránh tình trạng tri thức hệ thống làm "loãng" các yêu cầu thực tế của công việc.
*   **Giá trị Nghiên cứu:** Trong báo cáo NCKH, đây là minh chứng cho việc ứng dụng **Mô hình Phân tầng Ưu tiên (Hierarchical Priority Mapping)** thay vì gộp chung dữ liệu (Flat Data).

---

## 3. Tổng kết Quản trị Rủi ro (Edge Cases Governance)

1.  **Dải Tần Sinh viên (Interns / Freshers):** Sinh viên không có bề dày dự án thực tiễn (Framework). Hệ thống xử lý xuất sắc nhóm này nhờ cành tri thức `Computer_Science_Fundamentals` (OOP, Thuật toán, Cấu trúc dữ liệu...) nằm sâu trong Não Trái làm mỏ neo từ khóa vô cùng chuẩn xác.
2.  **Chứng chỉ Quy ước (Certifications):** Tách biệt với tư duy cũ, mọi "Chứng chỉ" (Kể cả IELTS, Scrum Master) trong NLP System được đối xử như **Kỹ năng Cứng tuyệt đối** (Nằm tại Não Trái). Bởi vì tên của chứng chỉ là dãy ký tự được chuẩn hóa toàn cầu. Áp dụng Vector Mềm (Fuzzy match) lên chứng chỉ chỉ gây tốn tài nguyên và dễ nhiễu.

---

## 4. Tuyên bố Thành tựu Cấp Hệ thống (Architecture Supremacy)

1.  **Minh Bạch Toán Học (White-box AI):** Bất kể hành vi nào của luồng code (Nhặt 1 skill, Sinh ra thêm 1 skill Nice-to-have, Đánh trượt ứng viên) đều do Toán Học Vector/Graph Tree quyết định và có ID truy vết tới gốc rễ.
2.  **Chi phí Zero - Tốc độ Millisecond (Ultra-Fast & Free):** Sự giao thoa của S-BERT và GLiNER (encoder-only models) thu gọn quy trình đánh giá hàng nghìn thẻ CV xuống ngưỡng ~0.25 giây trên tài nguyên CPU Local rẻ tiền. Băng thông và Token API của Big Tech (OpenAI/Anthropic) bị triệt tiêu hoàn toàn. Khắc phục được nhược điểm "Chết vì Chi Phí" của các Startups công nghệ.
3.  **Khả năng Chống chọi Rủi Ro (Foolproof / Anti-Brittle):** Sự bọc lót chéo cánh giữa *GLiNER (Thực thể đa dạng) - Regex (Mỏ neo số tuyệt đối) - S-BERT (Bắt sai chính tả) - OOV Mapping (Chống rớt Skill mới)* giúp mô hình đứng vững dẫu HR tải lên một JD với chất lượng viết lách rất tồi.
