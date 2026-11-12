import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class ExpenseTracker(BoxLayout):
    def __init__(self, data_file, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)
        self.data_file = data_file
        self.expenses = self.load_data()

        # Total dekhanor label
        self.total_label = Label(text="", size_hint_y=None, height=60, font_size=26)
        self.add_widget(self.total_label)

        # Khoroch-er naam
        self.name_input = TextInput(
            hint_text="Khoroch-er naam (jemon: Bazar)",
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        self.add_widget(self.name_input)

        # Taka-r poriman
        self.amount_input = TextInput(
            hint_text="Taka koto?",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=50,
        )
        self.add_widget(self.amount_input)

        # Add button
        add_btn = Button(text="Add korun", size_hint_y=None, height=50)
        add_btn.bind(on_press=self.add_expense)
        self.add_widget(add_btn)

        # Khorocher list (scroll kora jay)
        scroll = ScrollView()
        self.list_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))
        scroll.add_widget(self.list_layout)
        self.add_widget(scroll)

        self.refresh()

    # ---------- Data save/load ----------
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f)

    # ---------- Button-er kaj ----------
    def add_expense(self, instance):
        name = self.name_input.text.strip()
        amount_text = self.amount_input.text.strip()

        if not name or not amount_text:
            return

        try:
            amount = float(amount_text)
        except ValueError:
            return

        self.expenses.append({"name": name, "amount": amount})
        self.save_data()

        self.name_input.text = ""
        self.amount_input.text = ""
        self.refresh()

    def delete_expense(self, index):
        del self.expenses[index]
        self.save_data()
        self.refresh()

    # ---------- Screen update ----------
    def refresh(self):
        self.list_layout.clear_widgets()
        total = 0

        for i, item in enumerate(self.expenses):
            total += item["amount"]

            row = BoxLayout(size_hint_y=None, height=45, spacing=5)
            row.add_widget(Label(text=item["name"], halign="left"))
            row.add_widget(Label(text=f"{item['amount']:.2f} Tk", size_hint_x=0.4))

            del_btn = Button(text="X", size_hint_x=0.2)
            del_btn.bind(on_press=lambda btn, idx=i: self.delete_expense(idx))
            row.add_widget(del_btn)

            self.list_layout.add_widget(row)

        self.total_label.text = f"Total: {total:.2f} Tk"


class ExpenseApp(App):
    def build(self):
        data_file = os.path.join(self.user_data_dir, "expenses.json")
        return ExpenseTracker(data_file)


if __name__ == "__main__":
    ExpenseApp().run()