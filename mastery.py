from matplotlib import pyplot as plt
from data import (
    control_posttest_scores,
    experimental_posttest_scores,
    max_score,
)


class Mastery:
    def compute_mastery(self, scores, group_name):
        student_who_mastered = 0

        for score in scores:
            if score / max_score > 0.8:
                student_who_mastered += 1

        self.student_who_mastered = student_who_mastered
        self.mastery = round(student_who_mastered / len(scores), 2) * 100

        print(f"Mastery % of {group_name}:", self.mastery)

        return self.mastery

    def plot_result(self, control_mastery, experimental_mastery):
        # Data for the pie chart
        labels = ["Control Group", "Experimental Group"]
        values = [control_mastery, experimental_mastery]
        colors = ["red", "blue"]

        # Function to show actual values instead of computed percentages
        def format_label(pct, all_vals):
            absolute = int(round(pct * sum(all_vals) / 100.0))
            return f"{absolute}%"

        # Create pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(
            values,
            labels=labels,
            colors=colors,
            autopct=lambda pct: format_label(pct, values),
            textprops={"fontsize": 14},
        )
        plt.title("Mastery Percentage Comparison", fontdict={"fontsize": 16})
        plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle

        plt.show()


mastery = Mastery()
control_mastery = mastery.compute_mastery(control_posttest_scores, "Control Group")
experimental_mastery = mastery.compute_mastery(
    experimental_posttest_scores, "Experimental Group"
)
mastery.plot_result(control_mastery, experimental_mastery)
