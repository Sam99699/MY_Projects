import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp
import math

class CalculatorApp(App):
    def build(self):
        # Colors
        self.color_light_gray = [0.831, 0.831, 0.829, 1]  # #D4D4D2
        self.color_black = [0.109, 0.109, 0.109, 1]       # #1C1C1C
        self.color_dark_gray = [0.313, 0.313, 0.313, 1]   # #505050
        self.color_orange = [0.902, 0.588, 0.149, 1]      # #E69626
        self.color_white = [1, 1, 1, 1]                   # White
        
        # Calculator state
        self.A = "0"
        self.operator = None
        self.B = None
        self.new_input = True
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # Display label
        self.display = Label(
            text="0", 
            font_size=dp(50),
            size_hint=(1, 0.3),
            halign='right',
            valign='middle'
        )
        self.display.bind(size=self._update_display_text_size)
        main_layout.add_widget(self.display)
        
        # Button layout
        button_layout = GridLayout(cols=4, spacing=dp(5), size_hint=(1, 0.7))
        
        # Button values
        button_values = [
            ["Ac", "^", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "√", "="]
        ]
        
        # Create buttons
        for row in button_values:
            for value in row:
                btn = Button(
                    text=value,
                    font_size=dp(30),
                    background_color=self.get_button_color(value)
                )
                btn.bind(on_press=self.on_button_press)
                button_layout.add_widget(btn)
        
        main_layout.add_widget(button_layout)
        
        # Set window size for mobile-like appearance
        Window.size = (350, 550)
        
        return main_layout
    
    def _update_display_text_size(self, instance, value):
        instance.text_size = (instance.width, instance.height)
    
    def get_button_color(self, value):
        top_symbol = ["Ac", "^", "%", "√"]
        right_symbol = ["/", "*", "-", "+", "="]
        
        if value in top_symbol:
            return self.color_light_gray
        elif value in right_symbol:
            return self.color_orange
        else:
            return self.color_dark_gray
    
    def remove_zero_decimal(self, num):
        if num % 1 == 0:
            num = int(num)
        return str(num)
    
    def clear_all(self):
        self.A = "0"
        self.operator = None
        self.B = None
        self.new_input = True
    
    def on_button_press(self, instance):
        value = instance.text
        self.button_clicked(value)
    
    def button_clicked(self, value):
        right_symbol = ["/", "*", "-", "+", "="]
        top_symbol = ["Ac", "^", "%", "√"]
        
        if value in right_symbol:
            if value == "=":
                if self.A is not None and self.operator is not None:
                    self.B = self.display.text
                    try:
                        numA = float(self.A)
                        numB = float(self.B)
                        
                        if self.operator == "+":
                            result = numA + numB
                        elif self.operator == "-":
                            result = numA - numB
                        elif self.operator == "*":
                            result = numA * numB
                        elif self.operator == "/":
                            if numB != 0:
                                result = numA / numB
                            else:
                                self.display.text = "Error"
                                self.clear_all()
                                return
                        elif self.operator == "^":
                            result = numA ** numB
                        elif self.operator == "%":
                            result = numA % numB
                        
                        self.display.text = self.remove_zero_decimal(result)
                        self.clear_all()
                        
                    except (ValueError, ZeroDivisionError):
                        self.display.text = "Error"
                        self.clear_all()
                        
            elif value in "+-*/^%":
                if self.operator is None:
                    self.A = self.display.text
                    self.operator = value
                    self.new_input = True
        
        elif value in top_symbol:
            if value == "Ac":
                self.clear_all()
                self.display.text = "0"
            elif value == "^":
                if self.operator is None:
                    self.A = self.display.text
                    self.operator = "^"
                    self.new_input = True
            elif value == "%":
                if self.operator is None:
                    self.A = self.display.text
                    self.operator = "%"
                    self.new_input = True
            elif value == "√":
                # Square root function
                try:
                    current_value = float(self.display.text)
                    if current_value >= 0:
                        result = math.sqrt(current_value)
                        self.display.text = self.remove_zero_decimal(result)
                    else:
                        self.display.text = "Error"
                except ValueError:
                    self.display.text = "Error"
                self.new_input = True
        
        else:
            if value == ".":
                if self.new_input:
                    self.display.text = "0."
                    self.new_input = False
                elif "." not in self.display.text:
                    self.display.text += value
            elif value in "0123456789":
                if self.display.text == "0" or self.new_input:
                    self.display.text = value
                    self.new_input = False
                else:
                    self.display.text += value

if __name__ == "__main__":
    CalculatorApp().run()