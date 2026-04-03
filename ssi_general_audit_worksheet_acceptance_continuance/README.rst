.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================================
General Audit Worksheet - Acceptance and Continuance
====================================================

Modul ini mengimplementasikan prosedur pra-perikatan (pre-engagement) auditor
sesuai dengan **SA 220** (Pengendalian Mutu untuk Audit atas Laporan Keuangan),
**SA 300** (Perencanaan Suatu Audit atas Laporan Keuangan), dan regulasi
**PMPJ** (Prinsip Mengenal Pengguna Jasa) terkait Anti-Pencucian Uang.

Modul ini berisi **7 worksheet** yang bersama-sama membantu auditor memutuskan
apakah engagement audit dapat diterima atau dilanjutkan.

Arsitektur Worksheet
====================

Setiap worksheet dalam modul ini mengikuti pola dua lapisan:

- ``general_audit_worksheet`` — Model induk yang menyimpan field umum
  (tanggal, klien, partner, kesimpulan, dll.).
- ``general_audit_worksheet_mixin`` — Abstract mixin yang diwariskan oleh
  setiap model worksheet konkret melalui ``_inherits``.

Referensi lengkap arsitektur: lihat ``ssi_general_audit/models/worksheet/``.

Daftar Worksheet
================

``general_audit_ws_806c4e1`` — Acceptance and Continuance of Client Relationships
----------------------------------------------------------------------------------

Worksheet utama yang mengagregasi temuan risiko dari semua worksheet lain
dalam modul ini. Auditor menentukan tingkat risiko keseluruhan (Low / Medium /
High) dan membuat keputusan apakah hubungan klien dapat dilanjutkan (Yes / No).

**SA Reference:** SA 220, SA 300

``general_audit_ws_369c5a5`` — Previous Financial Reporting Issues
------------------------------------------------------------------

Mendokumentasikan dan menilai permasalahan pelaporan keuangan periode sebelumnya
(misalnya: opini modifikasian, salah saji material, ketidaksepakatan dengan
manajemen). Hasil penilaian risiko berkontribusi pada worksheet 806c4e1.

**SA Reference:** SA 220, SA 300

``general_audit_ws_f5e7049`` — Management Integrity
----------------------------------------------------

Mengevaluasi integritas dan nilai etika manajemen klien. Worksheet ini
mereferensikan hasil worksheet Money Laundering Issues (842f0d6) melalui
``link_1`` untuk menginkorporasikan temuan risiko PMPJ.

**SA Reference:** SA 220, ISQC 1

``general_audit_ws_842f0d6`` — Money Laundering Issues (PMPJ Risk Assessment)
------------------------------------------------------------------------------

Menilai risiko pencucian uang terkait klien audit berdasarkan empat dimensi:
profil klien, risiko negara, sektor bisnis, dan produk/jasa. Menghasilkan
kategori risiko PMPJ: Simplified, Intermediate, atau Enhanced.

**Regulasi:** PMPJ (Peraturan AML/CDD Indonesia)

``general_audit_ws_805d4d5`` — Know Your Customer (KYC) Principles — PMPJ
--------------------------------------------------------------------------

Mendokumentasikan prosedur Customer Due Diligence (CDD) sesuai regulasi PMPJ.
Level due diligence yang berlaku (Simplified / Intermediate / Enhanced) diturunkan
secara otomatis dari hasil worksheet 842f0d6 melalui field ``link_1``.

**Regulasi:** PMPJ (Peraturan AML/CDD Indonesia)

``general_audit_ws_0427d28`` — Communication With Previous Auditor
------------------------------------------------------------------

Mendokumentasikan komunikasi auditor masuk dengan auditor pendahulu (predecessor)
saat menerima perikatan baru (Initial Engagement). Worksheet secara otomatis
menentukan jenis perikatan berdasarkan ``num_of_consecutive_audit_firm``:

- **Initial Engagement**: Wajib berkomunikasi dengan auditor sebelumnya.
- **Recurring Engagement**: Tidak diperlukan karena KAP yang sama melanjutkan.

**SA Reference:** SA 300, Kode Etik IAPI

``general_audit_ws_b9d8a5c`` — Competency, Availability and Independency of Assignment Team
--------------------------------------------------------------------------------------------

Menilai apakah tim perikatan yang diusulkan secara kolektif memenuhi persyaratan
pengendalian mutu berdasarkan tiga dimensi:

- **Kompetensi** (``competency_analysis_ids``): Pengetahuan dan keahlian teknis.
- **Ketersediaan** (``availability_analysis_ids``): Waktu yang cukup tanpa konflik jadwal.
- **Independensi** (``independency_analysis_ids``): Bebas dari hubungan atau kepentingan
  yang dapat mengancam independensi.

**SA Reference:** SA 220, ISQC 1

Catatan Implementasi
====================

- Semua worksheet mewarisi ``general_audit_worksheet_mixin`` yang menggunakan
  ``_inherits`` ke ``general_audit_worksheet`` (delegated inheritance).
- Field umum seperti ``general_audit_id``, ``partner_id``, ``currency_id``,
  ``conclusion_id``, ``preparation_date``, dll. tersedia melalui delegasi.
- Worksheet 842f0d6 → 805d4d5 → 806c4e1 membentuk rantai referensi risiko PMPJ.
- Worksheet f5e7049 juga mereferensikan 842f0d6 untuk penilaian integritas manajemen.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Acceptance and Continuance*
6.  Install the module

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-general-audit/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>
* Michael Viriyananda <viriyananda.michael@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
