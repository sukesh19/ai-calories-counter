from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class CalorieCounterApp(App):
    def build(self):
        self.bmi = 22.0  # Example BMI, in a real app ask user input
        self.daily_requirement = self.calculate_daily_calorie_requirement(self.bmi)
        self.total_calories = 0

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.bmi_label = Label(text=f"BMI: {self.bmi:.1f}")
        self.layout.add_widget(self.bmi_label)

        self.requirement_label = Label(text=f"Estimated Daily Calorie Requirement: {self.daily_requirement} kcal")
        self.layout.add_widget(self.requirement_label)

        self.calorie_input = TextInput(hint_text="Enter calories consumed", multiline=False, input_filter='int')
        self.layout.add_widget(self.calorie_input)

        self.add_button = Button(text="Add Calories")
        self.add_button.bind(on_press=self.add_calories)
        self.layout.add_widget(self.add_button)

        self.total_label = Label(text=f"Total Calories Consumed: {self.total_calories} kcal")
        self.layout.add_widget(self.total_label)

        self.disclaimer_label = Label(text="Disclaimer: This is an AI-generated approximate value for reference only.", font_size='12sp')
        self.layout.add_widget(self.disclaimer_label)

        return self.layout

    def calculate_daily_calorie_requirement(self, bmi):
        # Simplified calculation: normal BMI daily calories ~ 2000
        # Adjust requirement linearly upward/downward by BMI difference from 22
        base_calories = 2000
        bmi_normal = 22
        adjustment = (bmi - bmi_normal) * 50  # 50 kcal per BMI point difference
        return max(1200, int(base_calories + adjustment))  # minimum 1200 kcal

    def add_calories(self, instance):
        try:
            calories = int(self.calorie_input.text)
            self.total_calories += calories
            self.total_label.text = f"Total Calories Consumed: {self.total_calories} kcal"
            self.calorie_input.text = ""
        except ValueError:
            self.calorie_input.text = ""

if __name__ == '__main__':
    CalorieCounterApp().run()
