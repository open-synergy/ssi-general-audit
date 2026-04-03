.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================================
General Audit Worksheet - Assignment Letter
===========================================

Modul ini mengimplementasikan prosedur verifikasi **Surat Penugasan** (*Assignment
Letter*) sebagai bagian dari fase pra-perikatan (*pre-engagement*) audit umum sesuai
dengan **SA 300** (Perencanaan Suatu Audit atas Laporan Keuangan) dan **SA 220**
(Pengendalian Mutu untuk Audit atas Laporan Keuangan).

Sebelum pekerjaan lapangan dimulai, auditor wajib memastikan bahwa Surat Penugasan
yang diterbitkan kepada klien telah memenuhi seluruh persyaratan formal. Modul ini
menyediakan worksheet terstruktur untuk mendokumentasikan proses verifikasi tersebut.

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

``general_audit_ws_c435bcd`` — Assignment Letter
-------------------------------------------------

Worksheet tunggal dalam modul ini. Auditor memverifikasi kelengkapan formal Surat
Penugasan melalui daftar periksa (*checklist*) terstruktur, lalu mencatat kesimpulan:

- **Assignment Letter is sufficient** (Surat Penugasan memadai) — seluruh persyaratan
  formal terpenuhi; perikatan dapat dilanjutkan.
- **Assignment Letter is not sufficient** (Surat Penugasan tidak memadai) — satu atau
  lebih persyaratan formal tidak terpenuhi; tindakan korektif diperlukan sebelum
  perikatan dikonfirmasi.

**SA Reference:** SA 220, SA 300

Daftar Periksa (*Checklist Items*)
====================================

Setiap worksheet memuat lima poin verifikasi standar:

1. **Nama klien** — Tujuan surat penugasan menggunakan nama klien yang benar.
2. **Tanggal surat** — Surat diberi tanggal sesuai dengan tanggal kesepakatan.
3. **Nomor surat** — Penomoran surat mengikuti prosedur administrasi yang berlaku.
4. **Nama tim penugasan** — Nama anggota tim dicantumkan sesuai personel yang terpilih.
5. **Periode penugasan** — Periode perikatan yang tercantum sesuai dengan rencana.

Opsi jawaban untuk setiap poin menggunakan ``checklist_option_set_1`` (misal: Ya /
Tidak / Tidak Berlaku) yang dikonfigurasi di modul ``ssi_general_audit``.

Model Python
============

``general_audit_ws_c435bcd``
    Model worksheet utama. Mewarisi ``general_audit_worksheet_mixin`` (alur approval
    dan field umum via delegasi) serta ``mixin.checklist`` (fungsionalitas daftar
    periksa).  Field utama: ``checklist_ids`` (``One2many`` ke
    ``general_audit_ws_c435bcd.checklist``).

``general_audit_ws_c435bcd.checklist``
    Satu baris jawaban auditor untuk satu poin checklist dalam sebuah worksheet.
    Mewarisi ``mixin.checklist.value`` yang menyediakan ``option_id`` (jawaban yang
    dipilih) dan ``notes`` (catatan auditor).

``general_audit_ws_c435bcd.item``
    Template master untuk poin-poin checklist.  Mewarisi ``mixin.checklist.item``
    yang menyediakan ``name`` (uraian poin), ``option_set_id`` (kumpulan opsi
    jawaban), dan ``sequence`` (urutan tampil).  Dikonfigurasi melalui data XML
    dan direferensikan oleh setiap baris ``checklist``.

Catatan Implementasi
====================

- Worksheet ini termasuk kategori ``worksheet_type_category_pe`` (Pre-Engagement)
  dengan kode tipe ``C435BCD``.
- Field ``main_worksheet = True`` menandai bahwa ini adalah worksheet utama (bukan
  worksheet tambahan) dalam tipe kategorinya.
- Seluruh field umum (``general_audit_id``, ``partner_id``, ``currency_id``,
  ``conclusion_id``, ``preparation_date``, dll.) tersedia melalui delegasi ke
  ``general_audit_worksheet`` — tidak perlu didefinisikan ulang di model ini.

Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-general-audit
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *General Audit Worksheet - Assignment Letter*
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
