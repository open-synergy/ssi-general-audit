[![Build Status](https://travis-ci.com/open-synergy/ssi-general-audit.svg?branch=14.0)](https://travis-ci.com/open-synergy/ssi-general-audit)
![pre-commit](https://github.com/open-synergy/ssi-general-audit/actions/workflows/pre-commit.yml/badge.svg)
[![codecov](https://codecov.io/gh/open-synergy/ssi-general-audit/branch/14.0/graph/badge.svg)](https://codecov.io/gh/open-synergy/ssi-general-audit)

<!-- /!\ do not modify above this line -->

# ssi-general-audit

Kumpulan modul Odoo 14 untuk mengelola proses **General Audit (Audit Umum atas Laporan Keuangan)** secara end-to-end, mengikuti **International Standards on Auditing (ISA)** / **Standar Audit Indonesia (SA)**.

Repository ini mengimplementasikan seluruh siklus audit — dari penerimaan perikatan hingga penerbitan laporan auditor independen — dalam bentuk **worksheet (kertas kerja)** digital yang saling terhubung.

## Arsitektur

- **Modul utama** (`ssi_general_audit`) mengelola objek *General Audit* (perikatan, tim, periode, materialitas, status engagement).
- **Modul core** (`ssi_general_audit_core`) menyediakan shared models dan infrastruktur dasar.
- **Modul worksheet** (`ssi_general_audit_worksheet_*`) masing-masing merepresentasikan satu atau lebih kertas kerja pada fase audit tertentu.
- Setiap worksheet diidentifikasi dengan **kode 7-karakter** (mis. `a033cc6`) dan di-publish sebagai model `general_audit_ws_<kode>`.
- Semua worksheet mewarisi `general_audit_worksheet_mixin` dan mengikuti alur status: **Draft → Open → Confirm → Done**.

## Daftar Modul per Fase Audit

### Fase 0 — Core & Infrastruktur

| Modul | Deskripsi | Standar |
|-------|-----------|---------|
| `ssi_general_audit` | Modul utama: manajemen engagement audit — perikatan, tim, periode, materialitas, status | SA 200/220/230/315/320/450/520 |
| `ssi_general_audit_core` | Shared models dan infrastruktur dasar untuk semua modul worksheet | — |

### Fase 1 — Pra-Perikatan (Pre-Engagement)

Sebelum menerima atau melanjutkan perikatan, auditor wajib menilai risiko perikatan, independensi, dan kelayakan klien (ISA 220/SA 220, ISA 210/SA 210).

| Modul | Deskripsi | Standar |
|-------|-----------|---------|
| `ssi_general_audit_worksheet_acceptance_continuance` | 7 WS: penilaian penerimaan/keberlanjutan klien — due diligence, latar belakang klien, konfirmasi partner, anti pencucian uang (PMPJ) | SA 220/300/PMPJ |
| `ssi_general_audit_worksheet_assignment_letter` | WS c435bcd: Assignment Letter Checklist — verifikasi kelengkapan surat penugasan internal | SA 220/300 |
| `ssi_general_audit_worksheet_engagement_letter_checklist` | WS d8aaebc: Engagement Letter Checklist — verifikasi ketentuan perikatan dengan klien | ISA 210/SA 210 |
| `ssi_general_audit_worksheet_independence_statement` | WS 09253fe: Independence Statement — pernyataan independensi seluruh tim audit sesuai IESBA Code of Ethics | ISA 200/SA 200 |

### Fase 2 — Perencanaan (Planning)

Auditor menyusun strategi audit keseluruhan dan rencana audit, termasuk alokasi sumber daya, komunikasi tim, dan kebutuhan tenaga ahli (ISA 300/SA 300).

| Modul | Deskripsi | Standar |
|-------|-----------|---------|
| `ssi_general_audit_worksheet_audit_working_plan` | WS cbbbaf4: Audit Working Plan — rencana kerja tim, alokasi jam (man-hours), kompetensi anggota tim | ISA 300/220 |
| `ssi_general_audit_worksheet_team_communication` | 2 WS: komunikasi tim pra-perikatan (437fc8f, ISQC 1/SA 220) dan briefing penilaian risiko (b1f820c, ISA 315) | ISQC 1/SA 220/ISA 315 |
| `ssi_general_audit_worksheet_expert` | 2 WS: evaluasi penggunaan ahli auditor (bab9d32) dan ahli manajemen (cda3a68) | ISA 620/500 |
| `ssi_general_audit_worksheet_external_communication` | 4 WS: jadwal komunikasi (ae48e68), komunikasi dengan manajemen (b3ff42f), TCWG (c94e287), dan auditor internal (d133f46) | ISA 260/265/610 |

### Fase 3 — Pemahaman Entitas & Penilaian Risiko

Auditor memahami entitas dan lingkungannya, menentukan materialitas, dan menilai risiko salah saji material (Risk of Material Misstatement/ROMM) pada tingkat laporan keuangan maupun asersi (ISA 315/SA 315).

| Modul | Deskripsi | Standar |
|-------|-----------|---------|
| `ssi_general_audit_worksheet_understanding_entity` | 10 WS: pemahaman entitas — lingkungan bisnis, sistem IT, pengendalian internal, going concern, pihak berelasi, ketidakpatuhan regulasi | ISA 315/240/250/402/550/570 |
| `ssi_general_audit_worksheet_preliminary_analytic_procedure` | 3 WS: prosedur analitis awal — analisis horizontal (b32655a), vertikal (d4289e4), dan rasio keuangan (c8740d4) | ISA 315/520 |
| `ssi_general_audit_worksheet_preliminary_materiality` | 3 WS: penentuan materialitas — pemilihan benchmark (d9d2b44), overall materiality (6dcda0e), performance materiality (1d9338d) | ISA 320 |
| `ssi_general_audit_worksheet_planning_memorandum` | 2 WS: memorandum perencanaan audit (a753ab9) dan ringkasan strategi audit keseluruhan (fbbe0f8) | ISA 300 |
| `ssi_general_audit_worksheet_inherent_risk` | 3 WS: risiko inheren per akun (bfb6dae), risiko kecurangan (a418d89), risiko kelangsungan usaha (c16abd7) | ISA 315/240/570 |
| `ssi_general_audit_worksheet_control_risk` | 6 WS: risiko pengendalian — walkthrough dan uji efektivitas desain & implementasi pengendalian internal | ISA 315/330 |
| `ssi_general_audit_worksheet_romm` | 3 WS: Risk of Material Misstatement (ROMM) — agregasi risiko salah saji material per asersi akun (c165170, d66d87a, de417a6) | ISA 315 |

### Fase 4 — Pelaksanaan Audit (Fieldwork)

Auditor mengumpulkan bukti audit yang cukup dan tepat melalui berbagai prosedur: inspeksi, observasi, konfirmasi, inquiry, recomputation, reperformance, dan prosedur analitis substantif (ISA 500/SA 500, ISA 330/SA 330).

| Modul | Deskripsi | Standar |
|-------|-----------|---------|
| `ssi_general_audit_worksheet_trial_balance` | WS a033cc6: Trial Balance — neraca saldo klien sebagai basis seluruh prosedur audit | ISA 230 |
| `ssi_general_audit_worksheet_client_package` | 5 WS: dokumen dari klien — saldo akun, rekonsiliasi, konfirmasi, daftar transaksi | ISA 240/500/315 |
| `ssi_general_audit_worksheet_lead_schedule` | 3 WS: lead schedule semua akun (b26d482), per tipe akun (f9f3299), prosedur audit kunci per tipe akun (e51bb1c). Termasuk master data audit procedure | ISA 230/300 |
| `ssi_general_audit_worksheet_population` | WS a01723b: Population — definisi populasi data untuk sampling statistik (menggunakan tabulate/pandas) | ISA 530/500 |
| `ssi_general_audit_worksheet_specific_procedure` | 5 WS: prosedur spesifik — inventaris (a8f4d88), estimasi akuntansi (c40cfd9), pihak berelasi (cb82c5f), subsequent events (fbf57ee), going concern (ee819ae) | ISA 501/540/550/560/570 |
| `ssi_general_audit_worksheet_test_of_detail` | 2 WS: rencana pengujian rinci (b7df2d5) dan pelaksanaan Test of Detail (a916660) dengan analisis data via numpy/pandas | ISA 500/330/530 |
| `ssi_general_audit_worksheet_audit_procedure_analytic` | 2 WS: prosedur analitis substantif — perencanaan dan pelaksanaan | SA 520/330 |
| `ssi_general_audit_worksheet_audit_procedure_confirmation` | WS: Confirmation — konfirmasi langsung kepada pihak ketiga (debitur, bank, pengacara) | ISA 505 |
| `ssi_general_audit_worksheet_audit_procedure_inquiry` | WS a145276: Inquiry — prosedur tanya-jawab/wawancara dengan manajemen dan karyawan | ISA 500/240 |
| `ssi_general_audit_worksheet_audit_procedure_observation` | WS d4d1ac0: Observation — pengamatan langsung atas aktivitas/proses klien | ISA 500/315/330 |
| `ssi_general_audit_worksheet_audit_procedure_recompute` | WS c6c86fd: Recomputation — perhitungan ulang angka-angka keuangan | ISA 500/330/520 |
| `ssi_general_audit_worksheet_audit_procedure_reperformance` | WS d1ecfb7: Reperformance — pelaksanaan ulang kontrol/proses klien | ISA 500/330 |
| `ssi_general_audit_worksheet_test_of_control` | WS e3f4a5b: Test of Control — pengujian efektivitas operasional pengendalian internal klien melalui attribute sampling statistis berbasis tabel AICPA | ISA 330/530 |

### Fase 5 — Penyelesaian & Pelaporan (Completion & Reporting)

Auditor mengevaluasi kecukupan bukti, menilai salah saji yang belum dikoreksi, mereview kualitas audit, menyusun draft laporan, dan menerbitkan laporan auditor independen (ISA 700/SA 700 series).

| Modul | Deskripsi | Standar |
|-------|-----------|---------|
| `ssi_general_audit_worksheet_final_materiality` | 3 WS: evaluasi materialitas akhir, daftar salah saji, dan keputusan koreksi/waiver | ISA 320/450 |
| `ssi_general_audit_worksheet_audit_result` | 4 WS: ringkasan hasil audit (a0319a2), temuan pengendalian internal (d33420f), komunikasi ke manajemen (ab19fd4), komunikasi ke TCWG (bc3e272) | ISA 260/265/450/700/705 |
| `ssi_general_audit_worksheet_review` | 6 WS: review kualitas audit (bcc0d76), evaluasi kecukupan bukti (cae598e), checklist bukti (dae9f3c), checklist pengungkapan LK (a025441), review pengungkapan (be62e79), review laporan auditor (fc75636) | ISA 500/700/705 |
| `ssi_general_audit_worksheet_draft_reporting` | 6 WS: management letter (ae598e6), management representation (bbbdfe7), pembahasan akhir (de69c2f), format laporan (b555edd), draf LK (e59c663), rekap hasil audit (ff42fdc) | ISA 260/265/450/580/700 |
| `ssi_general_audit_worksheet_final_report` | 3 WS: audit final memorandum (a8c54f3), independent auditor's report (b66777d), audit report (f3ed115) | ISA 700/701/705/706/220 |

## Referensi Standar Audit

Modul-modul dalam repository ini mengimplementasikan kertas kerja sesuai standar berikut:

| Standar | Topik |
|---------|-------|
| ISA 200 / SA 200 | Tujuan Keseluruhan Auditor Independen |
| ISA 210 / SA 210 | Persetujuan atas Ketentuan Perikatan Audit |
| ISA 220 / SA 220 | Pengendalian Mutu untuk Audit atas Laporan Keuangan |
| ISA 230 / SA 230 | Dokumentasi Audit |
| ISA 240 / SA 240 | Tanggung Jawab Auditor Terkait Kecurangan |
| ISA 250 / SA 250 | Pertimbangan atas Peraturan Perundang-undangan |
| ISA 260 / SA 260 | Komunikasi dengan Pihak yang Bertanggung Jawab atas Tata Kelola |
| ISA 265 / SA 265 | Pengkomunikasian Defisiensi Pengendalian Internal |
| ISA 300 / SA 300 | Perencanaan Suatu Audit atas Laporan Keuangan |
| ISA 315 / SA 315 | Pengidentifikasian dan Penilaian Risiko Salah Saji Material |
| ISA 320 / SA 320 | Materialitas dalam Tahap Perencanaan dan Pelaksanaan Audit |
| ISA 330 / SA 330 | Respons Auditor terhadap Risiko yang Telah Dinilai |
| ISA 402 / SA 402 | Pertimbangan Audit Terkait Entitas yang Menggunakan Organisasi Jasa |
| ISA 450 / SA 450 | Pengevaluasian atas Salah Saji yang Diidentifikasi |
| ISA 500 / SA 500 | Bukti Audit |
| ISA 501 / SA 501 | Bukti Audit — Pertimbangan Spesifik atas Unsur Pilihan |
| ISA 505 / SA 505 | Konfirmasi Eksternal |
| ISA 520 / SA 520 | Prosedur Analitis |
| ISA 530 / SA 530 | Sampling Audit |
| ISA 540 / SA 540 | Audit atas Estimasi Akuntansi |
| ISA 550 / SA 550 | Pihak Berelasi |
| ISA 560 / SA 560 | Peristiwa Kemudian |
| ISA 570 / SA 570 | Kelangsungan Usaha |
| ISA 580 / SA 580 | Representasi Tertulis |
| ISA 610 / SA 610 | Penggunaan Pekerjaan Auditor Internal |
| ISA 620 / SA 620 | Penggunaan Pekerjaan Pakar Auditor |
| ISA 700 / SA 700 | Perumusan Suatu Opini dan Pelaporan |
| ISA 701 / SA 701 | Pengomunikasian Hal Audit Utama |
| ISA 705 / SA 705 | Modifikasi terhadap Opini |
| ISA 706 / SA 706 | Paragraf Penekanan Suatu Hal dan Paragraf Hal Lain |
| ISQC 1 | Pengendalian Mutu bagi KAP yang Melaksanakan Perikatan |

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[ssi_general_audit](ssi_general_audit/) | 14.0.4.1.0 |  | General Audit
[ssi_general_audit_core](ssi_general_audit_core/) | 14.0.1.1.0 |  | General Audit - Core
[ssi_general_audit_worksheet_acceptance_continuance](ssi_general_audit_worksheet_acceptance_continuance/) | 14.0.1.4.0 |  | General Audit Worksheet - Acceptance and Continuance
[ssi_general_audit_worksheet_analytic_cycle](ssi_general_audit_worksheet_analytic_cycle/) | 14.0.1.4.0 |  | General Audit Worksheet - Analytical Procedures – Cycle
[ssi_general_audit_worksheet_assignment_letter](ssi_general_audit_worksheet_assignment_letter/) | 14.0.1.0.3 |  | General Audit Worksheet - Assignment Letter
[ssi_general_audit_worksheet_audit_procedure_analytic](ssi_general_audit_worksheet_audit_procedure_analytic/) | 14.0.1.4.0 |  | General Audit Worksheet - Observation Audit Procedure
[ssi_general_audit_worksheet_audit_procedure_confirmation](ssi_general_audit_worksheet_audit_procedure_confirmation/) | 14.0.1.4.0 |  | General Audit Worksheet - Reperformance Audit Procedure
[ssi_general_audit_worksheet_audit_procedure_inquiry](ssi_general_audit_worksheet_audit_procedure_inquiry/) | 14.0.1.2.2 |  | General Audit Worksheet - Inquiry Audit Procedure
[ssi_general_audit_worksheet_audit_procedure_observation](ssi_general_audit_worksheet_audit_procedure_observation/) | 14.0.1.2.0 |  | General Audit Worksheet - Observation Audit Procedure
[ssi_general_audit_worksheet_audit_procedure_recompute](ssi_general_audit_worksheet_audit_procedure_recompute/) | 14.0.1.4.0 |  | General Audit Worksheet - Recompute Audit Procedure
[ssi_general_audit_worksheet_audit_procedure_reperformance](ssi_general_audit_worksheet_audit_procedure_reperformance/) | 14.0.1.2.2 |  | General Audit Worksheet - Reperformance Audit Procedure
[ssi_general_audit_worksheet_audit_procedure_vouching](ssi_general_audit_worksheet_audit_procedure_vouching/) | 14.0.1.4.0 |  | General Audit Worksheet - Vouching Audit Procedure
[ssi_general_audit_worksheet_audit_result](ssi_general_audit_worksheet_audit_result/) | 14.0.1.1.1 |  | General Audit Worksheet - Audit Result
[ssi_general_audit_worksheet_audit_working_plan](ssi_general_audit_worksheet_audit_working_plan/) | 14.0.1.5.1 |  | General Audit Worksheet - Audit Working Plan
[ssi_general_audit_worksheet_client_package](ssi_general_audit_worksheet_client_package/) | 14.0.1.3.0 |  | General Audit Worksheet - Client Assistance Package
[ssi_general_audit_worksheet_control_risk](ssi_general_audit_worksheet_control_risk/) | 14.0.2.8.0 |  | General Audit Worksheet - Control Risk
[ssi_general_audit_worksheet_draft_reporting](ssi_general_audit_worksheet_draft_reporting/) | 14.0.1.1.2 |  | General Audit Worksheet - Draft Reporting
[ssi_general_audit_worksheet_engagement_letter_checklist](ssi_general_audit_worksheet_engagement_letter_checklist/) | 14.0.1.2.1 |  | General Audit Worksheet - Engagement Letter Checklist
[ssi_general_audit_worksheet_expert](ssi_general_audit_worksheet_expert/) | 14.0.1.2.1 |  | General Audit Worksheet - Expert
[ssi_general_audit_worksheet_external_communication](ssi_general_audit_worksheet_external_communication/) | 14.0.1.3.0 |  | General Audit Worksheet - External Communication
[ssi_general_audit_worksheet_final_materiality](ssi_general_audit_worksheet_final_materiality/) | 14.0.1.1.2 |  | General Audit Worksheet - Final Materiality & Analytical Procedures
[ssi_general_audit_worksheet_final_report](ssi_general_audit_worksheet_final_report/) | 14.0.1.1.1 |  | General Audit Worksheet - Final Report
[ssi_general_audit_worksheet_independence_statement](ssi_general_audit_worksheet_independence_statement/) | 14.0.1.2.0 |  | General Audit Worksheet - Independence Statement
[ssi_general_audit_worksheet_inherent_risk](ssi_general_audit_worksheet_inherent_risk/) | 14.0.2.3.6 |  | General Audit Worksheet - Inherent Risk
[ssi_general_audit_worksheet_lead_schedule](ssi_general_audit_worksheet_lead_schedule/) | 14.0.1.2.3 |  | General Audit Worksheet - Lead Schedule
[ssi_general_audit_worksheet_physical_check](ssi_general_audit_worksheet_physical_check/) | 14.0.1.1.0 |  | General Audit Worksheet - Inspection
[ssi_general_audit_worksheet_planning_memorandum](ssi_general_audit_worksheet_planning_memorandum/) | 14.0.1.5.0 |  | General Audit Worksheet - Planning Memorandum
[ssi_general_audit_worksheet_population](ssi_general_audit_worksheet_population/) | 14.0.1.2.0 |  | General Audit Worksheet - Population
[ssi_general_audit_worksheet_preliminary_analytic_procedure](ssi_general_audit_worksheet_preliminary_analytic_procedure/) | 14.0.1.2.0 |  | General Audit Worksheet - Preliminary Analytic Procedure
[ssi_general_audit_worksheet_preliminary_materiality](ssi_general_audit_worksheet_preliminary_materiality/) | 14.0.1.4.0 |  | General Audit Worksheet - Preliminary Materiality
[ssi_general_audit_worksheet_review](ssi_general_audit_worksheet_review/) | 14.0.1.1.1 |  | General Audit Worksheet - Review
[ssi_general_audit_worksheet_romm](ssi_general_audit_worksheet_romm/) | 14.0.1.5.5 |  | General Audit Worksheet - ROMM
[ssi_general_audit_worksheet_sample_determination](ssi_general_audit_worksheet_sample_determination/) | 14.0.1.5.0 |  | General Audit Worksheet - Sample Determination
[ssi_general_audit_worksheet_specific_procedure](ssi_general_audit_worksheet_specific_procedure/) | 14.0.1.2.2 |  | General Audit Worksheet - Specific Procedures
[ssi_general_audit_worksheet_team_communication](ssi_general_audit_worksheet_team_communication/) | 14.0.1.2.2 |  | General Audit Worksheet - Team Communication
[ssi_general_audit_worksheet_test_of_control](ssi_general_audit_worksheet_test_of_control/) | 14.0.1.5.0 |  | General Audit Worksheet - Test of Control
[ssi_general_audit_worksheet_test_of_detail](ssi_general_audit_worksheet_test_of_detail/) | 14.0.1.4.2 |  | General Audit Worksheet - Test of Detail
[ssi_general_audit_worksheet_test_planning](ssi_general_audit_worksheet_test_planning/) | 14.0.1.2.0 |  | General Audit Worksheet - Test Planning
[ssi_general_audit_worksheet_trial_balance](ssi_general_audit_worksheet_trial_balance/) | 14.0.1.0.2 |  | General Audit Worksheet - Trial Balance
[ssi_general_audit_worksheet_understanding_entity](ssi_general_audit_worksheet_understanding_entity/) | 14.0.1.15.2 |  | General Audit Worksheet - Understanding Entity and It's Environment

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to OCA
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----

OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.
