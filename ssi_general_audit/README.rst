.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Accountant General Audit
========================

Modul inti (core) untuk manajemen engagement **Audit Umum (General Audit)**
sesuai **Standar Audit (SA) Indonesia** yang mengadopsi **International
Standards on Auditing (ISA)**. Modul ini menyediakan seluruh fondasi data
dan proses yang digunakan oleh modul-modul worksheet audit.

Standar audit yang dirujuk mencakup antara lain:
SA 200 (Tujuan Keseluruhan Auditor), SA 220 (Pengendalian Mutu),
SA 230 (Dokumentasi Audit), SA 315 (Identifikasi & Penilaian Risiko),
SA 320 (Materialitas), SA 450 (Evaluasi Salah Saji), dan SA 520
(Prosedur Analitis).

Arsitektur & Domain Model
==========================

Modul ini diorganisasikan ke dalam beberapa domain model berikut:

General Audit
-------------

``general_audit``
    Dokumen transaksional utama yang merepresentasikan satu engagement
    audit umum. Menjadi induk dari seluruh dokumen turunan: neraca saldo,
    pemetaan akun, jurnal penyesuaian, dan worksheet. Status: draft → open
    → confirm → done (memerlukan approval).

``general_audit.detail``
    Baris akun klien dalam general audit. Menghubungkan setiap
    ``client_account`` dengan baris neraca saldo tiga periode (home,
    interim, previous).

``general_audit.standard_detail``
    Aggregasi saldo per tipe akun standar untuk analisis lintas periode.

``general_audit.group_detail``
    Aggregasi saldo per grup akun untuk analisis komparatif.

``general_audit.computation``
    Hasil komputasi item-item ringkasan (Total Aset, rasio keuangan, dll.)
    dari neraca saldo untuk dasar penetapan materialitas (SA 320).

``general_audit.adjustment`` *(SQL View)*
    Ringkasan jurnal penyesuaian audit per tipe akun.

``general_audit.account_adjustment`` *(SQL View)*
    Ringkasan jurnal penyesuaian audit per akun klien individual.

``general_audit.group_adjustment`` *(SQL View)*
    Ringkasan jurnal penyesuaian audit per grup akun.

``general_audit.worksheet_summary``
    Status kelengkapan worksheet per tipe worksheet; digunakan sebagai
    dashboard pengendalian mutu audit.

Master Data General Audit
--------------------------

``general_audit_business_environment``
    Lingkungan bisnis klien (SA 315); mis. manufaktur, jasa, keuangan.

``general_audit_evidence``
    Tipe bukti audit (SA 500): inspeksi, konfirmasi, observasi, tanya-jawab,
    komputasi ulang, reperformansi.

``general_audit_standard_audit``
    Standar audit yang dirujuk (mis. ISA 200, SA 500) dalam dokumentasi.

``general_audit_relevant_regulation``
    Regulasi / standar akuntansi relevan terhadap entitas klien (SA 315).

``general_audit_relevant_regulation.item``
    Butir-butir hierarkis dalam satu regulasi.

Worksheet
---------

``general_audit_worksheet``
    Shadow record yang mendasari setiap worksheet konkret melalui
    *delegated inheritance* (``_inherits``). Menyimpan field bersama:
    tanggal persiapan, reviewer, kesimpulan, dan catatan review.

``general_audit_worksheet_mixin``
    Abstract mixin yang harus diwarisi oleh setiap model worksheet
    konkret. Menyediakan alur approval dan injeksi view otomatis.

``general_audit_worksheet_type``
    Tipe worksheet (mis. Acceptance & Continuance, Assignment Letter,
    Audit Program, Risk Assessment, Audit Result, Draft Reporting).
    Mengontrol worksheet mana yang wajib dan berapa jumlah maksimumnya.

``general_audit_worksheet_type_category``
    Kategori tipe worksheet (mis. Planning, Fieldwork, Reporting).

``general_audit_worksheet_conclusion``
    Pilihan kesimpulan per tipe worksheet yang dapat dipilih auditor.

``general_audit.worksheet_control`` *(SQL View)*
    Panel kontrol gabungan (required + additional) untuk memantau status
    seluruh worksheet dalam satu audit.

``general_audit.worksheet_control_required`` *(SQL View)*
    Subset: tipe worksheet yang bersifat wajib per audit.

``general_audit.worksheet_control_additional`` *(SQL View)*
    Subset: tipe worksheet yang bersifat opsional per audit.

Client Account
--------------

``client_account_group``
    Grup akun tingkat tinggi (mis. Aset Lancar, Liabilitas Jangka Pendek).

``client_account_type``
    Tipe akun standar KAP (mis. Kas, Piutang, Persediaan). Dapat memiliki
    kode Python untuk komputasi kustom dan terhubung ke prosedur analitis.

``client_account_type_set``
    Kumpulan tipe akun standar yang dikonfigurasi per konteks klien.

``client_account_type.computation_item``
    Override kode Python untuk item komputasi tertentu dalam suatu set.

``client_account``
    Daftar akun dari Chart of Accounts klien yang diaudit.

``client_account_mapping``
    Dokumen pemetaan akun klien ke tipe akun standar (memerlukan approval).

``client_account_mapping.detail``
    Baris pemetaan akun klien individual ke tipe akun standar.

``client_relevant_account_type``
    Standar akuntansi relevan yang diterapkan klien (mis. PSAK 71, IFRS 9).

Client Trial Balance
--------------------

``client_trial_balance``
    Neraca saldo klien untuk satu periode. Dapat berupa neraca saldo akhir
    periode (home), interim, atau periode sebelumnya.

``client_trial_balance.detail``
    Baris akun dalam neraca saldo: saldo awal, debit, kredit, saldo akhir.

``client_trial_balance.standard_detail``
    Aggregasi saldo per tipe akun standar dalam neraca saldo.

``client_trial_balance.group_detail``
    Aggregasi saldo per grup akun dalam neraca saldo.

``client_trial_balance.computation``
    Hasil perhitungan satu item komputasi dari neraca saldo (mis. Total
    Aset, Current Ratio) untuk keperluan materialitas dan prosedur analitis.

``trial_balance_computation_item``
    Master formula komputasi (kode Python) untuk menghasilkan angka
    ringkasan dan rasio keuangan dari neraca saldo (SA 320, SA 520).

Client
------

``client_adjustment_entry``
    Jurnal penyesuaian audit (AAJ) yang mencatat koreksi yang diusulkan
    auditor (SA 450). Status: draft → confirm → done.

``client_adjustment_entry.detail``
    Baris debit/kredit dalam satu jurnal penyesuaian audit.

``client_business_process``
    Siklus bisnis klien (SA 315): mis. Siklus Pendapatan, Siklus Pembelian.

``client_financial_ratio``
    Formula rasio keuangan (kode Python) untuk prosedur analitis (SA 520):
    likuiditas, aktivitas, solvabilitas, profitabilitas.

Checklist
---------

``checklist.option_set``
    Kumpulan opsi jawaban checklist (mis. set "Ya/Tidak/Tidak Berlaku").

``checklist.option``
    Satu opsi jawaban dalam sebuah option set.

``mixin.checklist``
    Abstract mixin untuk menyuntikkan fungsionalitas checklist ke worksheet.

``mixin.checklist.item``
    Abstract base untuk master item checklist (pertanyaan/titik kontrol).

``mixin.checklist.value``
    Abstract base untuk jawaban checklist pada sebuah dokumen.

SDM & Organisasi
----------------

``team_role``
    Peran anggota tim audit (SA 220): Engagement Partner, Manager, Senior,
    Junior Auditor.

``hr.employee`` *(extension)*
    Tambahan flag ``audit_ok`` untuk menandai karyawan yang berwenang
    melakukan pekerjaan audit.

``res.company`` *(extension)*
    Konfigurasi default item komputasi materialitas (Total Aset, Total
    Pendapatan) pada level KAP (SA 320).

Hubungan antar Modul
====================

Modul ini adalah **modul inti** (``ssi_general_audit``) yang menjadi
ketergantungan (dependency) bagi seluruh modul worksheet berikut:

- ``ssi_general_audit_core`` — Mixin tambahan dan konfigurasi lanjutan
- ``ssi_general_audit_worksheet_acceptance_continuance``
- ``ssi_general_audit_worksheet_assignment_letter``
- ``ssi_general_audit_worksheet_audit_working_plan``
- ``ssi_general_audit_worksheet_control_risk``
- ``ssi_general_audit_worksheet_audit_procedure_*`` (berbagai prosedur)
- ``ssi_general_audit_worksheet_audit_result``
- ``ssi_general_audit_worksheet_final_materiality``
- ``ssi_general_audit_worksheet_draft_reporting``
- dan lainnya

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/opnsynid-vertical-accountant
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit*
6.  Install the module

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/opnsynid-vertical-accountant/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Michael Viriyananda <viriyananda.michael@gmail.com>
* Andhitia Rama <andhitia.r@gmail.com>
* Asrul Bastian Yunas <asrulbastianyunas@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
