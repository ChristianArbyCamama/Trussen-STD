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
        self.mastery = round((student_who_mastered / len(scores)) * 100, 2)

        print(f"Mastery % of {group_name}:", self.mastery)

        return self.mastery

    def plot_result(self, control_mastery, experimental_mastery):
        # Plot the results
        labels = ["Control Group", "Experimental Group"]
        values = [control_mastery, experimental_mastery]

        plt.bar(labels, values, color=["red", "blue"])
        plt.ylabel("Mastery Percentage (%)")
        plt.title("Mastery Percentage Comparison")
        plt.ylim(0, 100)

        # Display values on bars
        for i, v in enumerate(values):
            plt.text(i, v + 2, f"{v}%", ha="center", fontsize=12)

        plt.show()


mastery = Mastery()
control_mastery = mastery.compute_mastery(control_posttest_scores, "Control Group")
experimental_mastery = mastery.compute_mastery(
    experimental_posttest_scores, "Experimental Group"
)
mastery.plot_result(control_mastery, experimental_mastery)
