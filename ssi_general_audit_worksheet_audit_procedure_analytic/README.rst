.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================================
General Audit Worksheet - Analytic Audit Procedure
=====================================================

Modul ini mengimplementasikan dua jenis **Prosedur Audit Analitis** (*Analytical
Audit Procedures*) yang dilakukan sebagai respons terhadap risiko yang dinilai
(*Risk Responses*), sesuai dengan **SA 520** (Prosedur Analitis) dan **SA 330**
(Respons Auditor atas Risiko yang Dinilai).

Prosedur analitis substantif digunakan untuk mendeteksi salah saji yang
material dengan mengevaluasi informasi keuangan melalui analisis hubungan
yang masuk akal antara data keuangan maupun non-keuangan, dan melalui
perbandingan dengan nilai yang dapat diharapkan (*expected values*).

Arsitektur Worksheet
====================

Modul ini mengikuti pola dua lapisan (*two-layer pattern*) yang digunakan di seluruh
repository ``ssi-general-audit``:

- ``general_audit_worksheet`` — Shadow record yang menyimpan field-field umum
  (tanggal, klien, partner, kesimpulan, dll.) melalui *delegated inheritance*
  (``_inherits``).
- ``general_audit_worksheet_mixin`` — Abstract mixin yang diwariskan oleh setiap
  model worksheet konkret.

Referensi lengkap arsitektur: lihat ``ssi_general_audit/models/worksheet/``.

Daftar Worksheet
================

``general_audit_ws_aa899baf`` — Plausible Relationship Audit Procedure
-----------------------------------------------------------------------

Worksheet untuk mendokumentasikan prosedur analitis berbasis **hubungan yang
masuk akal** (*plausible relationship*) antara data.  Auditor mengidentifikasi
hubungan yang diperkirakan ada — misalnya antara jumlah karyawan dengan biaya
gaji, atau antara volume produksi dengan biaya bahan baku — kemudian menetapkan
nilai yang diharapkan (*expected value*) dan membandingkannya dengan nilai
tercatat.  Selisih melampaui ambang (*threshold*) merupakan indikasi salah saji.

**SA Reference:** SA 520, SA 330

**Kode Tipe Worksheet:** AA899BAF
**Kategori:** Risk Responses (RE)

``general_audit_ws_de3244b`` — Comparative Audit Procedure
-----------------------------------------------------------

Worksheet untuk mendokumentasikan prosedur analitis berbasis **perbandingan**
(*comparative*).  Auditor membandingkan angka periode berjalan dengan:

* Informasi periode sebelumnya (*prior-year*).
* Anggaran atau prakiraan yang disetujui manajemen.
* Rata-rata industri atau entitas sejenis.

Fluktuasi atau hubungan yang tidak konsisten dengan ekspektasi merupakan
indikasi potensi salah saji yang harus ditindaklanjuti (SA 520.6).

**SA Reference:** SA 520, SA 330

**Kode Tipe Worksheet:** DE3244B
**Kategori:** Risk Responses (RE)

Hubungan ke Worksheet Lain
==========================

Kedua worksheet dalam modul ini mensyaratkan referensi ke **WS-E51BB1C**
(Key Audit Procedures) yang telah berstatus *performed*.  Ketergantungan ini
memastikan bahwa setiap prosedur analitis yang dilakukan terhubung langsung
dengan program audit yang direncanakan dan didokumentasikan dalam worksheet
prosedur audit kunci.

Alur kerja umum:

1. Auditor membuka worksheet Key Audit Procedures (WS-E51BB1C) dan menandai
   prosedur-prosedur yang akan dilaksanakan dengan status *performed*.
2. Auditor membuat worksheet prosedur analitis (AA899BAF atau DE3244B) dan
   mereferensikan WS-E51BB1C yang telah diisi.
3. Sistem secara otomatis menyaring daftar prosedur audit kunci yang tersedia
   hanya dari prosedur berstatus *performed*.
4. Auditor memilih prosedur kunci, tipe akun, dan asersi yang relevan, kemudian
   mendokumentasikan hasil prosedur analitis.

Model Python
============

``general_audit_ws_aa899baf``
    Model worksheet Plausible Relationship Audit Procedure.  Mewarisi
    ``general_audit_worksheet_mixin`` yang menyediakan alur approval dan
    field umum via delegasi ke ``general_audit_worksheet``.

    Field utama:

    - ``ws_e51bb1c_id`` — Referensi ke WS-E51BB1C (Key Audit Procedures).
    - ``key_audit_procedure_id`` — Prosedur audit kunci yang direspons.
    - ``account_type_id`` — Tipe akun standar yang diuji.
    - ``assertion_type_ids`` — Asersi laporan keuangan yang diuji.
    - ``detail_ws_e51bb1c_id`` *(computed)* — Baris detail WS-E51BB1C yang
      berkorespondensi dengan prosedur kunci yang dipilih.

``general_audit_ws_de3244b``
    Model worksheet Comparative Audit Procedure.  Memiliki struktur field yang
    sama dengan ``general_audit_ws_aa899baf`` dan juga mewarisi
    ``general_audit_worksheet_mixin``.

Catatan Implementasi
====================

- Kedua worksheet termasuk kategori ``worksheet_type_category_rr``
  (Risk Responses) dengan ``main_worksheet = True``.
- ``max_number_allowed = 100`` memungkinkan auditor membuat banyak worksheet
  prosedur analitis untuk akun-akun yang berbeda dalam satu engagement audit.
- Seluruh field umum (``general_audit_id``, ``partner_id``, ``currency_id``,
  ``conclusion_id``, ``preparation_date``, dll.) tersedia melalui delegasi ke
  ``general_audit_worksheet`` — tidak perlu didefinisikan ulang di model ini.
- ``allowed_key_audit_procedure_ids`` hanya menampilkan prosedur berstatus
  ``performed`` dari WS-E51BB1C, mencegah auditor mereferensikan prosedur
  yang belum direncanakan.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Analytic Audit Procedure*
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
