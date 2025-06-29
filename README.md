# conflict-detection-remote-sensing-nlp

A Streamlit-ready pipeline that fuses open-source conflict reports with satellite-based land change detections (e.g., NDVI drops). Designed to verify violence-linked environmental change and support humanitarian monitoring in real-world settings like Myanmar.

---

## 🛰 Overview

This project:
- Scrapes or accepts geolocated conflict reports
- Detects NDVI-based vegetation change using Sentinel-2 imagery
- Matches events to land change via spatial + temporal rules
- Outputs a GeoDataFrame for inspection or downstream analysis

---

## 🚀 How to Run the Fusion Pipeline

```bash
python src/satellite/run_fusion.py \
  --text_path data/sample_inputs/gdf_text_sample.gpkg \
  --sat_path data/sample_inputs/ndvi_sample.geojson \
  --output_path outputs/output_fused_matches.gpkg \
  --delta_days 14
