from flask import Flask, Response
import json
from datetime import datetime
import os

app = Flask(__name__)

class EnterprisePlantManager:
    def __init__(self, shift_id, operator):
        self.shift_id = shift_id
        self.operator = operator
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_unloading_status(self, total_trucks, grain_received_mt, avg_moisture):
        return {
            "section": "Unloading",
            "trucks_processed": total_trucks,
            "grain_received_mt": grain_received_mt,
            "avg_moisture_percent": avg_moisture,
            "status": "Optimal" if avg_moisture <= 12 else "Warning: High Moisture"
        }

    def get_milling_status(self, total_flour_mt, downtime_mins, power_kwh):
        operating_mins = (24 * 60) - downtime_mins
        return {
            "section": "Milling",
            "flour_produced_mt": total_flour_mt,
            "uptime_percent": round((operating_mins / (24 * 60)) * 100, 2),
            "power_consumed_kwh": power_kwh
        }

    def get_liquefaction_status(self, slurry_volume_m3, enzyme_dosed_kg, avg_ph, final_de):
        return {
            "section": "Liquefaction",
            "slurry_volume_m3": slurry_volume_m3,
            "enzyme_dosed_kg": enzyme_dosed_kg,
            "avg_ph": avg_ph,
            "dextrose_equivalent_de": final_de,
            "status": "Optimal" if 9 <= final_de <= 15 else "Check Conversion"
        }

    def get_fermentation_status(self, active_fermenters, avg_temp, final_alcohol_percent):
        return {
            "section": "Fermentation",
            "active_fermenters": active_fermenters,
            "avg_temperature_c": avg_temp,
            "final_wash_alcohol_percent": final_alcohol_percent
        }

    def get_distillation_status(self, wash_consumed_m3, rs_produced_liters, steam_used_mt):
        return {
            "section": "Distillation",
            "wash_consumed_m3": wash_consumed_m3,
            "rs_produced_liters": rs_produced_liters,
            "steam_consumed_mt": steam_used_mt
        }

    def get_msdh_status(self, rs_fed_liters, absolute_alcohol_liters, moisture_ppm):
        return {
            "section": "MSDH",
            "rs_fed_liters": rs_fed_liters,
            "ethanol_produced_liters": absolute_alcohol_liters,
            "product_moisture_ppm": moisture_ppm,
            "purity_percent": round(100 - (moisture_ppm / 10000), 2)
        }

    def get_mee_status(self, thin_slop_fed_m3, syrup_brix, steam_economy):
        return {
            "section": "MEE",
            "thin_slop_fed_m3": thin_slop_fed_m3,
            "final_syrup_brix": syrup_brix,
            "steam_economy": steam_economy 
        }

    def get_decanter_dryer_status(self, wet_cake_mt, ddgs_produced_mt, dryer_temp_c):
        return {
            "section": "Decanter & Dryer",
            "wet_cake_processed_mt": wet_cake_mt,
            "ddgs_produced_mt": ddgs_produced_mt,
            "dryer_temperature_c": dryer_temp_c
        }

    def get_utilities_status(self, boiler_steam_mt, wtp_water_m3, cpu_water_m3, etp_recycled_m3):
        return {
            "section": "Utilities",
            "boiler_steam_generated_mt": boiler_steam_mt,
            "wtp_treated_water_m3": wtp_water_m3,
            "cpu_polished_water_m3": cpu_water_m3,
            "etp_recycled_water_m3": etp_recycled_m3
        }

    def generate_dashboard_api(self):
        dashboard_data = {
            "meta_data": {
                "shift_id": self.shift_id,
                "operator": self.operator,
                "timestamp": self.timestamp,
                "plant_status": "Running"
            },
            "plant_sections": {
                "raw_material": [
                    self.get_unloading_status(45, 900, 11.5),
                    self.get_milling_status(850, 45, 12000)
                ],
                "process_conversion": [
                    self.get_liquefaction_status(2500, 350, 5.2, 12.5),
                    self.get_fermentation_status(6, 32.5, 14.2)
                ],
                "ethanol_recovery": [
                    self.get_distillation_status(2400, 320000, 450),
                    self.get_msdh_status(320000, 315000, 2000)
                ],
                "byproduct_recovery": [
                    self.get_mee_status(1800, 35.5, 3.8),
                    self.get_decanter_dryer_status(600, 280, 185)
                ],
                "utilities": [
                    self.get_utilities_status(1100, 2200, 450, 300)
                ]
            }
        }
        return json.dumps(dashboard_data, indent=4)


@app.route('/')
def home():
    return "Plant Operations Backend API is Running successfully on Render!"


@app.route('/api/dashboard')
def get_dashboard_data():
    plant_system = EnterprisePlantManager(shift_id="SHIFT_A_LIVE", operator="Admin")
    json_data = plant_system.generate_dashboard_api()
    # Adding CORS headers so any frontend can access it
    response = Response(json_data, status=200, mimetype='application/json')
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
