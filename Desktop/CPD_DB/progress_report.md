# CPD_DB Project Progress Report

**Report Date:** February 10, 2025  
**Project Overview:** This Node.js-based system scrapes, processes, and stores Continuing Professional Development (CPD) course data from ~20 Hong Kong-focused professional organizations (primarily insurance, finance, accounting, engineering sectors) for 2025. Data is output as JSONL files, imported to SQLite DBs, and aggregated at root level. Modular scrapers per provider; archive for backups.

## Overall Progress
- **Completed Scrapers:** 15/20 providers have full outputs (JSONL courses data + DB + import script). These can be run via `npm install && node scraper.js` followed by `node import_to_db.js`.
- **Partial/Incomplete:** 3 providers have scrapers but no outputs (e.g., missing JSONL/DB).
- **Stubs/Empty:** 2 providers have minimal setup (package.json or HTML only); 1 empty research dir.
- **Aggregation:** 
  - `all_jsonl_files/`: 30+ JSONL files (one per provider + variants).
  - Root exports: `hk_cpd_courses_comprehensive_2025.jsonl` (combined), `cpd_providers.csv`.
  - Archive: Full backups of data (JSONL/configs) and DBs.
- **Data Volume:** ~50 JSONL files total; corresponding DBs in provider dirs and archive/database/.
- **Gaps:** Variants for some providers (e.g., HKFI has 3 dirs—consolidate?); stubs need implementation (e.g., PolyU, full Peak).
- **Tools/Deps:** All modules use npm; root has `scraper.sh` for orchestration. CLI tools available: node, npm, sqlite3, jq.

**Completion Estimate:** 75% (core providers scraped; focus on stubs and aggregation scripts).

## Per-Provider Progress
| Provider | Directory | Status | Key Files Present | Notes |
|----------|-----------|--------|-------------------|-------|
| ACCA (Global) | acca_cpd_scrape_2025/ | Partial | package.json, scraper.js | No JSONL/DB; run scraper to generate. |
| CII (HK) | cii_hk_scrape_2025/ | Complete | JSONL, DB, import_to_db.js, scraper.js | Ready for import. |
| EHP (CPD UK) | ehp_cpduk_scrape_2025/ | Complete | JSONL, DB, import_to_db.js, scraper.js | Full. |
| EHP (HK) | ehp_hk_scrape_2025/ | Partial | JSONL, scraper.js | Missing DB/import; add scripts. |
| HKCAAVQ | hkcaavq_scrape_2025/ | Complete | JSONL, DB, import_to_db.js, parse_hkcaavq_cpd.js, XLS source | Excel-based; parsed successfully. |
| HKCIB | hkcib_scrape_2025/ | Complete | JSONL, DB, import_to_db.js, scraper.js | Full. |
| HKCII | hkcii_cpd_scrape/ | Complete | JSONL, DB, import_to_db.js, scraper.js | Full (note: overlaps with hkcii in tabs). |
| HKEEC | hkeec_cpd_scrape_2025/ | Partial | JSONL, scraper.js | Missing DB/import. |
| HKEDU | hkeedu_cpd_scrape_2025/ | Complete | JSONL, DB, import_to_db.js, scraper.js | Full. |
| HKFI | hkfi_*_scrape_2025/ (3 variants: cpd, new, comprehensive) | Complete (variants) | JSONL (comprehensive variant), DB, import_to_db.js, scraper.js | Multiple versions; use comprehensive for latest. |
| HKICPA | hkicpa_cpd_scrape_2025/ | Complete | JSONL, DB, import_to_db.js, scraper.js | Full. |
| HKIE | hkie_cpd_scrape_2025/ | Partial | JSONL, import_to_db.js, scraper.js | Missing DB; import ready once DB created. |
| HKIIA | hkiia_scrape_2025/ | Complete | JSONL, DB, import_to_db.js, scraper.js | Full. |
| HKJCDPRI | hkjcdpri_scrape_2025/ | Complete | JSONL, DB, import_to_db.js, scraper.js, temp.html | Full; HTML temp file from scrape. |
| ICAC/TDI (BEDC) | icac_tdi_scrape_2025/ | Partial | JSONL, scraper.js | Missing DB/import. |
| ITC | itc_scrape_2025/ | Complete | JSONL, DB, import_to_db.js, scraper.js | Full. |
| Legal Beagle | legal_beagle_scrape_2025/ | Complete | JSONL, DB, import_to_db.js, scraper.js | Full. |
| Peak | peak_*_scrape_2025/ (scrape, comprehensive, full) | Partial (comprehensive complete) | JSONL, DB, import_to_db.js, scraper.js (comprehensive) | Use comprehensive; full is stub (only package.json). |
| PIBA | piba_cpd_scrape/ | Complete | JSONL, DB, import_to_db.js, scraper.js | Full. |
| PolyU | polyu_cpd_scrape/ | Stub | package.json, main_page.html | Incomplete; implement scraper. |
| The Digital Insurer | the_digital_insurer_scrape_2025/ | Stub | main.html | Minimal; add scraper. |
| Insurance Authority (IA) | ia_cpd_task/ | Complete | JSONL (data/), DB (database/), parse_ia_cpd.js, import_ia_cpd.js, XLS sources | Special Excel-based; full. |
| Research | research/ | Empty | None | For future notes/experiments. |

## Aggregated Data Status
- **all_jsonl_files/**: Comprehensive collection; includes all provider JSONLs + renames (e.g., `hong-kong-federation-of-insurers-hkfi.jsonl`). Ready for merging.
- **Root Exports:** 
  - CSVs: `cpd_providers.csv` (providers list), `cpd_courses_new.csv`, `hk_cpd_courses_comprehensive_2025.csv`.
  - JSONL: `hk_cpd_courses_comprehensive_2025.jsonl`, `the_digital_insurer_cdi_courses_2025.jsonl`.
- **Archive:**
  - data/: Configs (`providers_config.json`, `cpd_providers.json`) + ~15 provider JSONLs.
  - database/: ~15 provider DBs + `import_cpd.sql` (bulk import script).

## Next Steps & Recommendations
1. **Complete Stubs:** Implement scrapers for PolyU, The Digital Insurer, and full Peak (add scraper.js, JSONL output).
2. **Run Missing Imports:** For partials (e.g., EHP HK, HKEEC), generate DBs via import scripts.
3. **Consolidate Variants:** Merge HKFI/ Peak dirs into single canonical versions.
4. **Automation:** Enhance `scraper.sh` to run all complete scrapers and aggregate.
5. **Validation:** Query DBs (e.g., `sqlite3 hkfi_cpd.db "SELECT COUNT(*) FROM courses;"`) to count records; ensure 2025 data freshness.
6. **Backup:** Commit changes (git add . && git commit -m "Update progress"); push to https://github.com/codeprotege/MarketScanner.git.

**Total Estimated Records:** 1000+ courses across providers (based on file sizes; verify via jq or sqlite3).

For updates, re-run scrapers periodically or monitor provider sites.
