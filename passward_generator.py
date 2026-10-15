import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import math

SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/"
AMBIGUOUS = set("O0Il1")

WORDS = [
    "amber", "apple", "arrow", "autumn", "bamboo",
    "beacon", "berry", "bird", "breeze", "cactus",
    "candle", "canvas", "cedar", "cherry", "cloud",
    "comet", "coral", "crystal", "daisy", "delta",
    "desert", "diamond", "dolphin", "dream", "eagle",
    "earth", "echo", "ember", "falcon", "feather",
    "forest", "garden", "glacier", "gold", "harbor",
    "hazel", "honey", "island", "ivory", "jasmine",
    "jungle", "lagoon", "lantern", "lemon", "lotus",
    "maple", "marble", "meadow", "meteor", "mint",
    "moon", "mountain", "nectar", "nebula", "ocean",
    "olive", "orbit", "orchid", "otter", "panda",
    "pebble", "pepper", "phoenix", "planet", "pocket",
    "quartz", "rabbit", "rainbow", "raven", "river",
    "rocket", "shadow", "silver", "sparrow", "star",
    "stone", "summer", "sunrise", "tiger", "timber",
    "topaz", "tulip", "valley", "velvet", "violet",
    "willow", "winter", "wizard", "zephyr"
]


def generate_password(length, categories):
    if not categories:
        raise ValueError("Select at least one character category.")

    if length < len(categories):
        raise ValueError("Password length is too short.")

    password = [
        secrets.choice(category)
        for category in categories
    ]

    pool = "".join(categories)

    while len(password) < length:
        password.append(secrets.choice(pool))

    secrets.SystemRandom().shuffle(password)

    return "".join(password), len(set(pool))


def check_strength(password, pool_size):
    entropy = len(password) * math.log2(pool_size)

    if len(password) < 8 or entropy < 40:
        strength = "Weak"
    elif len(password) < 12 or entropy < 60:
        strength = "Moderate"
    elif len(password) >= 16 and entropy >= 90:
        strength = "Very Strong"
    else:
        strength = "Strong"

    return strength, entropy


def generate_passphrase(word_count, separator):
    words = [
        secrets.choice(WORDS)
        for _ in range(word_count)
    ]

    number = secrets.randbelow(900) + 100

    return separator.join(words) + separator + str(number)


class PasswordGeneratorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Security Tool")
        self.root.geometry("800x650")
        self.root.minsize(700, 550)

        self.upper = tk.BooleanVar(value=True)
        self.lower = tk.BooleanVar(value=True)
        self.digits = tk.BooleanVar(value=True)
        self.symbols = tk.BooleanVar(value=True)
        self.exclude = tk.BooleanVar(value=False)
        self.show_password = tk.BooleanVar(value=True)
        self.mode = tk.StringVar(value="password")

        self.passwords = []

        self.create_interface()

    def create_interface(self):
        main = ttk.Frame(self.root, padding=15)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="ADVANCED PASSWORD SECURITY TOOL",
            font=("Arial", 18, "bold")
        ).pack(pady=8)

        ttk.Label(
            main,
            text="Phase 3 | Secure Password Generator",
            font=("Arial", 10)
        ).pack(pady=3)

        mode_frame = ttk.LabelFrame(
            main, text="Generation Mode", padding=10
        )
        mode_frame.pack(fill="x", pady=8)

        ttk.Radiobutton(
            mode_frame,
            text="Custom Password",
            variable=self.mode,
            value="password",
            command=self.update_mode
        ).pack(side="left", padx=10)

        ttk.Radiobutton(
            mode_frame,
            text="Memorable Passphrase",
            variable=self.mode,
            value="passphrase",
            command=self.update_mode
        ).pack(side="left", padx=10)

        settings = ttk.LabelFrame(
            main, text="Settings", padding=10
        )
        settings.pack(fill="x", pady=5)

        row = ttk.Frame(settings)
        row.pack(fill="x", pady=5)

        ttk.Label(row, text="Password length (8-64):").pack(side="left")

        self.length_entry = ttk.Entry(row, width=7)
        self.length_entry.insert(0, "16")
        self.length_entry.pack(side="left", padx=8)

        ttk.Label(row, text="Number of passwords (1-5):").pack(
            side="left", padx=(15, 0)
        )

        self.count_entry = ttk.Entry(row, width=7)
        self.count_entry.insert(0, "3")
        self.count_entry.pack(side="left", padx=8)

        self.category_frame = ttk.Frame(settings)
        self.category_frame.pack(fill="x", pady=5)

        ttk.Checkbutton(
            self.category_frame,
            text="Uppercase",
            variable=self.upper
        ).pack(side="left", padx=5)

        ttk.Checkbutton(
            self.category_frame,
            text="Lowercase",
            variable=self.lower
        ).pack(side="left", padx=5)

        ttk.Checkbutton(
            self.category_frame,
            text="Numbers",
            variable=self.digits
        ).pack(side="left", padx=5)

        ttk.Checkbutton(
            self.category_frame,
            text="Symbols",
            variable=self.symbols
        ).pack(side="left", padx=5)

        self.exclude_check = ttk.Checkbutton(
            settings,
            text="Exclude confusing characters (O, 0, I, l, 1)",
            variable=self.exclude
        )
        self.exclude_check.pack(anchor="w", pady=5)

        self.phrase_frame = ttk.Frame(settings)

        ttk.Label(
            self.phrase_frame, text="Number of words (4-8):"
        ).pack(side="left")

        self.words_entry = ttk.Entry(self.phrase_frame, width=7)
        self.words_entry.insert(0, "5")
        self.words_entry.pack(side="left", padx=8)

        ttk.Label(
            self.phrase_frame, text="Separator:"
        ).pack(side="left", padx=(15, 0))

        self.separator_entry = ttk.Entry(
            self.phrase_frame, width=7
        )
        self.separator_entry.insert(0, "-")
        self.separator_entry.pack(side="left", padx=8)

        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=10)

        ttk.Button(
            buttons,
            text="Generate",
            command=self.generate
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons,
            text="Copy Selected",
            command=self.copy_password
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons,
            text="Clear Results",
            command=self.clear_results
        ).pack(side="left", padx=4)

        ttk.Checkbutton(
            buttons,
            text="Show Passwords",
            variable=self.show_password,
            command=self.refresh_results
        ).pack(side="right")

        result_frame = ttk.LabelFrame(
            main, text="Generated Results", padding=8
        )
        result_frame.pack(fill="both", expand=True, pady=5)

        self.results = tk.Listbox(
            result_frame,
            font=("Consolas", 10),
            height=10
        )
        self.results.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.results.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.results.configure(
            yscrollcommand=scrollbar.set
        )

        self.details = tk.StringVar(
            value="Generate a password and select it to view details."
        )

        ttk.Label(
            main,
            textvariable=self.details,
            wraplength=750
        ).pack(anchor="w", pady=8)

        ttk.Label(
            main,
            text="Passwords are not automatically saved.",
            font=("Arial", 9, "italic")
        ).pack(anchor="w")

        self.results.bind(
            "<<ListboxSelect>>",
            self.show_details
        )

        self.update_mode()

    def update_mode(self):
        if self.mode.get() == "password":
            self.category_frame.pack(fill="x", pady=5)
            self.exclude_check.pack(anchor="w", pady=5)
            self.phrase_frame.pack_forget()
            self.length_entry.configure(state="normal")
            self.count_entry.configure(state="normal")
        else:
            self.category_frame.pack_forget()
            self.exclude_check.pack_forget()
            self.phrase_frame.pack(fill="x", pady=5)
            self.length_entry.configure(state="disabled")
            self.count_entry.configure(state="disabled")

    def get_categories(self):
        categories = []

        if self.upper.get():
            categories.append(string.ascii_uppercase)

        if self.lower.get():
            categories.append(string.ascii_lowercase)

        if self.digits.get():
            categories.append(string.digits)

        if self.symbols.get():
            categories.append(SYMBOLS)

        if self.exclude.get():
            categories = [
                "".join(
                    char for char in category
                    if char not in AMBIGUOUS
                )
                for category in categories
            ]

        return [category for category in categories if category]

    def generate(self):
        self.passwords.clear()
        self.results.delete(0, tk.END)
        self.details.set("")

        if self.mode.get() == "passphrase":
            try:
                count = int(self.words_entry.get())

                if not 4 <= count <= 8:
                    raise ValueError(
                        "Choose between 4 and 8 words."
                    )

                separator = self.separator_entry.get()

                if len(separator) > 3:
                    raise ValueError(
                        "Separator must contain 0-3 characters."
                    )

                phrase = generate_passphrase(count, separator)

                self.passwords.append({
                    "value": phrase,
                    "type": "Passphrase",
                    "length": len(phrase),
                    "strength": "Not formally assessed",
                    "entropy": None
                })

                self.results.insert(tk.END, phrase)

                self.details.set(
                    f"Passphrase created using {count} random words "
                    "and a three-digit number."
                )

            except ValueError as error:
                messagebox.showerror("Input Error", str(error))

            return

        try:
            length = int(self.length_entry.get())
            count = int(self.count_entry.get())

            if not 8 <= length <= 64:
                raise ValueError(
                    "Password length must be between 8 and 64."
                )

            if not 1 <= count <= 5:
                raise ValueError(
                    "Generate between 1 and 5 passwords."
                )

            categories = self.get_categories()

            if not categories:
                raise ValueError(
                    "Select at least one character category."
                )

            if length < len(categories):
                raise ValueError(
                    "Length is too short for selected categories."
                )

            for index in range(1, count + 1):
                password, pool_size = generate_password(
                    length, categories
                )

                strength, entropy = check_strength(
                    password, pool_size
                )

                self.passwords.append({
                    "value": password,
                    "type": "Password",
                    "length": length,
                    "strength": strength,
                    "entropy": entropy
                })

                display = (
                    password if self.show_password.get()
                    else "*" * length
                )

                self.results.insert(
                    tk.END,
                    f"{index}. {display} | {strength}"
                )

            self.details.set(
                f"Successfully generated {count} password(s). "
                "Select a result to see its details."
            )

        except ValueError as error:
            messagebox.showerror("Input Error", str(error))

    def show_details(self, _event=None):
        selection = self.results.curselection()

        if not selection:
            return

        index = selection[0]

        if index >= len(self.passwords):
            return

        item = self.passwords[index]

        if item["type"] == "Passphrase":
            message = (
                f"Type: Passphrase | Length: {item['length']} characters"
            )
        else:
            message = (
                f"Type: Password | Length: {item['length']} | "
                f"Strength: {item['strength']} | "
                f"Estimated entropy: {item['entropy']:.1f} bits"
            )

        self.details.set(message)

    def refresh_results(self):
        selection = self.results.curselection()
        self.results.delete(0, tk.END)

        for index, item in enumerate(self.passwords, start=1):
            value = item["value"]

            if not self.show_password.get():
                value = "*" * len(value)

            if item["type"] == "Password":
                self.results.insert(
                    tk.END,
                    f"{index}. {value} | {item['strength']}"
                )
            else:
                self.results.insert(tk.END, value)

        if selection and selection[0] < self.results.size():
            self.results.selection_set(selection[0])

    def copy_password(self):
        selection = self.results.curselection()

        if not selection:
            messagebox.showinfo(
                "Select Result",
                "First select a generated password or passphrase."
            )
            return

        index = selection[0]
        value = self.passwords[index]["value"]

        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.root.update()

        messagebox.showinfo(
            "Copied",
            "Selected result copied to clipboard."
        )

    def clear_results(self):
        self.passwords.clear()
        self.results.delete(0, tk.END)
        self.details.set("All results cleared.")


def main():
    root = tk.Tk()
    PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
