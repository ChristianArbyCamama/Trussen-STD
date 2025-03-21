import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from data import (
    control_pretest_scores,
    control_posttest_scores,
    experimental_pretest_scores,
    experimental_posttest_scores,
)


class IndependentTTest:
    def __init__(self):
        self.alpha = 0.05  # Significance level (two-tailed)

    def calculate_critical_value(self, alpha, df):
        self.critical_value = stats.t.ppf(1 - alpha / 2, df)

    def check_variance_homogeneity(self, group1_scores, group2_scores):
        # Levene’s test for equality of variances
        _, levene_pvalue = stats.levene(group2_scores, group1_scores)
        self.levene_pvalue = levene_pvalue

        # If p-value > alpha, assume equal variances; otherwise, assume unequal variances.
        self.equal_variance = levene_pvalue > self.alpha

        return self.equal_variance

    def compute_independent_ttest(self, group1_scores, group2_scores):
        self.equal_variance = self.check_variance_homogeneity(
            group1_scores, group2_scores
        )

        result = stats.ttest_ind(
            group2_scores, group1_scores, equal_var=self.equal_variance
        )

        self.statistic = result.statistic
        self.pvalue = result.pvalue
        self.degree_of_freedom = result.df
        self.mean_difference = np.mean(group2_scores) - np.mean(group1_scores)

    def display_independent_ttest_result(
        self, group1_scores, group2_scores, group1_name, group2_name
    ):
        self.group1_name = group1_name
        self.group2_name = group2_name
        self.compute_independent_ttest(group1_scores, group2_scores)
        self.calculate_critical_value(self.alpha, self.degree_of_freedom)

        print(f"*" * 50, end="\n\n")
        print(f"{group1_name} vs {group2_name} Independent T-Test Result")
        print(f"Mean difference: {self.mean_difference}")
        print(
            f"Levene's Test P-value: {self.levene_pvalue} {'(Equal Variances Assumed)' if self.equal_variance else '(Unequal Variances Assumed)'}"
        )
        print(f"T-statistic: {self.statistic}")
        print(f"P-value: {self.pvalue}")
        print(f"Critical-value: {self.critical_value}")
        print(f"Degree of freedom: {self.degree_of_freedom}")
        print(f"Mean Difference: {self.mean_difference}")

        # Method 1: Compare t-statistic with critical value
        if abs(self.statistic) > self.critical_value:
            print("\nstatistic > critical value: Reject the null hypothesis.")
        else:
            print("\nstatistic <= critical value: Fail to reject the null hypothesis.")

        # Method 2: Compare p-value with alpha
        if self.pvalue <= self.alpha:
            print("pvalue <= alpha: Reject the null hypothesis.", end="\n\n")
        else:
            print("pvalue > alpha: Fail to reject the null hypothesis.", end="\n\n")

        # Determine direction of change
        if self.mean_difference > 0:
            print(f"{group2_name} has a higher mean than {group1_name}.")
        elif self.mean_difference < 0:
            print(f"{group1_name} has a higher mean than {group2_name}.")
        else:
            print("No difference in means.")

    def plot_result(self, group1_scores, group2_scores, test_type):
        mean1, std1 = np.mean(group1_scores), np.std(group1_scores, ddof=1)
        mean2, std2 = np.mean(group2_scores), np.std(group2_scores, ddof=1)

        x = np.linspace(
            min(min(group1_scores), min(group2_scores)) - 5,
            max(max(group1_scores), max(group2_scores)) + 5,
            100,
        )
        y1 = stats.norm.pdf(x, mean1, std1)
        y2 = stats.norm.pdf(x, mean2, std2)

        plt.plot(x, y1, label=f"{self.group1_name} (Mean={mean1:.2f})", color="red")
        plt.plot(x, y2, label=f"{self.group2_name} (Mean={mean2:.2f})", color="blue")
        plt.fill_between(x, y1, alpha=0.3, color="red")
        plt.fill_between(x, y2, alpha=0.3, color="blue")

        plt.title(
            f"{self.group1_name} vs {self.group2_name} Normal Distribution ({test_type})"
        )
        plt.xlabel("Scores")
        plt.ylabel("Probability Density")
        plt.legend()
        plt.show()


# Control Group Data
control_pretest_scores = np.array(control_pretest_scores)
control_posttest_scores = np.array(control_posttest_scores)

# Experimental Group Data
experimental_pretest_scores = np.array(experimental_pretest_scores)
experimental_posttest_scores = np.array(experimental_posttest_scores)

# Perform the independent t-test with Levene’s test
independent_ttest = IndependentTTest()
independent_ttest.display_independent_ttest_result(
    control_pretest_scores,
    experimental_pretest_scores,
    "Control Group",
    "Experimental Group",
)
independent_ttest.plot_result(
    control_pretest_scores, experimental_pretest_scores, "Pre-Test"
)
independent_ttest.plot_result(
    control_posttest_scores, experimental_posttest_scores, "Post-test"
)
