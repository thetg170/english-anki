# Business Analysis: học để xử lý công việc

Deck [Business Analysis](../source/business-analysis/notes.csv) có 108 thẻ trong một deck, phân theo nhãn chủ đề, loại thẻ và độ khó. Mỗi thẻ yêu cầu tự trả lời trước khi lật; mặt sau có đáp án ngắn, lý do và liên kết nguồn. Không có TTS hoặc media.

## Lộ trình

| Thứ tự | Chủ đề | Thẻ | Năng lực trọng tâm |
|---:|---|---:|---|
| 1 | BA Foundations & BACCM | 9 | Tìm need, stakeholder, context và value trước solution |
| 2 | Requirements Classification | 8 | Phân biệt mục tiêu, nhu cầu, năng lực và yêu cầu chuyển đổi |
| 3 | Elicitation & Stakeholders | 8 | Hỏi, quan sát, xác nhận và xử lý ý kiến mâu thuẫn |
| 4 | Requirements & Artifacts | 10 | Chọn BRD/SRS/story/criteria theo mục đích; viết rõ |
| 5 | Business Process & BPMN | 8 | Vẽ luồng, trách nhiệm, điều kiện và ngoại lệ |
| 6 | UML & System Modeling | 8 | Dùng use case, sequence và state khi có ích |
| 7 | Agile & Scrum | 8 | Hiểu accountability của PO, Sprint Goal và backlog |
| 8 | Prioritization & Change | 8 | Ưu tiên theo value, dependency và impact |
| 9 | Data, SQL & API | 8 | Hiểu quan hệ dữ liệu, JOIN, contract và request lặp |
| 10 | Verification, Validation & UAT | 9 | Kiểm tra chất lượng mô tả, nhu cầu và nghiệm thu |
| 11 | Business Rules & Edge Cases | 8 | Phát hiện tổ hợp điều kiện, ranh giới và lỗi |
| 12 | Product Value & KPI | 8 | Phân biệt output/outcome và chọn thước đo |
| 13 | Real-world BA Decisions | 8 | Thu thập dữ kiện và giải trade-off |

Mỗi loại thẻ có 27 câu: Concept Recall, Practical Application, Scenario Thinking và Artifact Review. Học nhóm 1–4 để có nền, sau đó kết hợp nhóm 5–13 theo công việc đang gặp. Với thẻ tình huống, đáp án là một hướng hợp lý theo điều kiện ghi trên thẻ, không phải quy trình duy nhất.

## Cách học

1. Đọc mặt trước, nói hoặc viết một quyết định và lý do ngắn.
2. Lật thẻ, so sánh ý chính với đáp án. Một hướng khác có điều kiện và trade-off hợp lý cũng có thể chấp nhận.
3. Với Artifact Review, thử viết lại requirement hoặc criterion bằng ví dụ của dự án thật.
4. Ghi trường hợp chưa giải được; bổ sung thẻ mới có Key ổn định sau khi xác nhận nguồn.

BRD, SRS, user story, BPMN và Scrum không bắt buộc cho mọi dự án. BA, Product Owner, Project Manager và QA có thể phối hợp hoặc chồng lấn nhiệm vụ tùy tổ chức; Scrum Guide chỉ quy định accountability trong Scrum.

## Nguồn

Nội dung thẻ được diễn giải, không chép nguyên văn. Trường Source của từng note dẫn tới nguồn tương ứng:

- [IIBA The Business Analysis Standard](https://www.iiba.org/knowledgehub/the-business-analysis-standard/) và [requirements classification](https://www.iiba.org/knowledgehub/the-business-analysis-standard/4-implementing-business-analysis/4-4-understanding-requirements-and-designs/): BACCM, requirement types, analysis và value.
- [IIBA BABOK Glossary](https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/glossary/): verification, validation và traceability.
- [IIBA Agile Extension](https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/agile-extension/): phân tích liên tục, ưu tiên value và feedback.
- [Scrum Guide 2020](https://scrumguides.org/scrum-guide.html): Product Owner, Sprint Goal và Product Backlog.
- [OMG BPMN 2.0.2](https://www.omg.org/spec/BPMN/) và [UML 2.5.1](https://www.omg.org/spec/UML/2.5.1): ký pháp quy trình và hệ thống.
- [PostgreSQL SQL tutorial](https://www.postgresql.org/docs/current/tutorial-sql.html), [RFC 9110 HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html), [OpenAPI Specification](https://spec.openapis.org/oas/latest.html): dữ liệu và API.

## Mở rộng

Batch tiếp theo nên dựa trên ca thật đã gặp: thêm một tình huống, câu hỏi ra quyết định và artifact cần sửa. Ưu tiên trường hợp có sai sót hoặc quyết định khó hơn việc thêm nhiều thuật ngữ. CSV là source of truth của nội dung note; backup Anki vẫn cần để giữ lịch ôn.

Batch đầu đã được nhập ngày 11/11/2026. Bản sao lưu đầy đủ ngay trước thao tác ở `private/backups/2026-11-11-before-business-analysis/`; bản sao lưu trước khi hoàn tất lượt nhập ở `private/backups/2026-11-11-business-analysis-resume/`. Chạy `tools/cards.py validate` rồi `diff` với CSV này trước các lần chỉnh sửa tiếp theo.
