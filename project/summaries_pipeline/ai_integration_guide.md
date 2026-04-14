# Hướng Dẫn Tích Hợp Dịch Vụ AI: Hệ Thống Xếp Hạng CV
*(Tài liệu dành riêng cho Software Engineer / Backend Developer)*

## 1. Lời Mở Đầu
Tài liệu này được thiết kế để giải thích luồng tích hợp của dịch vụ AI Đánh giá CV bằng ngôn ngữ phần mềm thông thường, bỏ qua các thuật ngữ Toán học và AI học thuật phức tạp. Mục tiêu là giúp **Đội ngũ Phát triển Phần mềm (Software Engineers)** trích xuất đúng đầu vào, dự đoán đúng đầu ra, và chuẩn bị tài nguyên cài đặt đúng cách.

Tóm tắt lại, cục AI này là một "Chiếc phễu". Hệ thống chỉ cần bạn thả vào đó 1 file Yêu cầu công việc (JD) và 1000 file CV (những thứ chưa qua dọn dẹp), nó sẽ dọn dẹp, xử lý và trả về cho bạn các bảng điểm (dưới dạng tập tin JSON/CSV) xếp hạng CV từ cao xuống thấp.

---

## 2. Yêu Cầu Về Hạ Tầng, Tài Nguyên & Lưu Trữ (Infrastructure & Storage)

Vì AI đã được thiết kế tối ưu hóa chi phí, bạn không cần thiết lập máy chủ có GPU đắt tiền.
*   **Máy chủ (Compute):** Thuật toán sử dụng các mô hình cực nhỏ (như GLiNER / S-BERT) có khả năng chạy tốt và tiết kiệm chỉ bằng CPU Server máy trạm thông thường (Ví dụ: 4-8 Cores, 8-16GB RAM) là đủ để xử lý hàng ngàn CV.
*   **External API Key:** Khi xử lý CV ở bước dùng AI Gemini 3.1 Flash Lite siêu tốc, Server cần có quyền ra mạng internet và truy cập API Key thông qua biến môi trường `.env`.
*   **Lưu trữ Database Cục Bộ - KHÔNG CẦN CHẠY LẠI TAXONOMY (Quan trọng):**
    *   Trong quá trình nghiên cứu, Hệ thống cây từ điển đa ngành (Taxonomy) đã được Đội AI xử lý làm sạch, chuẩn hóa và vector hoá xong xuôi một lần duy nhất.
    *   Thành phẩm tạo ra là một cơ sở dữ liệu Vector Database vô cùng gọn nhẹ bằng ChromaDB. Đội phần mềm chỉ việc lấy thư mục `data/chroma_db/` (trong đó có cục `chroma.sqlite3`) đính kèm ngang hàng với Database vào thư mục mã nguồn Backend (tương tự như cách tích hợp file SQLite). 
    *   Khi gọi luồng chấm điểm, Code AI chạy dưới quyền read-only truy vấn thẳng vào cục cơ sở dữ liệu có sẵn này cự ly siêu tốc. **Tuyệt đối không cần gọi model hoặc tính toán khởi tạo lại cấu trúc Taxonomy nữa**.

---

## 3. Luồng Dữ Liệu & Quy Chuẩn Vào/Ra (Pipelines & I/O Contracts)

Luồng hoạt động của hệ thống chia làm 3 bước. Sau mỗi khâu tốn thời gian, AI đều trả ra dữ liệu định dạng chuẩn, các Kỹ sư Backend chỉ việc lưu cục JSON này xuống Database để dùng thẳng, không cần bắt AI chạy lai rai từ A-Z gây timeout hệ thống.

### BƯỚC 1: Tiền Phân Tích Kỹ năng từ Yêu cầu công việc (JD Pipeline)
*Giai đoạn này được Back-end cấu hình chạy 1 lần duy nhất mỗi khi HR đăng một tin tuyển dụng mới.*
*   **Làm cái gì (Mô tả):** Máy sẽ đọc bài văn tự do của HR. Nó bắt đầu chia cắt văn bản ra các nhóm ý, sau đó "gắp" ra rành mạch các yêu cầu cứng cỏi (Độ tuổi giáo dục, Kỹ năng chuyên môn Bắt buộc) và những phẩm chất giao tiếp (Kỹ năng mềm). Hơn thế nữa, AI kết nối với Cây tri thức CSDL (Taxonomy) để chủ động nhận diện và "giãn nở" yêu cầu: nó tự động đề xuất 10 kỹ năng họ hàng gần nhất với công ty để đưa vào diện "Nếu ứng viên có thì càng tốt" (Nice-to-have). Quá trình này khử rác, chắt lọc yêu cầu thật mượt để so tiêu chuẩn.
*   **Công cụ/Công nghệ sử dụng (How to execute):**
    *   Sử dụng mô hình AI nhận diện thực thể cực nhẹ **GLiNER** (`urchade/gliner_multi-v2.1`) kết hợp với hàm Regex của Python để quét phân vùng (Must vs Nice-to-have).
    *   Sử dụng mô hình **S-BERT** (`all-MiniLM-L6-v2`) để dò tìm 10 kỹ năng mở rộng (Sibling Expansion) từ Hệ tri thức **ChromaDB_Taxonomy**.
    👉 *Chi tiết cơ cấu cụ thể gọi hàm nào, ngưỡng ra sao, Developer đọc tại tài liệu đặc tả:* [pipelineProcessJD.md](../pipeline/pipeline_process_JD/pipelineProcessJD.md) 
*   **Input Server bơm vào:** Text thuần (String đoạn văn mảng chữ cái dài) mô tả yêu cầu JD do quy trình HR input.
*   **Output Cục AI xuất trả ra:** 1 File/Cấu trúc **`JSON` chuẩn hoá** (định dạng như file mẫu `JD_BA_1_cleaned.json` trong thư mục `data/Cleaned_JD_V2/`). Object JSON này chứa một rổ tham số rõ ràng đã phân loại: Hard Constraints, Hard Skills (Must-have, Expansion), và Soft Skills.

### BƯỚC 2: Tiền Xử Lý & Bóc Tách Gen Hồ Sơ ứng viên (CV Preprocessing & DNA Extraction)
*Giai đoạn chạy bất cứ khi nào ứng viên nhấp Submit 1 CV mới lên hệ thống. Đưa tác vụ này vào Message Queue xử lý ngầm (Background Job/Workers).*
*   **Làm cái gì (Mô tả):** Hệ thống chia vế rõ ràng ranh giới giữa việc dùng LLM và máy quét nội bộ:
    1. **Giai đoạn Tái cấu trúc bằng LLM Cloud (Gọi mạng):** Sau khi tiền xử lý cơ bản thì ta thực hiện gọi LLm tái cấu trúc lại CV. Do CV của ứng viên thường trình bày cực kỳ tự do, dài dòng và lộn xộn dọc ngang, chúng ta mang đoạn văn bản này ném lên gọi API thẳng cho **LLM (Mô hình ngôn ngữ lớn Google Gemini)** xử lý. LLM đóng vai trò người đọc hiểu văn bản: nó bóc rách CV ra, gom ý và nặn ép tóm tắt lại và nhét rành mạch nội dung vào đúng 5 thẻ dạng XML rạch ròi (`<INFORMATION>`, `<SUMMARY>`, `<SKILLS>`, `<EXPERIENCE>`, `<EDUCATION>`). Nếu CV quá rườm rà (>2000 từ), LLM áp dụng lệnh ép thu gọn. Khâu chờ LLM nhả kết quả tốn độ trễ vài giây mạng, dễ dính Rate Limit nên phải tống vào chạy ngầm. Sau đó ta xử lý lưu lại thành file json.
    2. **Giai đoạn Quét DNA (Chạy Local tại máy chủ):** Lấy đoạn XML rất chuẩn sạch mà LLM nhả ra bên trên, hệ thống ngắt hoàn toàn kết nối mạng và chỉ sử dụng CPU máy chủ nội bộ để chạy 3 công đoạn nhỏ:
        *   **Bóc tách Tự động (Header Parser):** Trích xuất tự động 7 trường hành chính cốt lõi (Tên, SDT, Email, LinkedIn, Chức danh, Trần kinh nghiệm...) bằng thuật toán cắt theo nhãn.
        *   **Khoanh vùng Thực thể (Zonal NER):** Máy quét AI cục bộ sẽ trượt qua các khối. Nó tự động thay đổi "tiêu cự lọc": ở vùng văn xuôi dài dòng nó bắt chặt chẽ để lọc nhiễu (ngưỡng 0.4), còn ở vùng gạch đầu dòng liệt kê kỹ năng nó thả lỏng (ngưỡng 0.15) để vớt trọn bộ tệp kỹ năng cứng, công cụ, ngôn ngữ mà ứng viên liệt kê không bỏ sót từ nào.
        *   **Nội suy Năm Kinh nghiệm (Logic Toán học):** Với mỗi công nghệ sinh ra (VD: "ReactJS"), thuật toán lập trình Python thuần túy sẽ ngắt khối công việc đó ra, lấy Regex dò tìm "Ngày/Tháng bắt đầu - kết thúc". Đặc biệt nếu ứng viên làm ReactJS ở 2 dự án song song đè lên nhau cùng thời điểm, code sẽ chạy thuật toán "Hợp nhất khoảng thời gian" (Interval Merging) để nén chung lại chốt thâm niên đúng chuẩn thực tế thay vì cộng nhồi sai lệch.
    3. **Giai đoạn Tiêu chuẩn hóa & Neo Giữ (Taxonomy Mapping):** Hàng tá kỹ năng rác vừa nặn nọn xong sẽ được cấp mỏ neo bằng chức danh gốc (Ví dụ để phân biệt "Java" là kỹ năng backend). Toàn bộ được nhồi vào điểm CSDL nền tảng đối chiếu để quy đổi thẳng từ những từ khóa viết tắt/lỗi thành mã danh pháp chuyên chuẩn duy nhất của Cty (Taxonomy ID).
*   **Công cụ/Công nghệ sử dụng (How to execute):**
    *   Sử dụng API gọi ra mạng ngoài: **LLM Cloud (Google Gemini 3.1 Flash Lite Preview)** chuyên phụ trách đọc hiểu và nặn lại bộ khung bố cục xương sống (Segmentation/Summarization) cho phần 1.
    *   Sử dụng AI cục bộ: Mô hình siêu nhẹ nạp bằng RAM nội bộ **GLiNER** (`urchade/gliner_multi-v2.1`) chạy hàm Chunking 200 từ trên từng phân khúc cho phần 2.
    *   Sử dụng đối chiếu: Hệ mã hoá **S-BERT** (`all-MiniLM-L6-v2`) đâm vào `ChromaDB` quy đổi mã ngắt tại khoảng cách `< 0.4` cho phần 3.
    👉 *Chi tiết cấu hình cách LLM prompt ra sao, thuật toán nội suy ngày tháng hoạt động thế nào, Developer đọc mã chẩn đoán tại:* [preprocessDataCV.md](../pipeline/CV/preprocessDataCV.md) và luồng khai phá GLiNER DNA ở [cv_dna_colab_v1.md](../pipeline/CV/cv_dna_colab_v1.md).
*   **Input Server bơm vào:** Text thô cực kỳ lộn xộn độ dài lớn, trích xuất (OCR) từ file tải DOCX/PDF của hệ thống.
*   **Output Cục AI xuất trả ra:** 1 File/Cấu trúc **`JSON` chứa Hồ sơ DNA (DNA Profile)**. Dữ liệu mảng Object siêu tinh luyện liệt kê người này có mã kỹ năng tiêu chuẩn nào, thâm niên "float value" là bao nhiêu năm, bằng cấp v.v. 

### BƯỚC 3: Quy Trình Cân Đo Chấm Điểm & Xếp Hạng (Composite Scoring)
*Khâu tính nhẩm toán học, máy tính làm cực nhẹ (< 1s), Backend có thể thiết kế API chạy gọi đồng bộ (Synchronous API) khi User mở giao diện chiến dịch tuyển dụng mong muốn xuất bảng xếp rank.*
*   **Làm cái gì (Mô tả):** Đây là bàn cân điện toán. Nó cầm bảng JSON JD cực nhỏ đọ sức với hàng ngàn bảng JSON CV. Máy tính tiến hành mô phỏng một "Ứng viên hoàn hảo" dựa trên bộ kỹ năng yêu cầu và số năm kinh nghiệm tối thiểu trong JD (`Min_Experience_Years`) để làm thước đo chuẩn (Mẫu số 100%). Sau đó, năng lực thực tế của ứng viên sẽ được đem cân đong với thước đo này. Lượng năm thâm niên của ứng viên sẽ được khuyếch đại bù trừ đòn bẩy bằng phép toán Logarit để cho ra điểm công bằng nhất. Với ứng viên sở hữu năng lực thặng dư dầy đặc so với nhu cầu, toàn bộ lượng tài sản vượt trội đó sẽ đẩy vào rổ "Thưởng Vượt Trình" (Bonus) thay vì bị vứt bỏ.
*   **Công cụ/Công nghệ sử dụng (How to execute):**
    *   Bảo lưu toàn bộ máy móc AI ở vạch xuất phát, khâu này chạy tốc độ **thuần bằng ngôn ngữ Python cơ bản**, bằng cách lập trình (Code Logic) các quy tắc Toán Đa Chiều (Thuật toán Jaccard tĩnh, Multipliers Mảng Logarit bằng bộ mã thư viện Pandas / NumPy mặc định). Không dùng LLM hay ML nên tuyệt đối không tốn Token rate hay nặng RAM GPU.
    👉 *Chi tiết cấu trúc thuật toán đếm điểm, tỷ lệ hàm và trọng lượng chia chác cho Code Logic Toán học này, Developer khai thác sâu tại:* [composite_scoring_pipeline.md](../pipeline/pipline_evaluate/composite_scoring_pipeline.md).
*   **Input Server bơm vào:** 1 Hàm tính toán Data nhận 2 tham số: `Object JSON gốc của JD` và một `Mảng List (Array) các Object JSON DNA ứng viên`.
*   **Output Cục AI xuất trả ra:** Kết quả trả thẳng **1 object Data Frame / bảng dạng `CSV` (Table).**
    Bảng dữ liệu trả về cho Backend chỉ bao gồm đúng **04 Cột Toán học**:
    1.  `Candidate` (Định danh chuỗi Tên / ID duy nhất đối chiếu cho 1 ứng viên đối với JD).
    2.  `Base_Score` (Điểm tích lũy sàn. Hạn mức điểm thành quả ứng viên đó thỏa mãn JD bị ngắt chóp tại 100/100).
    3.  `Bonus_Score` (Điểm thưởng bùng nổ vinh danh, nằm ở ngoài barem JD chính quy do kinh nghiệm overqualified dồi dào).
    4.  `Total_Score` (Cộng gộp 2 cột Base và Bonus để làm cột tiêu chuẩn cho Front-End Data Table làm Order By từ cao xuống).

👉 *Backend Developer chỉ việc tống Input văn bản Cứng vào 2 API đầu đẻ ra 2 khối JSON rồi nhét lưu CSDL. Lúc List ứng viên thi tuyển JD thì bơm vào hàm số 3 trả về đúng 4 Cột File CSV đổ ra Interface. Tiến trình tích hợp khép kín 100%!*
