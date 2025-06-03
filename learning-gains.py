import matplotlib.pyplot as plt
import numpy as np
from data import (
    control_pretest_scores,
    control_posttest_scores,
    experimental_pretest_scores,
    experimental_posttest_scores,
    max_score,
)


class LearningGains:
    def compute_learning_gains(self, pretest_scores, posttest_scores):
        return [
            round(((post - pre) / (max_score - pre)) * 100, 2)
            for pre, post in zip(pretest_scores, posttest_scores)
        ]

    def plot_result(self, gains, group_name):
        students = [f"{i+1}" for i in range(len(gains))]

        # Plot Control Group
        plt.figure(figsize=(10, 5))
        plt.bar(
            students,
            gains,
            color="red" if group_name == "Control Group" else "blue",
        )
        plt.xlabel(f"{group_name} Students")
        plt.ylabel("Normalized Gain (%)")
        plt.title(f"Normalized Learning Gains - {group_name}")
        plt.xticks(rotation=45)
        plt.show()

    def display_stats(self, learning_gains, group_name):
        mean_val = np.mean(learning_gains)
        std_val = np.std(learning_gains, ddof=1)

        print(f"*" * 50, end="\n\n")
        print(f"Group: {group_name}")
        print(f"Mean: {mean_val:.2f}")
        print(f"Standard Deviation: {std_val:.2f}")


# Compute learning gains
lg = LearningGains()
control_gains = lg.compute_learning_gains(
    control_pretest_scores, control_posttest_scores
)
experimental_gains = lg.compute_learning_gains(
    experimental_pretest_scores, experimental_posttest_scores
)
lg.plot_result(control_gains, "Control Group")
lg.plot_result(experimental_gains, "Experimental Group")

lg.display_stats(control_gains, "Control Group")
lg.display_stats(experimental_gains, "Experimental Group")
