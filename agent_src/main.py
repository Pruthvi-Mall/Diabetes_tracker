import google.genai as genai
import os, joblib
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Try different model names - gemini-1.5-flash is most commonly available
MODEL_NAME = "gemini-1.5-flash"  # Try this first
# MODEL_NAME = "gemini-1.0-pro"  # Alternative
# MODEL_NAME = "gemini-pro"      # Another alternative

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, "artifacts", "diabetes_model.pkl"))


class RiskAgent:
    def analyze(self, data):
        return model.predict([data])[0]


class GeminiAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def get_response(self, prompt):
        try:
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            return response.text
        except Exception as e:
            # Fallback to hardcoded responses if API fails
            print(f"⚠️ API Error (using fallback): {str(e)[:100]}...")
            return self._get_fallback_response(prompt)

    def _get_fallback_response(self, prompt):
        """Fallback responses if Gemini API fails"""
        if "lifestyle tips" in prompt:
            return "1. Exercise regularly\n2. Stay hydrated\n3. Maintain healthy weight"
        elif "diet tips" in prompt:
            return "1. Eat more vegetables\n2. Reduce sugar intake\n3. Choose whole grains"
        elif "emergency medical warning" in prompt:
            return "⚠️ HIGH BLOOD SUGAR DETECTED - SEEK MEDICAL ATTENTION IMMEDIATELY"
        else:
            return "Advice unavailable"


class LifestyleAgent(GeminiAgent):
    def advise(self):
        return self.get_response("Give 3 lifestyle tips to prevent diabetes and dehydration")


class NutritionAgent(GeminiAgent):
    def plan(self, risk):
        prompt = "Give 3 healthy diet tips" if risk == 0 else "Give 3 diabetes diet tips"
        return self.get_response(prompt)


class EmergencyAgent(GeminiAgent):
    def check(self, glucose):
        if glucose > 180:
            return self.get_response("Write a one line emergency medical warning")
        return "No emergency"


class ReportAgent:
    def generate(self, risk, lifestyle, diet, emergency):
        return {
            "Diabetes Risk": "YES" if risk == 1 else "NO",
            "Lifestyle Advice": lifestyle,
            "Diet Advice": diet,
            "Emergency Status": emergency
        }


print("\n🛡 AI Community Health Guardian\n")

sample = [6, 148, 72, 35, 0, 33.6, 0.62, 50]
risk = RiskAgent().analyze(sample)

# Test the model first
test_agent = GeminiAgent()
test_response = test_agent.get_response("Say 'Hello' if working")
print(f"Model test: {test_response[:50]}...")

lifestyle = LifestyleAgent().advise()
diet = NutritionAgent().plan(risk)
emergency = EmergencyAgent().check(sample[1])

report = ReportAgent().generate(risk, lifestyle, diet, emergency)

for k, v in report.items():
    print(f"{k}: {v}")