import customtkinter as ctk
from tkinter import messagebox
import math

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Grade → Grade Points
GRADE_POINTS = {
    "O":  10,   # Outstanding  (≥ 85%)
    "A":   9,   # Excellent    (80–84.99%)
    "B":   8,   # Very Good    (70–79.99%)
    "C":   7,   # Good         (60–69.99%)
    "D":   6,   # Fair         (50–59.99%)
    "E":   5,   # Average      (45–49.99%)
    "P":   4,   # Pass         (40–44.99%)
    "F":   0,   # Fail         (< 40%)
}

# Minimum % of total marks required to achieve each grade
GRADE_PCT_THRESHOLD = {
    "O":  85,
    "A":  80,
    "B":  70,
    "C":  60,
    "D":  50,
    "E":  45,
    "P":  40,
    "F":   0,
}

GRADE_OPTIONS = list(GRADE_POINTS.keys())


class SGPIPredictor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SGPA Predictor & Study Planner - Dynamic Assessment Model")
        self.geometry("1500x750")

        self.grid_columnconfigure(0, weight=60)
        self.grid_columnconfigure(1, weight=40)
        self.grid_rowconfigure(0, weight=1)

        self.subjects = []

        self.create_left_panel()
        self.create_right_panel()

        # Seed with initial dynamic rows  (name, credits, total_max, e1, e2, e3, e4, e5, target_grade)
        self.add_subject_row("Engg. Maths",  "4", "100", "18/20", "22/30", "",      "", "", "B")
        self.add_subject_row("Programming",  "3", "150", "15/20", "20/30", "40/50", "", "", "A")
        self.add_subject_row("Physics Lab",  "1", "50",  "15/20", "",      "",      "", "", "O")

    #  LEFT PANEL
    def create_left_panel(self):
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.left_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(
            self.left_frame,
            text="Dynamic Course Inputs",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        header.grid(row=0, column=0, pady=(15, 5), sticky="w", padx=20)

        sub_header = ctk.CTkLabel(
            self.left_frame,
            text="Format: Enter completed exams as 'Obtained/Max' (e.g., 18/20). Leave blank for upcoming exams.",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        )
        sub_header.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 15))

        # Column header row
        header_row = ctk.CTkFrame(self.left_frame, fg_color="#2B2B2B", corner_radius=5)
        header_row.grid(row=2, column=0, sticky="w", padx=10, pady=5, ipady=5)

        bold_font = ctk.CTkFont(weight="bold", size=13)
        ctk.CTkLabel(header_row, text="Subject Name",  width=150, anchor="w",      font=bold_font).pack(side="left", padx=5)
        ctk.CTkLabel(header_row, text="Credits",            width=50,  anchor="center", font=bold_font).pack(side="left", padx=2)
        ctk.CTkLabel(header_row, text="Total Max",     width=80,  anchor="center", font=bold_font, text_color="#F9A826").pack(side="left", padx=2)
        ctk.CTkLabel(header_row, text="Eval 1 (O/M)",  width=90,  anchor="center", font=bold_font).pack(side="left", padx=2)
        ctk.CTkLabel(header_row, text="Eval 2 (O/M)",  width=90,  anchor="center", font=bold_font).pack(side="left", padx=2)
        ctk.CTkLabel(header_row, text="Eval 3 (O/M)",  width=90,  anchor="center", font=bold_font).pack(side="left", padx=2)
        ctk.CTkLabel(header_row, text="Eval 4 (O/M)",  width=90,  anchor="center", font=bold_font).pack(side="left", padx=2)
        ctk.CTkLabel(header_row, text="Eval 5 (O/M)",  width=90,  anchor="center", font=bold_font).pack(side="left", padx=2)
        ctk.CTkLabel(header_row, text="Target Grade",  width=100, anchor="center", font=bold_font, text_color="#A78BFA").pack(side="left", padx=2)

        # Scrollable subject rows
        self.subjects_frame = ctk.CTkScrollableFrame(self.left_frame, fg_color="transparent")
        self.subjects_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.left_frame.grid_rowconfigure(3, weight=1)

        self.add_btn = ctk.CTkButton(
            self.left_frame,
            text="+ Add Subject",
            font=ctk.CTkFont(weight="bold"),
            command=lambda: self.add_subject_row("", "3", "100", "", "", "", "", "", "B"),
            height=40,
        )
        self.add_btn.grid(row=4, column=0, pady=15)

    # ------------------------------------------------------------------ #
    #  RIGHT PANEL
    # ------------------------------------------------------------------ #
    def create_right_panel(self):
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid_rowconfigure(2, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Action button panel
        control_frame = ctk.CTkFrame(self.right_frame, corner_radius=15)
        control_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        ctk.CTkLabel(
            control_frame,
            text="Set a Target Grade per subject →",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#A78BFA",
        ).pack(pady=(18, 6))

        ctk.CTkLabel(
            control_frame,
            text="O=10  A=9  B=8  C=7  D=6  E=5  P=4  F=0",
            font=ctk.CTkFont(size=12),
            text_color="gray",
        ).pack(pady=(0, 10))

        calc_btn = ctk.CTkButton(
            control_frame,
            text="Generate Study Plan & SGPA",
            command=self.calculate_plan,
            fg_color="#3C3489",
            hover_color="#534AB7",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        calc_btn.pack(pady=(0, 20), padx=20, fill="x")

        # SGPA result banner (hidden until calculated)
        self.sgpa_frame = ctk.CTkFrame(self.right_frame, corner_radius=12, fg_color="#1C1C2E")
        self.sgpa_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.sgpa_label = ctk.CTkLabel(
            self.sgpa_frame,
            text="Projected SGPA: —",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#A78BFA",
        )
        self.sgpa_label.pack(pady=12)

        # Results Panel
        self.results_frame = ctk.CTkScrollableFrame(
            self.right_frame,
            label_text="Prioritized Study Plan",
            label_font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.results_frame.grid(row=2, column=0, sticky="nsew")

        # Legend note inside results frame (always visible at top)
        legend_lines = [
            ("🔴 IMPOSSIBLE", "#A32D2D", "Gap exceeds remaining marks — target unachievable"),
            ("🔴 CRITICAL",   "#A32D2D", "Near-perfect scores needed — extremely tough"),
            ("🟠 HIGH",       "#BA7517", "Achievable with intense, dedicated effort"),
            ("🔵 MEDIUM",     "#185FA5", "Comfortable with consistent preparation"),
            ("🟢 LOW",        "#0F6E56", "Small gap — manageable with light effort"),
            ("✅ SAFE",       "#3B6D11", "Target already achieved!"),
        ]
        legend_frame = ctk.CTkFrame(self.results_frame, fg_color="#1C1C2E", corner_radius=8)
        legend_frame.pack(fill="x", pady=(4, 10), padx=4)
        ctk.CTkLabel(legend_frame, text="Priority Legend", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="gray").pack(anchor="w", padx=10, pady=(6, 2))
        for label, color, desc in legend_lines:
            row = ctk.CTkFrame(legend_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=1)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=color, width=110, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=desc, font=ctk.CTkFont(size=11),
                         text_color="gray", anchor="w").pack(side="left")
        ctk.CTkFrame(legend_frame, height=6, fg_color="transparent").pack()

    #  ADD / DELETE ROWS
    def add_subject_row(self, name, credits, total_max, e1, e2, e3, e4, e5, target_grade):
        row_frame = ctk.CTkFrame(self.subjects_frame)
        row_frame.pack(fill="x", pady=5, ipady=3)

        name_var      = ctk.StringVar(value=name)
        credits_var   = ctk.StringVar(value=str(credits))
        total_max_var = ctk.StringVar(value=str(total_max))
        e1_var        = ctk.StringVar(value=e1)
        e2_var        = ctk.StringVar(value=e2)
        e3_var        = ctk.StringVar(value=e3)
        e4_var        = ctk.StringVar(value=e4)
        e5_var        = ctk.StringVar(value=e5)
        grade_var     = ctk.StringVar(value=target_grade if target_grade in GRADE_OPTIONS else "B")

        ctk.CTkEntry(row_frame,    textvariable=name_var,      width=150).pack(side="left", padx=5)
        ctk.CTkComboBox(row_frame, values=["1","2","3","4","5"], variable=credits_var, width=50).pack(side="left", padx=2)
        ctk.CTkEntry(row_frame,    textvariable=total_max_var,  width=80, placeholder_text="e.g. 150").pack(side="left", padx=2)
        ctk.CTkEntry(row_frame,    textvariable=e1_var,         width=90, placeholder_text="18/20").pack(side="left", padx=2)
        ctk.CTkEntry(row_frame,    textvariable=e2_var,         width=90, placeholder_text="25/30").pack(side="left", padx=2)
        ctk.CTkEntry(row_frame,    textvariable=e3_var,         width=90, placeholder_text="-").pack(side="left", padx=2)
        ctk.CTkEntry(row_frame,    textvariable=e4_var,         width=90, placeholder_text="-").pack(side="left", padx=2)
        ctk.CTkEntry(row_frame,    textvariable=e5_var,         width=90, placeholder_text="-").pack(side="left", padx=2)

        # Target grade dropdown — purple tint to stand out
        grade_menu = ctk.CTkComboBox(
            row_frame,
            values=GRADE_OPTIONS,
            variable=grade_var,
            width=100,
            button_color="#534AB7",
            border_color="#534AB7",
        )
        grade_menu.pack(side="left", padx=4)

        subject_tuple = (name_var, credits_var, total_max_var, e1_var, e2_var, e3_var, e4_var, e5_var, grade_var)

        del_btn = ctk.CTkButton(
            row_frame,
            text="X",
            width=30,
            fg_color="#A32D2D",
            hover_color="#F09595",
            command=lambda f=row_frame, s=subject_tuple: self.delete_row(f, s),
        )
        del_btn.pack(side="left", padx=(5, 2))

        self.subjects.append(subject_tuple)

    def delete_row(self, frame, subject_tuple):
        frame.destroy()
        if subject_tuple in self.subjects:
            self.subjects.remove(subject_tuple)

    #  PARSING
    def parse_eval(self, eval_var):
        val = eval_var.get().strip()
        if not val or val.upper() in ("N/A", "-", ""):
            return 0.0, 0.0
        try:
            obt, mx = val.split("/")
            return float(obt), float(mx)
        except ValueError:
            raise ValueError

    #  MAIN CALCULATION
    def calculate_plan(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        analysis = []
        total_credits = 0
        weighted_grade_points = 0.0

        for name_v, cred_v, max_v, e1, e2, e3, e4, e5, grade_v in self.subjects:
            name    = name_v.get() or "Unnamed"
            credits = int(cred_v.get())
            grade   = grade_v.get()

            try:
                total_max = float(max_v.get().strip())
            except ValueError:
                messagebox.showerror("Error", f"Please enter a valid Total Max score for '{name}'.")
                return

            current_secured      = 0.0
            max_assessed_so_far  = 0.0

            try:
                for ev in [e1, e2, e3, e4, e5]:
                    obt, mx = self.parse_eval(ev)
                    current_secured     += obt
                    max_assessed_so_far += mx
            except ValueError:
                messagebox.showerror("Error", f"Invalid format in '{name}'. Use 'Obtained/Max' (e.g., 18/20).")
                return

            if max_assessed_so_far > total_max:
                messagebox.showerror("Error", f"Assessed marks ({max_assessed_so_far}) exceed Total Max ({total_max}) in '{name}'.")
                return

            target_pct   = GRADE_PCT_THRESHOLD[grade]
            grade_point  = GRADE_POINTS[grade]
            target_marks = (target_pct / 100.0) * total_max

            remaining_max    = total_max - max_assessed_so_far
            remaining_needed = max(0.0, target_marks - current_secured)

            if remaining_needed == 0:
                instruction = f"Target for {grade} secured! You have crossed the threshold for '{name}'."
            elif remaining_max == 0 and remaining_needed > 0:
                instruction = f"All exams done but you fell short of {grade} by {remaining_needed:.1f} marks."
            else:
                instruction = (
                    f"Need {math.ceil(remaining_needed)} more marks out of "
                    f"{remaining_max:.0f} remaining to hit {grade} "
                    f"({target_pct}% of {total_max:.0f})."
                )

            study_weight = credits * remaining_needed

            # For SGPA: assume best-case — if target is achievable (remaining_needed ≤ remaining_max),
            # count the target grade; otherwise count the best reachable grade.
            if remaining_needed <= remaining_max:
                projected_grade_point = grade_point
            else:
                best_possible_pct = ((current_secured + remaining_max) / total_max) * 100
                projected_grade_point = 0
                for g in GRADE_OPTIONS:
                    if best_possible_pct >= GRADE_PCT_THRESHOLD[g]:
                        projected_grade_point = GRADE_POINTS[g]
                        break

            total_credits          += credits
            weighted_grade_points  += credits * projected_grade_point

            analysis.append({
                "name":                 name,
                "credits":              credits,
                "current":              current_secured,
                "target_marks":         target_marks,
                "max":                  total_max,
                "assessed_max":         max_assessed_so_far,
                "remaining_max":        remaining_max,
                "needed":               remaining_needed,
                "weight":               study_weight,
                "instruction":          instruction,
                "target_grade":         grade,
                "target_grade_point":   grade_point,
                "projected_grade_point":projected_grade_point,
            })


        sgpa = (weighted_grade_points / total_credits) if total_credits > 0 else 0.0
        self.sgpa_label.configure(
            text=f"Projected SGPA: {sgpa:.2f} / 10.00",
            text_color="#A78BFA" if sgpa >= 7 else "#F9A826" if sgpa >= 5 else "#FF6B6B",
        )

    
        analysis.sort(key=lambda x: x["weight"], reverse=True)

        for i, item in enumerate(analysis):
            rem = item["remaining_max"]
            needed = item["needed"]

            if rem > 0:
                pct_needed = (needed / rem) * 100
            else:
                pct_needed = 0 if needed == 0 else 999

            if pct_needed > 100:
                status_color, status_text = "#A32D2D", "IMPOSSIBLE: Gap exceeds remaining marks"
            elif pct_needed > 75:
                status_color, status_text = "#A32D2D", "CRITICAL: Near-perfect scores required"
            elif pct_needed > 50:
                status_color, status_text = "#BA7517", "HIGH PRIORITY: Intense focus required"
            elif pct_needed > 25:
                status_color, status_text = "#185FA5", "MEDIUM: Achievable with steady prep"
            elif pct_needed > 0:
                status_color, status_text = "#0F6E56", "LOW: Manageable gap"
            else:
                status_color, status_text = "#3B6D11", "SAFE: Target achieved!"

            card = ctk.CTkFrame(self.results_frame, border_width=2, border_color=status_color, corner_radius=10)
            card.pack(fill="x", pady=8, padx=5, ipady=10)

            # Card header
            hf = ctk.CTkFrame(card, fg_color="transparent")
            hf.pack(fill="x", padx=15, pady=(5, 3))
            ctk.CTkLabel(hf, text=f"{i+1}. {item['name']}", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
            ctk.CTkLabel(
                hf,
                text=f"Cr: {item['credits']} | Max: {item['max']:.0f}",
                font=ctk.CTkFont(weight="bold"),
                text_color="gray",
            ).pack(side="right")

            # Grade badge row
            gf = ctk.CTkFrame(card, fg_color="transparent")
            gf.pack(fill="x", padx=15, pady=(0, 4))
            badge_color = "#534AB7" if item["projected_grade_point"] >= item["target_grade_point"] else "#A32D2D"
            ctk.CTkLabel(
                gf,
                text=f"Target: {item['target_grade']}  ({item['target_grade_point']} pts)",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#A78BFA",
            ).pack(side="left")
            ctk.CTkLabel(
                gf,
                text=f"Projected: {item['projected_grade_point']} pts",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=badge_color,
            ).pack(side="left", padx=15)

            # Progress bar
            progress_ratio = min(1.0, max(0.0, item["current"] / item["target_marks"])) if item["target_marks"] > 0 else 1.0
            prog_bar = ctk.CTkProgressBar(card, height=10, progress_color=status_color)
            prog_bar.pack(fill="x", padx=15, pady=5)
            prog_bar.set(progress_ratio)

            # Metrics
            ctk.CTkLabel(
                card,
                text=f"Secured: {item['current']:.1f}  |  Target marks needed: {item['target_marks']:.1f}",
                font=ctk.CTkFont(size=12, slant="italic"),
                anchor="w",
                justify="left",
            ).pack(fill="x", padx=15)

            ctk.CTkLabel(
                card,
                text=item["instruction"],
                font=ctk.CTkFont(size=13),
                wraplength=420,
                anchor="w",
                justify="left",
            ).pack(fill="x", padx=15, pady=(8, 0))

            ctk.CTkLabel(
                card,
                text=status_text,
                text_color=status_color,
                font=ctk.CTkFont(size=12, weight="bold"),
                wraplength=420,
                anchor="w",
                justify="left",
            ).pack(fill="x", padx=15, pady=(5, 5))


if __name__ == "__main__":
    app = SGPIPredictor()
    app.mainloop()