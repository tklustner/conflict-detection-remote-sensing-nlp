# conflict-detection-remote-sensing-nlp
A Streamlit application that scrapes open-source conflict reports, extracts geolocated events, and measures environmental change (e.g., vegetation loss) in their aftermath using satellite imagery.

## 🚀 How to Run the Fusion Pipeline

python src/satellite/run_fusion.py \
 --text_path data/sample_inputs/gdf_text_sample.gpkg \
--sat_path data/sample_inputs/ndvi_sample.geojson \
  --output_path path/to/output_fused_matches.gpkg \
  --delta_days 14

- `text_path`: path to a GeoPackage or GeoJSON file containing geolocated conflict reports
- `sat_path`: path to a GeoJSON file containing NDVI-based change detections
- `output_path`: path to save the matched output (GeoPackage or GeoJSON)
- `delta_days`: (optional) maximum time difference (in days) allowed between report and satellite detection 
